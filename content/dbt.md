## [Main title](../README.md)
### [Interview questions](full.md)

# dbt

+ [What is dbt?](#What-is-dbt)
+ [How is dbt different from Airflow?](#How-is-dbt-different-from-Airflow)
+ [What is a dbt model?](#What-is-a-dbt-model)
+ [What does ref do and why is it important?](#What-does-ref-do-and-why-is-it-important)
+ [How do you structure a dbt project?](#How-do-you-structure-a-dbt-project)
+ [What are the typical dbt layers (staging, intermediate, marts)?](#What-are-the-typical-dbt-layers-staging-intermediate-marts)
+ [What is a materialization in dbt?](#What-is-a-materialization-in-dbt)
+ [When would you use view vs table materializations?](#When-would-you-use-view-vs-table-materializations)
+ [What is an incremental model and what problems does it solve?](#What-is-an-incremental-model-and-what-problems-does-it-solve)
+ [How do you design a reliable unique_key for incremental models?](#How-do-you-design-a-reliable-unique_key-for-incremental-models)
+ [How do you handle backfills and late-arriving data in dbt?](#How-do-you-handle-backfills-and-late-arriving-data-in-dbt)
+ [What are dbt tests and what types exist?](#What-are-dbt-tests-and-what-types-exist)
+ [What dbt tests should you add to critical models?](#What-dbt-tests-should-you-add-to-critical-models)
+ [What are sources in dbt and how do you test them?](#What-are-sources-in-dbt-and-how-do-you-test-them)
+ [What are snapshots in dbt and when would you use them?](#What-are-snapshots-in-dbt-and-when-would-you-use-them)
+ [What are macros in dbt and when should you use them?](#What-are-macros-in-dbt-and-when-should-you-use-them)
+ [How do you document and expose dbt models?](#How-do-you-document-and-expose-dbt-models)
+ [How do you orchestrate dbt with Airflow?](#How-do-you-orchestrate-dbt-with-Airflow)
+ [What is dbt state selection (slim CI) and why is it useful?](#What-is-dbt-state-selection-slim-CI-and-why-is-it-useful)
+ [How do you approach CI/CD for dbt projects?](#How-do-you-approach-CICD-for-dbt-projects)
+ [How do you tune dbt performance?](#How-do-you-tune-dbt-performance)
+ [What are common dbt anti-patterns?](#What-are-common-dbt-anti-patterns)
+ [Real world use cases for dbt](#Real-world-use-cases-for-dbt)

## What is dbt?

dbt (data build tool) is a transformation framework: you write transformations as SQL (with Jinja), and dbt builds a DAG of models, runs them in dependency order, tests them, and documents them. It pushes compute into the warehouse (Snowflake, BigQuery, Redshift, Databricks, Postgres, Trino) instead of moving data into a separate processing cluster.

```text
raw sources -> staging (clean) -> intermediate (join/logic) -> marts (facts, dims, metrics)
                    |                     |                        |
                 tests/docs          ref() lineage          exposures to BI
```

dbt is not an orchestrator and not a scheduler. Airflow (or dbt Cloud jobs, Dagster, Prefect) decides *when* dbt runs; dbt decides *what* SQL runs and in what order.

[Table of Contents](#dbt)

## How is dbt different from Airflow?

Airflow schedules and coordinates work across systems (extract, dbt, Spark, ML, alerts). dbt owns the SQL transformation graph, its tests, and its documentation. In practice Airflow triggers dbt as one or a few steps inside a larger pipeline: `ingest -> dbt build -> validate -> publish`.

```text
Airflow DAG: extract_orders >> dbt_build(tag:daily) >> publish_marts >> notify
dbt inside:  stg_orders -> int_orders_enriched -> fct_orders -> dim_customer
```

The interview point: dbt has its own DAG, but it cannot wait for a partner file, retry only a failed non-SQL step, or coordinate a Spark job - that is Airflow's job.

[Table of Contents](#dbt)

## What is a dbt model?

A model is a `select` statement in a `.sql` file under `models/`. dbt wraps it in the DDL/DML needed to materialize a relation, and resolves dependencies from `ref()` calls.

```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('postgres', 'orders') }}
),

renamed as (
    select
        id                              as order_id,
        customer_id,
        cast(created_at as timestamp)   as created_at,
        (amount_cents / 100.0)::numeric(18, 2) as amount,
        lower(status)                   as status
    from source
    where _deleted is not true
)

select * from renamed
```

Everything in a model should be deterministic and set-based. If you find yourself writing procedural loops, the logic usually belongs in SQL windows or in an upstream job.

[Table of Contents](#dbt)

## What does ref do and why is it important?

`ref('model_name')` is the only supported way to refer to another model. It lets dbt build the execution DAG, resolve the right database/schema per environment (dev vs prod), and render lineage in `dbt docs`. Directly hard-coding `analytics.fct_orders` breaks all three.

```sql
-- models/marts/fct_orders.sql
select
    o.order_id,
    o.customer_id,
    o.amount,
    c.segment
from {{ ref('stg_orders') }} as o
left join {{ ref('dim_customer') }} as c
    on o.customer_id = c.customer_id
```

`source('system', 'table')` is the same idea for raw tables you do not build: it gives you freshness checks, lineage from ingestion tools, and a single place to change a schema name.

[Table of Contents](#dbt)

## How do you structure a dbt project?

Separate raw access, cleaning, reusable business logic, and consumer-facing marts. Keep each layer small enough to test and name consistently.

```text
dbt/
  dbt_project.yml
  packages.yml
  models/
    staging/
      _sources.yml
      stg_orders.sql
      stg_customers.sql
    intermediate/
      int_orders_enriched.sql
    marts/
      finance/fct_orders.sql
      core/dim_customer.sql
      core/_models.yml
  snapshots/dim_customer_snapshot.sql
  tests/assert_revenue_non_negative.sql
  macros/cents_to_dollars.sql
```

```yaml
# dbt_project.yml - materialization defaults per folder
name: acme_analytics
version: "1.0.0"
profile: acme
model-paths: ["models"]

models:
  acme_analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +tags: ["marts"]
```

Naming rules that scale: `stg_` for staging, `int_` for intermediate, `fct_`/`dim_` for marts. One model, one grain, stated in the model description.

[Table of Contents](#dbt)

## What are the typical dbt layers (staging, intermediate, marts)?

+ **Staging** - rename, cast, deduplicate, and filter raw sources. One staging model per source table, no joins.
+ **Intermediate** - reusable joins and business logic that more than one mart needs. Often ephemeral (CTE-only, no relation).
+ **Marts** - facts, dimensions, and metrics-ready tables that BI and data scientists query. These get the strongest tests and documentation.

This separation stops each dashboard model from re-implementing the same casts and joins, and it makes impact analysis possible when a source changes.

[Table of Contents](#dbt)

## What is a materialization in dbt?

A materialization is the strategy dbt uses to build a model in the warehouse:

| Materialization | What dbt creates | Use when |
|---|---|---|
| `view` | a database view | cheap transformations, fast iteration, freshness on read |
| `table` | a full rebuild each run | moderate size, expensive joins, stable data |
| `incremental` | insert/merge/append of new rows | large facts, event tables, late-arriving data |
| `ephemeral` | a CTE inlined into downstream models | shared logic without a relation |
| `materialized_view` | warehouse-native MV (where supported) | pre-aggregated, auto-refreshing results |

```sql
{{ config(materialized='table', tags=['finance']) }}

select * from {{ ref('int_orders_enriched') }}
```

[Table of Contents](#dbt)

## When would you use view vs table materializations?

Views cost storage nothing and always reflect the latest data, but every downstream query pays the compute. Tables cost storage and build time but make repeated BI queries cheap and predictable.

Rules of thumb:

+ Staging and light intermediate models: `view` or `ephemeral`.
+ Marts queried by many dashboards: `table`.
+ Very large fact tables: `incremental`.
+ Pre-aggregated metrics queried constantly: `table` refreshed on schedule, or a warehouse materialized view.

The failure mode to avoid is a chain of views on views on views, where a single dashboard query re-scans the raw layer.

[Table of Contents](#dbt)

## What is an incremental model and what problems does it solve?

An incremental model processes only new or changed rows instead of rebuilding the whole table. On a billion-row fact table that turns a two-hour rebuild into a two-minute merge.

```sql
-- models/marts/fct_orders.sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    partition_by={'field': 'order_date', 'data_type': 'date'},
    cluster_by=['customer_id']
  )
}}

select
    order_id,
    customer_id,
    order_date,
    amount,
    status,
    updated_at
from {{ ref('int_orders_enriched') }}

{% if is_incremental() %}
    -- only rows changed since the last successful load
    where updated_at > (select coalesce(max(updated_at), timestamp '1900-01-01') from {{ this }})
{% endif %}
```

The `{% if is_incremental() %}` block only applies on incremental runs, so the same model works for the first full build and later merges.

[Table of Contents](#dbt)

## How do you design a reliable unique_key for incremental models?

The `unique_key` must be unique in the target table and stable across source changes - usually a business key (`order_id`) or a deterministic surrogate key built from stable columns (`dbt_utils.generate_surrogate_key`).

Additional rules:

+ Keep a monotonic `updated_at` (or CDC sequence) so you can filter "changed since last run".
+ Use `incremental_strategy='merge'` for updates; `append` only for immutable events; `delete+insert` for warehouses without merge.
+ Add a small lookback window (for example `updated_at > max(updated_at) - interval '3 days'`) to absorb late-arriving rows and clock skew.
+ Handle deletes explicitly: CDC with a `_deleted` flag or the `hard_deletes` snapshot config (dbt 1.9+), otherwise deleted rows live forever.
+ Make the key unique in the source too; if not, deduplicate in the staging model with a window function.

```sql
-- deduplicate the source before merging
select *
from (
    select
        *,
        row_number() over (partition by order_id order by updated_at desc) as rn
    from {{ source('postgres', 'orders') }}
) where rn = 1
```

[Table of Contents](#dbt)

## How do you handle backfills and late-arriving data in dbt?

Parameterize the window and let orchestration pass it. Never hand-edit SQL to backfill.

```sql
-- use a var with a sensible default so production and backfills share one model
{% set start_date = var('start_date', '1900-01-01') %}
{% set end_date = var('end_date', '2999-12-31') %}

select *
from {{ ref('int_orders_enriched') }}
where order_date between date '{{ start_date }}' and date '{{ end_date }}'
```

```bash
# reprocess one month
dbt build --select fct_orders --vars '{"start_date": "2026-09-01", "end_date": "2026-09-30"}'
```

For late-arriving data, combine a lookback window with idempotent merges so reprocessing a day is safe. If the model cannot be made idempotent, rebuild it fully for the affected partitions instead of appending.

[Table of Contents](#dbt)

## What are dbt tests and what types exist?

+ **Generic tests** - reusable, declared in YAML: `unique`, `not_null`, `accepted_values`, `relationships`, plus packages such as `dbt_utils` and `dbt_expectations`.
+ **Singular tests** - a SQL file under `tests/` that returns offending rows; the test passes when it returns zero rows.
+ **Unit tests** - dbt 1.8+ fixtures that verify transformation logic on fixed inputs without touching the warehouse.

```sql
-- tests/assert_revenue_non_negative.sql
select *
from {{ ref('fct_orders') }}
where amount < 0
```

```sql
-- tests/generic/test_not_future.sql : a custom generic test
{% test not_future(model, column_name) %}
select *
from {{ model }}
where {{ column_name }} > current_timestamp
{% endtest %}
```

Tests run as SQL in the warehouse, so they cost compute: put the expensive ones on critical marts, not on every staging view.

[Table of Contents](#dbt)

## What dbt tests should you add to critical models?

Protect the model's contract, not random columns: uniqueness and nullability of keys, accepted values, referential integrity to dimensions, non-negative amounts, and one current row per key in SCD2 tables.

```yaml
# models/marts/core/_models.yml
models:
  - name: fct_orders
    description: One row per order, at the order grain.
    config:
      contract:
        enforced: true
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customer')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ["placed", "shipped", "delivered", "cancelled"]
      - name: amount
        tests:
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

Also check **freshness** on sources and **volume** (row counts vs trailing average) so a silently empty load fails the run instead of the dashboard.

[Table of Contents](#dbt)

## What are sources in dbt and how do you test them?

Sources declare raw tables so dbt can track freshness and lineage from ingestion to BI.

```yaml
# models/staging/_sources.yml
sources:
  - name: postgres
    database: raw
    schema: public
    loaded_at_field: _ingested_at
    freshness:
      warn_after: {count: 6, period: hour}
      error_after: {count: 24, period: hour}
    tables:
      - name: orders
        columns:
          - name: id
            tests: [unique, not_null]
      - name: customers
```

```bash
dbt source freshness          # fails when a source is stale past error_after
```

Freshness is the cheapest early warning you can buy: it catches broken ingestion before transformations run on stale or partial data.

[Table of Contents](#dbt)

## What are snapshots in dbt and when would you use them?

Snapshots capture the history of a mutable table so you can answer "what did this row look like on date X". They implement SCD2 with `dbt_valid_from` / `dbt_valid_to`.

```sql
-- snapshots/dim_customer_snapshot.sql
{% snapshot dim_customer_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='timestamp',
    updated_at='updated_at'
  )
}}
select * from {{ source('postgres', 'customers') }}
{% endsnapshot %}
```

Use `strategy='check'` when there is no reliable `updated_at` (dbt compares a list of columns). Snapshots are append-only history - they grow forever, so plan retention and never "fix" history by editing them.

[Table of Contents](#dbt)

## What are macros in dbt and when should you use them?

Macros are Jinja functions that generate SQL. Use them for repeated column logic, standard filters, and cross-database compatibility - not for hiding business rules that reviewers must approve.

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, scale=2) %}
    ({{ column_name }} / 100.0)::numeric(16, {{ scale }})
{% endmacro %}
```

```sql
select
    order_id,
    {{ cents_to_dollars('amount_cents') }} as amount
from {{ ref('stg_orders') }}
```

Macros can be tested indirectly through the models that use them, and `dbt run-operation` lets you call one directly for operational tasks.

[Table of Contents](#dbt)

## How do you document and expose dbt models?

Documentation lives with the model and is rendered by `dbt docs generate`. Exposures declare downstream consumers (dashboards, ML models) so impact analysis reaches BI.

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    url: https://bi.acme.com/dashboards/revenue
    owner:
      name: Finance Analytics
      email: finance-data@acme.com
    depends_on:
      - ref('fct_orders')
      - ref('dim_customer')
```

Add `description` and `meta` fields to models, and enforce `contract: enforced: true` on marts that other teams consume so a column rename fails fast instead of breaking a dashboard silently.

[Table of Contents](#dbt)

## How do you orchestrate dbt with Airflow?

Run dbt as a step inside a larger DAG. Airflow handles waiting for data, retries, and non-SQL work; dbt handles the SQL graph.

Airflow 3:

```python
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG, task

with DAG(dag_id="daily_revenue", schedule="0 3 * * *", start_date=...) as dag:

    wait_for_orders = S3KeySensor(
        task_id="wait_for_orders",
        bucket_name="acme-raw",
        bucket_key="orders/ds={{ ds }}/_SUCCESS",
        mode="reschedule",
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/dbt/acme && dbt build --select tag:daily --target prod",
    )

    @task
    def publish() -> None:
        notify_bi_refresh()

    wait_for_orders >> dbt_build >> publish()
```

Airflow 2 uses `from airflow.operators.bash import BashOperator` and `from airflow.decorators import task`. Alternatives worth naming: dbt Cloud jobs triggered by `DbtCloudRunJobOperator`, or Cosmos, which renders each dbt model as an Airflow task so retries and logs are per model.

[Table of Contents](#dbt)

## What is dbt state selection (slim CI) and why is it useful?

State selection compares the current project against a previous manifest and selects only changed models plus their downstream dependents. In CI this avoids rebuilding the whole warehouse while still validating the affected part of the DAG.

```bash
# CI: run only what changed, deferring unmodified refs to the production manifest
dbt build \
  --select state:modified+ \
  --defer \
  --state ./prod-manifest \
  --target ci
```

`--defer` makes unmodified `ref()`s resolve to production, so the CI schema only contains the models under test. Generate the manifest in production on every deploy (`dbt build --select ...` then copy `target/manifest.json`) and store it as an artifact.

[Table of Contents](#dbt)

## How do you approach CI/CD for dbt projects?

A practical pipeline:

+ **CI on every PR** - `dbt deps`, `dbt build --select state:modified+ --defer --state ./prod-manifest --target ci`, then run the full test suite on the changed selection.
+ **CD on merge** - deploy the project, then run `dbt build` for the changed selection in production (or the full graph nightly).
+ **Guardrails** - code review for marts, enforced contracts, source freshness alerts, and a rollback plan (revert the PR, then rebuild affected models).
+ **Observability** - store `run_results.json` and `manifest.json` artifacts, alert on failures and on tests that start failing repeatedly.

```yaml
# .github/workflows/dbt.yml (sketch)
steps:
  - run: dbt deps
  - run: dbt build --select state:modified+ --defer --state prod-manifest --target ci
  - run: dbt test --select state:modified+
```

[Table of Contents](#dbt)

## How do you tune dbt performance?

+ **Reduce data scanned** - partition and cluster large facts, filter early in staging, avoid `select *` across layers.
+ **Choose the right materialization** - the biggest lever; a table instead of a view chain can cut warehouse cost dramatically.
+ **Increase threads** - `dbt run --threads 8` (bounded by warehouse concurrency and cost).
+ **Make incrementals correct and narrow** - a tight `updated_at` filter plus a small lookback beats a full rebuild.
+ **Precompute heavy joins** - materialize the intermediate model once instead of joining raw tables in every mart.
+ **Watch full-refresh cost** - `dbt build --full-refresh` on a huge incremental is an incident if it is not planned.

```bash
dbt run --select fct_orders --threads 8
dbt build --select tag:finance --exclude tag:experimental
dbt run --full-refresh --select fct_orders     # deliberate, not routine
```

[Table of Contents](#dbt)

## What are common dbt anti-patterns?

+ One giant model with hundreds of CTEs that nobody can test or review.
+ Views on views on views, so every dashboard query re-scans raw data.
+ Hard-coded schema/table names instead of `ref()` and `source()`.
+ Incremental models without a `unique_key`, causing duplicate rows on retry.
+ Tests on trivial columns while key relationships and freshness go unchecked.
+ Business logic in macros that reviewers cannot see in the model SQL.
+ `dbt run` in production without tests (`dbt build` runs both).
+ Snapshots used as a substitute for CDC and then never pruned.
+ No manifest artifact, so CI cannot use state selection.
+ Treating dbt as a scheduler; complex non-SQL orchestration does not belong in a dbt project.

[Table of Contents](#dbt)

## Real world use cases for dbt

### 1. E-commerce revenue marts on Snowflake

Raw orders, payments, and refunds land from CDC. Staging models clean them; intermediate models join and allocate refunds; marts produce `fct_orders`, `fct_payments`, and `dim_customer` used by finance dashboards.

```sql
-- fct_orders: one row per order, incremental merge, partitioned by date
{{ config(materialized='incremental', unique_key='order_id', incremental_strategy='merge',
          partition_by={'field': 'order_date', 'data_type': 'date'}) }}

select o.order_id, o.customer_id, o.order_date, o.amount - coalesce(r.refunded, 0) as net_amount
from {{ ref('stg_orders') }} o
left join {{ ref('int_refunds_by_order') }} r using (order_id)
{% if is_incremental() %}
where o.updated_at > (select coalesce(max(updated_at), '1900-01-01') from {{ this }})
{% endif %}
```

Why dbt: one tested, documented definition of revenue, rebuilt incrementally instead of re-derived in every dashboard.

### 2. Fintech regulatory reporting with SCD2 history

A licensed lender must reproduce "the customer segment as of the reporting date". A snapshot keeps SCD2 history for `customers`, and marts join each transaction to the row valid on its booking date.

```sql
select
    t.transaction_id,
    t.amount,
    s.customer_segment,
    s.dbt_valid_from,
    s.dbt_valid_to
from {{ ref('fct_transactions') }} t
join {{ ref('dim_customer_snapshot') }} s
  on t.customer_id = s.customer_id
 and t.booked_at >= s.dbt_valid_from
 and t.booked_at <  coalesce(s.dbt_valid_to, timestamp '9999-12-31')
```

Why dbt: snapshots make point-in-time correctness a modelling concern rather than an audit scramble.

### 3. Multi-tenant SaaS metrics

Each tenant's usage events are transformed into tenant-scoped marts, with tests asserting that tenant ids never leak across accounts.

```sql
select tenant_id, date_trunc('day', event_at) as ds, count(*) as events
from {{ ref('stg_usage_events') }}
group by 1, 2
```

```yaml
models:
  - name: fct_usage_daily
    columns:
      - name: tenant_id
        tests:
          - not_null
          - relationships: {to: ref('dim_tenant'), field: tenant_id}
```

Why dbt: consistent tenant-level metric definitions and contract tests, which is exactly what a multi-tenant data product needs.

### 4. Migrating stored procedures to governed SQL

A team replaces a 4,000-line stored procedure with staging, intermediate, and mart models. Each step gets tests, and the final numbers are reconciled against the legacy procedure before cutover.

```bash
dbt build --select +fct_billing_statement     # build the model and all its ancestors
dbt test --select fct_billing_statement
```

Why dbt: the migration becomes reviewable and testable, and the lineage makes the replacement plan obvious.

### 5. Feature tables for machine learning

Data scientists need the same feature definitions in training and serving. dbt builds `fct_customer_features` with a documented grain and freshness test; the training pipeline reads the table, and Airflow triggers retraining when the model is rebuilt.

Why dbt: training/serving skew drops when both sides read one versioned, tested definition instead of two copies of SQL.

[Table of Contents](#dbt)
