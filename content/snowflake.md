## [Main title](../README.md)
### [Interview questions](full.md)

# Snowflake

**Notebook:** [`notebooks/topics/snowflake.ipynb`](../notebooks/topics/snowflake.ipynb) - runnable version of this topic with self-checking exercises.

Snowflake is a fully managed, multi-cluster, shared-data cloud data platform: storage, compute, and services scale independently.

+ [What is Snowflake?](#What-is-Snowflake)
+ [How does Snowflake separate storage and compute?](#How-does-Snowflake-separate-storage-and-compute)
+ [What are virtual warehouses and how do they work?](#What-are-virtual-warehouses-and-how-do-they-work)
+ [What is the cloud services layer?](#What-is-the-cloud-services-layer)
+ [What are micro-partitions and how does pruning work?](#What-are-micro-partitions-and-how-does-pruning-work)
+ [What is a clustering key and when should you use one?](#What-is-a-clustering-key-and-when-should-you-use-one)
+ [How do you read a query profile and tune a slow query?](#How-do-you-read-a-query-profile-and-tune-a-slow-query)
+ [How do you use EXPLAIN and the query profile for pruning?](#How-do-you-use-EXPLAIN-and-the-query-profile-for-pruning)
+ [How do you size a virtual warehouse?](#How-do-you-size-a-virtual-warehouse)
+ [What are multi-cluster warehouses and when do you use them?](#What-are-multi-cluster-warehouses-and-when-do-you-use-them)
+ [How do auto-suspend and auto-resume affect cost?](#How-do-auto-suspend-and-auto-resume-affect-cost)
+ [What caching layers does Snowflake have?](#What-caching-layers-does-Snowflake-have)
+ [What is Time Travel and Fail-safe?](#What-is-Time-Travel-and-Fail-safe)
+ [What is zero-copy cloning?](#What-is-zero-copy-cloning)
+ [What are streams and how do they capture CDC?](#What-are-streams-and-how-do-they-capture-CDC)
+ [What are tasks and how do you build incremental pipelines?](#What-are-tasks-and-how-do-you-build-incremental-pipelines)
+ [What are dynamic tables?](#What-are-dynamic-tables)
+ [What is Snowpipe and when do you use it?](#What-is-Snowpipe-and-when-do-you-use-it)
+ [What are stages and how do you load with COPY INTO?](#What-are-stages-and-how-do-you-load-with-COPY-INTO)
+ [How do you handle semi-structured data with VARIANT?](#How-do-you-handle-semi-structured-data-with-VARIANT)
+ [How do external tables work?](#How-do-external-tables-work)
+ [How do Snowflake Iceberg tables work?](#How-do-Snowflake-Iceberg-tables-work)
+ [What is Snowpark and how do you use Python in Snowflake?](#What-is-Snowpark-and-how-do-you-use-Python-in-Snowflake)
+ [What are UDFs and stored procedures?](#What-are-UDFs-and-stored-procedures)
+ [What is the RBAC role and privilege model?](#What-is-the-RBAC-role-and-privilege-model)
+ [What are secure views, row access policies, and column masking?](#What-are-secure-views-row-access-policies-and-column-masking)
+ [How do resource monitors control cost?](#How-do-resource-monitors-control-cost)
+ [How do transactions and isolation work in Snowflake?](#How-do-transactions-and-isolation-work-in-Snowflake)
+ [What is Snowflake data sharing?](#What-is-Snowflake-data-sharing)
+ [What is the search optimization service?](#What-is-the-search-optimization-service)
+ [What are materialized views?](#What-are-materialized-views)
+ [What is the query acceleration service?](#What-is-the-query-acceleration-service)
+ [How do you migrate from Redshift, Hadoop, or another warehouse?](#How-do-you-migrate-from-Redshift-Hadoop-or-another-warehouse)
+ [What are common Snowflake anti-patterns?](#What-are-common-Snowflake-anti-patterns)
+ [Real world use cases for Snowflake](#Real-world-use-cases-for-Snowflake)

## What is Snowflake?

Snowflake is a fully managed cloud data platform where storage, compute, and services are separated, so you pick warehouse sizes instead of nodes and never shard data or collect statistics by hand.

```text
clients (Snowsight, JDBC/ODBC, Python, dbt, Spark)
   -> cloud services (metadata, optimizer, transactions, security, governance)
   -> virtual warehouses (isolated compute) over storage (micro-partitions in S3/Blob/GCS)
```

An account runs several warehouses - small BI, large ELT, data science - all reading the same tables without copies or CPU contention.

[Table of Contents](#Snowflake)

## How does Snowflake separate storage and compute?

Data is stored once in object storage as Snowflake-managed micro-partitions, while compute is elastic and every virtual warehouse is an independent cluster with its own local cache sharing neither memory nor CPU.

```sql
CREATE WAREHOUSE bi_wh  WAREHOUSE_SIZE = 'SMALL' AUTO_SUSPEND = 300 AUTO_RESUME = TRUE;
CREATE WAREHOUSE elt_wh WAREHOUSE_SIZE = 'LARGE' AUTO_SUSPEND = 60  AUTO_RESUME = TRUE;
```

Workload isolation becomes configuration, idle compute is cheap with auto-suspend, and a bigger warehouse can never rescue a badly pruned scan.

[Table of Contents](#Snowflake)

## What are virtual warehouses and how do they work?

A virtual warehouse is a named cluster that executes queries and DML; size runs XS to 6XL and each step doubles the credit rate, parallelizing scans, joins, and sorts without reducing the bytes that must be read.

```sql
CREATE OR REPLACE WAREHOUSE transform_wh
  WAREHOUSE_SIZE = 'MEDIUM' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;

ALTER WAREHOUSE transform_wh SET WAREHOUSE_SIZE = 'LARGE';  -- heavy backfill
```

Credits are billed per second with a 60-second minimum per start, and an idle running warehouse still burns credits, so separate loading, transformation, BI, and ad-hoc compute.

[Table of Contents](#Snowflake)

## What is the cloud services layer?

Cloud services is the control plane Snowflake operates: authentication and access control, query parsing and optimization, metadata (definitions, micro-partition statistics, versions), transaction coordination, and warehouse provisioning.

```sql
SELECT query_id, total_elapsed_time / 1000 AS seconds,
       partitions_scanned, partitions_total, bytes_spilled_to_remote_storage
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('hour', -24, CURRENT_TIMESTAMP())
ORDER BY total_elapsed_time DESC LIMIT 20;
```

Most cloud services usage is included at no extra charge, except serverless features - automatic clustering, materialized view maintenance, Snowpipe, search optimization, query acceleration - whose credits you should monitor.

[Table of Contents](#Snowflake)

## What are micro-partitions and how does pruning work?

Every table is automatically partitioned into immutable, compressed, columnar micro-partitions of roughly 50-500 MB uncompressed, each with per-column min/max, distinct, and null statistics so the planner can skip partitions a filter cannot match.

```sql
INSERT INTO analytics.orders SELECT order_id, order_date, customer_id, amount
FROM staging.orders_raw ORDER BY order_date, customer_id;

SELECT ROUND(partitions_scanned / NULLIF(partitions_total, 0) * 100, 1) AS pct_scanned,
       partitions_scanned, partitions_total
FROM snowflake.account_usage.query_history
WHERE query_text ILIKE '%analytics.orders%' ORDER BY start_time DESC LIMIT 5;
```

Rows land in insertion order, so an unordered load puts every date in every partition and no filter helps - the most common performance root cause in Snowflake.

[Table of Contents](#Snowflake)

## What is a clustering key and when should you use one?

A clustering key co-locates rows by one or more expressions so pruning improves on very large tables, and it is only worth adding when a multi-terabyte table is repeatedly filtered on the same columns and pruning is measurably poor.

```sql
ALTER TABLE analytics.events CLUSTER BY (event_date, customer_id);

-- Clustering depth: lower is better, average_depth near 1 is excellent
SELECT SYSTEM$CLUSTERING_INFORMATION('analytics.events', '(event_date, customer_id)');

ALTER TABLE analytics.events SUSPEND RECLUSTERING;
```

Prefer `(date, high_cardinality_id)`, keep to a few expressions, and measure query improvement against reclustering spend because maintenance runs on serverless compute after DML.

[Table of Contents](#Snowflake)

## How do you read a query profile and tune a slow query?

Find the expensive statement in Query History, then open its profile in Snowsight: a tree of operators carrying partitions scanned versus total, bytes scanned, rows produced, time per operator, and bytes spilled to local or remote storage.

```sql
SELECT query_id, total_elapsed_time / 1000 AS elapsed_s,
       queued_overload_time / 1000 AS queued_s,
       partitions_scanned, partitions_total,
       bytes_spilled_to_remote_storage / POWER(1024, 3) AS gb_spill_remote,
       percentage_scanned_from_cache
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('day', -1, CURRENT_TIMESTAMP())
ORDER BY total_elapsed_time DESC LIMIT 25;
```

A high scanned/total ratio is a pruning problem rather than a size problem, remote spilling means the warehouse is too small or the query shape is wrong, and queue time points at concurrency rather than SQL.

[Table of Contents](#Snowflake)

## How do you use EXPLAIN and the query profile for pruning?

`EXPLAIN` shows the plan before execution and is cheap, while the profile shows what actually happened, so use `EXPLAIN USING JSON` to confirm estimated partitions, filter pushdown, and join order against the real profile.

```sql
EXPLAIN USING TEXT
SELECT customer_id, SUM(amount) FROM analytics.orders
WHERE order_date BETWEEN '2026-09-01' AND '2026-09-30' GROUP BY customer_id;

EXPLAIN USING JSON
SELECT COUNT(*) FROM analytics.events WHERE event_date = '2026-10-04';
```

Filters should be pushed near the scan and estimated partitions a small fraction of the total; a full scan of a huge table is fixed by a filter, a clustering key, or a pre-aggregated table, never by warehouse size.

[Table of Contents](#Snowflake)

## How do you size a virtual warehouse?

Sizing trades latency, concurrency, and credits: doubling the size doubles credits per hour and helps scan-heavy and spill-heavy queries, but never fixes a badly pruned scan, a lock wait, or a single-row lookup.

```text
XS   =  1 credit/hour    -- dashboards, small transforms, dev
S    =  2 credits/hour   -- light BI, moderate dbt models
M    =  4 credits/hour   -- standard ELT, mixed concurrency
L    =  8 credits/hour   -- large joins, big backfills
XL   = 16 credits/hour   -- heavy transformations
2XL+ = 32+ credits/hour  -- rare; usually a signal to fix the query
```

Scale up to shorten a critical path and scale out for concurrency, remembering that the 60-second minimum makes many short-lived warehouses costlier than one warm warehouse.

[Table of Contents](#Snowflake)

## What are multi-cluster warehouses and when do you use them?

A multi-cluster warehouse adds and removes clusters automatically to absorb concurrency, which is the scale-out answer when many users run the same query shape and queue for compute.

```sql
ALTER WAREHOUSE bi_wh SET
  MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 6 SCALING_POLICY = 'STANDARD';
ALTER WAREHOUSE reporting_wh SET
  MIN_CLUSTER_COUNT = 2 MAX_CLUSTER_COUNT = 10 SCALING_POLICY = 'ECONOMY';

SELECT warehouse_name, COUNT(*) AS queued FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('hour', -6, CURRENT_TIMESTAMP()) AND queued_overload_time > 0
GROUP BY warehouse_name ORDER BY queued DESC;
```

`STANDARD` adds clusters quickly for interactive BI while `ECONOMY` adds slowly and removes after about six idle minutes for batch, `MIN_CLUSTER_COUNT > 1` keeps clusters warm at extra cost, and Enterprise Edition is required.

[Table of Contents](#Snowflake)

## How do auto-suspend and auto-resume affect cost?

Auto-suspend shuts a warehouse down after inactivity and auto-resume starts it on the next query, which is the simplest cost control available; the tradeoff is cache warmth, because a suspended warehouse loses its local SSD cache.

```sql
ALTER WAREHOUSE bi_wh  SET AUTO_SUSPEND = 600 AUTO_RESUME = TRUE;  -- interactive bursts
ALTER WAREHOUSE elt_wh SET AUTO_SUSPEND = 60  AUTO_RESUME = TRUE;  -- batch
ALTER WAREHOUSE reporting_wh SET AUTO_SUSPEND = 0;                 -- costs idle credits
```

Use 60 seconds for batch and 300-600 for interactive workloads, keep auto-resume on unless you want a scheduled job to fail silently, and check `WAREHOUSE_EVENTS_HISTORY` before tuning.

[Table of Contents](#Snowflake)

## What caching layers does Snowflake have?

Snowflake caches at three levels, and naming them precisely is the point of the question.

+ **Result cache** - results keyed by query text and current table versions, valid 24 hours and free; any DML on the table invalidates it.
+ **Local disk (SSD) cache** - table data cached on warehouse nodes, lost when the warehouse suspends.
+ **Remote (metadata) cache** - micro-partition metadata persisted in cloud services and shared across warehouses, making first scans cheaper.

```sql
SELECT query_id, percentage_scanned_from_cache, partitions_scanned, partitions_total
FROM snowflake.account_usage.query_history
WHERE start_time >= DATEADD('hour', -3, CURRENT_TIMESTAMP()) LIMIT 20;

SELECT CURRENT_TIMESTAMP(), COUNT(*) FROM analytics.orders;  -- non-deterministic: never cached
SELECT COUNT(*) FROM analytics.orders;                       -- cacheable
```

The result cache makes repeated dashboard refreshes nearly free, while a constantly mutating table gets no benefit at all.

[Table of Contents](#Snowflake)

## What is Time Travel and Fail-safe?

Time Travel queries or restores data as it existed earlier using historical table versions, and Fail-safe is the non-configurable 7 days after Time Travel during which only Snowflake support can recover data; Standard Edition allows 0-1 day and Enterprise up to 90.

```sql
ALTER TABLE analytics.orders SET DATA_RETENTION_TIME_IN_DAYS = 30;

SELECT COUNT(*) FROM analytics.orders AT (TIMESTAMP => '2026-10-01 00:00:00'::TIMESTAMP);
SELECT COUNT(*) FROM analytics.orders BEFORE (STATEMENT => '<query_id>');
UNDROP TABLE analytics.orders;
CREATE TABLE analytics.orders_audit CLONE analytics.orders AT (OFFSET => -86400);
```

Time Travel is a safety net, not a backup: it is retention-bound, retained versions cost storage, and Fail-safe is not queryable, so real DR needs replication and exports.

[Table of Contents](#Snowflake)

## What is zero-copy cloning?

A clone creates a table, schema, or database sharing micro-partitions with the source, copying metadata only, so it is fast and nearly free and you pay storage only for partitions that diverge afterwards.

```sql
CREATE DATABASE analytics_dev CLONE analytics;

CREATE TABLE analytics.orders_snapshot CLONE analytics.orders
  AT (TIMESTAMP => '2026-10-01 00:00:00'::TIMESTAMP);

-- The clone becomes independent as soon as these partitions are modified
UPDATE analytics_dev.marts.daily_revenue SET revenue = 0 WHERE order_date < '2026-01-01';
```

Clone production, run migrations and tests against the clone, then swap; note that clones inherit privileges through the object hierarchy rather than from the source grants.

[Table of Contents](#Snowflake)

## What are streams and how do they capture CDC?

A stream is a change-tracking object over a table, view, or external table that exposes inserts, updates, and deletes relative to the last read; consuming it in a DML statement advances the offset (querying it alone does not), which makes it Snowflake's native CDC primitive.

```sql
CREATE OR REPLACE STREAM raw.orders.orders_stream ON TABLE raw.orders.orders;

MERGE INTO analytics.orders AS t
USING (SELECT order_id, status, METADATA$ACTION AS action FROM raw.orders.orders_stream
       QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY METADATA$ROW_ID DESC) = 1) AS s
ON t.order_id = s.order_id
WHEN MATCHED AND s.action = 'DELETE' THEN DELETE
WHEN MATCHED THEN UPDATE SET status = s.status
WHEN NOT MATCHED AND s.action = 'INSERT' THEN INSERT (order_id, status) VALUES (s.order_id, s.status);
```

A stream becomes stale when its offset falls outside the source object's data-retention window; Snowflake temporarily extends retention for an unconsumed stream up to 14 days by default (`MAX_DATA_EXTENSION_TIME_IN_DAYS`). A stream gives you the delta rather than idempotency, so write the consumer as a merge that is safe to retry.

[Table of Contents](#Snowflake)

## What are tasks and how do you build incremental pipelines?

A task runs SQL, a stored procedure, or a Snowflake Scripting block on a schedule or after another task; tasks form a DAG, and gating a task on `SYSTEM$STREAM_HAS_DATA` is the canonical incremental pattern.

```sql
CREATE OR REPLACE TASK raw.orders.load_task
  WAREHOUSE = elt_wh SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders.orders_stream')
AS CALL analytics.load_orders_incremental();

CREATE OR REPLACE TASK analytics.transform_task
  WAREHOUSE = transform_wh AFTER raw.orders.load_task
AS CALL analytics.build_orders_marts();

ALTER TASK analytics.transform_task RESUME;  -- children first, then the root
```

Omit `WAREHOUSE` and the task is serverless, which removes idle cost at the price of less control; keep tasks small, ordered, and safe to retry after a partial failure.

[Table of Contents](#Snowflake)

## What are dynamic tables?

A dynamic table is a declarative, continuously refreshed table defined by a query: you set a target freshness with `TARGET_LAG` and Snowflake decides when and how to refresh, incrementalizing automatically where it can.

```sql
CREATE OR REPLACE DYNAMIC TABLE analytics.daily_revenue
  TARGET_LAG = '10 minutes' WAREHOUSE = transform_wh
AS
  SELECT o.order_date, c.segment, SUM(o.amount) AS revenue, COUNT(*) AS orders
  FROM analytics.orders o JOIN analytics.customers c USING (customer_id)
  GROUP BY o.order_date, c.segment;

SELECT name, target_lag_sec, scheduling_state, latest_data_timestamp
FROM TABLE(information_schema.dynamic_tables());
```

Dynamic tables honor lag rather than exact schedules and chain refreshes downstream, so they fit pipelines expressible as SQL but not procedural logic or precisely timed loads.

[Table of Contents](#Snowflake)

## What is Snowpipe and when do you use it?

Snowpipe is Snowflake-managed continuous ingestion from files in a stage: a pipe wraps a `COPY INTO`, and new files trigger it through cloud event notifications or the REST API without a scheduled warehouse, billed serverless per file handled.

```sql
CREATE OR REPLACE PIPE raw.orders.orders_pipe AUTO_INGEST = TRUE
AS COPY INTO raw.orders.orders FROM @raw.orders.orders_landing
   FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

SELECT SYSTEM$PIPE_STATUS('raw.orders.orders_pipe');

SELECT file_name, row_count, error_count, status
FROM TABLE(information_schema.copy_history(table_name => 'raw.orders.orders',
     start_time => DATEADD('hour', -24, CURRENT_TIMESTAMP())));
```

Use Snowpipe for file-based landing and Snowpipe Streaming for row-level, low-latency writes from an application or the Kafka connector; both are at-least-once, so dedupe on a business key or file name.

[Table of Contents](#Snowflake)

## What are stages and how do you load with COPY INTO?

A stage is a named location Snowflake loads from or unloads to: internal stages are Snowflake-managed while external stages point at your S3, GCS, or Azure container through a storage integration, and both directions use `COPY INTO`.

```sql
CREATE OR REPLACE STORAGE INTEGRATION s3_orders_int
  TYPE = EXTERNAL_STAGE STORAGE_PROVIDER = 'S3' ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('s3://acme-raw/orders/');

CREATE OR REPLACE STAGE raw.orders.landing URL = 's3://acme-raw/orders/'
  STORAGE_INTEGRATION = s3_orders_int FILE_FORMAT = (TYPE = PARQUET);

COPY INTO raw.orders.orders FROM @raw.orders.landing
  FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  PATTERN = '.*2026-10-04.*[.]parquet' ON_ERROR = 'CONTINUE' FORCE = FALSE;
```

Know the `ON_ERROR` modes, `VALIDATION_MODE` for dry runs, the 64-day load metadata behind `FORCE`, and `MATCH_BY_COLUMN_NAME` for drift-tolerant loads; loading thousands of tiny files is the classic ingestion anti-pattern.

[Table of Contents](#Snowflake)

## How do you handle semi-structured data with VARIANT?

`VARIANT` stores JSON, Avro, Parquet, ORC, or XML in a single column with an internal structure Snowflake manages; access fields with `:` and cast with `::`, explode arrays with `FLATTEN`, and note that keys seen in the data are captured in metadata so path lookups stay fast.

```sql
CREATE OR REPLACE TABLE raw.events (event_id STRING, payload VARIANT);

COPY INTO raw.events (event_id, payload)
FROM (SELECT $1:event_id::STRING, $1 FROM @raw.events.event_stage)
FILE_FORMAT = (TYPE = JSON STRIP_OUTER_ARRAY = TRUE);

SELECT payload:user.id::NUMBER AS user_id,
       TRY_CAST(payload:amount AS NUMBER(12, 2)) AS amount
FROM raw.events WHERE payload:event_type::STRING = 'purchase';

SELECT i.value:sku::STRING AS sku
FROM raw.events e, LATERAL FLATTEN(input => e.payload:items) i;
```

Model in two layers: keep raw `VARIANT` for replay and schema drift, then flatten the fields you actually query into typed columns in a view or dynamic table.

[Table of Contents](#Snowflake)

## How do external tables work?

An external table is read-only and points at data in your own cloud storage with Snowflake storing only metadata and partition information, so you can query a lake in place without loading it.

```sql
CREATE OR REPLACE EXTERNAL TABLE raw.lake.events_ext (
  event_id STRING AS (VALUE:c1::STRING), payload VARIANT AS (VALUE))
LOCATION = @raw.lake.events_stage/events/
FILE_FORMAT = (TYPE = PARQUET) AUTO_REFRESH = TRUE;

ALTER EXTERNAL TABLE raw.lake.events_ext REFRESH;

SELECT METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, event_id
FROM raw.lake.events_ext LIMIT 10;
```

There is no clustering, Time Travel, materialized view, or DML support and performance depends entirely on object-storage layout, so external tables suit cold lake data while hot analytics belongs in native tables.

[Table of Contents](#Snowflake)

## How do Snowflake Iceberg tables work?

A Snowflake-managed Iceberg table stores Parquet in your external volume with Iceberg metadata so Spark, Trino, and Flink can read and write the same table, and you can also attach an externally managed table from AWS Glue or an Iceberg REST catalog.

```sql
CREATE OR REPLACE EXTERNAL VOLUME iceberg_vol
  STORAGE_LOCATIONS = ((NAME = 's3_primary' STORAGE_PROVIDER = 'S3'
    STORAGE_BASE_URL = 's3://acme-iceberg/'
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::111122223333:role/snowflake-iceberg'));

CREATE OR REPLACE ICEBERG TABLE analytics.orders_iceberg (
  order_id NUMBER, order_date DATE, amount NUMBER(12, 2))
  CATALOG = 'SNOWFLAKE' EXTERNAL_VOLUME = 'iceberg_vol' BASE_LOCATION = 'analytics/orders';

CREATE OR REPLACE ICEBERG TABLE analytics.orders_glue
  CATALOG = 'glue_catalog_integration' CATALOG_TABLE_NAME = 'orders' EXTERNAL_VOLUME = 'iceberg_vol';
```

The design decision is ownership: a Snowflake-managed Iceberg table is written through Snowflake, while a catalog-linked table is treated as read-mostly when another engine owns writes.

[Table of Contents](#Snowflake)

## What is Snowpark and how do you use Python in Snowflake?

Snowpark lets you write DataFrame-style Python, Java, or Scala that is translated to SQL and executed inside Snowflake, so data never leaves the platform and the client ships a plan instead of pulling rows into memory.

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder.configs(
    {"account": "acme-org_acme", "user": "TRANSFORMER", "password": "<password>",
     "role": "TRANSFORM_ROLE", "warehouse": "TRANSFORM_WH"}
).create()

orders = session.table("RAW.ORDERS.ORDERS")
daily = orders.group_by(col("ORDER_DATE")).agg(sum_(col("AMOUNT")).alias("REVENUE"))
daily.write.mode("overwrite").save_as_table("ANALYTICS.MARTS.DAILY_REVENUE")
```

The DataFrame API is lazy, so nothing runs until an action such as `collect()`, `count()`, or `save_as_table()`, and memory-heavy Python benefits from a Snowpark-optimized warehouse.

[Table of Contents](#Snowflake)

## What are UDFs and stored procedures?

A UDF returns a value per row and is called from SQL, while a stored procedure runs procedural logic, can execute DML and DDL, and is invoked with `CALL`; UDFs support SQL, JavaScript, Python, and Java, and procedures support the same languages plus Snowflake Scripting.

```python
from snowflake.snowpark.functions import udf


@udf(name="mask_email", replace=True, is_permanent=True, stage_location="@utils.udf_stage")
def mask_email(value: str) -> str:
    if not value or "@" not in value:
        return "invalid"
    return value[0] + "***" + value[value.index("@"):]
```

```sql
CREATE OR REPLACE PROCEDURE analytics.load_daily(load_date DATE)
  RETURNS STRING LANGUAGE SQL
AS
$$
BEGIN
  DELETE FROM analytics.marts.daily_revenue WHERE order_date = :load_date;
  INSERT INTO analytics.marts.daily_revenue
  SELECT order_date, SUM(amount) FROM raw.orders.orders
  WHERE order_date = :load_date GROUP BY order_date;
  RETURN 'loaded ' || :load_date::STRING;
END;
$$;
CALL analytics.load_daily('2026-10-04');
```

Keep UDFs pure and small because they cannot query other tables, avoid row-by-row Python UDFs on large scans, and grant `USAGE` on the function to every calling role.

[Table of Contents](#Snowflake)

## What is the RBAC role and privilege model?

Access control is role-based: privileges go to roles, roles are granted to roles to form a hierarchy, users receive roles, and there are no user-to-object grants in a good design, with built-in roles `ACCOUNTADMIN`, `SYSADMIN`, `SECURITYADMIN`, `USERADMIN`, and `PUBLIC`.

```sql
USE ROLE SECURITYADMIN;
CREATE ROLE IF NOT EXISTS analytics_engineer;

USE ROLE SYSADMIN;
GRANT USAGE ON WAREHOUSE transform_wh TO ROLE analytics_engineer;
GRANT USAGE ON SCHEMA analytics.marts TO ROLE analytics_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics.marts TO ROLE analytics_engineer;
GRANT SELECT ON FUTURE TABLES IN SCHEMA analytics.marts TO ROLE analytics_engineer;
GRANT ROLE analytics_engineer TO ROLE SYSADMIN;
```

Create functional roles, one per job to be done, grant on `FUTURE` objects so new tables inherit access, keep `ACCOUNTADMIN` for account administration only, and remember that `OWNERSHIP` implies full control.

[Table of Contents](#Snowflake)

## What are secure views, row access policies, and column masking?

These features enforce least privilege below the SQL layer: a secure view hides its definition and disables optimizer shortcuts that could leak data, a row access policy filters which rows a role sees, and a masking policy rewrites a column value per query.

```sql
CREATE OR REPLACE SECURE VIEW analytics.v_orders AS
SELECT order_id, customer_id, amount FROM analytics.orders WHERE order_status <> 'test';

CREATE OR REPLACE ROW ACCESS POLICY security.region_policy
  AS (region STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() = 'ACCOUNTADMIN'
    OR EXISTS (SELECT 1 FROM security.region_map m
               WHERE m.role_name = CURRENT_ROLE() AND m.region = region);
ALTER TABLE analytics.orders ADD ROW ACCESS POLICY security.region_policy ON (region);

CREATE OR REPLACE MASKING POLICY security.email_mask
  AS (val STRING) RETURNS STRING ->
    CASE WHEN CURRENT_ROLE() IN ('PII_ADMIN', 'ACCOUNTADMIN') THEN val
         ELSE REGEXP_REPLACE(val, '^[^@]+', '***') END;
ALTER TABLE analytics.customers MODIFY COLUMN email SET MASKING POLICY security.email_mask;
```

Masking and row access policies require Enterprise Edition, so key on `CURRENT_ROLE()` rather than `CURRENT_USER()` and use a secure view when the rule is a query rather than a predicate.

[Table of Contents](#Snowflake)

## How do resource monitors control cost?

A resource monitor tracks credit consumption against a quota and fires actions at thresholds, and you attach one to the account and to the warehouses that matter so cost control is enforced rather than merely observed.

```sql
CREATE OR REPLACE RESOURCE MONITOR elt_monitor WITH CREDIT_QUOTA = 2000
  FREQUENCY = MONTHLY TRIGGERS ON 75 PERCENT DO NOTIFY
                          ON 100 PERCENT DO SUSPEND
                          ON 110 PERCENT DO SUSPEND_IMMEDIATE;
ALTER WAREHOUSE elt_wh SET RESOURCE_MONITOR = elt_monitor;

SELECT warehouse_name, SUM(credits_used) AS credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP()) GROUP BY 1;
```

`SUSPEND` lets running statements finish while `SUSPEND_IMMEDIATE` cancels them, so notify early and escalate slowly, and watch `METERING_HISTORY` because serverless features consume credits too.

[Table of Contents](#Snowflake)

## How do transactions and isolation work in Snowflake?

Snowflake is ACID-compliant and defaults to read-committed snapshot isolation, so each statement sees a consistent snapshot as of statement start and uncommitted changes are invisible, with serializable isolation available per session.

```sql
ALTER SESSION SET TRANSACTION_ISOLATION_LEVEL = 'SERIALIZABLE';

BEGIN;
UPDATE analytics.accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE analytics.accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
```

DDL runs in its own transaction and auto-commits even inside an explicit block, so a create-then-roll-back does not undo it, and because readers never block writers, contention surfaces as warehouse queueing rather than lock waits.

[Table of Contents](#Snowflake)

## What is Snowflake data sharing?

Data sharing exposes read-only databases to other accounts without copying data: consumers mount a database from the share and query it with their own warehouses, and shares can be published as listings and replicated across regions and clouds.

```sql
CREATE SHARE sales_share;
GRANT USAGE ON DATABASE analytics TO SHARE sales_share;
GRANT SELECT ON TABLE analytics.marts.fct_orders TO SHARE sales_share;
ALTER SHARE sales_share ADD ACCOUNTS = consumer_org.consumer_acct;

CREATE DATABASE shared_sales FROM SHARE provider_org.provider_acct.sales_share;
GRANT IMPORTED PRIVILEGES ON DATABASE shared_sales TO ROLE analyst;
```

Shares are read-only, zero-copy, and live, so consumers see new data as the provider loads it and the provider's Time Travel still governs it; cross-region sharing needs replication and reader accounts serve organizations without a Snowflake account.

[Table of Contents](#Snowflake)

## What is the search optimization service?

Search optimization adds a persistent index-like structure that makes highly selective point lookups fast, targeting equality and `IN` predicates, leading-wildcard `LIKE`, `ARRAY_CONTAINS`, and geospatial predicates that micro-partition pruning cannot help with.

```sql
ALTER TABLE analytics.customers ADD SEARCH OPTIMIZATION ON EQUALITY(email, customer_id);
ALTER TABLE analytics.events    ADD SEARCH OPTIMIZATION ON SUBSTRING(url);

SELECT customer_id, email FROM analytics.customers WHERE email = 'someone@example.com';

ALTER TABLE analytics.customers DROP SEARCH OPTIMIZATION ON EQUALITY(email);
```

Maintenance is serverless and runs on every DML, so it pays off on large, slowly changing tables with selective lookups and hurts on small, high-churn tables; it is not a general accelerator.

[Table of Contents](#Snowflake)

## What are materialized views?

A materialized view stores the precomputed result of a query and is maintained automatically as the base table changes, and the optimizer can transparently rewrite eligible queries to use it, though Enterprise Edition is required.

```sql
CREATE OR REPLACE MATERIALIZED VIEW analytics.mv_daily_revenue AS
SELECT order_date, SUM(amount) AS revenue, COUNT(*) AS orders
FROM analytics.orders GROUP BY order_date;

SHOW MATERIALIZED VIEWS IN SCHEMA analytics;
ALTER MATERIALIZED VIEW analytics.mv_daily_revenue SUSPEND;  -- pause maintenance
```

Materialized views are deliberately narrow - one table, no joins, no `HAVING`, no window functions, no UDFs - and maintenance uses serverless credits, so reserve them for a few expensive aggregations on moderate-churn tables.

[Table of Contents](#Snowflake)

## What is the query acceleration service?

The query acceleration service offloads parts of a scan and aggregation to serverless compute for eligible queries, which is most valuable when a few outlier queries scan far more data than the typical workload on a warehouse.

```sql
ALTER WAREHOUSE bi_wh SET ENABLE_QUERY_ACCELERATION = TRUE
  QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;

SELECT SYSTEM$ESTIMATE_QUERY_ACCELERATION('<query_id>');

SELECT query_id, query_acceleration_bytes_scanned
FROM snowflake.account_usage.query_history
WHERE query_acceleration_bytes_scanned > 0 ORDER BY start_time DESC;
```

QAS helps a warehouse sized for the median query that occasionally receives a much larger one because it avoids scaling everything up for the outlier, but it does not fix poor pruning and its usage is metered.

[Table of Contents](#Snowflake)

## How do you migrate from Redshift, Hadoop, or another warehouse?

The pattern is consistent: land source data as files, load it, translate the SQL and semantics, then validate before cutover, with SnowConvert and the Snowflake Migration Assistant automating much of the syntax work while data model, permissions, and workload placement stay design decisions.

```python
import snowflake.connector

conn = snowflake.connector.connect(
    account="acme-org_acme", user="MIGRATOR", role="MIGRATION_ROLE",
    warehouse="MIGRATION_WH",
)
cur = conn.cursor()

for source, target in [("migration.orders_raw", "analytics.fct_orders")]:
    cur.execute(f"SELECT COUNT(*) FROM {source}")
    before = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM {target}")
    after = cur.fetchone()[0]
    print(source, target, before, after, "ok" if before == after else "MISMATCH")
```

Move data before logic, keep the source running until reconciliation passes, and expect to re-express distribution and sort keys as clustering plus warehouse sizing, validating counts, sums, distinct keys, and sample business reports.

[Table of Contents](#Snowflake)

## What are common Snowflake anti-patterns?

+ **One always-on warehouse for every workload.** Separate loading, transformation, BI, and ad-hoc compute.
+ **`AUTO_SUSPEND = 0` by default.** You pay for idle compute; use short suspend for batch and longer for interactive bursts.
+ **Auto-resume disabled.** Scheduled loads fail silently instead of waking the warehouse.
+ **Scaling up or clustering before fixing the query.** An unordered load makes every filter a full scan at any warehouse size.
+ **Over-clustering.** Keys on small or low-selectivity tables cost maintenance and buy nothing.
+ **Thousands of tiny files into a pipe or `COPY INTO`.** Batch them first, or use Snowpipe Streaming.
+ **`SELECT *` everywhere.** Column pruning is one of the few levers that always works.
+ **Treating `VARIANT` as the schema.** Flatten queried fields into typed columns; raw JSON belongs in landing.
+ **Assuming Time Travel is backup.** It is retention-bound, and Fail-safe is not queryable.
+ **No resource monitors.** Cost grows invisibly until someone reads the bill.
+ **Long transactions mixing DDL and DML.** DDL auto-commits independently and cannot be rolled back.

[Table of Contents](#Snowflake)

## Real world use cases for Snowflake

### 1. Retail ELT with dbt and incremental loads

A retailer lands POS, e-commerce, and inventory feeds in S3, loads them with `COPY INTO`, and transforms them with dbt; daily volume is roughly 400 million order lines and 2 TB of raw files.

```sql
COPY INTO raw.orders.orders FROM @raw.orders.landing/order_date=2026-10-04/
  FILE_FORMAT = (TYPE = PARQUET) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

MERGE INTO analytics.fct_orders AS t
USING stg_orders AS s ON t.order_id = s.order_id
WHEN MATCHED THEN UPDATE SET amount = s.amount, status = s.status, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (order_id, customer_id, order_date, amount, status, updated_at)
VALUES (s.order_id, s.customer_id, s.order_date, s.amount, s.status, s.updated_at);
```

Why: loading and transformation use separate warehouses, the merge makes retries safe, and clustering on `(order_date, customer_id)` keeps month-over-month reporting scans small.

### 2. Fintech regulatory reporting with Time Travel

A licensed lender must reproduce balances and classifications as of a reporting date, so loads are immutable and the reporting query pins a timestamp to make the number auditable.

```sql
CREATE TABLE analytics.regulatory_snapshot CLONE analytics.fct_balances
  AT (TIMESTAMP => '2026-09-30 23:59:59'::TIMESTAMP);

SELECT customer_id, SUM(CASE WHEN balance >= 10000 THEN balance ELSE 0 END) AS reportable_balance
FROM analytics.regulatory_snapshot GROUP BY customer_id;
```

Why: Time Travel plus clones make point-in-time reporting a query rather than a restore exercise, and secure views with masking policies keep PII out of the analyst role.

### 3. Multi-tenant SaaS analytics with row access policies

A SaaS vendor serves all customers from one warehouse but must guarantee tenant isolation, so a mapping table links roles to tenant ids and a row access policy on the fact tables enforces the filter for every client, including BI tools.

```sql
CREATE OR REPLACE ROW ACCESS POLICY security.tenant_policy
  AS (tenant_id STRING) RETURNS BOOLEAN ->
    CURRENT_ROLE() IN ('ACCOUNTADMIN', 'TENANT_ADMIN')
    OR EXISTS (SELECT 1 FROM security.tenant_map m
               WHERE m.role_name = CURRENT_ROLE() AND m.tenant_id = tenant_id);

ALTER TABLE analytics.fct_usage ADD ROW ACCESS POLICY security.tenant_policy ON (tenant_id);
```

Why: isolation is enforced by the engine rather than by each dashboard, so a misconfigured report cannot leak another tenant's data and one copy serves everyone.

### 4. Streaming CDC with Snowpipe Streaming and streams

A payments platform emits change events to Kafka, a connector writes them through Snowpipe Streaming into a raw table, a stream captures deltas, and a task merges them every few minutes with sub-10-minute end-to-end latency.

```sql
CREATE OR REPLACE TASK analytics.apply_payments
  WAREHOUSE = transform_wh SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('raw.payments.payments_stream')
AS
  MERGE INTO analytics.fct_payments AS t
  USING (SELECT payment_id, status, amount, METADATA$ACTION AS action
         FROM raw.payments.payments_stream
         QUALIFY ROW_NUMBER() OVER (PARTITION BY payment_id ORDER BY updated_at DESC) = 1) AS s
  ON t.payment_id = s.payment_id
  WHEN MATCHED AND s.action = 'DELETE' THEN DELETE
  WHEN MATCHED THEN UPDATE SET status = s.status, amount = s.amount;

ALTER TASK analytics.apply_payments RESUME;
```

Why: Snowpipe Streaming removes file-landing latency, the stream makes each task incremental, and the merge makes a retried task safe.

### 5. Cost-optimization program with resource monitors

A platform team runs dozens of warehouses and must cut spend without hurting SLAs, so it attributes credits per warehouse and query tag, right-sizes the biggest consumers, and adds account-level guardrails.

```sql
ALTER SESSION SET QUERY_TAG = 'team:marketing_pipeline';

SELECT warehouse_name, SUM(credits_used) AS credits,
       ROUND(SUM(credits_used) * 3.00, 2) AS approx_usd
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name ORDER BY credits DESC;
```

Why: credits are attributable per warehouse, user, and query tag, so the program is measured rather than argued about; typical wins are shorter auto-suspend, right-sizing, fewer full refreshes, and separated workload compute.

### 6. Lakehouse with Iceberg tables shared across engines

A media company keeps one copy of its event data as Iceberg on S3: Snowflake writes curated tables, Spark reads and backfills them, and Trino serves ad-hoc queries against the same Parquet files.

```sql
CREATE ICEBERG TABLE analytics.events (
  event_id STRING, event_date DATE, customer_id NUMBER, payload VARIANT)
  CATALOG = 'SNOWFLAKE' EXTERNAL_VOLUME = 'iceberg_vol' BASE_LOCATION = 'analytics/events';

INSERT INTO analytics.events
SELECT event_id, event_date, customer_id, payload
FROM raw.events_staging WHERE event_date = '2026-10-04';
```

Why: the table is open, so no engine is locked out and the organization stops paying to copy the same data into a warehouse-native format for every consumer, at the cost of making write ownership, maintenance, and catalog choice explicit.

[Table of Contents](#Snowflake)
