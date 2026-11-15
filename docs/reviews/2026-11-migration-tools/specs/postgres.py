import sys; sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad")
from nbtools import build

SPEC = r'''
%% md
# PostgreSQL for data pipelines

Most pipelines start in an application database: orders, customers and payments written by a web service into
PostgreSQL. The data engineer does not own that database, but every extract, every incremental load and every
change feed depends on how it behaves: its constraints, its transactions, and what a reader can and cannot see
while others write.

This lesson covers what a pipeline needs from a source database: constraints, idempotent upserts, transactions,
concurrent writers, incremental extraction that does not miss rows, safe pagination, indexes and query plans,
change data capture and bulk loading.

*Last reviewed: November 2026, against the PostgreSQL 18 documentation.*

**How this notebook runs.** Colab has no PostgreSQL server, and the handbook never connects to one. The runnable
cells use **DuckDB**, whose SQL follows PostgreSQL closely: the same `create table` constraints, `insert ... on
conflict`, transactions with snapshot isolation, and `merge`. Where PostgreSQL behaves differently (locking,
isolation levels, replication), the PostgreSQL commands are shown in fenced blocks labelled `sql` and are not run.

**Prerequisites:** [SQL 12: views and changing data](../sql/sql-12-views-and-changing-data.ipynb) and
[Data modeling 5: normalized and operational models](../data-modeling/data-modeling-05-normalized-and-operational-models.ipynb).
%% code
# Setup: installs the packages this notebook needs when they are missing (e.g. in Colab).
!pip install -q duckdb~=2.0
%% md
## Setup and sample data

The first cell creates a database file in a scratch folder, so that several connections can share it like
sessions on one server. The second creates the shop's operational tables, `customers` and `orders`, with the
keys and constraints an application database would have, and inserts a few rows.
%% code
import tempfile
import time
from pathlib import Path

import duckdb

work = Path(tempfile.mkdtemp(prefix="postgres-"))
db = duckdb.connect(str(work / "shop.duckdb"))


def session():
    """A second session on the same database, like another client connected to the server."""
    return db.cursor()


def show(sql, con=None):
    (con or db).sql(sql).show()
%% code
db.sql("""
create table customers (
    customer_id integer primary key,
    email       varchar not null unique,
    segment     varchar not null check (segment in ('smb', 'mid-market', 'enterprise')),
    updated_at  timestamp not null
);
create table orders (
    order_id    integer primary key,
    customer_id integer not null references customers (customer_id),
    status      varchar not null check (status in ('placed', 'paid', 'shipped', 'cancelled')),
    amount      decimal(10, 2) not null check (amount >= 0),
    updated_at  timestamp not null
);
insert into customers values
    (1, 'ops@acme.example',   'smb',        timestamp '2026-03-01 09:00:00'),
    (2, 'buy@bright.example', 'enterprise', timestamp '2026-03-01 09:05:00');
insert into orders values
    (101, 1, 'paid',    120.00, timestamp '2026-03-01 10:00:00'),
    (102, 2, 'placed',   80.00, timestamp '2026-03-01 10:01:00'),
    (103, 1, 'shipped',  45.50, timestamp '2026-03-01 10:02:00');
""")
show("select * from orders order by order_id")
%% md
## Know what the source database is for

PostgreSQL is a **row store** built for many small transactions: insert one order, update one status, read one
customer by key. Each row is stored together on a page, and indexes find rows by key. An analytical scan of a
year of orders reads every page and competes with the application for disk, memory and locks.

So a pipeline treats the primary database as something to read from carefully: extract incrementally, read from
a **replica** where one exists, keep queries indexed and short, and move analysis into a warehouse or lakehouse.

**Where it matters**
- Agreeing an extraction method with the team that owns the database: replica, export, or change data capture.

**Watch out for**
- A long-running extract on the primary: in PostgreSQL it holds back `VACUUM` cleanup (old row versions cannot be
  removed while your snapshot might need them) and table bloat grows.
- `select *` from a wide table when the pipeline needs five columns.
%% md
## Constraints enforce the model

Primary keys, `not null`, `unique`, `check` and foreign keys (`references`) are rules the database enforces on
every write. They are the strongest data-quality checks a pipeline will ever get, because a bad row never exists.
Knowing them tells you which assumptions are safe downstream: an order always has a customer; an amount is never
negative.

**Where it matters**
- Deciding which data-quality tests a pipeline needs: test what the source does *not* enforce.

**Watch out for**
- Constraints the application enforces in code but the database does not: they break during a bug or a
  backfill script. Check the actual DDL (`\d orders` in `psql`).
%% md
### Try writes that break the rules

Each insert below breaks one constraint. The loop prints the error type and the first line of the message.
%% code
bad_writes = {
    "duplicate key": "insert into orders values (101, 1, 'paid', 10, now())",
    "unknown customer": "insert into orders values (104, 9, 'paid', 10, now())",
    "negative amount": "insert into orders values (105, 1, 'paid', -5, now())",
    "unknown status": "insert into orders values (106, 1, 'lost', 10, now())",
}
for label, sql in bad_writes.items():
    try:
        db.sql(sql)
        print(f"{label:17} accepted")
    except duckdb.Error as error:
        print(f"{label:17} {type(error).__name__}: {str(error).splitlines()[0][:70]}")
show("select count(*) as orders from orders")
%% md
**What to notice:** All four writes were rejected, each with a constraint error, and the table still has three
orders. Downstream, a pipeline does not need a test for duplicate `order_id` or negative amounts from this
source; it does need tests for rules the source cannot express, such as "a shipped order was paid first".
%% md
## Upserts make loads idempotent

A load that runs twice must leave the same result as a load that runs once: retries and backfills depend on it.
`insert ... on conflict (key) do update` inserts new keys and updates existing ones in one statement; PostgreSQL
spells it the same way. `excluded` refers to the row that was proposed for insertion.

**Where it matters**
- Loading a batch of changed rows into a current-state table, in the source or in a staging database.

**Watch out for**
- An upsert that always overwrites: a late, older delivery can replace newer data. Add a condition on a version or
  timestamp column (`where excluded.updated_at > orders.updated_at`).
%% md
### Apply the same batch twice

The batch updates order 102 and adds order 104. Run it twice and compare.
%% code
upsert = """
insert into orders as o
select * from (values
    (102, 2, 'paid',   80.00, timestamp '2026-03-01 11:00:00'),
    (104, 2, 'placed', 15.00, timestamp '2026-03-01 11:01:00')
) v(order_id, customer_id, status, amount, updated_at)
on conflict (order_id) do update
set status = excluded.status, amount = excluded.amount, updated_at = excluded.updated_at
where excluded.updated_at > o.updated_at
"""
for attempt in (1, 2):
    db.sql(upsert)
    rows = db.sql("select count(*), sum(amount) from orders").fetchall()[0]
    print(f"after run {attempt}: {rows[0]} orders, total {rows[1]}")
show("select * from orders order by order_id")
%% md
**What to notice:** The second run changed nothing: still four orders and a total of 260.50. Order 102 is `paid`
with the 11:00 timestamp, and the `where excluded.updated_at > o.updated_at` guard means an older copy of the row
arriving later would be ignored rather than undoing the payment.
%% md
## Transactions keep a batch whole

A transaction groups statements so they all apply or none do. A pipeline that writes a batch in one transaction
never leaves half a batch behind when it fails; a reader sees the table before the batch or after it.

**Where it matters**
- Writing a batch and its control row (the new high-water mark) together, so the two never disagree.

**Watch out for**
- Autocommit drivers: each statement is its own transaction unless you open one (`begin`, or `with conn:` in
  psycopg), so a failure halfway leaves the first statements applied.
%% md
### Fail halfway through a batch

The batch inserts two orders and then breaks a constraint. Roll back and count.
%% code
try:
    db.begin()
    db.sql("insert into orders values (105, 1, 'placed', 30.00, timestamp '2026-03-01 12:00:00')")
    db.sql("insert into orders values (106, 2, 'placed', 25.00, timestamp '2026-03-01 12:01:00')")
    db.sql("insert into orders values (107, 9, 'placed', 10.00, timestamp '2026-03-01 12:02:00')")  # no customer 9
    db.commit()
except duckdb.Error as error:
    db.rollback()
    print("rolled back:", type(error).__name__)
show("select count(*) as orders, max(order_id) as last_order from orders")
%% md
**What to notice:** Orders 105 and 106 were inserted successfully before order 107 failed, yet the table still has
four orders ending at 104. The rollback removed the whole batch, so a retry can simply run it again.
%% md
## Concurrent writers

Two sessions that update the same row at the same time are the classic source of **lost updates**: both read the
stock level 10, both subtract one, both write 9, and one sale disappears. Databases prevent it in two ways:

- **Locking** (PostgreSQL's default `read committed`): the second `update` of a row waits for the first transaction
  to finish, then applies to the new value. `update ... set stock = stock - 1` is safe; reading the value into
  Python, subtracting there and writing it back is not, unless the read used `select ... for update`.
- **Conflict detection** (DuckDB, and PostgreSQL's `repeatable read` and `serializable`): the transaction that would
  overwrite another's change fails with a serialization error and must retry.

```sql
-- PostgreSQL: lock the row while computing the new value in application code
begin;
select stock from products where sku = 'SKU-01' for update;   -- other writers of this row wait here
update products set stock = 9 where sku = 'SKU-01';
commit;
```

**Where it matters**
- Control tables a pipeline updates (watermarks, job state) when two runs can overlap.

**Watch out for**
- Retrying a failed transaction by re-sending only the last statement: retry the whole transaction.
%% md
### Two sessions update the same order

Session A and session B both mark order 104 as paid, with different amounts. A writes first; neither has committed.
%% code
a, b = session(), session()
a.begin()
b.begin()
a.execute("update orders set status = 'paid', amount = 16.00 where order_id = 104").fetchall()
try:
    b.execute("update orders set status = 'paid', amount = 15.00 where order_id = 104").fetchall()
    print("B updated")
except duckdb.Error as error:
    print("B failed:", type(error).__name__, "-", str(error).splitlines()[0][:80])
    b.rollback()
a.commit()
show("select order_id, status, amount from orders where order_id = 104")
%% md
**What to notice:** B's update failed at once with a conflict error, because A had an uncommitted change to the
same row; A then committed its 16.00. Nothing was overwritten silently. In PostgreSQL under `read committed`, B's
`update` would instead have **waited** for A to finish and then applied on top of it (15.00 would win); under
`repeatable read` it would wait and then fail like here. Either way the application must decide: retry the whole
failed transaction, or report the conflict.
%% md
## Extract incrementally without missing rows

The usual incremental extract asks for rows with `updated_at` greater than the last high-water mark. It has a
blind spot: `updated_at` is set when a statement runs, but the row becomes visible only when its transaction
**commits**. A transaction that started before your extract and commits after it carries an `updated_at` older
than your new high-water mark, so the next extract skips it.

Three fixes, from simplest to most robust:

- Re-read a **lookback window** (for example the last 10 minutes before the high-water mark) and upsert, so
  re-reading a row is harmless.
- Use a commit-ordered value instead of a wall clock: PostgreSQL's `xmin` with `pg_snapshot_xmin(pg_current_snapshot())`,
  or a sequence assigned by a trigger at commit.
- Read the change log with **change data capture** instead of querying the table.

**Where it matters**
- Every timestamp-based incremental load from a busy database.

**Watch out for**
- Rows updated without touching `updated_at` (a bulk fix run by hand): only CDC sees those.
%% md
### Reproduce the missed row

A slow writer updates order 103 inside a transaction at 12:10 but has not committed. The extractor reads, then the
writer commits, then the extractor reads again from its new high-water mark.
%% code
writer, extractor = session(), session()
watermark = "2026-03-01 11:00:00"

writer.begin()
writer.execute("update orders set status = 'cancelled', updated_at = timestamp '2026-03-01 12:10:00' where order_id = 103").fetchall()
writer.execute("insert into orders values (108, 1, 'placed', 12.00, timestamp '2026-03-01 12:12:00')").fetchall()

db.sql("insert into orders values (109, 2, 'placed', 33.00, timestamp '2026-03-01 12:15:00')")  # a quick writer commits

first = extractor.execute(f"select order_id, status, updated_at from orders where updated_at > '{watermark}' order by updated_at").fetchall()
print("extract 1:", [(r[0], r[1], str(r[2])[11:]) for r in first])
watermark = str(max(r[2] for r in first))

writer.commit()  # the slow transaction becomes visible now, with timestamps older than the watermark

second = extractor.execute(f"select order_id, status from orders where updated_at > '{watermark}'").fetchall()
print("new watermark:", watermark[11:], "| extract 2:", second)

lookback = extractor.execute(f"""
select order_id, status from orders
where updated_at > timestamp '{watermark}' - interval 10 minute order by order_id""").fetchall()
print("extract 2 with a 10-minute lookback:", lookback)
%% md
**What to notice:** Extract 1 saw only the committed rows (104 at 11:01 and 109 at 12:15) and moved the watermark
to 12:15. When the slow writer committed, its rows carried 12:10 and 12:12, both older than the watermark, so the
plain extract 2 returned nothing and the cancellation of order 103 and new order 108 were lost. The lookback re-read
both, along with 109 again, which an idempotent upsert absorbs.
%% md
## Paginate with keys, not offsets

Extracting a large table in pages with `limit 1000 offset 2000` is fragile: an insert or delete between two pages
shifts every later row, so rows are skipped or read twice, and each page re-scans all earlier rows. **Keyset
pagination** remembers the last key and asks for `where order_id > :last order by order_id limit 1000`: stable
under concurrent writes, and an index range scan for every page.

**Where it matters**
- API-style extracts and backfills that read a big table in chunks.

**Watch out for**
- Keyset pagination on a non-unique column: add the primary key as a tie-breaker (`order by updated_at, order_id`).
%% md
### Delete a row between two pages

Read pages of two orders. Between page 1 and page 2, the application deletes an order from page 1.
%% code
def offset_pages():
    seen, page = [], 0
    while rows := db.sql(f"select order_id from orders order by order_id limit 2 offset {page * 2}").fetchall():
        seen += [r[0] for r in rows]
        if page == 0:
            db.sql("delete from orders where order_id = 102")  # happens while we paginate
        page += 1
    return seen


def keyset_pages():
    seen, last = [], 0
    while rows := db.sql(f"select order_id from orders where order_id > {last} order by order_id limit 2").fetchall():
        seen += [r[0] for r in rows]
        if last == 0:
            db.sql("delete from orders where order_id = 104")  # the same kind of change
        last = rows[-1][0]
    return seen


before = [r[0] for r in db.sql("select order_id from orders order by order_id").fetchall()]
print("orders before:", before)
print("offset pages: ", offset_pages())
print("keyset pages: ", keyset_pages())
%% md
**What to notice:** With offsets, deleting 102 after page 1 shifted every later row one place left, so page 2
started at 104 and order 103 was never read. With keys, page 2 asked for orders after 103 and read everything that
still existed (104 had been deleted before it was reached), skipping nothing.
%% md
## Indexes and query plans

A PostgreSQL index is usually a **B-tree**: a sorted structure that finds one key, or a range of keys, in a few page
reads. The primary key and `unique` constraints create one automatically. A composite index on `(customer_id,
updated_at)` serves filters on `customer_id` alone or on both, but not on `updated_at` alone, because the tree is
sorted by the first column first.

`explain` shows the plan; `explain (analyze, buffers)` runs the query and shows actual rows, time and pages read.
Look for `Seq Scan` on a large table where you expected `Index Scan`, and for estimated rows far from actual rows
(stale statistics: run `analyze`).

```sql
-- PostgreSQL: the index an incremental extract needs, built without blocking writes
create index concurrently orders_updated_at_idx on orders (updated_at, order_id);

explain (analyze, buffers)
select order_id, status from orders
where updated_at > '2026-03-01 11:00' order by updated_at, order_id limit 1000;
```

**Where it matters**
- Asking the database owners for the index an extract needs, instead of scanning their largest table nightly.

**Watch out for**
- `create index` without `concurrently` on a busy table: it blocks writes until it finishes.
- Functions on the indexed column (`where date(updated_at) = ...`): a plain index on `updated_at` cannot be used.
%% md
## Change data capture from the write-ahead log

Every change in PostgreSQL is first written to the **write-ahead log (WAL)**. With `wal_level = logical`, a
**replication slot** and a **publication**, a client such as Debezium receives each committed insert, update and
delete in commit order, with before and after images. This is the only extraction method that sees deletes, sees
every intermediate version, and has no commit-time blind spot.

```sql
-- PostgreSQL: what Debezium's connector needs
alter system set wal_level = logical;              -- restart required
create publication shop_pub for table customers, orders;
select pg_create_logical_replication_slot('shop_slot', 'pgoutput');
```

**Where it matters**
- Near-real-time replication into a lakehouse or warehouse, and any source where deletes must be captured.

**Watch out for**
- An abandoned replication slot: PostgreSQL keeps all WAL the slot has not confirmed, and the disk fills up.
  Monitor `pg_replication_slots` and the lag of each slot.
%% md
### Apply change events with `merge`

Three change events arrive from the log, in commit order: an update, an insert and a delete. `merge` applies them
to a replica of `orders` in one statement.
%% code
db.sql("create table orders_replica as select * from orders")
db.sql("""
create table change_events as select * from (values
    (1, 'u', 101, 1, 'shipped', 120.00, timestamp '2026-03-01 13:00:00'),
    (2, 'c', 110, 2, 'placed',   55.00, timestamp '2026-03-01 13:01:00'),
    (3, 'd', 109, null, null,     null, timestamp '2026-03-01 13:02:00')
) e(lsn, op, order_id, customer_id, status, amount, updated_at)
""")
db.sql("""
merge into orders_replica r
using change_events e on r.order_id = e.order_id
when matched and e.op = 'd' then delete
when matched then update set status = e.status, amount = e.amount, updated_at = e.updated_at
when not matched and e.op <> 'd' then insert values (e.order_id, e.customer_id, e.status, e.amount, e.updated_at)
""")
show("select order_id, status, amount from orders_replica order by order_id")
%% md
**What to notice:** Order 101 is now `shipped`, order 110 was inserted and order 109 is gone, all from one `merge`.
The events carry a log sequence number (`lsn`); a real consumer applies them in that order and records the last
`lsn` it applied, so a restart resumes without gaps or duplicates. If one batch could hold several events for the
same key, keep only the last one per key before merging.
%% md
## Bulk loading

Inserting rows one statement at a time pays a round trip and a transaction per row. Bulk paths stream many rows
in one command: PostgreSQL's `copy orders from stdin (format csv)` (psycopg's `cursor.copy()`), DuckDB's `copy` and
`read_csv`. For staging loads, copy into an unindexed staging table, then upsert into the target in one statement.

**Where it matters**
- Initial loads and backfills of millions of rows.

**Watch out for**
- `executemany` with a driver that sends one statement per row: it looks like a batch but is not.
%% md
### Compare row-by-row inserts with `copy`

Write 20,000 rows to a CSV file, then load them with one `insert` per row and with one `copy` command.
%% code
import csv

rows = [(i, i % 2 + 1, "placed", i % 100, "2026-03-02 09:00:00") for i in range(1000, 21000)]
csv_path = work / "orders_bulk.csv"
with csv_path.open("w", newline="") as handle:
    csv.writer(handle).writerows(rows)

db.sql("create table staging_rowwise (order_id int, customer_id int, status varchar, amount decimal(10,2), updated_at timestamp)")
db.sql("create table staging_copy as select * from staging_rowwise limit 0")

start = time.perf_counter()
db.begin()
for row in rows:
    db.execute("insert into staging_rowwise values (?, ?, ?, ?, ?)", row).fetchall()
db.commit()
rowwise = time.perf_counter() - start

start = time.perf_counter()
db.sql(f"copy staging_copy from '{csv_path}'")
bulk = time.perf_counter() - start

counts = db.sql("select (select count(*) from staging_rowwise), (select count(*) from staging_copy)").fetchall()[0]
print(f"row by row: {counts[0]} rows in {rowwise:.2f}s | copy: {counts[1]} rows in {bulk:.3f}s | copy was {rowwise / bulk:.0f}x faster")
%% md
**What to notice:** Both tables hold 20,000 rows, but `copy` loaded them many times faster (the exact ratio varies
by machine; it is usually in the tens or hundreds). Row-by-row inserts were already inside one transaction here;
with autocommit they would be slower still. Against a remote PostgreSQL server each row would also add a network
round trip.
%% md
## Check yourself

Answer each question in your own words before reading the answer.

**Q1.** Your nightly extract uses `where updated_at > :last_max`. The source team says some cancellations never reach the warehouse. What is the likely cause and fix?

**A.** Transactions that commit after the extract carry older `updated_at` values and fall behind the watermark. Re-read a lookback window and upsert, use a commit-ordered column, or switch to CDC.

**Q2.** Why is `update stock set qty = qty - 1 where sku = ?` safe under concurrency when reading `qty` into Python and writing back `qty - 1` is not?

**A.** The single statement reads and writes the row under the row lock, so a concurrent update waits and applies to the new value. Read-then-write in the application lets two sessions read the same old value; you need `select ... for update` or a retry on a serialization error.

**Q3.** Which source constraints let you skip downstream tests?

**A.** Those the database enforces: primary keys (uniqueness), `not null`, `check`, foreign keys. Test business rules the database cannot express, and anything enforced only in application code.

**Q4.** Why does a replication slot need monitoring?

**A.** PostgreSQL keeps every WAL segment the slot has not confirmed. If the consumer stops, WAL accumulates until the disk is full and the database stops accepting writes.

**Q5.** Why is keyset pagination better than offset pagination for extraction?

**A.** Offsets shift when rows are inserted or deleted between pages, so rows are skipped or duplicated, and each page rescans earlier rows. Keyset pages continue from the last key: stable and served by an index range scan.
%% md
## Key takeaways

- Treat the primary database as a shared production system: replicas, indexed incremental reads, short queries.
- Source constraints are guaranteed quality; test what they do not cover.
- `insert ... on conflict do update` with a version guard makes loads idempotent and safe against late deliveries.
- Transactions keep batches whole; concurrent writers need locks or retries, never read-modify-write in the app.
- Timestamp watermarks miss late commits: use a lookback with upserts, a commit-ordered column, or CDC.
- Paginate by key, load in bulk with `copy`, and give extracts the index they need.
%% md
**Next:** Continue with [Change data capture](../concepts/change-data-capture.ipynb) to go deeper into log-based
extraction, or with [Data modeling 7: loading and late data](../data-modeling/data-modeling-07-loading-and-late-data.ipynb)
for what happens to these rows in the warehouse.
'''

build("notebooks/topics/postgres/postgres.ipynb", SPEC)
