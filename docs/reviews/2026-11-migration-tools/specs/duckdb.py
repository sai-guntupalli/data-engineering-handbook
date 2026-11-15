import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# DuckDB

A finance analyst sends you three months of order exports as CSV and Parquet and asks for revenue by month and
region by lunchtime. Starting a Spark cluster or loading a warehouse is overkill; the data fits on a laptop.
DuckDB is an analytical SQL engine that runs inside your Python process: no server, no install beyond a pip
package, and it reads CSV, Parquet and JSON files directly.

This lesson covers when DuckDB is the right tool, how to query files in place, how it exchanges data with pandas
and Arrow without copying, how to write partitioned output, how to read its query plans, and where its single-process
design stops.

*Last reviewed: November 2026, against DuckDB 2.0.*

**Prerequisites:** [SQL 5: aggregations and CTEs](../sql/sql-05-aggregations-and-ctes.ipynb) and
[Parquet](../parquet/parquet.ipynb) for the file format.
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q duckdb~=2.0 pyarrow pandas
%% md
## Setup and sample data

The first cell opens an in-memory database and creates a scratch folder. The second writes the analyst's files:
`orders_2026_01.csv` and `orders_2026_02.csv` (one row per order, with a header), and `orders_2026_03.parquet`
for March, plus a small `regions.csv` lookup. The files are the data; nothing is loaded into tables yet.
%% code
import tempfile
from pathlib import Path

import duckdb

con = duckdb.connect()  # no path: an in-memory database that disappears when the connection closes
work = Path(tempfile.mkdtemp(prefix="duckdb-"))
print("DuckDB", duckdb.__version__)
%% code
con.sql(f"""
copy (select * from (values
    (1, 'C1', 'N', date '2026-01-03', 120.00), (2, 'C2', 'S', date '2026-01-09',  80.00),
    (3, 'C1', 'N', date '2026-01-21',  45.50), (4, 'C3', 'E', date '2026-01-28', 300.00)
) t(order_id, customer_id, region_code, order_date, amount)) to '{work}/orders_2026_01.csv' (header);

copy (select * from (values
    (5, 'C2', 'S', date '2026-02-02',  60.00), (6, 'C4', 'N', date '2026-02-14', 210.00),
    (7, 'C3', 'E', date '2026-02-20',  99.99)
) t(order_id, customer_id, region_code, order_date, amount)) to '{work}/orders_2026_02.csv' (header);

copy (select * from (values
    (8, 'C1', 'N', date '2026-03-05', 150.00), (9, 'C5', 'W', date '2026-03-11',  75.00),
    (10, 'C2', 'S', date '2026-03-30', 40.00)
) t(order_id, customer_id, region_code, order_date, amount)) to '{work}/orders_2026_03.parquet' (format parquet);

copy (select * from (values ('N', 'North'), ('S', 'South'), ('E', 'East'))
      t(region_code, region_name)) to '{work}/regions.csv' (header);
""")
print(sorted(p.name for p in work.iterdir()))
%% md
## Decide when DuckDB is the right tool

DuckDB is a **columnar, vectorized** engine like a cloud warehouse, but **embedded**: it is a library your
program calls, the way SQLite is for transactions. It uses every core of the machine and spills to disk when a
query needs more memory than it has, so it handles tens or hundreds of gigabytes on one machine.

The boundary is the process. One process writes a database file at a time; there is no user management, no
network endpoint and no cluster. That makes DuckDB a great tool for local analysis, tests of SQL
transformations, small and medium batch jobs, and a reader of files in object storage, and the wrong tool for an
application database with many concurrent writers or a shared warehouse for a company.

**Where it matters**
- Exploring an extract before you design a pipeline for it.
- Unit tests for SQL models: dbt with `dbt-duckdb`, or plain SQL run against fixture tables.
- Batch jobs whose input fits on one machine, where Spark's startup and shuffle cost buy nothing.

**Watch out for**
- Opening the same database file for writing from two processes: the second one fails to get the lock.
- Treating a laptop timing as a benchmark for production data sizes.
%% md
### Check what an in-memory database holds

