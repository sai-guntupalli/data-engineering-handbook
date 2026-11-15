import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from nbtools import build, run

PATH = "notebooks/topics/ingestion/ingestion-04-dlt.ipynb"
SPEC = """%% md
# Ingestion 4: Load into DuckDB with dlt

Ingestion 1 to 3 wrote cursors, retries, ledgers and upserts by hand. **dlt** (data load tool) is an open-source Python
library that packages those patterns: you yield records, and it infers a schema, creates and evolves tables, merges by
key, and keeps incremental state in the destination. This lesson loads orders into DuckDB with dlt and looks at what
it does at each step.

Every example runs real dlt with its DuckDB destination in a temporary folder. The same pipeline code runs against
BigQuery, Snowflake, Postgres or files on S3 by changing the `destination`.
%% code
# Setup: install notebook dependencies in Colab.
!pip install -q dlt[duckdb] duckdb~=2.0
%% md
## Setup and sample data

The next cell creates a temporary folder for the DuckDB file and dlt's working directory, defines `new_pipeline` to
build a pipeline into it, and `sql` to query the result. The sample data is a list of orders as an API would return
them, each with a nested list of items.
%% code
import os
from pathlib import Path
from tempfile import TemporaryDirectory

os.environ["RUNTIME__LOG_LEVEL"] = "WARNING"  # keep dlt's progress logs out of the output

import dlt
import duckdb

workspace = TemporaryDirectory()
base = Path(workspace.name)
database = base / "warehouse.duckdb"


def new_pipeline(name="shop"):
    return dlt.pipeline(
        pipeline_name=name,
        destination=dlt.destinations.duckdb(credentials=str(database)),
        dataset_name="raw",
        pipelines_dir=str(base / "pipelines"),
    )


def sql(statement):
    with duckdb.connect(str(database)) as connection:
        return connection.execute(statement).fetchall()


api_orders = [
    {"id": 1, "status": "placed", "updated_at": "2026-02-01T09:00:00Z", "items": [{"sku": "A", "qty": 1}]},
    {"id": 2, "status": "placed", "updated_at": "2026-02-01T10:00:00Z", "items": [{"sku": "B", "qty": 2}, {"sku": "C", "qty": 1}]},
]
print(len(api_orders), "orders from the API")
%% md
## A pipeline, a schema and load metadata

`pipeline.run(data, table_name=...)` normalizes the records, infers column names and types, creates the tables, and
loads them in one **load package**. dlt adds `_dlt_load_id` and `_dlt_id` to every row, and records each load in a
`_dlt_loads` table, so you can always tell which run wrote a row.

Nested lists do not fit in a column, so dlt **unnests** them into a child table, here `orders__items`, linked to the
parent row by `_dlt_parent_id`.

**Where it matters**

Most API payloads are nested JSON. dlt turns them into relational tables without hand-written flattening code, and the
load metadata answers "when did this row arrive?" during an incident.

**Watch out for**

Inferred types come from the first values dlt sees. A field that is `null` in the first batch, or a number that later
arrives as text, can end up with a type you did not intend. Declare important columns explicitly with `columns=` on
the resource.
%% code
pipeline = new_pipeline()
info = pipeline.run(api_orders, table_name="orders", write_disposition="merge", primary_key="id")
print("failed jobs:", info.has_failed_jobs)
print("tables:", [t[0] for t in sql("select table_name from information_schema.tables where table_schema = 'raw' order by 1")])
print("orders:", sql("select id, status from raw.orders order by id"))
print("items:", sql("select o.id, i.sku, i.qty from raw.orders o join raw.orders__items i on i._dlt_parent_id = o._dlt_id order by i.sku"))
%% md
**What to notice:** One run created `orders`, the child table `orders__items` and dlt's own `_dlt_loads`,
`_dlt_pipeline_state` and `_dlt_version` tables. The three items are linked to their orders through
`_dlt_parent_id`, so the join gives one row per item.
%% md
## Write dispositions: append, replace, merge

The **write disposition** decides what a load does to existing rows: `append` adds them (the default), `replace` swaps
the table for the new data, and `merge` upserts by a `primary_key`, like the incremental merges in dbt 3. dlt also
deduplicates within a load when merging.

**Where it matters**

Use `append` for immutable events, `replace` for small reference tables you reload whole, and `merge` for records that
change, such as orders or customers.

**Watch out for**

`append` is the default. Loading mutable records with it doubles them on every rerun, which looks fine until someone
sums a column. Choose the disposition before the first load: switching an existing table that has nested child tables
from `append` to `merge` fails, because merge needs a `_dlt_root_id` column the existing child rows do not have.
%% code
appended = new_pipeline("append_demo")
for _ in range(2):
    appended.run(api_orders, table_name="orders_appended")
print("append twice:", sql("select id, count(*) from raw.orders_appended group by id order by id"))

api_orders[0] = {**api_orders[0], "status": "paid", "updated_at": "2026-02-01T11:00:00Z"}
pipeline.run(api_orders, table_name="orders", write_disposition="merge", primary_key="id")
print("merge by id:", sql("select id, status from raw.orders order by id"))
%% md
**What to notice:** Appending the same two orders twice left two copies of each. Merging with `primary_key="id"`
updated order 1 to `paid` in place and left one row per order.
%% md
## Incremental loading with state

A resource can declare an **incremental cursor** with `dlt.sources.incremental("updated_at")`. dlt passes the last
value it saw into the next run, filters out records at or below it, and stores the new value as pipeline **state**.
The state is saved in the destination (the `_dlt_pipeline_state` table), so a pipeline restored on a new machine, with
its local working folder gone, continues where it stopped.

**Where it matters**

This is the high-water-mark pattern from Ingestion 1 and 2 without the bookkeeping: the checkpoint is committed with
the load, and moving the job between workers does not reset it.

**Watch out for**

The cursor only moves forward. To reprocess history, start a fresh pipeline name or reset the state deliberately; and
add a lag (the `lag` argument) for sources whose records can arrive late.
%% code
calls = []


@dlt.resource(name="orders_inc", primary_key="id", write_disposition="merge")
def orders_since(updated_at=dlt.sources.incremental("updated_at", initial_value="2026-01-01T00:00:00Z")):
    calls.append(updated_at.last_value)  # what an API call would send as updated_since
    yield [order for order in api_orders if order["updated_at"] > updated_at.last_value]


incremental = new_pipeline("incremental_demo")
incremental.run(orders_since())
api_orders.append({"id": 3, "status": "placed", "updated_at": "2026-02-01T12:00:00Z", "items": []})
incremental.run(orders_since())

import shutil

shutil.rmtree(base / "pipelines" / "incremental_demo")  # lose the local working folder
restored = new_pipeline("incremental_demo")
restored.run(orders_since())
print("cursor passed to each run:", calls)
print("rows:", sql("select id from raw.orders_inc order by id"))
%% md
**What to notice:** The first run started from the initial value; the second started from 11:00, the newest
`updated_at` it had loaded, and added only order 3. After the local folder was deleted, the restored pipeline still
started from 12:00, because dlt read its state back from the destination.
%% md
## Schema evolution and contracts

When records gain a field, dlt adds the column; when they nest deeper, it adds child tables. That keeps loads running
while sources change, but sometimes a new column should be a decision, not a surprise. A **schema contract** sets what
may change, separately for new tables, new columns and changed data types: `"evolve"` (the default) allows it,
`"freeze"` makes the load fail, and `"discard_value"` or `"discard_row"` drop the unexpected data. A bare
`schema_contract="freeze"` freezes all three, so it even refuses to create a table on the first load.

**Where it matters**

Use `evolve` for raw landing tables, so nothing is lost, and `freeze` for tables with downstream contracts, so a new or
renamed field is caught at load time rather than in a dashboard.

**Watch out for**

Evolution only adds. A field that disappears from the source leaves a column that is suddenly all nulls, and a renamed
field becomes a new column next to the old one; neither raises an error under `evolve`.
%% code
pipeline.run([{**api_orders[1], "coupon": "WELCOME"}], table_name="orders", write_disposition="merge", primary_key="id")
print("orders columns:", [c[0] for c in sql("select column_name from information_schema.columns where table_name = 'orders' and table_schema = 'raw'")])

frozen = new_pipeline("frozen_demo")
frozen.run(api_orders, table_name="orders_frozen")  # the first load creates the table
try:
    frozen.run([{**api_orders[0], "channel": "app"}], table_name="orders_frozen", schema_contract={"columns": "freeze"})
except Exception as error:
    print("frozen table rejected the load:", type(error).__name__)
%% md
**What to notice:** The record with a `coupon` field added a `coupon` column to `orders` without any code change. The
same kind of change against the frozen table, a new `channel` field, failed the load instead.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Items per order

**Difficulty:** Easy · about 5 min

Using the parent and child tables, count the items and total quantity per order.
%% code
# Try your solution here.
%% solution
print(sql(\"\"\"
select o.id, count(i._dlt_id) as items, coalesce(sum(i.qty), 0) as quantity
from raw.orders o left join raw.orders__items i on i._dlt_parent_id = o._dlt_id
group by o.id order by o.id
\"\"\"))
%% md
### Exercise 2: A reference table

**Difficulty:** Easy · about 10 min

Load a small `plans` table twice with `write_disposition="replace"`, changing a price between runs, and show that it
holds only the second version.
%% code
# Try your solution here.
%% solution
plans = new_pipeline("plans_demo")
plans.run([{"plan": "basic", "cents": 500}, {"plan": "plus", "cents": 900}], table_name="plans", write_disposition="replace")
plans.run([{"plan": "basic", "cents": 600}, {"plan": "plus", "cents": 900}], table_name="plans", write_disposition="replace")
print(sql("select plan, cents from raw.plans order by plan"))
%% md
### Exercise 3: Discard instead of fail

**Difficulty:** Medium · about 10 min

Load a record with an unexpected `channel` field into a new table using `schema_contract={"columns": "discard_value"}`
after a first normal load, and check whether a `channel` column exists.
%% code
# Try your solution here.
%% solution
discard = new_pipeline("discard_demo")
discard.run(api_orders[:1], table_name="orders_discard")
discard.run([{**api_orders[1], "channel": "app"}], table_name="orders_discard", schema_contract={"columns": "discard_value"})
columns = [c[0] for c in sql("select column_name from information_schema.columns where table_name = 'orders_discard'")]
print("channel column:", "channel" in columns, "| rows:", sql("select count(*) from raw.orders_discard")[0][0])
%% md
## Key takeaways

- dlt infers and creates tables from yielded records, unnests nested lists into child tables, and tags every row with
  the load that wrote it.
- Choose the write disposition deliberately: `append` for events, `replace` for small reference data, `merge` with a
  `primary_key` for records that change.
- `dlt.sources.incremental` keeps the cursor as state in the destination, so runs resume correctly even on a new
  machine.
- Schemas evolve by default; use a contract (`freeze` or `discard_*`) where a new column should be a decision.
%% md
**Next:** Continue the learning path with [PySpark: Start here](../pyspark/pyspark-00-start-here.ipynb). To validate
what you load, see [Validate data with Pandera](../concepts/pandera-data-quality.ipynb).
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
