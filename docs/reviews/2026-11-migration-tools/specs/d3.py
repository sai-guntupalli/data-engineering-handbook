import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from dbt_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/dbt/dbt-03-incremental-models.ipynb"
SPEC = f"""%% md
# dbt 3: Incremental models

Rebuilding a billion-row fact table every hour is slow and expensive. An **incremental** model builds the table once
and afterwards processes only new or changed rows. This lesson builds one step by step: filtering on a high-water
mark, merging updates by key, catching late-arriving rows with a lookback window, and handling a new source column.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell creates an empty dbt project with the `write`, `dbt` and `sql` helpers from dbt 1, then loads a raw
orders table where each row carries `updated_at`, the time the source system last changed it.

{HELPERS}


sql(\"\"\"
create table raw_orders as select * from (values
    (1, 'placed', 1200, timestamp '2026-02-01 09:00'),
    (2, 'placed', 800, timestamp '2026-02-01 10:00'),
    (3, 'placed', 950, timestamp '2026-02-01 11:00')
) t(id, status, cents, updated_at)
\"\"\")
write("models/sources.yml", \"\"\"
version: 2
sources:
  - name: raw
    schema: main
    tables: [{{name: raw_orders}}]
\"\"\")


def show():
    for row in sql("select id, status, cents, updated_at from orders order by id"):
        print(row[:3], row[3].strftime("%m-%d %H:%M"))
%% md
## The first build and every build after it

An incremental model is a normal `SELECT` plus a filter that applies only on later runs. `is_incremental()` is false
on the first build (or with `--full-refresh`), so dbt builds the whole table; on later runs it is true and the model
can compare the source with `{{{{ this }}}}`, the table it is about to update.

The filter below is a **high-water mark**: select only rows changed after the latest `updated_at` already loaded.

**Where it matters**

Large facts (events, orders, page views) are usually incremental. The first build is a full load; each later run
reads only the new slice, which keeps runtime and warehouse cost flat as the table grows.

**Watch out for**

Without a `unique_key`, dbt only **appends** the new rows. A changed row arrives as a second copy of the same `id`, so
the table silently gains duplicates.
%% code
write("models/orders.sql", \"\"\"
{{{{ config(materialized='incremental') }}}}
select id, status, cents, updated_at
from {{{{ source('raw', 'raw_orders') }}}}
{{% if is_incremental() %}}
where updated_at > (select max(updated_at) from {{{{ this }}}})
{{% endif %}}
\"\"\")
dbt("run")
sql("update raw_orders set status = 'paid', updated_at = timestamp '2026-02-01 12:00' where id = 2")
sql("insert into raw_orders values (4, 'placed', 400, timestamp '2026-02-01 12:30')")
dbt("run")
show()
%% md
**What to notice:** The second run selected only the two rows changed after 11:00, the high-water mark. Order 4 was
added correctly, but order 2 now appears twice, `placed` and `paid`, because an append cannot replace a row.
%% md
## Merge changed rows by key

Setting `unique_key='id'` tells dbt that incoming rows replace existing rows with the same key. With the `merge`
strategy dbt issues a `MERGE` (update matched rows, insert new ones); `delete+insert` deletes matching keys and inserts
the batch, which some warehouses run faster.

**Where it matters**

Any source whose rows change after they are first loaded, such as orders moving through statuses or customer
profiles, needs a unique key, or the fact table drifts from the source.

**Watch out for**

The key must really be unique **within each batch** too: if the source sends two versions of `id` 2 in one run, the
merge either fails or keeps an arbitrary one. Deduplicate inside the model first, keeping the latest `updated_at`.
%% code
write("models/orders.sql", \"\"\"
{{{{ config(materialized='incremental', unique_key='id', incremental_strategy='merge') }}}}
select id, status, cents, updated_at
from {{{{ source('raw', 'raw_orders') }}}}
{{% if is_incremental() %}}
where updated_at > (select max(updated_at) from {{{{ this }}}})
{{% endif %}}
qualify row_number() over (partition by id order by updated_at desc) = 1
\"\"\")
dbt("run", "--full-refresh")
sql("update raw_orders set status = 'shipped', updated_at = timestamp '2026-02-01 13:00' where id = 2")
dbt("run")
show()
%% md
**What to notice:** After a full refresh rebuilt the table cleanly, the next run's update for order 2 replaced its row
instead of adding one: order 2 appears once, as `shipped`, and the other orders are untouched.
%% md
## Late-arriving rows and a lookback window

A high-water mark assumes rows arrive in `updated_at` order. They often do not: a mobile app syncs hours late, or a
source replica lags. A row whose `updated_at` is **older** than the current maximum is skipped forever. The usual fix
is a **lookback window**: reprocess a margin before the high-water mark on every run, and let the merge make the
overlap harmless.

**Where it matters**

Event and CDC sources nearly always deliver some rows late. Measure how late (the gap between event time and load
time) and size the lookback to cover nearly all of it.

**Watch out for**

A lookback costs a little re-reading on every run, and nothing older than the window is caught. Schedule an
occasional wider backfill or full refresh to sweep up very late rows.
%% code
sql("insert into raw_orders values (5, 'placed', 700, timestamp '2026-02-01 12:45')")  # arrives late
sql("insert into raw_orders values (6, 'placed', 300, timestamp '2026-02-01 14:00')")
dbt("run")
print("high-water mark only:", [row[0] for row in sql("select id from orders order by id")])

model = (project / "models/orders.sql").read_text()
write("models/orders.sql", model.replace(
    "where updated_at > (select max(updated_at) from {{{{ this }}}})",
    "where updated_at > (select max(updated_at) - interval 3 hour from {{{{ this }}}})",
))
sql("insert into raw_orders values (7, 'placed', 250, timestamp '2026-02-01 13:30')")  # also late
dbt("run")
print("with a 3-hour lookback:", [row[0] for row in sql("select id from orders order by id")])
%% md
**What to notice:** Order 5 arrived after order 6 had pushed the high-water mark to 14:00, so the plain filter never
selected it. With the 3-hour lookback, the next run caught both late order 7 and order 5, and the merge kept order 6
as one row even though it was read again.
%% md
## New columns and full refreshes

When the source gains a column, an incremental model must decide whether the existing table changes. The
`on_schema_change` setting decides: `ignore` (the default) never changes the table, `append_new_columns` adds it (old rows get `NULL`), `sync_all_columns` also removes dropped ones, and `fail` stops the
run. `dbt run --full-refresh` rebuilds the table from scratch, which also back-fills the new column for old rows.

**Where it matters**

Source schemas change without notice. Choose the setting per model: `append_new_columns` for wide event tables,
`fail` for marts with contracts.

**Watch out for**

What `ignore` does next depends on the strategy: with `append` the new column is dropped and runs stay green, which is
silent data loss; with `merge`, as below, the run fails. And a full refresh of a very large table can take hours, so
plan it rather than reaching for it during an incident.
%% code
sql("alter table raw_orders add column channel varchar default 'web'")
sql("insert into raw_orders values (8, 'placed', 500, timestamp '2026-02-01 15:00', 'app')")
model = (project / "models/orders.sql").read_text().replace("select id, status, cents, updated_at", "select id, status, cents, updated_at, channel")
write("models/orders.sql", model)
dbt("run", expect_success=False)
print("columns after ignore:", [c[0] for c in sql("select column_name from information_schema.columns where table_name = 'orders'")])

write("models/orders.sql", model.replace("incremental_strategy='merge'", "incremental_strategy='merge', on_schema_change='append_new_columns'"))
dbt("run")
print("append_new_columns:", sql("select id, channel from orders where id in (1, 8) order by id"))
%% md
**What to notice:** With the default `ignore`, dbt left the table without a `channel` column, so the merge of rows that
have one failed with a binder error. With `append_new_columns`, dbt added the column first: order 8, inside the
lookback window, has `app`, while order 1, loaded before the column existed and outside the window, has `NULL` until
a full refresh.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Back-fill the new column

**Difficulty:** Easy · about 5 min

Rebuild `orders` so that every row has its `channel`, and show the channels.
%% code
# Try your solution here.
%% solution
dbt("run", "--full-refresh")
print(sql("select id, channel from orders order by id"))
%% md
### Exercise 2: Size the lookback

**Difficulty:** Medium · about 15 min

Insert order 9 with `updated_at` 4 hours before the current maximum. Does the 3-hour lookback catch it? Change the
window so it does, and verify.
%% code
# Try your solution here.
%% solution
newest = sql("select max(updated_at) from orders")[0][0]
sql(f"insert into raw_orders values (9, 'placed', 100, timestamp '{{newest}}' - interval 4 hour, 'web')")
dbt("run")
print("caught with 3 hours:", sql("select count(*) from orders where id = 9")[0][0] == 1)
write("models/orders.sql", (project / "models/orders.sql").read_text().replace("interval 3 hour", "interval 6 hour"))
dbt("run")
print("caught with 6 hours:", sql("select count(*) from orders where id = 9")[0][0] == 1)
%% md
### Exercise 3: delete+insert

**Difficulty:** Medium · about 10 min

Switch the model to `incremental_strategy='delete+insert'`, update order 1 to `refunded`, and check that it still
appears once.
%% code
# Try your solution here.
%% solution
write("models/orders.sql", (project / "models/orders.sql").read_text().replace("incremental_strategy='merge'", "incremental_strategy='delete+insert'"))
sql("update raw_orders set status = 'refunded', updated_at = (select max(updated_at) from raw_orders) + interval 1 minute where id = 1")
dbt("run")
print(sql("select id, status, count(*) over (partition by id) as copies from orders where id = 1"))
%% md
## Key takeaways

- `is_incremental()` separates the first full build from later runs, which filter the source against
  `{{{{ this }}}}`, usually on a high-water mark.
- Without a `unique_key` an incremental model only appends, so changed rows become duplicates; with one, a merge or
  delete+insert replaces them. Deduplicate each batch first.
- A plain high-water mark skips rows that arrive late. Reprocess a lookback window on every run and let the merge
  absorb the overlap.
- Set `on_schema_change` deliberately; the default ignores new columns silently. A full refresh rebuilds everything
  and back-fills.
%% md
**Next:** [dbt 4: Snapshots and history](dbt-04-snapshots.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