An in-memory database starts empty. The files on disk are not tables until you query or load them.
%% code
con.sql("select database_name, path from duckdb_databases() where not internal").show()
con.sql("show tables").show()
%% md
**What to notice:** The database is called `memory` and has no path, and `show tables` lists nothing: the
CSV and Parquet files are not part of it. Passing a file name to `duckdb.connect("shop.duckdb")` would persist
tables in a single file instead.
%% md
## Query files in place

DuckDB treats a file path in `from` as a table. `read_csv` detects the delimiter, header and column types by
sampling the file, `read_parquet` uses the schema stored in the file, and a glob such as `orders_*.csv` reads
many files as one table. `filename = true` adds a column with the source file of each row, which is how you
trace a bad row back to its delivery.

**Where it matters**
- First look at an unfamiliar extract: column types, row counts and obvious problems in seconds.
- Joining files of different formats without an import step.

**Watch out for**
- Type detection from a sample: a column whose first rows are numbers and later rows text is guessed wrong.
  Pass `types={...}` or `columns={...}` for files you load repeatedly.
- Globs across files with different columns: use `union_by_name = true` so columns are matched by name.
%% md
### Let DuckDB detect the CSV schema

`describe` shows the types DuckDB inferred from the January file.
%% code
con.sql(f"describe select * from read_csv('{work}/orders_2026_01.csv')").show()
%% md
**What to notice:** `order_date` came back as `DATE` and `amount` as `DOUBLE` without being declared: DuckDB
sampled the values. A money column usually wants `DECIMAL(10,2)`, which you get by passing
`types={'amount': 'DECIMAL(10,2)'}`.
%% md
### Read many files and formats as one table

Read both CSV months with a glob, add March from Parquet, and record which file each row came from.
%% code
orders = con.sql(f"""
select order_id, customer_id, region_code, order_date, amount::decimal(10, 2) as amount,
       parse_filename(filename) as source_file
from read_csv('{work}/orders_*.csv', filename = true)
union all by name
select *, 'orders_2026_03.parquet' as source_file
from read_parquet('{work}/orders_2026_03.parquet')
""")
orders.show()
%% md
**What to notice:** Ten orders from three files form one relation. `source_file` says which delivery each row
came from, and `union all by name` matched the Parquet columns by name rather than by position. Nothing was
loaded into a table: `orders` is a query that runs again each time it is used.
%% md
## Use SQL and the Python relational API together

`con.sql(...)` returns a **relation**: a lazy query object. You can query a relation from SQL by its Python
variable name, chain methods on it (`filter`, `aggregate`, `order`), and only an action such as `.show()`,
`.fetchall()` or `.df()` runs it. That makes it easy to build a pipeline from small named steps.

**Where it matters**
- Notebooks and scripts that mix Python control flow with SQL steps.

**Watch out for**
- Re-running an expensive relation many times: materialize it with `create table ... as` once it is final.
%% md
### Join a relation to a CSV and aggregate

`orders` is the Python variable from the previous cell; the SQL refers to it directly.
%% code
monthly = con.sql(f"""
select date_trunc('month', o.order_date)::date as month,
       coalesce(r.region_name, 'Unknown') as region,
       count(*) as orders, sum(o.amount) as revenue
from orders o
left join read_csv('{work}/regions.csv') r using (region_code)
group by all
order by month, region
""")
monthly.show()
%% md
**What to notice:** March's order from region `W` appears as `Unknown`: the lookup file has no `W`, and the
left join kept the order instead of dropping its 75.00. `group by all` groups by every non-aggregated column, so
the query does not repeat the select list.
%% md
### Chain methods instead of writing SQL

The same relation API without a SQL string: filter, aggregate and order.
%% code
big = orders.filter("amount >= 100").aggregate("customer_id, count(*) as big_orders, sum(amount) as revenue").order("revenue desc")
print(big.sql_query()[:200], "...")
big.show()
%% md
**What to notice:** The method chain compiles to one SQL query (the first part is printed) and runs only at
`.show()`. Customer C3's 300.00 order puts it first; C1 has two orders of at least 100.
%% md
## Exchange data with pandas and Arrow

