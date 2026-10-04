## [Main title](../README.md)
### [Interview questions](full.md)

# Data System Design

**Notebook:** [`notebooks/topics/system-design.ipynb`](../notebooks/topics/system-design.ipynb) - runnable version of this topic with self-checking exercises.

Data system design interviews ask you to reason from requirements (freshness, volume, correctness, budget) to an architecture, then defend the trade-offs.

+ [How would you design an end-to-end batch analytics pipeline?](#How-would-you-design-an-end-to-end-batch-analytics-pipeline)
+ [How do you design a batch ingestion system?](#How-do-you-design-a-batch-ingestion-system)
+ [How do you design a streaming ingestion system?](#How-do-you-design-a-streaming-ingestion-system)
+ [How do you choose between batch, micro-batch, and streaming?](#How-do-you-choose-between-batch-micro-batch-and-streaming)
+ [How would you design a near-real-time ingestion pipeline?](#How-would-you-design-a-near-real-time-ingestion-pipeline)
+ [How do you ensure idempotency in data pipelines?](#How-do-you-ensure-idempotency-in-data-pipelines)
+ [How do you handle late arriving events and backfills?](#How-do-you-handle-late-arriving-events-and-backfills)
+ [How do you choose between batch and streaming?](#How-do-you-choose-between-batch-and-streaming)
+ [How do you model raw/silver/gold layers (bronze/silver/gold)?](#How-do-you-model-rawsilvergold-layers-bronzesilvergold)
+ [How do you design a data platform for multiple teams (multi-tenancy)?](#How-do-you-design-a-data-platform-for-multiple-teams-multi-tenancy)
+ [How do you design for schema evolution?](#How-do-you-design-for-schema-evolution)
+ [What are the main reliability patterns for pipelines?](#What-are-the-main-reliability-patterns-for-pipelines)
+ [How do you design observability for a data platform?](#How-do-you-design-observability-for-a-data-platform)
+ [How do you manage cost while meeting SLAs?](#How-do-you-manage-cost-while-meeting-SLAs)
+ [Real world use cases for Data System Design](#Real-world-use-cases-for-Data-System-Design)

## How would you design an end-to-end batch analytics pipeline?

A typical design is ingestion into a raw layer (immutable), transformation into curated datasets (cleaned and modeled), and publishing into marts/BI-serving datasets. You define SLAs, data quality checks, and ownership for each dataset. Batch pipelines are often scheduled daily/hourly and optimized for correctness and cost.

```text
sources                      raw (immutable)            silver (conformed)        gold (marts)
OLTP CDC / SaaS APIs  ->  s3://raw/orders/ds=/  ->  typed + deduped  ->  fct_orders, dim_customer
files / events        ->  s3://raw/events/ds=/  ->  sessionized      ->  mart_funnel_daily
                             |                          |                    |
                        contract check            DQ gates + tests     BI / reverse ETL
```

The design contract per layer:

+ Raw: append-only, never edited, one directory per logical date, replayable from source.
+ Silver: one row per business key per event time, typed, deduplicated, partitioned on the column everyone filters.
+ Gold: pre-aggregated to the grain the business asks for, refreshed after DQ passes.

Sizing drives most choices. A pipeline that processes 450 GB/day of raw JSON, compresses ~6x into Parquet, and backs up 90 days:

```python
raw_gb_per_day = 450
compression_ratio = 6
silver_gb_per_day = raw_gb_per_day / compression_ratio          # 75 GB
hot_days = 90
hot_tb = silver_gb_per_day * hot_days / 1000                     # 6.75 TB
scan_gb_per_query = 12                                           # one partition + 3 columns
warehouse_price_per_tb = 6.25                                    # $ per TB scanned (example)
cost_per_query = scan_gb_per_query / 1000 * warehouse_price_per_tb
print(round(cost_per_query, 4), "USD per query")                 # 0.075 USD per query
```

Reliability: idempotent partition rewrites, retries with backoff, and a DQ gate between layers so a bad batch never reaches a mart. Trade-off to voice: the raw+silver+gold split costs more storage and one extra copy, but it buys replayability and independent ownership; collapsing raw and silver into one layer is cheaper until the first schema incident.

[Table of Contents](#Data-System-Design)

## How do you design a batch ingestion system?

Start with source characteristics, freshness SLA, volume, schema, failure behavior, and replay needs. Land immutable raw data first, validate it, transform into curated tables, and publish only after checks pass. Track pipeline state in a control table.

```text
source API -> raw object storage -> validation -> curated Parquet -> warehouse mart
```

A control table makes every load observable and resumable:

```sql
CREATE TABLE control.pipeline_runs (
  pipeline_name    STRING,
  logical_date     DATE,
  source_watermark TIMESTAMP,
  new_watermark    TIMESTAMP,
  rows_read        INT64,
  rows_written     INT64,
  status           STRING,   -- running | success | failed
  error_message    STRING,
  started_at       TIMESTAMP,
  finished_at      TIMESTAMP
)
PARTITION BY logical_date
CLUSTER BY pipeline_name;
```

The loader reads the last successful watermark and requests only the delta, then commits a single atomic write:

```python
from datetime import datetime, timezone

def incremental_window(last_watermark: datetime, skew_minutes: int = 10):
    """Re-read a small overlap window to absorb late commits from the source."""
    from datetime import timedelta
    start = last_watermark - timedelta(minutes=skew_minutes)
    return start, datetime.now(timezone.utc)

# With an overlap window, the same source row can be seen twice;
# deduplicate on (business_key, updated_at) before publishing.
```

Key design points include idempotency, partitioning, retries, backfills, schema evolution, observability, and access control. Trade-off: an overlap window plus dedupe costs a little compute but removes the silent data-loss failure mode of a strict `>` watermark. For sources that support snapshot/CDC, prefer log-based capture over timestamp polling because it cannot miss deletes.

[Table of Contents](#Data-System-Design)

## How do you design a streaming ingestion system?

A streaming design needs a message broker, schema strategy, consumers/processors, state/checkpoints, dead-letter handling, and an idempotent sink. Decide whether ordering is required globally, per key, or not at all.

```text
application events
   -> Kafka / Pub/Sub / Kinesis (key = entity_id, 7-day retention)
   -> stream processor (Flink/Beam/Spark Structured Streaming)
        state store + event-time watermarks + checkpointing
   -> sink (lakehouse table, upsert keyed by entity_id + event_id)
   -> dead-letter topic (parse/schema errors, poison pills)
```

Event-time windows are the core abstraction: partition by key for per-entity ordering, window by event time, and emit after a watermark so out-of-order events are not dropped silently.

```python
# Structured Streaming: dedupe within the watermark and upsert into a Delta table
from pyspark.sql import functions as F

events = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "orders.v1")
    .option("startingOffsets", "earliest")
    .load()
    .selectExpr("CAST(value AS STRING) AS json", "timestamp AS kafka_ts")
    .select(F.from_json("json", schema).alias("e"), "kafka_ts")
    .select("e.*", "kafka_ts")
)

deduped = events.withWatermark("event_ts", "10 minutes").dropDuplicates(["event_id"])

(
    deduped.writeStream
    .option("checkpointLocation", "s3://acme/checkpoints/orders/")
    .trigger(processingTime="1 minute")
    .foreachBatch(lambda df, _: upsert(df))
    .start()
)
```

Discuss event time, late data, replay, exactly-once vs effectively-once semantics, and how you recover from downstream failures. Trade-off: exactly-once end to end requires a transactional sink (Delta/Iceberg/Kafka transactions) or idempotent upserts; many teams choose effectively-once with idempotent keys because it is simpler to operate, and they accept that a retry may reprocess rather than double-write.

[Table of Contents](#Data-System-Design)

## How do you choose between batch, micro-batch, and streaming?

Choose based on freshness SLA, cost, operational complexity, and business value. Batch is simpler and cheaper for daily/hourly reporting. Micro-batch fits near-real-time analytics where seconds/minutes are acceptable. Streaming fits low-latency operational decisions and event-driven systems.

Example:

+ daily finance close: batch
+ dashboard refreshed every 5 minutes: micro-batch
+ fraud decision before checkout completes: streaming

The cost gap is real and worth quantifying: a continuously running streaming job pays for provisioned workers 24x7, while a batch job pays only for its window.

```python
# Monthly compute cost of three options for the same 450 GB/day workload
gb_per_day = 450
days = 30

batch_hours_per_day = 2
batch_workers, worker_dpus = 20, 1          # example Dataflow/Spark worker sizing
dpu_hour = 0.10

stream_workers = 8
micro_batch_hours_per_day = 24 / 0.25       # a 15-minute trigger, per-day equivalent

batch_cost = batch_workers * worker_dpus * batch_hours_per_day * days * dpu_hour
stream_cost = stream_workers * worker_dpus * 24 * days * dpu_hour
print(f"batch ${batch_cost:,.0f}/mo vs always-on ${stream_cost:,.0f}/mo")

# Break-even freshness: how much is a 5-minute SLA worth per month?
freshness_premium = stream_cost - batch_cost
print(f"premium for continuous freshness: ${freshness_premium:,.0f}/mo")
```

The best design is the simplest one that meets the SLA. When someone asks for "real time", ask what decision changes in the next five minutes versus tomorrow morning; if nothing does, micro-batch is usually the correct answer.

[Table of Contents](#Data-System-Design)

## How would you design a near-real-time ingestion pipeline?

You typically use an event log or CDC stream (Kafka/PubSub/Kinesis) and write to a raw append-only store with durable offsets. Downstream, you materialize current-state tables and metrics with windowing and deduplication. You must design for replays, ordering, and late events.

```text
Postgres (WAL) -> Debezium -> Kafka (customers.cdc, key = id)
   -> landing sink (append-only, 1-min micro-batches) -> raw.customer_changes
   -> MERGE into silver.customers (current state, keyed by id, LATEST by lsn)
   -> 1-min aggregate into gold.customer_metrics
```

The current-state merge must be deterministic even when the same change arrives twice:

```sql
MERGE INTO silver.customers AS t
USING (
  SELECT id, name, tier, email, updated_at, lsn
  FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY id ORDER BY lsn DESC, updated_at DESC) AS rn
    FROM raw.customer_changes
    WHERE ds = CURRENT_DATE()
  ) WHERE rn = 1
) AS s
ON t.id = s.id AND s.lsn >= t.lsn
WHEN MATCHED AND s.lsn > t.lsn THEN UPDATE SET
  t.name = s.name, t.tier = s.tier, t.email = s.email,
  t.updated_at = s.updated_at, t.lsn = s.lsn
WHEN NOT MATCHED THEN INSERT (id, name, tier, email, updated_at, lsn)
VALUES (s.id, s.name, s.tier, s.email, s.updated_at, s.lsn);
```

Trade-offs: the LSN/version column makes replays safe but requires the source to emit a monotonic version. A 1-minute micro-batch is far cheaper and easier to operate than a true streaming state machine, and for most CDC use cases the business cannot tell the difference.

[Table of Contents](#Data-System-Design)

## How do you ensure idempotency in data pipelines?

Idempotency means retries do not change the final result. Common strategies include writing with deterministic keys (upserts/merges), using exactly-once features where available, and keeping raw data immutable while rebuilding derived layers. You also store checkpoints/watermarks consistently with writes.

Three patterns cover most production pipelines:

+ Partition replacement: recompute one `ds=` partition and atomically overwrite it. The unit of retry is the partition.
+ Deterministic merge: upsert on a business key with a monotonic version, so applying the same batch twice is a no-op.
+ Immutable append + dedupe at read: write every attempt, dedupe by key in the silver model (only viable if the key is stable).

```python
import hashlib

def event_key(row: dict) -> str:
    """Stable surrogate key: deterministic for the same logical event."""
    raw = f"{row['source']}|{row['event_id']}|{row['event_ts']}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def partition_path(ds: str) -> str:
    return f"s3://acme-curated/orders/ds={ds}/"

# A rerun of the same logical date writes to the same path and replaces it.
```

```sql
-- Idempotent merge: rerunning the same batch changes nothing
MERGE INTO gold.orders_daily AS t
USING (
  SELECT order_date, country, SUM(amount) AS revenue, COUNT(*) AS orders
  FROM silver.orders
  WHERE order_date = DATE '2026-10-04'
  GROUP BY order_date, country
) AS s
ON t.order_date = s.order_date AND t.country = s.country
WHEN MATCHED THEN UPDATE SET t.revenue = s.revenue, t.orders = s.orders
WHEN NOT MATCHED THEN INSERT (order_date, country, revenue, orders)
VALUES (s.order_date, s.country, s.revenue, s.orders);
```

Trade-off: merges on large tables are expensive compared with a partition overwrite, so use merges at the current-state layer (customers, inventory) and partition overwrite at the fact/aggregate layer (orders, daily metrics).

[Table of Contents](#Data-System-Design)

## How do you handle late arriving events and backfills?

You define allowed lateness and design tables by event time, not just ingestion time. For late events, you reprocess affected windows/partitions and update derived outputs deterministically. Backfills should be incremental, validated, and isolated so they do not corrupt current reporting.

```text
event arrives at T+3h with event_ts = yesterday 23:40
   -> belongs to ds=2026-10-03 (event-time partition)
   -> affected partition list = {2026-10-03} for daily, plus any rolling windows
   -> recompute those partitions, then recompute dependent marts
```

Allowed lateness is a business decision expressed as a contract:

```python
# Freshness and lateness policy per dataset
SLA = {
    "raw.orders":      {"max_lateness_hours": 48, "recompute": "event_partition"},
    "gold.orders_daily": {"max_lateness_hours": 48, "depends_on": ["raw.orders"]},
    "gold.fraud_alerts": {"max_lateness_hours": 0, "recompute": "stream_only"},
}

def impacted_partitions(late_event_ts, now, policy):
    from datetime import timedelta
    if now - late_event_ts > timedelta(hours=policy["max_lateness_hours"]):
        return []                       # beyond policy: route to a corrections table
    return [late_event_ts.date()]
```

Backfill rules that prevent incidents: run backfills into a temporary schema or table suffix, validate row counts and key uniqueness, compare against the old output, then swap. Never backfill in place while a dashboard is serving the same partition, and always bound the range (`--start`/`--end`) so a typo cannot rewrite two years of history. Trade-off: rolling windows (7/28/90-day) require recomputing every downstream window that a late event touches; if late data is common, either widen the raw layer's correction path or dedupe at read time so the window is rebuilt from a single source of truth.

[Table of Contents](#Data-System-Design)

## How do you choose between batch and streaming?

Streaming is chosen for low latency and continuous updates, but it adds complexity (state, ordering, exactly-once). Batch is simpler and often cheaper for many analytics use cases. Many real systems are hybrid: streaming ingestion into raw, batch modeling into marts.

```text
Decision checklist
1. What decision changes with freshness? (fraud block, dynamic pricing, ops alerting)
2. What is the true latency need? (<1s, <1min, <1h, daily)
3. Is ordering required? globally, per key, or not at all?
4. Can the sink accept idempotent upserts (Iceberg/Delta/Hudi), or is it append-only?
5. Who operates it at 3am, and what is the on-call cost?
```

The hybrid pattern is the most common production answer, and it keeps the expensive low-latency path narrow:

```text
Kafka -> stream processor -> raw.events (append, seconds)
                         -> gold.live_alerts (tiny, keyed aggregates)

S3/GCS raw.events -> hourly batch -> silver.events (dedupe, conform)
                                 -> gold.marts (full history, BI)
```

Trade-off: duplicating logic in both a stream and a batch job ("lambda architecture") means two implementations of the same metric that drift apart. Prefer one engine that supports both modes (Flink/Beam/Spark Structured Streaming) and a single business-logic module, or accept batch-only and make the freshness SLA explicit with stakeholders.

[Table of Contents](#Data-System-Design)

## How do you model raw/silver/gold layers (bronze/silver/gold)?

Bronze/raw is immutable ingestion with minimal transformation. Silver is cleaned, standardized, and deduplicated data with consistent schemas. Gold is business-ready marts and aggregates designed for BI and applications. This layering helps with reprocessing, governance, and clear contracts.

```sql
-- Bronze: append-only, source-shaped, cheap to write
CREATE TABLE bronze.orders (
  ingested_at TIMESTAMP,
  source_file STRING,
  payload     STRING
) PARTITION BY DATE(ingested_at);

-- Silver: typed, deduplicated, conformed grain = one row per order
CREATE TABLE silver.orders (
  order_id     STRING NOT NULL,
  customer_id  STRING NOT NULL,
  order_ts     TIMESTAMP,
  status       STRING,
  amount       NUMERIC,
  currency     STRING,
  updated_at   TIMESTAMP,
  _ingested_at TIMESTAMP
) PARTITION BY DATE(order_ts) CLUSTER BY customer_id;

-- Gold: pre-aggregated to the reporting grain
CREATE TABLE gold.orders_daily (
  order_date DATE,
  country    STRING,
  revenue    NUMERIC,
  orders     INT64
) PARTITION BY order_date CLUSTER BY country;
```

Each layer has a different owner and a different test strategy: bronze tests for arrival/completeness, silver tests for uniqueness and referential integrity, gold tests for reconciliation against the source of truth.

```python
# Layer contract check (runs in CI before a model is promoted)
def assert_silver_orders_uniqueness(conn, ds: str) -> None:
    n_dupes = conn.execute(
        "SELECT COUNT(*) FROM ("
        "  SELECT order_id FROM silver.orders WHERE DATE(order_ts) = %s"
        "  GROUP BY order_id HAVING COUNT(*) > 1)", (ds,)
    ).fetchone()[0]
    if n_dupes:
        raise AssertionError(f"{n_dupes} duplicate order_id values on {ds}")
```

Trade-off: more layers add storage and latency; a two-layer design (raw + marts) is fine for small teams. The value of silver is that reprocessing and joining happen once, in one governed place, instead of being re-derived by every consumer.

[Table of Contents](#Data-System-Design)

## How do you design a data platform for multiple teams (multi-tenancy)?

You need isolation (separate compute or quotas), clear ownership, and strong governance. Provide shared standards for naming, testing, and documentation, and a catalog for discovery. Multi-tenancy also requires controlling cost and preventing one team's workloads from impacting others.

```text
Platform plane
  catalog + lineage + contracts + CI checks (shared)
Workload plane per team
  team_a: warehouse namespace team_a, compute quota 200 slots, own service account
  team_b: warehouse namespace team_b, compute quota 100 slots, own service account
Storage plane
  s3://acme-curated/team=team_a/...   (bucket policies + Lake Formation/IAM)
  s3://acme-curated/team=team_b/...
```

Isolation is enforced at the compute, storage, and identity layers:

```yaml
# BigQuery: per-team reservation so a bad query cannot starve other teams
reservation: team_a_reservation
  slot_capacity: 200
  edition: STANDARD
  assignment: project acme-team-a
  max_slots: 400          # burst ceiling
```

S3 bucket policy fragment in which a team can only write under its own prefix:

```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::111122223333:role/team-a-etl"},
  "Action": ["s3:PutObject", "s3:DeleteObject"],
  "Resource": "arn:aws:s3:::acme-curated/team=team_a/*",
  "Condition": {"StringEquals": {"s3:prefix": "team=team_a/"}}
}
```

Cost accountability needs a shared dimension on every table:

```sql
-- Daily warehouse spend by team (BigQuery INFORMATION_SCHEMA example)
SELECT
  REGEXP_EXTRACT(job_id, r'^([^.]+)') AS team,
  ROUND(SUM(total_bytes_billed) / POW(1024, 4) * 6.25, 2) AS usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
GROUP BY team
ORDER BY usd DESC;
```

Trade-offs: physical isolation (separate projects/accounts per tenant) is the strongest control but multiplies operational overhead; logical isolation (namespaces, quotas, tags) is cheaper and usually sufficient. For regulated tenants, combine logical isolation on the platform with encryption keys or buckets scoped per tenant. Never let tenants share a mutable table without row-level security — one bad `DELETE` becomes a cross-tenant incident.

[Table of Contents](#Data-System-Design)

## How do you design for schema evolution?

You define compatibility rules, version schemas/contracts, and enforce them in CI and ingestion. Downstream transforms should tolerate additive fields but fail fast on breaking changes. You also maintain backward-compatible outputs where multiple consumers depend on stable schemas.

Compatibility rules, from safest to riskiest:

+ Backward compatible: add an optional field with a default; old readers still work.
+ Forward compatible: remove an optional field; new readers tolerate old data.
+ Full: both directions, the target for shared event contracts.
+ Breaking: rename, change type, change semantics, make a field required.

```json
{
  "type": "record",
  "name": "OrderEvent",
  "namespace": "acme.events",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "amount", "type": "double"},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "channel", "type": ["null", "string"], "default": null}
  ]
}
```

Enforce compatibility in CI against the registry, so a breaking change fails the pull request instead of production:

```python
# Illustrative compatibility gate for a schema registry
import json

REQUIRED = {"order_id", "amount"}

def check_backward_compatible(old: dict, new: dict) -> list[str]:
    errors: list[str] = []
    old_types = {f["name"]: f["type"] for f in old["fields"]}
    for field in new["fields"]:
        name, ftype = field["name"], field["type"]
        if name in old_types and old_types[name] != ftype:
            errors.append(f"type changed for {name}: {old_types[name]} -> {ftype}")
        if name not in old_types and "default" not in field:
            errors.append(f"new field {name} has no default (not backward compatible)")
    for name in REQUIRED:
        if name not in {f["name"] for f in new["fields"]}:
            errors.append(f"required field {name} removed")
    return errors

print(json.dumps({"ok": True}))
```

Trade-offs: strict full compatibility slows product teams but keeps shared pipelines stable; permissive evolution speeds delivery but requires defensive readers (`COALESCE`, `TRY_CAST`) everywhere. Table formats (Iceberg/Delta) let you add columns and even rename with column mapping, but they cannot fix a semantic change (a field that meant gross and now means net) — that requires a new column and a migration.

[Table of Contents](#Data-System-Design)

## What are the main reliability patterns for pipelines?

Common patterns include idempotent writes, retries with backoff, dead-letter queues, exactly-once or effectively-once processing, and separation of raw from derived layers. You also use checkpointing and consistent watermark management to avoid gaps and duplicates.

```text
retry with jitter -> dead-letter -> replay tool
   |                    |
   +-- transient         +-- poison record, schema error, bad key
checkpoint + watermark -> no gaps, no duplicates after restart
raw immutable layer    -> rebuild any derived table from source
```

A retry policy must distinguish transient from permanent failures, or it will hammer a broken dependency:

```python
import random
import time

class PermanentError(Exception):
    """Do not retry: schema violation, missing permission, bad key."""

class TransientError(Exception):
    """Retry with exponential backoff and jitter."""

def with_retry(fn, attempts: int = 5, base_delay: float = 1.0):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except PermanentError:
            raise
        except TransientError:
            if attempt == attempts:
                raise
            delay = base_delay * (2 ** (attempt - 1))
            time.sleep(delay + random.uniform(0, delay * 0.25))
    raise AssertionError("unreachable")
```

Dead-letter handling and replay:

```sql
-- Every failed record is quarantined with enough context to replay it
CREATE TABLE ops.dead_letter (
  pipeline_name STRING,
  stage         STRING,
  payload       STRING,
  error         STRING,
  failed_at     TIMESTAMP,
  replay_after  TIMESTAMP,
  replayed      BOOL DEFAULT FALSE
) PARTITION BY DATE(failed_at);

-- Replay after a fix
SELECT payload FROM ops.dead_letter
WHERE pipeline_name = 'orders_ingest' AND replayed = FALSE
  AND failed_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY);
```

Trade-offs: exactly-once sinks cost latency and require transactional storage; at-least-once plus idempotent writes is usually the pragmatic choice. A circuit breaker (stop consuming when the sink is down) protects the warehouse from a backlog storm, but it must page a human — silent pausing is how data freshness incidents start.

[Table of Contents](#Data-System-Design)

## How do you design observability for a data platform?

You monitor freshness, volume, quality, and lineage, plus pipeline runtime and failure rates. Alerts should be actionable with runbooks. Observability should be end-to-end: from source to final BI datasets and critical metrics.

The four signals that catch almost every incident:

```text
freshness  -> max(event_ts) vs now (is the data current?)
volume     -> row count vs trailing median (did we lose or double rows?)
schema     -> contract + nullability/range checks (is it the shape we expect?)
runtime    -> duration, queue time, retries (is it degrading?)
```

```sql
-- Freshness + volume as a single monitoring query
WITH daily AS (
  SELECT DATE(order_ts) AS ds, COUNT(*) AS rows, MAX(order_ts) AS max_ts
  FROM silver.orders
  WHERE DATE(order_ts) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY ds
)
SELECT
  ds,
  rows,
  ROUND(SAFE_DIVIDE(rows, AVG(rows) OVER (ORDER BY ds ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING)), 3) AS vs_7d_avg,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), max_ts, MINUTE) AS freshness_min
FROM daily
ORDER BY ds DESC;
```

Alert on symptoms users feel, not just on task failure: "gold.orders_daily is stale by more than 60 minutes during business hours" is actionable; "the 02:00 task printed a warning" is noise.

```python
# Threshold-based alert worth paging on
def evaluate_freshness(freshness_min: int, sla_min: int, rows: int, expected_rows: int) -> str:
    if freshness_min > sla_min:
        return "PAGE: freshness SLA breach"
    if expected_rows and rows < 0.5 * expected_rows:
        return "PAGE: volume drop > 50% vs expected"
    if expected_rows and rows > 2.0 * expected_rows:
        return "WARN: volume spike > 2x expected (possible duplicate load)"
    return "OK"
```

Trade-offs: every alert has a cost (on-call fatigue), so map each alert to a runbook and a decision. Column-level lineage is expensive to maintain manually; capture it automatically from the transformation tool (dbt/OpenLineage) and use it for impact analysis during incidents and deprecations. Trade-off: sampling 1% of rows for DQ checks is cheap and catches gross breakage but will miss a single corrupt customer; check referential and uniqueness constraints on full keys where the cost is acceptable.

[Table of Contents](#Data-System-Design)

## How do you manage cost while meeting SLAs?

You optimize storage layout (partitioning, file sizes), avoid unnecessary recomputation, and use selective materialization. You also schedule heavy jobs off-peak, enforce resource quotas, and track cost per dataset/pipeline. Cost is part of design, not just an afterthought.

```text
Biggest levers, roughly in order of impact
1. Stop scanning data you do not need: partition pruning, clustering, column pruning
2. Stop recomputing what has not changed: incremental models, change data only
3. Right-size compute: autoscaling, spot/preemptible for batch, quotas to stop runaway jobs
4. Tier storage: hot recent partitions, cold archive, expire snapshots and old raw files
5. Attribute cost: tag jobs, publish cost per dataset, put it on the team's dashboard
```

Sizing math makes the choice concrete: scanning an unpartitioned 6.75 TB table versus a single day's 75 GB partition.

```python
total_tb = 6.75
daily_tb = 0.075
price_per_tb = 6.25
queries_per_day = 400

unpartitioned_cost = total_tb * price_per_tb * queries_per_day * 30
partitioned_cost = daily_tb * price_per_tb * queries_per_day * 30
print(f"${unpartitioned_cost:,.0f} vs ${partitioned_cost:,.0f} per month")
print(f"saving: {1 - partitioned_cost / unpartitioned_cost:.1%}")
# $506,250 vs $5,625 per month -> 98.9% saving
```

```sql
-- Incremental model: only rebuild the days that changed
INSERT INTO gold.orders_daily
SELECT DATE(order_ts), country, SUM(amount), COUNT(*)
FROM silver.orders
WHERE DATE(order_ts) BETWEEN DATE '2026-10-01' AND DATE '2026-10-04'
GROUP BY 1, 2;

-- Expire snapshots and old raw files so storage does not grow forever
ALTER TABLE silver.orders EXPIRE SNAPSHOTS OLDER THAN INTERVAL '30' DAY;
```

Trade-offs: aggressive incremental models are cheap but harder to backfill and debug; the full-refresh simplicity of a small mart is worth its compute cost. Caching dashboards and materializing a few expensive joins buys latency at the cost of freshness — state the acceptable staleness explicitly rather than letting it happen implicitly. Finally, quota a team's compute so one accidental `SELECT *` cannot produce a five-figure bill; alert at 50% and 80% of budget, not after the fact.

[Table of Contents](#Data-System-Design)

## Real world use cases for Data System Design

### 1. Retail omni-channel daily revenue close

Business context: 1,800 stores plus an e-commerce site need a single revenue number by 07:00 local time, reconciled to the general ledger within 0.5%. Volume: 40M order lines/day at peak season (Black Friday 3-4x), ~450 GB raw JSON/day.

```text
POS batches + web/Kafka orders
   -> raw.orders_events (ds=, immutable, 2-year retention)
   -> silver.orders (dedupe by order_id+line_no, event-time partition)
   -> gold.orders_daily (date x channel x country)
   -> GL reconciliation report + BI dashboard at 07:00
```

```sql
-- Reconciliation gate: pipeline is not "done" until this delta is within tolerance
WITH pos AS (
  SELECT DATE(sale_ts) AS ds, SUM(amount) AS pos_revenue
  FROM silver.pos_sales WHERE DATE(sale_ts) = DATE '2026-10-04' GROUP BY 1
), web AS (
  SELECT DATE(order_ts) AS ds, SUM(amount) AS web_revenue
  FROM silver.orders WHERE DATE(order_ts) = DATE '2026-10-04' GROUP BY 1
)
SELECT ds, pos_revenue, web_revenue, pos_revenue + web_revenue AS total,
       ABS(1 - (pos_revenue + web_revenue) / NULLIF(gl_revenue, 0)) AS variance
FROM pos JOIN web USING (ds) JOIN ledger.gl_revenue USING (ds)
WHERE ABS(1 - (pos_revenue + web_revenue) / NULLIF(gl_revenue, 0)) > 0.005;  -- must return 0 rows
```

Why this design: the ledger needs a defensible number at a fixed time, so correctness and reproducibility beat freshness; the immutable raw layer lets finance replay any disputed day, and the reconciliation gate turns a silent accounting bug into a failed pipeline.

### 2. Fintech payments ledger with near-real-time balances

Business context: a payments processor must show merchants a near-current balance and feed anti-fraud rules within seconds, while keeping an immutable, auditable ledger. Volume: 25M transactions/day (~300 events/s, 2,000/s peak), 5 KB/event.

```text
core ledger (Postgres, WAL) -> Debezium -> Kafka (key = account_id, 7-day retention)
   -> Flink: event-time windows, 30s watermark, state per account
        -> gold.account_balances (upsert, keyed by account_id)
        -> gold.txn_alerts (fraud rule hits)
   -> raw.ledger_changes (append) -> hourly batch -> silver.ledger (dedupe by lsn)
```

```python
# Sizing the stream: can a single keyed state machine keep up?
tps_peak = 2000
event_bytes = 5 * 1024
state_per_account_bytes = 4 * 1024
accounts = 8_000_000

ingress_mb_s = tps_peak * event_bytes / 1e6
total_state_gb = accounts * state_per_account_bytes / 1e9
print(f"ingress {ingress_mb_s:.1f} MB/s, state {total_state_gb:.1f} GB")
# Fine for a distributed Flink job; checkpoint interval bounds recovery time.
```

Why this design: the Kafka log is the replayable source of truth, the stream maintains only the small balance state, and the batch path rebuilds the full ledger for audit. Keeping fraud logic on the streaming path (not the dashboard) keeps the latency budget under the checkout timeout.

### 3. Marketing attribution across paid channels

Business context: growth teams spend $2M/month across Google, Meta, TikTok, and affiliates and need cost-per-acquisition per channel within an hour of spend changes. Volume: 60M ad impressions/day, 12M sessions/day, 300K conversions/day, 15 source APIs.

```text
ad platform APIs (daily spend) -> raw.ad_spend
web/app clickstream (Kafka)   -> raw.sessions
CRM conversions (CDC)         -> raw.conversions
   -> silver.session_attribution (last-touch, 30-day lookback)
   -> gold.channel_cac_daily (spend, conversions, CAC, ROAS)
```

```sql
-- Last-touch attribution with a bounded lookback window
WITH touches AS (
  SELECT s.session_id, s.user_id, s.channel, s.session_ts, c.conversion_id, c.revenue,
         ROW_NUMBER() OVER (PARTITION BY c.conversion_id ORDER BY s.session_ts DESC) AS rn
  FROM silver.sessions s
  JOIN silver.conversions c
    ON s.user_id = c.user_id
   AND s.session_ts BETWEEN TIMESTAMP_SUB(c.conversion_ts, INTERVAL 30 DAY) AND c.conversion_ts
)
SELECT DATE(c.conversion_ts) AS ds, t.channel,
       COUNT(DISTINCT t.conversion_id) AS conversions, SUM(t.revenue) AS revenue
FROM touches t JOIN silver.conversions c USING (conversion_id)
WHERE t.rn = 1
GROUP BY 1, 2;
```

Why this design: channel spend changes daily but creatives and budgets change hourly, so the daily spend feed is joined to clickstream in a micro-batch rather than a stream; the lookback window is bounded at 30 days so the join stays affordable, and the fact table is keyed by conversion to keep the attribution model reproducible when late conversions arrive.

### 4. Multi-tenant B2B SaaS product analytics

Business context: 900 tenant companies each see only their own usage analytics, and the platform team needs cross-tenant health metrics. Volume: 2B product events/month (~800/s), 50 TB compressed in the lakehouse, 900 tenants.

```text
tenant SDKs -> Kafka (key = tenant_id) -> raw.events (tenant_id partition + ds)
   -> silver.events (conformed, dedup by event_id)
   -> gold.tenant_usage_daily (tenant_id, date, feature, events, seats)
   -> BI: row-level security filters by tenant_id; platform view aggregates across tenants
```

```sql
-- Row-level security for tenant-facing dashboards
CREATE ROW ACCESS POLICY tenant_isolation
ON gold.tenant_usage_daily
GRANT TO ('group:tenant_viewers@acme.com')
FILTER USING (tenant_id = SESSION_USER());
```

Why this design: the tenant key leads the partition and cluster keys so each tenant's queries scan only their slice, RLS prevents an application bug from leaking another tenant's data, and usage-based billing meters are computed from the same gold table the customer sees, which removes reconciliation disputes.

### 5. Industrial IoT predictive maintenance

Business context: 12,000 sensors across 40 plants stream vibration and temperature; the maintenance team wants alerts when a machine drifts, and data science wants labeled history for model training. Volume: 12,000 sensors x 1 reading/5s = 2,400 readings/s, ~900 GB/day uncompressed, 180 TB retained.

```text
sensors -> MQTT gateway -> Kafka (key = device_id)
   -> stream: 1-min tumbling aggregates, threshold + drift detector
        -> gold.device_alerts (near real time, paged to ops)
        -> raw.readings -> hourly batch -> silver.readings_1m (features)
   -> training snapshots (Parquet, immutable, per model version)
```

```python
import json
# 1-minute tumbling aggregate in Beam (runs on Dataflow/Flink)
import apache_beam as beam
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms.trigger import AfterWatermark, AccumulationMode

def extract_device(payload: dict):
    return payload["device_id"], payload

def to_reading(element):
    device_id, payload = element
    return {"device_id": device_id, "ts": payload["ts"], "value": payload["value"]}

with beam.Pipeline() as p:
    (
        p
        | "Read" >> beam.io.ReadFromPubSub(topic="projects/acme/topics/readings")
        | "Parse" >> beam.Map(lambda b: json.loads(b.decode("utf-8")))
        | "Key" >> beam.Map(extract_device)
        | "Window" >> beam.WindowInto(
            FixedWindows(60),
            trigger=AfterWatermark(late=beam.transforms.trigger.Repeatedly(
                beam.transforms.trigger.AfterProcessingTime(30))),
            accumulation_mode=AccumulationMode.DISCARDING,
        )
        | "Readings" >> beam.Map(to_reading)
        | "Aggregate" >> beam.CombinePerKey(
            beam.combiners.MeanCombineFn(), key=lambda r: r["device_id"])
        | "Write" >> beam.io.WriteToBigQuery(
            "acme:gold.device_minute_avg",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )
```

Why this design: alerting requires low latency, so a small streaming aggregate feeds operations, while the heavy feature engineering and model training run hourly on Parquet snapshots. Separating the hot alert path from the cold training path keeps the streaming job small and reproducible, and the raw append-only layer lets data science rebuild features when the model changes without touching production.

[Table of Contents](#Data-System-Design)
