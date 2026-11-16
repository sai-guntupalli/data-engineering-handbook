import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from dbt_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/dbt/dbt-02-tests-and-contracts.ipynb"
SPEC = f"""%% md
# dbt 2: Tests, unit tests and contracts

dbt can check three different things: that the **data** meets expectations (data tests), that a model's **logic**
gives the right answer for known inputs (unit tests), and that a model's **shape** matches what consumers rely on
(contracts). This lesson runs each against a small project with deliberately bad data, and shows how `dbt build`
stops bad data from reaching the models downstream.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell creates an empty dbt project with the `write`, `dbt` and `sql` helpers from dbt 1, then loads raw
orders and customers with three problems planted in them: order 2 appears twice, order 3 has an unknown status, and
order 3 belongs to customer 99, who does not exist.

{HELPERS}


sql(\"\"\"
create table raw_orders as select * from (values
    (1, 10, 'paid', 1200), (2, 11, 'paid', 800), (2, 11, 'paid', 800), (3, 99, 'lost', 500)
) t(id, customer_id, status, cents)
\"\"\")
sql("create table raw_customers as select * from (values (10, 'Ana'), (11, 'Ben')) t(id, name)")
write("models/sources.yml", \"\"\"
version: 2
sources:
  - name: raw
    schema: main
    tables: [{{name: raw_orders}}, {{name: raw_customers}}]
\"\"\")
write("models/stg_orders.sql", "select * from {{{{ source('raw', 'raw_orders') }}}}")
write("models/stg_customers.sql", "select * from {{{{ source('raw', 'raw_customers') }}}}")
write("models/fct_revenue.sql", "select status, sum(cents) as cents from {{{{ ref('stg_orders') }}}} group by status")
dbt("run")
%% md
## Data tests

A **data test** is a query that returns the rows breaking a rule; it passes when it returns none. The four built-in
**generic tests** are declared on columns in YAML: `unique`, `not_null`, `accepted_values` and `relationships`
(every value exists in another model's column). Arguments for a test go under `arguments:`.

`dbt test` runs them and reports the number of failing rows for each.

**Where it matters**

`unique` and `not_null` on every model's primary key catch most join fan-outs and broken loads before anyone sees
a wrong number. They are the minimum for any model others depend on.

**Watch out for**

A test only checks what you declare. A passing suite on a model with no tests proves nothing, so test the keys and
the columns that drive business logic, not only the easy ones.
%% code
write("models/schema.yml", \"\"\"
version: 2
models:
  - name: stg_orders
    columns:
      - name: id
        data_tests: [unique, not_null]
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['paid', 'refunded']
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('stg_customers')
                field: id
\"\"\")
dbt("test", expect_success=False)
%% md
**What to notice:** Three of the four tests found exactly the planted problems: one duplicated `id`, one status
outside the accepted list, and one `customer_id` with no matching customer. `not_null` passed. Each failure reports a
row count, not the rows themselves.
%% md
## Severity and stored failures

Not every broken rule should stop a pipeline. Setting a test's `severity: warn` reports it without failing the run,
and `warn_if` or `error_if` (such as `">10"`) set thresholds. With `--store-failures`, dbt writes each failing test's
rows to a table in an `..._dbt_test__audit` schema, so you can see **which** rows broke the rule.

**Where it matters**

Use `error` for rules whose violation makes the output wrong (duplicate keys) and `warn` for data-quality signals you
monitor but tolerate (late reference data). Stored failures turn a red test into a ticket someone can act on.

**Watch out for**

Warnings that nobody reads become noise. Route warnings somewhere visible, and promote a warning to an error once
the upstream team has fixed the source.
%% code
schema = (project / "models/schema.yml").read_text()
write("models/schema.yml", schema.replace(
    "                field: id\\n",
    "                field: id\\n              config:\\n                severity: warn\\n",
))
dbt("test", "--store-failures", expect_success=False)
print(sql('select * from main_dbt_test__audit."unique_stg_orders_id"'))
%% md
**What to notice:** The orphan customer is now a `warn`, while the duplicate and the unknown status still `fail`. The
stored-failure table for `unique` names the culprit: `id` 2, which appears twice.
%% md
## dbt build keeps bad data from spreading

`dbt build` interleaves runs and tests in DAG order: it builds a model, runs that model's tests, and only then moves
on to its children. When a test fails with `error` severity, every model downstream of the failing model is
**skipped**, so the bad data stays where it was found.

**Where it matters**

This is the main reason to schedule `dbt build` rather than `dbt run` followed by `dbt test`: with separate commands,
every mart is rebuilt from bad staging data before the tests notice.

**Watch out for**

Skipped models keep their previous contents, which are stale but consistent. Alert on skips as well as failures, or
a dashboard can quietly show yesterday's numbers for days.
%% code
dbt("build", expect_success=False)
%% md
**What to notice:** The two staging models were built, their tests ran, and because `stg_orders` failed `unique` and
`accepted_values`, `fct_revenue` was skipped rather than rebuilt from duplicated orders.
%% md
## Singular tests

When a rule does not fit a generic test, write a **singular test**: a `.sql` file in `tests/` that selects the rows
breaking the rule. It can join several models and use any SQL.

**Where it matters**

Reconciliation checks are singular tests: "revenue in the mart equals the sum of paid orders in staging", or
"every shipped order has a payment".

**Watch out for**

A singular test that selects nothing because of a typo in a filter passes forever. Check new tests by making them
fail once on purpose.
%% code
write("tests/revenue_reconciles.sql", \"\"\"
select r.cents as mart_cents, s.cents as staging_cents
from (select sum(cents) as cents from {{{{ ref('fct_revenue') }}}}) r
cross join (select sum(cents) as cents from {{{{ ref('stg_orders') }}}}) s
where r.cents != s.cents
\"\"\")
dbt("run", "--select", "fct_revenue")
dbt("test", "--select", "revenue_reconciles")
%% md
**What to notice:** The reconciliation passes: the mart's total equals the staging total, duplicates included. A
singular test checks only the rule it encodes, which is why it complements `unique` rather than replacing it.
%% md
## Unit tests

Data tests check today's data; a **unit test** checks the model's logic against fixed inputs. You declare rows for
each `ref` or `source` the model reads (`given`) and the rows the model must return (`expect`). dbt runs the model's
SQL on those rows only, without touching the real tables, and compares.

**Where it matters**

Use unit tests for logic with edge cases: CASE statements, date arithmetic, window functions, and the
deduplication rule below. They run in CI before any data exists.

**Watch out for**

Unit tests run the compiled SQL against the warehouse, so the warehouse must be reachable in CI, and every input the
model reads must be given (or `ref`ed with an empty fixture).
%% code
write("models/stg_orders_deduped.sql", \"\"\"
select * from {{{{ ref('stg_orders') }}}}
qualify row_number() over (partition by id order by cents desc) = 1
\"\"\")
write("models/unit_tests.yml", \"\"\"
version: 2
unit_tests:
  - name: keeps_one_row_per_order
    model: stg_orders_deduped
    given:
      - input: ref('stg_orders')
        rows:
          - {{id: 7, customer_id: 1, status: paid, cents: 100}}
          - {{id: 7, customer_id: 1, status: paid, cents: 100}}
          - {{id: 8, customer_id: 2, status: paid, cents: 50}}
    expect:
      rows:
        - {{id: 7, customer_id: 1, status: paid, cents: 100}}
        - {{id: 8, customer_id: 2, status: paid, cents: 50}}
\"\"\")
dbt("build", "--select", "stg_orders_deduped")
%% md
**What to notice:** dbt ran the unit test first, on the three fixture rows, and only built `stg_orders_deduped` after
it passed. The real `raw_orders` table played no part.
%% md
## Model contracts

A **contract** fixes a model's columns and types. With `contract: {{enforced: true}}`, dbt checks the model's
`SELECT` against the declared columns before building and refuses to build on a mismatch; declared `constraints`
(such as `not_null`) are added to the table where the warehouse supports them.

**Where it matters**

Put contracts on models other teams or tools query directly. A renamed column or a changed type then fails your
build, instead of breaking their dashboards after deployment.

**Watch out for**

A contract checks shape, not values: a column of wrong numbers with the right type passes. Use contracts together
with data tests, not instead of them.
%% code
write("models/fct_orders.sql", "select id, cast(cents as varchar) as cents from {{{{ ref('stg_orders_deduped') }}}}")
write("models/contracts.yml", \"\"\"
version: 2
models:
  - name: fct_orders
    config:
      materialized: table
      contract: {{enforced: true}}
    columns:
      - name: id
        data_type: integer
        constraints: [{{type: not_null}}]
      - name: cents
        data_type: integer
\"\"\")
dbt("run", "--select", "fct_orders", expect_success=False)
%% md
**What to notice:** dbt refused to build `fct_orders` because the model returns `cents` as `VARCHAR` while the contract
declares `INTEGER`. The error lists the mismatched column, and no table was created.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Make the build pass

**Difficulty:** Easy · about 10 min

Fix the contract violation in `fct_orders`, then build it and confirm it is a table with integer `cents`.
%% code
# Try your solution here.
%% solution
write("models/fct_orders.sql", "select id, cents from {{{{ ref('stg_orders_deduped') }}}}")
dbt("run", "--select", "fct_orders")
print(sql("select column_name, data_type from information_schema.columns where table_name = 'fct_orders'"))
%% md
### Exercise 2: A threshold instead of zero tolerance

**Difficulty:** Medium · about 10 min

Change the `accepted_values` test on `status` so that it warns for one bad row but would fail above five, and run it.
%% code
# Try your solution here.
%% solution
schema = (project / "models/schema.yml").read_text()
write("models/schema.yml", schema.replace(
    "                values: ['paid', 'refunded']\\n",
    "                values: ['paid', 'refunded']\\n              config:\\n                warn_if: '>0'\\n                error_if: '>5'\\n",
))
dbt("test", "--select", "stg_orders,test_name:accepted_values")
%% md
### Exercise 3: Unit-test a CASE expression

**Difficulty:** Medium · about 15 min

Write a model `order_size` that labels orders under 1,000 cents `small` and the rest `large`, and a unit test that
covers 999 and 1,000 cents.
%% code
# Try your solution here.
%% solution
write("models/order_size.sql", \"\"\"
select id, case when cents < 1000 then 'small' else 'large' end as size from {{{{ ref('stg_orders_deduped') }}}}
\"\"\")
write("models/order_size_tests.yml", \"\"\"
version: 2
unit_tests:
  - name: labels_the_boundary
    model: order_size
    given:
      - input: ref('stg_orders_deduped')
        rows: [{{id: 1, cents: 999}}, {{id: 2, cents: 1000}}]
    expect:
      rows: [{{id: 1, size: small}}, {{id: 2, size: large}}]
\"\"\")
dbt("build", "--select", "order_size")
%% md
## Key takeaways

- Data tests return the rows that break a rule. Put `unique` and `not_null` on every key, and `accepted_values` and
  `relationships` where values drive logic or joins.
- Use `severity`, `warn_if` and `error_if` to separate what must stop the pipeline from what you monitor, and
  `--store-failures` to see the offending rows.
- `dbt build` tests each model before building its children, so a failure skips everything downstream instead of
  spreading bad data.
- Unit tests check a model's logic on fixed inputs; contracts check its columns and types before it is built.
%% md
**Next:** [dbt 3: Incremental models](dbt-03-incremental-models.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