DuckDB reads pandas DataFrames, Polars DataFrames and Arrow tables in the Python scope as if they were tables,
and returns results as any of them (`.df()`, `.pl()`, `.to_arrow_table()`; `.arrow()` streams record batches). With Arrow the exchange is **zero-copy**: both
sides use the same columnar memory layout, so no rows are converted.

**Where it matters**
- Running a SQL step in the middle of a pandas or Polars workflow, or the reverse.
- Handing query results to a library that speaks Arrow (PyArrow datasets, Polars, Spark's Arrow path).

**Watch out for**
- `.df()` on a huge result: pandas holds everything in memory. Write to Parquet from DuckDB instead.
%% md
### Query a pandas DataFrame and get Arrow back

A pandas DataFrame of refunds lives only in Python. Join it to the orders and return an Arrow table.
%% code
import pandas as pd

refunds = pd.DataFrame({"order_id": [4, 7], "refund": [300.00, 20.00]})
net = con.sql("""
select o.order_id, o.amount, coalesce(r.refund, 0) as refund, o.amount - coalesce(r.refund, 0) as net_amount
from orders o left join refunds r using (order_id)
where r.refund is not null
order by o.order_id
""").to_arrow_table()
print(type(net).__name__, net.schema)
print(net.to_pandas())
%% md
**What to notice:** SQL referenced `refunds`, a pandas variable, without registering it. The result is a PyArrow
`Table` with typed columns, and `to_pandas()` converts it only when you ask. `amount` kept `decimal128(10, 2)`, but
`refund` arrived from pandas as a float, so `net_amount` became a `double`: mixing a decimal with a float widens to
float. Cast the pandas column (`refund::decimal(10, 2)`) when exact money arithmetic matters.
%% md
## Write partitioned Parquet

`copy (query) to 'folder' (format parquet, partition_by (col))` writes one Hive-style folder per value
(`month=2026-01/`), the layout Spark, Trino and warehouses expect. Reading it back with `hive_partitioning = true`
turns the folder names into a column, and a filter on that column skips whole folders.

**Where it matters**
- Producing a curated dataset for other engines from a single-machine job.

**Watch out for**
- Partitioning by a column with thousands of values: thousands of tiny files are slower to read than one.
- Re-running into an existing folder: add `overwrite_or_ignore` or write to a fresh folder per run.
%% md
### Write by month and read one month back

Write all orders partitioned by month, list the folders, then read only February.
%% code
con.sql(f"""
copy (select *, strftime(order_date, '%Y-%m') as month from orders)
to '{work}/curated_orders' (format parquet, partition_by (month))
""")
print(sorted(p.name for p in (work / "curated_orders").iterdir()))
con.sql(f"""
select month, count(*) as orders, sum(amount) as revenue
from read_parquet('{work}/curated_orders/*/*.parquet', hive_partitioning = true)
where month = '2026-02'
group by month
""").show()
%% md
**What to notice:** One folder per month, named `month=2026-01` and so on. The filter on `month` matched only
the February folder's three orders (369.99 in total); the next section shows the plan that skips the other
folders.
%% md
## Read query plans

`explain` shows the plan DuckDB will run; `explain analyze` runs the query and shows the rows and time per
operator. Read it from the bottom up: the scan, the filters pushed into it, then joins and aggregates. For Parquet
the scan shows which columns it reads and which filters it applies while reading, using the min and max values
stored per row group.

**Where it matters**
- Checking that a filter is pushed into the scan before blaming DuckDB for a slow query.

**Watch out for**
- Functions around a column (`where year(order_date) = 2026`) can stop min/max skipping; compare the column
  with a literal range instead.
%% md
### See the partition filter in the plan

Explain the February query from the previous section.
%% code
plan = con.sql(f"""
explain select count(*) from read_parquet('{work}/curated_orders/*/*.parquet', hive_partitioning = true)
where month = '2026-02'
""").fetchall()[0][1]
print("\n".join(line for line in plan.splitlines() if line.strip(" │┌┐└┘─")))
%% md
**What to notice:** The `Read Parquet` node shows `File Filters: month = '2026-02'` and `Scanning Files: 1/3`:
the other two folders were excluded from their names alone, before any file was opened. There is no separate
`Filter` operator above the scan.
%% md
## Persist, share and stop

A database file (`duckdb.connect("shop.duckdb")`) stores tables, views and macros. Many processes can open it
**read-only** at once; only one can open it for writing. For pipelines this suggests a pattern: a job writes a
file or a Parquet folder, then readers open the result read-only. For a shared, concurrent service use a
warehouse, Postgres, or MotherDuck (DuckDB as a hosted service).

**Where it matters**
- Shipping a small analytical dataset as one file to colleagues or to a dashboard tool.

**Watch out for**
- Storing the only copy of important data in a local `.duckdb` file: treat it as a build output.
%% md
### Save a table to a file and reopen it read-only

Create a database file with a `monthly_revenue` table, close it, and open it again read-only.
%% code
db_path = work / "shop.duckdb"
monthly_rows = monthly.to_arrow_table()  # `monthly` belongs to the in-memory connection; hand its rows over as Arrow
with duckdb.connect(str(db_path)) as writer:
    writer.sql("create table monthly_revenue as select * from monthly_rows")
with duckdb.connect(str(db_path), read_only=True) as reader:
    reader.sql("select count(*) as rows, sum(revenue) as revenue from monthly_revenue").show()
    try:
        reader.sql("delete from monthly_revenue")
    except duckdb.Error as error:
        print(type(error).__name__, "-", str(error).splitlines()[0][:90])
%% md
**What to notice:** The file kept the 9 month-and-region rows and their 1,180.49 total after the writer closed. The
read-only connection could query but not delete: DuckDB raised an error instead. A relation belongs to the
connection that made it, so `monthly` was handed to the file's connection as an Arrow table.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** A colleague wants three dashboards and a nightly job to write to the same `.duckdb` file at the same time. What do you tell them?

**A.** Only one process can open the file for writing. Have the job write a new file or Parquet folder and the dashboards open it read-only, or use a server database or warehouse if writes must be concurrent.

**Q2.** `read_csv('exports/*.csv')` fails because the newest file has an extra column. How do you read all files?

**A.** Add `union_by_name = true`: columns are matched by name and the missing column is null in the older files.

**Q3.** Why is `.to_arrow_table()` cheaper than `.df()` for a large result?

**A.** Arrow is DuckDB's own columnar layout, so the result is handed over without converting each value; pandas needs its own copy of every column.

**Q4.** A filter on a Parquet folder is slow. What do you check first?

**A.** Run `explain` and check whether the filter appears in the scan (pushed down) or as a separate `FILTER` above a full scan; then check whether a function around the column prevents min/max skipping.

**Q5.** When would you choose Spark over DuckDB for a batch job?

**A.** When the data does not fit one machine's disk and memory budget, when the job must share a cluster's resources and scheduler, or when it already runs in a Spark platform with Spark-specific connectors.
%% md
## Key takeaways

- DuckDB is an embedded, columnar SQL engine: a library in your process, not a server.
- Query CSV, Parquet and JSON in place with `read_csv`, `read_parquet` and globs; add `filename` for lineage.
- Relations are lazy; SQL can reference pandas, Polars and Arrow objects, and `.to_arrow_table()` returns results without copying.
- `copy ... (partition_by ...)` writes Hive-style folders that other engines read, and filters on the partition column skip folders.
- One writer per database file; share results as files opened read-only.
%% md
**Next:** Continue with [PostgreSQL for data pipelines](../postgres/postgres.ipynb), the database most pipelines
extract from, or with [Parquet](../parquet/parquet.ipynb) for the file format underneath.
'''

build("notebooks/topics/duckdb/duckdb.ipynb", SPEC)
