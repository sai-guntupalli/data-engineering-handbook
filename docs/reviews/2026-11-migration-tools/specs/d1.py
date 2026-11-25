import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from dbt_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/dbt/dbt-01-models-and-ref.ipynb"
SPEC = f"""%% md
# dbt 1: Models, sources and ref

dbt turns `SELECT` statements into tables and views, in dependency order, inside your warehouse. This lesson builds
a three-model project from raw tables: declaring sources, writing staging and mart models, reading the dependency
graph that `ref` creates, choosing materializations, and selecting part of the graph to run.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell creates an empty dbt project and a DuckDB warehouse, and defines three helpers: `write` puts a file in
the project, `dbt` runs a command and prints a line per node, and `sql` queries the warehouse directly. Then it loads
two raw tables, as an ingestion tool would leave them: column names from the source system, amounts as text.

{HELPERS}


sql(\"\"\"
create table raw_orders as select * from (values
    (1, 10, 'PAID', '12.00', date '2026-02-01'),
    (2, 11, 'paid', '8.00', date '2026-02-01'),
    (3, 10, 'refunded', '5.50', date '2026-02-02')
) t(order_id, cust_id, order_status, amount, order_date)
\"\"\")
sql("create table raw_customers as select * from (values (10, 'Ana', 'PT'), (11, 'Ben', 'UK')) t(id, full_name, country)")
print(sql("select * from raw_orders"))
%% md
## Sources and staging models

A **model** is a `.sql` file in `models/` that contains one `SELECT`. dbt wraps it in the DDL that creates a view or
table named after the file. A **source** declares a table that dbt did not build, such as a raw ingestion table, in a
YAML file; models read it with `{{{{ source('raw', 'orders') }}}}` rather than a hard-coded name.

By convention each source table gets one **staging** model that renames columns, casts types and fixes obvious
inconsistencies, and nothing else. Every later model reads the staging model, never the raw table.

**Where it matters**

Declaring sources lets dbt draw lineage from raw data to dashboards and test source freshness. Staging models put
the clean-up for each source in exactly one place.

**Watch out for**

Keep business logic out of staging: no joins, filters or aggregations. A staging model that drops "bad" rows hides
data problems from every model downstream.
%% code
write("models/sources.yml", \"\"\"
version: 2
sources:
  - name: raw
    schema: main
    tables:
      - name: orders
        identifier: raw_orders
      - name: customers
        identifier: raw_customers
\"\"\")
write("models/stg_orders.sql", \"\"\"
select
    order_id,
    cust_id as customer_id,
    lower(order_status) as status,
    cast(amount as decimal(10, 2)) as amount,
    order_date
from {{{{ source('raw', 'orders') }}}}
\"\"\")
write("models/stg_customers.sql", \"\"\"
select id as customer_id, full_name as name, country
from {{{{ source('raw', 'customers') }}}}
\"\"\")
dbt("run")
print(sql("select * from stg_orders order by order_id"))
%% md
**What to notice:** dbt built both staging models as views (the default materialization). `stg_orders` now has
consistent names, lower-case statuses (`PAID` became `paid`) and decimal amounts, while the raw table is untouched.
%% md
## ref builds the dependency graph

A model that reads another model uses `{{{{ ref('stg_orders') }}}}`. At compile time dbt replaces it with the full
relation name, and it records the edge, so it always builds `stg_orders` before the model that refs it. The edges
form a **DAG** (directed acyclic graph) that dbt uses for ordering, selection, documentation and lineage.

`dbt ls --select +fct_orders` lists a model and everything upstream of it, and the compiled SQL in `target/compiled`
shows exactly what dbt sent to the warehouse.

**Where it matters**

Because dependencies come from `ref` rather than from a hand-written order, adding a model never requires editing
a schedule, and impact analysis ("what breaks if I change this?") is one command.

**Watch out for**

A hard-coded table name such as `from main.stg_orders` works once but is invisible to dbt: no ordering, no lineage, and
it points at the wrong schema in another environment. Always `ref` models and `source` raw tables.
%% code
write("models/fct_orders.sql", \"\"\"
select
    o.order_id,
    o.order_date,
    c.name as customer,
    c.country,
    o.status,
    o.amount
from {{{{ ref('stg_orders') }}}} as o
join {{{{ ref('stg_customers') }}}} as c using (customer_id)
\"\"\")
dbt("run", "--select", "fct_orders")
print("upstream of fct_orders:")
dbt("ls", "--select", "+fct_orders")
compiled = (project / "target/compiled/handbook/models/fct_orders.sql").read_text()
print([line.strip() for line in compiled.splitlines() if "stg_" in line])
%% md
**What to notice:** `dbt ls` shows the mart, its two staging models and the two sources behind them. In the compiled
SQL each `ref` became a fully qualified name such as `"warehouse"."main"."stg_orders"`, which is why the same model
code can run against development and production schemas.
%% md
## Materializations

A model's **materialization** decides what dbt creates:

```text
view          a stored query: always fresh, recomputed on every read       default; good for staging
table         the result is written out on every run                       marts that many people query
incremental   only new or changed rows are added after the first build      large facts (dbt 3)
ephemeral     inlined as a CTE into the models that ref it; nothing created small reusable logic
```

Set it in the model with `{{{{ config(materialized='table') }}}}`, or for a whole folder in `dbt_project.yml`.

**Where it matters**

Views keep storage at zero but push the cost to every query; tables cost a rebuild per run but make dashboards fast.
Most projects use views for staging and tables or incremental models for marts.

**Watch out for**

A view over a view over a view re-runs the whole chain on every read. If dashboards on a mart are slow, check how many
views it stacks before tuning anything else.
%% code
write("models/fct_orders.sql", "{{{{ config(materialized='table') }}}}\\n" + (project / "models/fct_orders.sql").read_text())
dbt("run")
print(sql(\"\"\"
select table_name, table_type from information_schema.tables
where table_name in ('stg_orders', 'stg_customers', 'fct_orders') order by table_name
\"\"\"))
%% md
**What to notice:** After adding the config line, `fct_orders` is a `BASE TABLE` while the staging models remain views.
dbt dropped the old view and created the table in its place; nothing else changed.
%% md
## Selecting part of the graph

`--select` (`-s`) chooses which nodes a command runs. `model_name` selects one model, `+model_name` adds its
ancestors, `model_name+` adds its descendants, and `tag:`, `path:` and `state:modified` select by metadata or by what
changed. `dbt build` runs models, tests, snapshots and seeds together in DAG order, so testing a model happens right
after it is built.

**Where it matters**

In development you rebuild only what you touched and its children (`dbt build -s stg_orders+`). In CI, `state:modified+`
builds just the changed models and everything downstream of them.

**Watch out for**

Selecting a model without its parents uses whatever versions of the parents already exist in the warehouse. If they
are stale, the result is too, so use `+` when upstream logic has changed.
%% code
sql("insert into raw_orders values (4, 11, 'Paid', '20.00', date '2026-02-03')")
dbt("build", "--select", "stg_orders+")
print(sql("select order_id, customer, status, amount from fct_orders order by order_id"))
%% md
**What to notice:** Selecting `stg_orders+` rebuilt `stg_orders` and `fct_orders` but not `stg_customers`. The new raw
order appears in the mart with its status normalized and its amount cast, because it flowed through staging.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Add a mart

**Difficulty:** Easy · about 10 min

Write a `revenue_by_country` model that sums `amount` of paid orders per country from `fct_orders`, build it, and
query it.
%% code
# Try your solution here.
%% solution
write("models/revenue_by_country.sql", \"\"\"
select country, sum(amount) as revenue
from {{{{ ref('fct_orders') }}}}
where status = 'paid'
group by country
\"\"\")
dbt("run", "--select", "revenue_by_country")
print(sql("select * from revenue_by_country order by country"))
%% md
### Exercise 2: Impact analysis

**Difficulty:** Easy · about 5 min

List every node that would need rebuilding if `stg_customers` changed.
%% code
# Try your solution here.
%% solution
dbt("ls", "--select", "stg_customers+")
%% md
### Exercise 3: An ephemeral model

**Difficulty:** Medium · about 15 min

Move the paid-order filter into an ephemeral model `paid_orders`, make `revenue_by_country` read it, and confirm that
no `paid_orders` relation exists in the warehouse.
%% code
# Try your solution here.
%% solution
write("models/paid_orders.sql", \"\"\"
{{{{ config(materialized='ephemeral') }}}}
select * from {{{{ ref('fct_orders') }}}} where status = 'paid'
\"\"\")
write("models/revenue_by_country.sql", \"\"\"
select country, sum(amount) as revenue from {{{{ ref('paid_orders') }}}} group by country
\"\"\")
dbt("run", "--select", "+revenue_by_country")
print(sql("select * from revenue_by_country order by country"))
print("paid_orders relations:", sql("select count(*) from information_schema.tables where table_name = 'paid_orders'"))
%% md
## Key takeaways

- A model is one `SELECT` in a file; dbt creates the view or table and names it after the file.
- Declare raw tables as sources and read them through one staging model each; keep business logic in later models.
- `ref` and `source` give dbt the dependency graph it uses to order, select, document and trace models. Never
  hard-code a relation name.
- Choose materializations deliberately: views for staging, tables or incremental models for marts that are queried
  often.
- `--select` with `+` runs part of the graph, and `dbt build` tests each model right after building it.
%% md
**Next:** [dbt 2: Tests and contracts](dbt-02-tests-and-contracts.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
