import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from nbtools import build, run

PATH = "notebooks/topics/ingestion/ingestion-01-batch-patterns.ipynb"
SPEC = """%% md
# Ingestion 1: Replayable batch extraction

Most pipelines start by copying rows out of an operational database. This lesson builds that extract step by step
against a real SQL database: choosing between full and incremental extraction, paging with a cursor that never skips
rows, committing data and progress together so a crash is harmless, and catching the deletes an incremental extract
cannot see.

Every example uses Python's built-in `sqlite3` for both the source database and the landing table, so there is
nothing to install. The SQL is standard and carries over to PostgreSQL, MySQL or a warehouse.
%% md
## Setup and sample data

The next cell creates a source `orders` table, as an application would maintain it, and an empty landing database.
Each order has an `updated_at` timestamp the application sets on every change; two orders were updated in the same
second, which matters later.
%% code
import sqlite3

source = sqlite3.connect(":memory:")
source.execute("create table orders (id integer primary key, status text, cents integer, updated_at text)")
source.executemany(
    "insert into orders values (?, ?, ?, ?)",
    [
        (1, "placed", 1200, "2026-02-01 09:00:00"),
        (2, "placed", 800, "2026-02-01 09:05:00"),
        (3, "placed", 950, "2026-02-01 09:05:00"),  # same second as order 2
        (4, "placed", 400, "2026-02-01 09:10:00"),
        (5, "placed", 700, "2026-02-01 09:20:00"),
    ],
)
landing = sqlite3.connect(":memory:")
landing.execute("create table orders (id integer primary key, status text, cents integer, updated_at text)")
landing.execute("create table checkpoints (source text primary key, updated_at text, id integer)")
print(source.execute("select count(*) from orders").fetchone()[0], "orders in the source")
%% md
## Full and incremental extraction

A **full extract** copies the whole table every run. It is simple and always correct, including for deletes, but its
cost grows with the table. An **incremental extract** copies only rows changed since the last run, using a **cursor
column** that increases on every change, usually `updated_at` or a sequence number.

**Where it matters**

Full extracts suit small reference tables (countries, plans). Large, busy tables (orders, events) need incremental
extraction, or each run reads millions of unchanged rows.

**Watch out for**

An incremental extract is only as good as its cursor. If some code path updates rows without touching `updated_at`
(a bulk fix, a database trigger), those changes are never extracted. Confirm with the source team how the column is
maintained.
%% code
def full_extract():
    return source.execute("select * from orders order by id").fetchall()


def changed_since(updated_at):
    return source.execute("select * from orders where updated_at > ? order by updated_at, id", (updated_at,)).fetchall()


print("first run, full:", len(full_extract()), "rows")
source.execute("update orders set status = 'paid', updated_at = '2026-02-01 09:30:00' where id = 1")
print("second run, full:", len(full_extract()), "rows")
print("second run, incremental since 09:20:", changed_since("2026-02-01 09:20:00"))
%% md
**What to notice:** After one order changed, the full extract still read all five rows, while the incremental extract
read only order 1, now `paid` at 09:30. On a table with millions of rows, that difference is the whole cost of the
pipeline.
%% md
## Paging with a cursor that cannot skip rows

Large extracts read in pages. **Keyset pagination** remembers the last row of a page and asks for rows after it,
which stays fast at any depth (unlike `OFFSET`). The trap is ties: if the cursor is only `updated_at` and two rows
share a timestamp across a page boundary, `updated_at > last` skips the second one. The fix is a **tie-breaker**:
compare `(updated_at, id)` as a pair, with the same pair in `ORDER BY`.

**Where it matters**

Timestamps collide all the time: batch updates, second-precision columns, bulk imports. A skipped row is not an error;
it simply never arrives.

**Watch out for**

The tie-breaker must be unique and in the same order as the comparison. And rows committed late with an older
`updated_at` (a long transaction) can still slip behind the cursor; re-read a small overlap window, as dbt 3 does with
its lookback.
%% code
def extract_pages(page_size, tie_breaker):
    cursor, seen = ("", 0), []
    while True:
        if tie_breaker:
            sql = "select * from orders where (updated_at, id) > (?, ?) order by updated_at, id limit ?"
            page = source.execute(sql, (*cursor, page_size)).fetchall()
        else:
            sql = "select * from orders where updated_at > ? order by updated_at, id limit ?"
            page = source.execute(sql, (cursor[0], page_size)).fetchall()
        if not page:
            return seen
        seen.extend(row[0] for row in page)
        cursor = (page[-1][3], page[-1][0])


print("cursor on updated_at only:", extract_pages(1, tie_breaker=False))
print("cursor on (updated_at, id):", extract_pages(1, tie_breaker=True))
%% md
**What to notice:** With one row per page, the first page ended at order 2 (09:05). The timestamp-only cursor then
asked for rows after 09:05 and skipped order 3, which has the same timestamp; the pair cursor returned all five
orders. Larger pages only make the skip rarer, not impossible.
%% md
## Commit the data and the checkpoint together

The cursor value at the end of a run is the **checkpoint**. If the checkpoint is saved before the data is safely
written, a crash loses rows; if it is saved separately after, a crash re-extracts rows that were already written. The
robust design writes both in **one transaction** in the landing database, and makes the write an upsert keyed on the
primary key, so even a replay changes nothing.

**Where it matters**

Every extract eventually crashes mid-run: a network blip, a deploy, an out-of-memory kill. With data and checkpoint in
one transaction, the next run simply resumes.

**Watch out for**

A checkpoint kept in a local file or in the orchestrator's memory cannot share a transaction with the warehouse. If it
must live elsewhere, update it only after the load commits, and make the load idempotent.
%% code
def run_extract(page_size=2, crash_after_pages=None):
    row = landing.execute("select updated_at, id from checkpoints where source = 'orders'").fetchone()
    cursor = row or ("", 0)
    pages = 0
    while True:
        page = source.execute(
            "select * from orders where (updated_at, id) > (?, ?) order by updated_at, id limit ?", (*cursor, page_size)
        ).fetchall()
        if not page:
            return
        if crash_after_pages is not None and pages == crash_after_pages:
            raise RuntimeError("worker killed")
        cursor = (page[-1][3], page[-1][0])
        with landing:  # one transaction: the rows and the checkpoint commit together, or neither does
            landing.executemany(
                "insert into orders values (?, ?, ?, ?) on conflict (id) do update set "
                "status = excluded.status, cents = excluded.cents, updated_at = excluded.updated_at",
                page,
            )
            landing.execute("insert or replace into checkpoints values ('orders', ?, ?)", cursor)
        pages += 1


try:
    run_extract(crash_after_pages=1)
except RuntimeError as error:
    print("crashed:", error, "| landed ids:", [r[0] for r in landing.execute("select id from orders order by id")])
    print("checkpoint:", landing.execute("select updated_at, id from checkpoints").fetchone())
run_extract()
print("after resuming:", landing.execute("select id, status from orders order by id").fetchall())
%% md
**What to notice:** The crash came after the first page committed, so the landing table held orders 2 and 3 and the
checkpoint pointed at order 3. The rerun resumed from that checkpoint and landed the remaining three orders, including
order 1 in its `paid` state; nothing was lost or loaded twice.
%% md
## Deletes are invisible to incremental extraction

A row deleted in the source has no `updated_at` to compare, so an incremental extract never learns about it, and the
landing table keeps it forever. The options are to have the source **soft-delete** (set a `deleted_at` column, which
the cursor then sees), to use **change data capture** from the database log, or to **reconcile**: periodically compare
the sets of keys and remove what no longer exists.

**Where it matters**

Cancelled orders, closed accounts and GDPR erasure requests are deletes. A pipeline that misses them overstates
counts and can keep personal data it was required to remove.

**Watch out for**

Key reconciliation reads every key from both sides, so it is a scheduled job (daily or weekly), not part of every
run. Compare counts first; only when they differ do you need the full key comparison.
%% code
source.execute("delete from orders where id = 4")
run_extract()
source_count = source.execute("select count(*) from orders").fetchone()[0]
landed_count = landing.execute("select count(*) from orders").fetchone()[0]
print("source rows:", source_count, "| landed rows:", landed_count)
source_ids = {r[0] for r in source.execute("select id from orders")}
landed_ids = {r[0] for r in landing.execute("select id from orders")}
print("in landing but gone from the source:", sorted(landed_ids - source_ids))
%% md
**What to notice:** The incremental run after the delete found nothing to extract, so the landing table still has five
rows against four in the source. Comparing keys identifies order 4 as the row to remove.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Apply the reconciliation

**Difficulty:** Easy · about 5 min

Delete the rows that the reconciliation found from the landing table, and show that the counts now match.
%% code
# Try your solution here.
%% solution
with landing:
    landing.executemany("delete from orders where id = ?", [(i,) for i in landed_ids - source_ids])
print(source.execute("select count(*) from orders").fetchone()[0], landing.execute("select count(*) from orders").fetchone()[0])
%% md
### Exercise 2: One row per page

**Difficulty:** Medium · about 10 min

Update orders 2 and 3 to `shipped` with the same new `updated_at`, then run `run_extract(page_size=1)`. Show that both
changes landed.
%% code
# Try your solution here.
%% solution
source.execute("update orders set status = 'shipped', updated_at = '2026-02-01 10:00:00' where id in (2, 3)")
run_extract(page_size=1)
print(landing.execute("select id, status from orders where id in (2, 3) order by id").fetchall())
%% md
### Exercise 3: Soft deletes

**Difficulty:** Medium · about 15 min

Add a `deleted_at` column to the source, soft-delete order 5 by setting `deleted_at` and `updated_at`, and write a
query that an incremental extract could use to see the delete.
%% code
# Try your solution here.
%% solution
source.execute("alter table orders add column deleted_at text")
source.execute("update orders set deleted_at = '2026-02-01 11:00:00', updated_at = '2026-02-01 11:00:00' where id = 5")
checkpoint = landing.execute("select updated_at, id from checkpoints").fetchone()
print(source.execute("select id, deleted_at from orders where (updated_at, id) > (?, ?)", checkpoint).fetchall())
%% md
## Key takeaways

- Full extracts are simple and see deletes; incremental extracts scale, but depend on a cursor column that every change
  really updates.
- Page with a keyset cursor on `(updated_at, id)`, never on a timestamp alone, or rows that share a timestamp at a page
  boundary are skipped.
- Commit each batch and its checkpoint in one transaction, and upsert by primary key, so a crash or replay changes
  nothing.
- Incremental extraction cannot see hard deletes: use soft deletes, CDC or a scheduled key reconciliation.
%% md
**Next:** [Ingestion 2: APIs, pagination and retries](ingestion-02-apis.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
