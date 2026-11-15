import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from dbt_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/dbt/dbt-04-snapshots.ipynb"
SPEC = f"""%% md
# dbt 4: Snapshots and history

Source tables usually hold only the current state: when a customer upgrades, the old tier is overwritten. A dbt
**snapshot** records each version of a row with the period it was valid, which is a Type 2 slowly changing dimension
built for you. This lesson snapshots a customer table with both change-detection strategies, records deletes, and
joins facts to the version that was true when they happened.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell creates an empty dbt project with the `write`, `dbt` and `sql` helpers from dbt 1, declares a source
`customers` table with an `updated_at` column, and loads two customers on the basic tier.

{HELPERS}


sql(\"\"\"
create table customers as select * from (values
    (1, 'basic', timestamp '2026-01-01 00:00'),
    (2, 'basic', timestamp '2026-01-05 00:00')
) t(id, tier, updated_at)
\"\"\")
write("models/sources.yml", \"\"\"
version: 2
sources:
  - name: crm
    schema: main
    tables: [{{name: customers}}]
\"\"\")


def history(table="customer_history"):
    rows = sql(f"select id, tier, dbt_valid_from, dbt_valid_to from {{table}} order by id, dbt_valid_from")
    for id_, tier, valid_from, valid_to in rows:
        print(id_, f"{{tier:<6}}", valid_from.date(), "->", valid_to.date() if valid_to else "current")
%% md
## The timestamp strategy

A snapshot is declared in YAML under `snapshots/`: which relation to watch, its `unique_key`, and how to detect a
change. With `strategy: timestamp`, a row has changed when its `updated_at` is newer than the version already
recorded. Each `dbt snapshot` run compares the source with the snapshot table, closes the old version of every changed
row by setting `dbt_valid_to`, and inserts the new version with `dbt_valid_to` empty.

**Where it matters**

Snapshots give you history that the source system does not keep: customer tiers, product prices, account owners.
Facts can then be reported with the attributes that applied at the time.

**Watch out for**

A snapshot sees only what the source looks like **when it runs**. If a customer changes tier twice between two
runs, the middle version is never recorded. Run snapshots at least as often as the changes you need to capture, or
take history from CDC instead.
%% code
write("snapshots/customer_history.yml", \"\"\"
snapshots:
  - name: customer_history
    relation: source('crm', 'customers')
    config:
      unique_key: id
      strategy: timestamp
      updated_at: updated_at
\"\"\")
dbt("snapshot")
sql("update customers set tier = 'plus', updated_at = timestamp '2026-02-01 00:00' where id = 1")
dbt("snapshot")
history()
%% md
**What to notice:** The first run recorded both customers as current. After customer 1 moved to `plus` on February 1,
the second run closed the `basic` version with `dbt_valid_to` 2026-02-01 and opened a `plus` version from that same
instant. Customer 2 did not change, so it still has a single row.
%% md
## The check strategy

Some sources have no trustworthy `updated_at`. `strategy: check` compares the columns listed in `check_cols`
instead, and records a new version when any of them differs. Without a timestamp from the source, the version
boundaries are the times the snapshot ran.

**Where it matters**

Use `check` for sources exported as full files or tables whose timestamp is missing or updated by unrelated
processes. List only the columns whose history matters.

**Watch out for**

`check_cols: all` records a new version whenever any column changes, including technical ones such as a sync
timestamp, which can multiply the table's size. The validity dates are run times, so they say when you noticed the
change, not when it happened.
%% code
write("snapshots/tier_history.yml", \"\"\"
snapshots:
  - name: tier_history
    relation: source('crm', 'customers')
    config:
      unique_key: id
      strategy: check
      check_cols: [tier]
\"\"\")
dbt("snapshot", "--select", "tier_history")
sql("update customers set tier = 'gold' where id = 2")  # no updated_at change
dbt("snapshot")
print(sql("select id, tier, dbt_valid_to is null as is_current from tier_history order by id, dbt_valid_from"))
print("timestamp strategy saw the change:", sql("select count(*) from customer_history where id = 2")[0][0] > 1)
%% md
**What to notice:** Customer 2's tier changed to `gold` without its `updated_at` changing. The check snapshot recorded
a new version; the timestamp snapshot did not, because by its rule nothing had changed.
%% md
## Recording deletes

By default a row that disappears from the source stays "current" in the snapshot forever. `hard_deletes: invalidate`
closes its open version when the row is missing, and `hard_deletes: new_record` also inserts a row marked deleted,
which makes the delete itself visible as an event.

**Where it matters**

Customers close accounts and products are discontinued. Without delete handling, a dimension keeps counting them as
active, and every report that filters on "current" rows is wrong.

**Watch out for**

`invalidate` treats any row missing from the source query as deleted. If the source is a partial extract (only
yesterday's changes), every untouched row would be closed. Snapshot only complete tables.
%% code
write("snapshots/customer_history.yml", \"\"\"
snapshots:
  - name: customer_history
    relation: source('crm', 'customers')
    config:
      unique_key: id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: invalidate
\"\"\")
sql("delete from customers where id = 2")
dbt("snapshot", "--select", "customer_history")
print(sql("select id, tier, dbt_valid_to is null as is_current from customer_history order by id, dbt_valid_from"))
%% md
**What to notice:** Customer 2's only version is no longer current: its `dbt_valid_to` was set when the snapshot found
the row missing. Customer 1's history is unchanged.
%% md
## Joining facts to the version that applied

The point of history is to answer "what was true then?". Join each fact to the snapshot row whose validity period
contains the fact's time, treating an empty `dbt_valid_to` as "still valid". Periods are half-open: a version is
valid from `dbt_valid_from` inclusive to `dbt_valid_to` exclusive, so a fact exactly on a boundary matches one
version only.

**Where it matters**

Revenue by customer tier, commissions by account owner and sales by product category all need the attribute value
at the time of the sale, not today's value.

**Watch out for**

Use `>=` on the start and `<` on the end. Using `between` matches both versions at a boundary instant and doubles the
fact.
%% code
write("models/orders_with_tier.sql", \"\"\"
with orders as (
    select * from (values
        (101, 1, timestamp '2026-01-20 00:00', 1200),
        (102, 1, timestamp '2026-02-01 00:00', 800),
        (103, 1, timestamp '2026-02-10 00:00', 950)
    ) t(order_id, customer_id, ordered_at, cents)
)
select o.order_id, o.ordered_at, h.tier, o.cents
from orders as o
join {{{{ ref('customer_history') }}}} as h
  on h.id = o.customer_id
 and o.ordered_at >= h.dbt_valid_from
 and (h.dbt_valid_to is null or o.ordered_at < h.dbt_valid_to)
\"\"\")
dbt("run", "--select", "orders_with_tier")
for order_id, ordered_at, tier, cents in sql("select * from orders_with_tier order by order_id"):
    print(order_id, ordered_at.date(), tier, cents)
%% md
**What to notice:** Order 101 is reported at `basic`, and orders 102 and 103 at `plus`. Order 102 falls exactly on the
February 1 boundary and matches only the new version, because the old one ends there exclusively. Each order joined
exactly one row.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Current rows only

**Difficulty:** Easy · about 5 min

Write a query on `customer_history` that returns each customer's current tier only.
%% code
# Try your solution here.
%% solution
print(sql("select id, tier from customer_history where dbt_valid_to is null order by id"))
%% md
### Exercise 2: The boundary bug

**Difficulty:** Medium · about 10 min

Rewrite the point-in-time join with `between dbt_valid_from and coalesce(dbt_valid_to, timestamp '9999-12-31')` as a
plain SQL query, and count how many rows order 102 gets.
%% code
# Try your solution here.
%% solution
rows = sql(\"\"\"
select h.tier from customer_history h
where h.id = 1 and timestamp '2026-02-01 00:00' between h.dbt_valid_from and coalesce(h.dbt_valid_to, timestamp '9999-12-31')
\"\"\")
print(len(rows), "rows for order 102:", rows)
%% md
### Exercise 3: A missed version

**Difficulty:** Medium · about 10 min

Change customer 1 to `gold` and then to `platinum` (with later `updated_at` values each time) before running the
snapshot once. Which versions does the snapshot record?
%% code
# Try your solution here.
%% solution
sql("update customers set tier = 'gold', updated_at = timestamp '2026-03-01 00:00' where id = 1")
sql("update customers set tier = 'platinum', updated_at = timestamp '2026-03-02 00:00' where id = 1")
dbt("snapshot", "--select", "customer_history")
print([row[1] for row in sql("select id, tier from customer_history where id = 1 order by dbt_valid_from")])
%% md
## Key takeaways

- A snapshot turns a current-state table into Type 2 history with `dbt_valid_from` and `dbt_valid_to`; an empty
  `dbt_valid_to` marks the current version.
- Use `strategy: timestamp` when the source has a reliable `updated_at`, and `strategy: check` on chosen columns when
  it does not.
- Snapshots see only the state at run time, so changes between runs are lost; set `hard_deletes` so removed rows stop
  being current.
- Join facts to history on `>= dbt_valid_from` and `< dbt_valid_to` so each fact matches exactly one version.
%% md
**Next:** [dbt 5: Microbatch incremental models](dbt-05-microbatch.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
