## [Main title](../README.md)
### [Interview questions](full.md)

# Python for Data Engineering

Python is the default glue language of data engineering: orchestrators are written in it, engines expose a first-class API, and most pipeline code is Python even when the compute runs in Spark or a warehouse. The interview bar is not algorithmic trivia; it is whether you can write pipeline code that is memory-safe, idempotent, observable, testable, and reproducibly packaged.

Three themes run through this page: **scale** (processing more than memory allows), **correctness** (idempotent writes, retries, dead-letter handling), and **operability** (structured logs, pinned environments, CI tests).

+ [Why is Python widely used in data engineering?](#Why-is-Python-widely-used-in-data-engineering)
+ [How do iterators and generators help with large data processing?](#How-do-iterators-and-generators-help-with-large-data-processing)
+ [What is the difference between threads, multiprocessing, and async IO in Python?](#What-is-the-difference-between-threads-multiprocessing-and-async-IO-in-Python)
+ [What is the GIL and why does it matter?](#What-is-the-GIL-and-why-does-it-matter)
+ [How do you read and write Parquet efficiently in Python?](#How-do-you-read-and-write-Parquet-efficiently-in-Python)
+ [How do you process large CSV files without running out of memory?](#How-do-you-process-large-CSV-files-without-running-out-of-memory)
+ [How do you implement retries with exponential backoff?](#How-do-you-implement-retries-with-exponential-backoff)
+ [What logging practices are important for data pipelines?](#What-logging-practices-are-important-for-data-pipelines)
+ [How do you structure a Python project for data pipelines?](#How-do-you-structure-a-Python-project-for-data-pipelines)
+ [How do you manage dependencies and reproducible environments?](#How-do-you-manage-dependencies-and-reproducible-environments)
+ [How do you test data transformations in Python?](#How-do-you-test-data-transformations-in-Python)
+ [How do you profile and optimize slow Python code?](#How-do-you-profile-and-optimize-slow-Python-code)
+ [How do you write memory-safe Python ETL code?](#How-do-you-write-memory-safe-Python-ETL-code)
+ [How do you design Python code so a data pipeline is restartable?](#How-do-you-design-Python-code-so-a-data-pipeline-is-restartable)
+ [How do you handle bad records in Python pipelines?](#How-do-you-handle-bad-records-in-Python-pipelines)
+ [When should you use pandas, Polars, PyArrow, or Spark from Python?](#When-should-you-use-pandas-Polars-PyArrow-or-Spark-from-Python)
+ [Real world use cases for Python for Data Engineering](#Real-world-use-cases-for-Python-for-Data-Engineering)

## Why is Python widely used in data engineering?

Python is popular because it is productive, readable, and has a strong ecosystem for data processing, orchestration, and integration. It is commonly used for glue code, transformations, APIs, and automation, even when the heavy compute runs on distributed engines.

What that looks like in a real stack: **orchestration** (Airflow, Dagster), **transformation** (PySpark, Polars, pandas, SQLAlchemy), **ingestion** (`httpx`, `boto3`, Kafka clients), and **testing/CI** (pytest, Great Expectations). The trade-off to name: Python is slow per CPU-cycle and heavy per process, so the winning pattern is "Python for control flow and small data, native or distributed engines for heavy lifting."

```python
# Python usually plays the control-plane role: orchestrate, do not crunch
from airflow.sdk import dag, task


@dag(dag_id="orders_elt", schedule="0 3 * * *", start_date=None, tags=["elt"])
def orders_elt():
    @task
    def extract() -> str:
        return extract_to_s3("orders", "2026-10-04")

    @task
    def transform(path: str) -> int:
        return run_spark_job("jobs/transform_orders.py", path)

    transform(extract())


orders_elt()
```

[Table of Contents](#Python-for-Data-Engineering)

## How do iterators and generators help with large data processing?

Iterators and generators allow streaming data instead of loading everything into memory. They enable processing large datasets row-by-row or batch-by-batch. This reduces memory usage and often improves stability of ETL jobs.

Gotchas: a generator is **single-use**; `yield` defers side effects to consumption; `itertools.islice`/`batched` compose well; and batching avoids per-row overhead.

```python
# Streaming pipeline: parse -> batch -> write with memory bounded by batch size
import csv
import itertools
from collections.abc import Iterable, Iterator
from typing import Any


def read_rows(path: str) -> Iterator[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        yield from csv.DictReader(handle)


def batched(items: Iterable[Any], size: int) -> Iterator[list[Any]]:
    iterator = iter(items)
    while chunk := list(itertools.islice(iterator, size)):
        yield chunk


def run(path: str, batch_size: int = 10_000) -> int:
    return sum(write_batch(batch) for batch in batched(read_rows(path), batch_size))
```

Each stage is independently testable with a list, and peak memory tracks `batch_size` rather than the file.

[Table of Contents](#Python-for-Data-Engineering)

## What is the difference between threads, multiprocessing, and async IO in Python?

Threads are useful for IO-bound workloads (network, disk) but limited by the GIL for CPU-bound tasks. Multiprocessing runs multiple processes and can use multiple CPU cores for CPU-bound work. Async IO uses an event loop to handle many concurrent IO operations efficiently when tasks spend time waiting.

```python
# Async IO: thousands of concurrent requests without thousands of threads
import asyncio

import httpx


async def fetch(client: httpx.AsyncClient, url: str) -> dict:
    response = await client.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


async def fetch_many(urls: list[str], concurrency: int = 100) -> list[dict]:
    limits = httpx.Limits(max_connections=concurrency)
    async with httpx.AsyncClient(limits=limits) as client:
        return await asyncio.gather(*(fetch(client, url) for url in urls))
```

For CPU-bound work swap in `ProcessPoolExecutor`; for blocking IO that is not async-friendly, a `ThreadPoolExecutor` with bounded workers is often the simplest correct choice. Measure whether the workload is IO-bound or CPU-bound first.

[Table of Contents](#Python-for-Data-Engineering)

## What is the GIL and why does it matter?

The Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time in CPython. This limits CPU-bound parallelism with threads. Many data engineering tasks are IO-bound, so threads can still help, but CPU-bound tasks often require multiprocessing or native libraries.

Recent nuance: CPython 3.13 introduced an **experimental free-threaded build** (PEP 703) where the GIL can be disabled, though it is not the default; the GIL is **released** around blocking IO and inside many C extensions (NumPy, Arrow, compression); and it is a CPython implementation detail, not a language rule.

```python
# If 4 threads take ~4x one thread, the GIL is serializing pure-Python CPU work
import time
from concurrent.futures import ThreadPoolExecutor


def cpu_task(n: int) -> int:
    return sum(i * i for i in range(n))


start = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(cpu_task, [2_000_000] * 4))
print(f"4 threads took {time.perf_counter() - start:.2f}s")
```

When the hot path sits in a GIL-releasing native library, threading scales much better; once it does not, move the work to processes or a distributed engine.

[Table of Contents](#Python-for-Data-Engineering)

## How do you read and write Parquet efficiently in Python?

Using `pyarrow` is common because it supports efficient columnar reads, predicate pushdown (engine-dependent), and schema handling. You should select only needed columns, write reasonably sized row groups/files, and avoid creating many tiny files. For large datasets, integrate with a distributed engine rather than pure local processing.

```python
# Column projection + pushed-down filter, then a typed write
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pyarrow.parquet as pq

dataset = ds.dataset("s3://acme-curated/orders/", format="parquet", partitioning=["order_date"])
table = dataset.to_table(
    columns=["order_id", "customer_id", "amount"],
    filter=(pc.field("order_date") == "2026-10-04") & (pc.field("amount") > 0),
)

schema = pa.schema([("order_id", pa.string()), ("customer_id", pa.string()),
                    ("amount", pa.decimal128(12, 2))])
with pq.ParquetWriter("orders/ds=2026-10-04/part-00000.parquet", schema,
                      compression="zstd", use_dictionary=True) as writer:
    for batch in table.select(schema.names).to_batches(max_chunksize=100_000):
        writer.write_batch(batch)
```

Rules: never write one file per row from a local process; size files at 128-512 MB; use `zstd` cold and `snappy` hot; read with an explicit schema in production; use `pyarrow.fs`/`fsspec` for remote paths; and hand off to Spark/Polars when the work needs shuffles or hundreds of GB.

[Table of Contents](#Python-for-Data-Engineering)

## How do you process large CSV files without running out of memory?

You can stream the file in chunks (for example using chunked readers), process line-by-line, or use a library that supports streaming and type inference control. You also avoid loading wide columns you do not need, and you write results incrementally. For very large data, consider Parquet and/or distributed processing.

```python
# pandas chunks: aggregate incrementally, never hold the whole file
import pandas as pd

agg: dict[str, float] = {}
for chunk in pd.read_csv(
    "orders_2026.csv",
    usecols=["order_id", "amount", "country"],
    dtype={"amount": "float64", "country": "category"},
    chunksize=1_000_000,
):
    for country, total in chunk.groupby("country", observed=True)["amount"].sum().items():
        agg[country] = agg.get(country, 0.0) + total
```

```bash
# One-off scale: SQL over a CSV larger than memory (moves parsing into DuckDB)
duckdb -c "COPY (SELECT country, sum(amount) FROM read_csv_auto('orders_2026.csv') GROUP BY country) TO 'by_country.parquet' (FORMAT PARQUET);"
```

The theme is to aggregate or filter incrementally and emit as you go, so peak memory depends on chunk size and aggregation state rather than file size. Set explicit dtypes, because inference is itself a memory and time cost.

[Table of Contents](#Python-for-Data-Engineering)

## How do you implement retries with exponential backoff?

Retries should include exponential backoff and jitter to avoid thundering herds. You should only retry on transient errors (timeouts, rate limits) and limit total retry time. Always make operations idempotent or use deduplication to prevent duplicates on retries.

```python
# Capped exponential backoff with full jitter, or use tenacity's
# wait_exponential_jitter + retry_if_exception_type for the declarative version
import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class TransientError(Exception):
    """Raised for retryable failures (timeouts, 429, 503)."""


def retry(fn: Callable[[], T], *, attempts: int = 5, base: float = 0.5, cap: float = 30.0) -> T:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except TransientError as exc:
            last = exc
            if attempt == attempts:
                break
            time.sleep(random.uniform(0, min(cap, base * 2 ** (attempt - 1))))
    raise RuntimeError(f"retries exhausted after {attempts} attempts") from last
```

Rules: retry only transient classes; honor `Retry-After` on 429/503; cap total time, not just attempts; use idempotency keys on writes; add jitter; and log every attempt with the attempt number.

[Table of Contents](#Python-for-Data-Engineering)

## What logging practices are important for data pipelines?

Logs should include pipeline identifiers, run ids, input/output counts, and key timestamps. Structured logging (JSON) helps search and correlation. You should log errors with context and avoid logging sensitive data.

```python
# JSON logging with run-scoped context fields
import json
import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("orders")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {"level": record.levelname,
                                   "logger": record.name,
                                   "message": record.getMessage()}
        payload.update(getattr(record, "extra_fields", {}))
        if record.exc_info:
            payload["traceback"] = self.formatException(record.exc_info)
        return json.dumps(payload)


handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
log.handlers = [handler]
log.info("stage_complete", extra={"extra_fields": {"run_id": "r-123", "rows_in": 1000, "rows_out": 998}})
```

Standards that matter: one start/end line per stage with `run_id`, dataset, and partition; counts in and out; `logging` with a JSON formatter rather than `print`; never log secrets or raw PII; `exc_info=True` for exceptions; and a correlation id so logs join to traces and the control table.

[Table of Contents](#Python-for-Data-Engineering)

## How do you structure a Python project for data pipelines?

A common structure separates reusable library code from job entrypoints. You keep configuration separate, use dependency injection for external services, and standardize logging and error handling. Small CLI entrypoints improve local runs and CI tests.

A common layout is `src/<pkg>/` with `config.py`, `io/`, `transforms/` (pure functions), and `jobs/` (thin CLI entrypoints), plus `tests/unit`, `tests/integration`, and `dags/` where Airflow files import the package.

Principles: business logic lives in importable modules while `jobs/` is a thin shell; config is parsed into a typed object once (`Settings.from_env()` returning a frozen dataclass); clients are injected so tests can substitute fakes; there are **no import-time side effects** (DAG parsing depends on this); and the package is installed (`uv sync`) so jobs and tests import the same code.

[Table of Contents](#Python-for-Data-Engineering)

## How do you manage dependencies and reproducible environments?

Use pinned dependencies and a lockfile (or equivalent) and isolate environments (virtualenv/containers). Reproducibility also requires pinning Python versions and building deterministic images. CI should use the same environment definition as production.

```bash
# Reproducible workflow: lock once, install exactly what CI and prod use
uv lock                         # writes uv.lock with hashes
uv sync --frozen                # install exactly the lockfile
uv run pytest                   # tests run in the pinned environment
```

```yaml
# pyproject.toml (excerpt, shown as YAML for readability)
project:
  name: acme-data
  requires-python: ">=3.12"
  dependencies: ["pyarrow>=17,<18", "polars>=1.0,<2", "httpx>=0.27,<1"]
  optional-dependencies:
    spark: ["pyspark==3.5.1"]
    dev: ["pytest>=8", "ruff", "mypy"]
```
Anti-patterns: unpinned transitive dependencies (behavior changes silently on rebuild); installing packages at task runtime; different environments for CI and production; and hand-maintaining hundreds of `==` pins instead of using a lockfile tool. Container images should pin the base Python by digest, `COPY uv.lock`, run `uv sync --frozen`, and then copy `src` - the same lock the tests use.

[Table of Contents](#Python-for-Data-Engineering)

## How do you test data transformations in Python?

Use small fixture datasets and assert expected outputs (golden tests). Add property tests for invariants (non-negative amounts, uniqueness). Integration tests validate real connectors and schemas, but they should be isolated and stable.

Keep transformations **pure** so the fast unit layer covers most logic, then add one integration test per connector behind a marker.

```python
# tests/unit/test_orders.py
import pandas as pd
import pytest

from acme_data.transforms.orders import add_tax


@pytest.fixture
def orders() -> pd.DataFrame:
    return pd.DataFrame({"order_id": ["o1", "o2"], "amount_cents": [1000, 2000],
                         "country": ["DE", "US"]})


def test_add_tax(orders):
    out = add_tax(orders, rates={"DE": 0.19, "US": 0.0})
    assert out["amount_cents"].tolist() == [1190, 2000]


# Property test: for any list of non-negative amounts the tax never decreases them
# @given(st.lists(st.integers(min_value=0), min_size=1))
# def test_tax_never_decreases(amounts): ...
```

```bash
uv run pytest tests/unit -q                       # always, in CI
uv run pytest -m integration --maxfail=1          # opt-in, needs a test warehouse
```

Keep fixtures small enough to verify by eye, and assert business rules rather than snapshotting current output - change-detector tests pass forever and catch nothing.

[Table of Contents](#Python-for-Data-Engineering)

## How do you profile and optimize slow Python code?

Profile first to find hotspots (CPU, IO, memory). Common fixes include vectorizing operations, reducing data copies, using efficient data structures, and offloading heavy compute to native libraries or distributed engines. Optimization should be guided by measurable impact.

Pick the tool by question: `cProfile` + `pstats` for wall-clock hotspots, `line_profiler` for a specific line, `tracemalloc`/`memray` for peak or leaking memory, and `py-spy dump` to see whether a running process is IO- or CPU-bound.

```python
# cProfile + pstats: sort by cumulative time to find the real hotspot
import cProfile
import pstats


def main() -> None:
    run_pipeline("2026-10-04")


profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()
pstats.Stats(profiler).sort_stats("cumulative").print_stats(20)
```

Common wins in order of impact: vectorize row-wise `.apply`/loops (`(df["amount"] * (1 + df["tax_rate"])).sum()` instead of `iterrows`); avoid copies (`copy=False`, reuse buffers, prefer Arrow over `to_list()`); choose the right container; reduce IO by batching and streaming; and move compute to SQL/Spark when the data never needed to be in Python.

[Table of Contents](#Python-for-Data-Engineering)

## How do you write memory-safe Python ETL code?

Memory-safe ETL code avoids loading unbounded data into lists or DataFrames. Prefer iterators, chunked reads, streaming writes, and explicit column selection. This is especially important for scripts that run in containers with fixed memory limits.

Example:

```python
import csv

def active_users(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "active":
                yield {
                    "user_id": int(row["user_id"]),
                    "email": row["email"].lower(),
                }

for user in active_users("users.csv"):
    send_to_api(user)
```

This processes one row at a time instead of building a full in-memory collection. In interviews, call out the trade-off: row-by-row code is memory efficient, while vectorized/batch processing can be faster when data fits in memory.

Checklist: bound every buffer (chunk, batch, and queue sizes); select columns in the reader rather than dropping later; use `category` dtype for low-cardinality strings and downcast numerics; never `concat` inside a loop (collect and concat once, or stream to disk); and cap concurrency so parallel fetches cannot exceed the container limit. Test with a larger-than-expected input, because a pipeline that only works on the sample partition is an outage waiting to happen.

[Table of Contents](#Python-for-Data-Engineering)

## How do you design Python code so a data pipeline is restartable?

A restartable pipeline can safely resume after failure without corrupting downstream data. Use idempotent writes, deterministic output paths, checkpoints/control tables, and stable run identifiers. Avoid hidden global state and make external side effects explicit.

Example pattern:

```python
def run_partition(ds: str) -> None:
    source = f"s3://raw/events/ds={ds}/"
    staging = f"s3://warehouse/events_staging/run_ds={ds}/"
    final = f"s3://warehouse/events/ds={ds}/"

    records = transform(read_json(source))
    write_parquet(records, staging)
    validate_partition(staging)
    replace_partition(staging, final)
    mark_success("events", ds)
```

The important idea is to write to staging first, validate, then atomically publish or replace the final partition. If the job retries, it produces the same partition instead of appending duplicates. A control table (`platform.partition_state` with dataset, partition, status, attempt, rows_written, finished_at) tracks per-partition state so the loop can skip completed work.

Rules that make restart safe: deterministic paths (same logical date, same output); atomic publish via rename, partition overwrite, or MERGE; a stable run id passed through every stage; explicit enumeration of external side effects; and no mutable module-level state that assumes one run per process.

[Table of Contents](#Python-for-Data-Engineering)

## How do you handle bad records in Python pipelines?

Do not let one malformed row either crash an entire batch blindly or disappear silently. A strong pipeline separates valid records from rejected records, records the reason for rejection, and emits metrics so data quality issues are visible.

```python
# Dead-letter records carry enough context to replay, plus a metric
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class DeadLetter:
    source_file: str
    line_number: int
    error_message: str
    payload: str
    detected_at: str


def parse_with_dlq(row: dict[str, str], source_file: str, line_number: int) -> dict[str, Any] | None:
    try:
        return {"order_id": row["order_id"], "amount": float(row["amount"])}
    except (KeyError, ValueError) as exc:
        dead_letter.write(asdict(DeadLetter(
            source_file=source_file, line_number=line_number, error_message=str(exc),
            payload=json.dumps(row)[:4000], detected_at=datetime.now(timezone.utc).isoformat(),
        )))
        REJECTED.labels(pipeline="orders").inc()
        return None
```

In production, rejected records go to a dead-letter path/table with the source file, line number, pipeline version, and error message, so teams can fix upstream data or replay rejects after correction. Enforce a reject-rate threshold so a flood of malformed records blocks rather than silently publishing. **Failure mode:** swallowing bad rows with `try/except: pass` - the job goes green, the metric declines, and the records cannot be replayed.

[Table of Contents](#Python-for-Data-Engineering)

## When should you use pandas, Polars, PyArrow, or Spark from Python?

Use pandas for small to medium in-memory analysis and simple transformations. Use Polars or PyArrow when you need faster columnar processing, lazy execution, or efficient Parquet/Arrow interoperability on a single machine. Use Spark/PySpark when data volume, shuffle requirements, or production architecture require distributed processing.

Example decision rule:

+ pandas: one CSV or Parquet extract that fits comfortably in memory
+ PyArrow: efficient file/schema operations, Parquet datasets, Arrow interchange
+ Polars: fast local transformations and lazy query optimization
+ PySpark: joins, aggregations, and pipelines over data too large for one machine

The interview answer should emphasize workload shape, not tool popularity. A 5 GB file may be fine in Polars on a large instance, while a 500 GB join with skewed keys usually belongs in Spark or a warehouse.

```python
# Polars: lazy scan with projection and predicate pushdown on a large local dataset
import polars as pl

result = (
    pl.scan_parquet("s3://acme-curated/orders/*/*.parquet")
    .filter(pl.col("order_date") == "2026-10-04")
    .group_by("country")
    .agg(pl.col("amount").sum().alias("revenue"))
    .collect(streaming=True)
)
```

Rule of thumb: **stay single-node until the data genuinely exceeds memory or the shuffle does not fit on one machine.** Polars/DuckDB push that boundary higher than pandas, and moving to Spark prematurely costs cluster operations and JVM serialization you did not need to pay.

[Table of Contents](#Python-for-Data-Engineering)

## Real world use cases for Python for Data Engineering

### 1. E-commerce: API ingestion with retries and a dead-letter queue

A retailer pulls orders from a partner REST API that rate-limits aggressively. Roughly 4M orders/day arrive in 5-minute windows, then land in S3 and load into the warehouse.

```python
# Bounded-concurrency fetcher with retry and backoff; exhausted pages go to a DLQ
import asyncio

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter


class RateLimited(Exception):
    pass


@retry(retry=retry_if_exception_type((RateLimited, httpx.TransportError)),
       wait=wait_exponential_jitter(initial=1, max=60), stop=stop_after_attempt(5), reraise=True)
async def fetch_page(client: httpx.AsyncClient, cursor: str | None) -> dict:
    response = await client.get("/orders", params={"cursor": cursor, "limit": 500})
    if response.status_code == 429:
        raise RateLimited(response.headers.get("Retry-After", "unknown"))
    response.raise_for_status()
    return response.json()
```

A page that exhausts retries is written to a quarantine prefix with its cursor, so the pull resumes from the last good cursor instead of re-reading the whole day.

**Why this design:** the API is the bottleneck, so async IO plus bounded concurrency maximizes throughput, retries with jitter absorb 429s, and a durable cursor makes a failure cost one page rather than one day.

### 2. Fintech: reconciliation of two systems with Polars

A payments team reconciles ~120M transactions/day between a core ledger and the warehouse, classifying differences before the close.

```python
# Vectorized reconciliation: a set join, not a loop over 120M rows
import polars as pl

ledger = pl.scan_parquet("s3://acme-ledger/txn/dt=2026-10-04/*.parquet").select("txn_id", "amount_cents")
warehouse = pl.scan_parquet("s3://acme-wh/txn/dt=2026-10-04/*.parquet").select("txn_id", "amount_cents")

recon = (
    ledger.join(warehouse, on="txn_id", how="full", suffix="_wh")
    .with_columns(
        pl.when(pl.col("amount_cents").is_null()).then(pl.lit("missing_in_warehouse"))
        .when(pl.col("amount_cents_wh").is_null()).then(pl.lit("missing_in_ledger"))
        .when(pl.col("amount_cents") != pl.col("amount_cents_wh")).then(pl.lit("amount_mismatch"))
        .otherwise(pl.lit("match")).alias("recon_status")
    )
    .group_by("recon_status").agg(pl.len().alias("count"))
    .collect(streaming=True)
)
```

**Why this design:** reconciliation is a set operation, so a vectorized join handles 120M rows on one node in minutes, and the output classifies every difference instead of returning a binary gate the finance team cannot act on.

### 3. Multi-tenant SaaS: memory-bounded export per tenant

A B2B platform lets customers download their data. Some tenants have billions of events; the export service runs in a container with a 2 GB limit and must never OOM.

```python
# Server-side cursor plus fetchmany keeps memory proportional to the batch
BATCH = 100_000


def stream_tenant_events(conn, tenant_id: str, out_path: str) -> int:
    written = 0
    with gzip.open(out_path, "wt", encoding="utf-8") as handle, conn.cursor(name="export_cursor") as cur:
        cur.itersize = BATCH
        cur.execute("SELECT event_id, event_ts FROM events WHERE tenant_id = %s", (tenant_id,))
        while rows := cur.fetchmany(BATCH):
            for row in rows:
                handle.write(json.dumps(row) + "\n")
            written += len(rows)
    return written
```

**Why this design:** the container limit is a hard constraint, so memory is bounded by the batch rather than the tenant, and compressed NDJSON streams bytes to disk instead of buffering them.

### 4. ML feature platform: a reproducible training snapshot

An ML team builds daily features for 40M users. Reproducibility matters because model comparisons must attribute changes to the model, not to a re-run of feature code.

```python
# Installable, versioned feature job with a content hash for the snapshot
import hashlib

import polars as pl


def build_features(input_glob: str, code_version: str) -> tuple[pl.DataFrame, str]:
    frame = (
        pl.scan_parquet(input_glob)
        .group_by("user_id")
        .agg(pl.col("event_type").eq("view").sum().alias("views_1d"),
             pl.col("amount").sum().alias("spend_1d"))
        .collect(streaming=True)
    )
    digest = hashlib.sha256(f"{code_version}{frame.shape}{frame.sum().to_dict()}".encode())
    return frame, digest.hexdigest()[:16]
```

**Why this design:** the job is a normal installable package with a lockfile, so CI and production run the same code and dependency versions, and a content hash identifies the exact snapshot an experiment trained on.

[Table of Contents](#Python-for-Data-Engineering)
