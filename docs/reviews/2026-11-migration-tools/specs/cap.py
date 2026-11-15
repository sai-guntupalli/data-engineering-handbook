import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from nbtools import build, run

PATH = "notebooks/topics/concepts/end-to-end-pipeline-capstone.ipynb"
SPEC = """%% md
# Capstone: an end-to-end batch pipeline

This capstone joins the tools from the ingestion, data quality, dbt and Airflow lessons into one pipeline that runs
for real: a paginated partner API is loaded into DuckDB with dlt, each day is checked by a Pandera quality gate,
dbt builds and tests a revenue mart from validated days only, and an Airflow DAG runs the steps per data interval,
including a rerun and a day that fails its checks.

The pipeline code lives in one Python module, `orders_pipeline.py`, which the notebook calls while developing against
a **dev** warehouse and the Airflow DAG calls unchanged against a **prod** warehouse. Keeping logic out of the DAG file
is how production pipelines stay testable.
%% code
# Setup: install notebook dependencies in Colab.
!pip install -q apache-airflow~=3.4 dbt-core~=1.12 dbt-duckdb~=1.11 dlt[duckdb] pandera[pandas] httpx duckdb~=2.0 pandas~=3.0
%% md
## Setup and sample data

The next cell creates a workspace with separate dev and prod folders and writes three things into it:

- `orders_pipeline.py`, the pipeline module: the partner API (served by `httpx.MockTransport`) with three days of
  orders, and the functions `ingest`, `validate`, `transform` and `reconcile`;
- a dbt project whose DuckDB path comes from the `PIPELINE_HOME` environment variable, so one project serves both
  environments;
- an empty `validated_days` table in each warehouse, which the quality gate fills.

February 3 contains a bad record (a negative amount), which the gate must stop.
%% code
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

workspace = TemporaryDirectory()
root = Path(workspace.name)
code = root / "dags"  # Airflow's DAGs folder; the pipeline module lives beside the DAG
code.mkdir()
dev, prod = root / "dev", root / "prod"

(code / "orders_pipeline.py").write_text('''
\"\"\"Partner orders -> DuckDB (dlt) -> quality gate (Pandera) -> revenue mart (dbt).\"\"\"
import os
from pathlib import Path

import dlt
import duckdb
import httpx
import pandera.pandas as pa
from dbt.cli.main import dbtRunner

HOME = Path(os.environ["PIPELINE_HOME"])
WAREHOUSE = HOME / "warehouse.duckdb"
DBT_PROJECT = Path(__file__).resolve().parent.parent / "dbt"

SOURCE = {  # what the partner API returns for each day
    "2026-02-01": [(1, 10, "paid", 1200), (2, 11, "paid", 800), (3, 10, "refunded", 500)],
    "2026-02-02": [(4, 12, "paid", 950), (5, 11, "placed", 300)],
    "2026-02-03": [(6, 10, "paid", 700), (7, 13, "paid", -40)],
}


def partner_api(request):
    day, page = request.url.params["day"], int(request.url.params.get("page", 1))
    rows = [dict(zip(["id", "customer_id", "status", "cents"], r)) for r in SOURCE.get(day, [])]
    chunk = rows[(page - 1) * 2 : page * 2]
    return httpx.Response(200, json={"data": chunk, "next_page": page + 1 if page * 2 < len(rows) else None})


def fetch(day):
    with httpx.Client(base_url="https://partner.example.com", transport=httpx.MockTransport(partner_api)) as api:
        page = 1
        while page:
            body = api.get("/orders", params={"day": day, "page": page}).json()
            yield from body["data"]
            page = body["next_page"]


def ingest(day):
    \"\"\"Land one day's orders in raw.orders, merged by id so a rerun replaces rather than duplicates.\"\"\"
    pipeline = dlt.pipeline(
        pipeline_name="partner_orders",
        destination=dlt.destinations.duckdb(credentials=str(WAREHOUSE)),
        dataset_name="raw",
        pipelines_dir=str(HOME / "dlt"),
    )
    rows = [{**row, "order_day": day} for row in fetch(day)]
    pipeline.run(rows, table_name="orders", write_disposition="merge", primary_key="id")
    return len(rows)


SCHEMA = pa.DataFrameSchema(
    {
        "id": pa.Column(int, unique=True),
        "customer_id": pa.Column(int),
        "status": pa.Column(str, pa.Check.isin(["placed", "paid", "refunded"])),
        "cents": pa.Column(int, pa.Check.ge(0)),
    }
)


def validate(day):
    \"\"\"Check one landed day; only a day that passes is recorded in validated_days and reaches the mart.\"\"\"
    with duckdb.connect(str(WAREHOUSE)) as con:
        frame = con.execute("select id, customer_id, status, cents from raw.orders where order_day = ?", [day]).df()
        try:
            SCHEMA.validate(frame, lazy=True)
        except pa.errors.SchemaErrors as errors:
            cases = errors.failure_cases[["column", "check", "failure_case"]].to_dict("records")
            raise ValueError(f"{day} failed {len(cases)} check(s): {cases}") from None
        con.execute("insert or replace into main.validated_days values (?)", [day])
    return len(frame)


def transform():
    \"\"\"dbt build: staging and mart models, with their tests, in dependency order.\"\"\"
    result = dbtRunner().invoke(
        ["--log-level", "none", "build", "--project-dir", str(DBT_PROJECT), "--profiles-dir", str(DBT_PROJECT)]
    )
    statuses = {node.node.name: str(node.status) for node in result.result}
    if not result.success:
        raise RuntimeError(f"dbt build failed: {statuses}")
    return statuses


def reconcile(day):
    \"\"\"Paid revenue in the mart must equal paid revenue at the source.\"\"\"
    expected = sum(cents for _, _, status, cents in SOURCE[day] if status == "paid")
    with duckdb.connect(str(WAREHOUSE)) as con:
        actual = con.execute("select coalesce(sum(revenue_cents), 0) from main.daily_revenue where day = ?", [day]).fetchone()[0]
    if actual != expected:
        raise ValueError(f"{day}: mart has {actual} cents, source has {expected}")
    return actual
''')

dbt_project = root / "dbt"
(dbt_project / "models").mkdir(parents=True)
(dbt_project / "dbt_project.yml").write_text("name: orders\\nversion: '1.0'\\nprofile: orders\\n")
(dbt_project / "profiles.yml").write_text(
    "orders:\\n  target: env\\n  outputs:\\n    env:\\n      type: duckdb\\n"
    "      path: \\"{{ env_var('PIPELINE_HOME') }}/warehouse.duckdb\\"\\n      threads: 1\\n"
)
(dbt_project / "models" / "sources.yml").write_text('''
version: 2
sources:
  - name: raw
    schema: raw
    tables: [{name: orders}]
  - name: gate
    schema: main
    tables: [{name: validated_days}]
''')
(dbt_project / "models" / "stg_orders.sql").write_text('''
select id, customer_id, status, cents, order_day
from {{ source('raw', 'orders') }}
where order_day in (select day from {{ source('gate', 'validated_days') }})
''')
(dbt_project / "models" / "daily_revenue.sql").write_text('''
{{ config(materialized='table') }}
select order_day as day, count(*) as paid_orders, sum(cents) as revenue_cents
from {{ ref('stg_orders') }}
where status = 'paid'
group by order_day
''')
(dbt_project / "models" / "schema.yml").write_text('''
version: 2
models:
  - name: stg_orders
    columns:
      - name: id
        data_tests: [unique, not_null]
      - name: status
        data_tests:
          - accepted_values:
              arguments: {values: [placed, paid, refunded]}
  - name: daily_revenue
    columns:
      - name: day
        data_tests: [unique, not_null]
''')

import duckdb

for home in (dev, prod):
    home.mkdir()
    with duckdb.connect(str(home / "warehouse.duckdb")) as con:
        con.execute("create table main.validated_days (day varchar primary key)")

os.environ["PIPELINE_HOME"] = str(dev)  # the notebook develops against dev
sys.path.insert(0, str(code))
import orders_pipeline as pipeline

print("workspace:", sorted(p.name for p in root.iterdir()))
%% md
## Step 1: ingest a day from the API

`ingest(day)` pages through the partner API and loads the day into `raw.orders` with dlt, merged by `id`. Each row
carries `order_day`, the day it was loaded for, which every later step uses as the partition key.

**Where it matters**

Landing raw data first, unchanged, means every later step can be rerun from the warehouse without calling the API
again, and the raw table is the evidence when numbers are questioned.

**Watch out for**

The raw table holds whatever the source sent, including bad records. Nothing downstream should read it directly;
only the gated staging model does.
%% code
print("rows landed:", pipeline.ingest("2026-02-01"))
with duckdb.connect(str(dev / "warehouse.duckdb")) as con:
    print(con.execute("select id, status, cents, order_day from raw.orders order by id").fetchall())
%% md
**What to notice:** The API returned three orders over two pages, and dlt landed all three in `raw.orders`, each tagged
with its `order_day`.
%% md
## Step 2: the quality gate

`validate(day)` reads the landed day into pandas and checks it against a Pandera schema: unique IDs, known statuses and
non-negative amounts. If the day passes, it is recorded in `validated_days`; if not, the function raises with every
failing value, and the day is never recorded.

**Where it matters**

A gate between landing and publishing keeps bad source data out of marts and dashboards while still keeping it in raw
for investigation, and the error lists exactly which values to send back to the partner.

**Watch out for**

`lazy=True` collects all failures instead of stopping at the first, which is what you want in an alert. And the gate
must be the only way a day reaches staging, or a later transform will publish it anyway.
%% code
print("2026-02-01 passed:", pipeline.validate("2026-02-01"), "rows")
pipeline.ingest("2026-02-03")
try:
    pipeline.validate("2026-02-03")
except ValueError as error:
    print("gate stopped:", error)
with duckdb.connect(str(dev / "warehouse.duckdb")) as con:
    print("validated days:", con.execute("select day from main.validated_days").fetchall())
%% md
**What to notice:** February 1 passed and was recorded. February 3 failed one check: order 7's amount of -40 broke
`greater_than_or_equal_to(0)`. Its rows are in raw, but the day is not in `validated_days`.
%% md
## Step 3: build and test the mart with dbt

`transform()` runs `dbt build`: the staging model reads only validated days, the `daily_revenue` mart aggregates paid
orders per day, and the tests on both run right after each model is built. `reconcile(day)` then compares the mart
with the source.

**Where it matters**

Tests inside the build stop a broken model from feeding the mart; the reconciliation catches errors no schema test can
see, such as a wrong filter or a lost join.

**Watch out for**

Reconcile against the source, not against another table the pipeline built. A comparison between two outputs of the
same bug always agrees.
%% code
for name, status in pipeline.transform().items():
    print(f"{name}: {status}")
print("reconciled 2026-02-01:", pipeline.reconcile("2026-02-01"), "cents")
with duckdb.connect(str(dev / "warehouse.duckdb")) as con:
    print("mart:", con.execute("select * from main.daily_revenue order by day").fetchall())
%% md
**What to notice:** dbt built both models and all five tests passed. The mart holds only February 1, with two paid
orders totalling 2,000 cents, which matches the source; February 3's rows stayed out because that day never passed
the gate.
%% md
## Step 4: orchestrate with Airflow

The DAG below only orchestrates: each task calls one function from `orders_pipeline` for the run's data interval.
`ingest` takes the day from `data_interval_start`, so every run, rerun and backfill processes exactly its own day, and
`retries=0` keeps the demonstration's failure visible. The DAG runs against the **prod** warehouse: the same code,
a different `PIPELINE_HOME`.

It runs for February 1 and 2, reruns February 2 as a retry would, and then runs February 3, which must stop at the gate.

**Where it matters**

This is the shape of most batch pipelines in production: thin DAG, tested module, one partition per run, idempotent
steps, and a gate that fails loudly.

**Watch out for**

A failed day leaves a gap in the mart rather than a wrong number. Alert on it, fix the source or the code, and rerun
that one interval; nothing else needs touching.
%% code
(code / "orders_daily.py").write_text('''
from datetime import datetime, timezone

from airflow.sdk import dag, task
from airflow.timetables.interval import CronDataIntervalTimetable

import orders_pipeline as pipeline


@dag(
    schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"),
    start_date=datetime(2026, 2, 1, tzinfo=timezone.utc),
    default_args={"retries": 0},
    max_active_runs=1,
)
def orders_daily():
    @task
    def ingest(data_interval_start=None):
        day = data_interval_start.date().isoformat()
        print(f"LAB {day} ingest: {pipeline.ingest(day)} rows")
        return day

    @task
    def validate(day):
        try:
            print(f"LAB {day} validate: {pipeline.validate(day)} rows passed")
        except ValueError as error:
            print(f"LAB {day} validate FAILED: {error}")
            raise
        return day

    @task
    def transform(day):
        statuses = pipeline.transform()
        print(f"LAB {day} dbt build: {len(statuses)} nodes OK")
        return day

    @task
    def reconcile(day):
        print(f"LAB {day} reconcile: {pipeline.reconcile(day)} cents match the source")

    reconcile(transform(validate(ingest())))


dag_object = orders_daily()

if __name__ == "__main__":
    import sys

    for day in sys.argv[1:]:
        run = dag_object.test(logical_date=datetime.fromisoformat(day).replace(tzinfo=timezone.utc))
        print(f"LAB run for logical date {day}: {run.state}")
''')

airflow_home = root / "airflow"
env = {**os.environ, "PIPELINE_HOME": str(prod), "AIRFLOW_HOME": str(airflow_home),
       "AIRFLOW__CORE__DAGS_FOLDER": str(code), "AIRFLOW__CORE__LOAD_EXAMPLES": "False"}
subprocess.run([sys.executable, "-m", "airflow", "db", "migrate"], env=env, check=True, capture_output=True)


def run_dag(*logical_dates):
    done = subprocess.run([sys.executable, str(code / "orders_daily.py"), *logical_dates], env=env, capture_output=True, text=True)
    for line in (done.stdout + done.stderr).splitlines():
        if "LAB " in line and 'f"LAB' not in line:  # skip source lines quoted in tracebacks
            print(line.split("LAB ", 1)[1].split(" [airflow.")[0])
    if done.returncode:
        raise RuntimeError(done.stderr[-1500:])


run_dag("2026-02-02", "2026-02-03", "2026-02-03", "2026-02-04")
with duckdb.connect(str(prod / "warehouse.duckdb")) as con:
    print("prod mart:", con.execute("select * from main.daily_revenue order by day").fetchall())
    print("prod raw rows:", con.execute("select count(*) from raw.orders").fetchone()[0])
%% md
**What to notice:** Each logical date processed the day before it. February 1 and 2 went through all four tasks and
reconciled, and the repeated February 2 run did the same work again without adding rows: the mart has one row per day,
and raw holds seven orders (three, two and two), not nine. The February 3 run ingested its two orders but failed at
`validate` with the same message as in dev, so `transform` and `reconcile` never ran and the mart has no February 3
row.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Fix the source and rerun one day

**Difficulty:** Medium · about 15 min

The partner corrects order 7's amount to 40 cents. Change it in `orders_pipeline.py`, rerun the DAG for February 3's
interval, and show that the prod mart now has a February 3 row.
%% code
# Try your solution here.
%% solution
module = code / "orders_pipeline.py"
module.write_text(module.read_text().replace("(7, 13, \\"paid\\", -40)", "(7, 13, \\"paid\\", 40)"))
run_dag("2026-02-04")
with duckdb.connect(str(prod / "warehouse.duckdb")) as con:
    print(con.execute("select * from main.daily_revenue order by day").fetchall())
%% md
### Exercise 2: Add a mart test

**Difficulty:** Medium · about 10 min

Add a singular dbt test that fails if any day in `daily_revenue` has negative revenue, and run `transform()` in dev.
%% code
# Try your solution here.
%% solution
(dbt_project / "tests").mkdir(exist_ok=True)
(dbt_project / "tests" / "no_negative_revenue.sql").write_text(
    "select * from {{ ref('daily_revenue') }} where revenue_cents < 0\\n"
)
print({name: status for name, status in pipeline.transform().items() if "negative" in name})
%% md
### Exercise 3: What did each run publish?

**Difficulty:** Easy · about 10 min

Write one query on the prod warehouse that lists every loaded day with its raw row count, whether it passed the gate,
and its mart revenue.
%% code
# Try your solution here.
%% solution
with duckdb.connect(str(prod / "warehouse.duckdb")) as con:
    print(con.execute(\"\"\"
        select r.order_day, count(*) as raw_rows, v.day is not null as validated, max(m.revenue_cents) as revenue_cents
        from raw.orders r
        left join main.validated_days v on v.day = r.order_day
        left join main.daily_revenue m on m.day = r.order_day
        group by r.order_day, v.day order by r.order_day
    \"\"\").fetchall())
%% md
## Key takeaways

- Keep pipeline logic in a tested module and keep the DAG thin; the same functions then run in a notebook, in CI and
  under Airflow, against different environments.
- Land raw data unchanged, then gate each partition with explicit quality checks before anything downstream reads it.
- Let dbt build and test the models in one command, and reconcile the result against the source, not against another
  output.
- Drive every step from the run's data interval and make each idempotent, so a rerun or backfill touches only its own
  day and a failure leaves a gap instead of a wrong number.
%% md
**Next:** Continue the learning path with [Change data capture](change-data-capture.ipynb), which starts the streaming
half of this stage.
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
