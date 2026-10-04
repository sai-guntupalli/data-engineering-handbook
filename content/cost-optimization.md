## [Main title](../README.md)
### [Interview questions](full.md)

# Cost Optimization

**Notebook:** [`notebooks/topics/cost-optimization.ipynb`](../notebooks/topics/cost-optimization.ipynb) - runnable version of this topic with self-checking exercises.

Cost optimization in data engineering is delivering the same SLAs and business value with fewer resources. It is not a one-off project: storage grows, pipelines multiply, and query patterns drift, so cost work is a recurring discipline alongside performance and reliability.

Platform spend falls into four buckets: **storage**, **compute** (warehouse credits, cluster hours, serverless bytes scanned), **data movement** (egress, cross-region replication), and **operational overhead** (backfills, retries, duplicate pipelines). Interviewers want to see you find the biggest bucket with data, not guess.

+ [Why is cost optimization a core data engineering skill?](#Why-is-cost-optimization-a-core-data-engineering-skill)
+ [How do you reduce warehouse and lake query costs?](#How-do-you-reduce-warehouse-and-lake-query-costs)
+ [How do you explain cost trade-offs in a data architecture interview?](#How-do-you-explain-cost-trade-offs-in-a-data-architecture-interview)
+ [What are the main cost drivers in data platforms?](#What-are-the-main-cost-drivers-in-data-platforms)
+ [How does partitioning affect cost and performance?](#How-does-partitioning-affect-cost-and-performance)
+ [What is the small files problem and why does it increase cost?](#What-is-the-small-files-problem-and-why-does-it-increase-cost)
+ [How do you choose a target file size for Parquet tables?](#How-do-you-choose-a-target-file-size-for-Parquet-tables)
+ [How do you detect and fix data skew in distributed processing?](#How-do-you-detect-and-fix-data-skew-in-distributed-processing)
+ [What is shuffle and how do you reduce it in Spark?](#What-is-shuffle-and-how-do-you-reduce-it-in-Spark)
+ [When should you pre-aggregate or materialize tables?](#When-should-you-pre-aggregate-or-materialize-tables)
+ [How do you prevent runaway queries and protect shared clusters?](#How-do-you-prevent-runaway-queries-and-protect-shared-clusters)
+ [How do you optimize joins in large-scale analytics?](#How-do-you-optimize-joins-in-large-scale-analytics)
+ [How do you plan and estimate the cost of a backfill?](#How-do-you-plan-and-estimate-the-cost-of-a-backfill)
+ [What metrics would you track for FinOps in data engineering?](#What-metrics-would-you-track-for-FinOps-in-data-engineering)
+ [Real world use cases for Cost Optimization](#Real-world-use-cases-for-Cost-Optimization)

## Why is cost optimization a core data engineering skill?

Data platforms can scale costs linearly or worse with data volume and usage. Cost optimization ensures the platform remains sustainable while meeting SLAs. It requires understanding storage layout, compute behavior, query patterns, and operational practices like backfills and compaction.

Frame it as **engineering with a second objective function**. A pipeline that meets its SLA while scanning 50 TB for 20 rows of output is a defect. The efficient patterns - partition pruning, columnar formats, incremental processing, right-sized partitions - are usually the same ones that improve performance and reliability, so cost work rarely forces a trade-off with quality.

Start with measurement, not guesses. The warehouse's own billing views explain most of a bill:

```sql
-- BigQuery: the 20 most expensive queries in the last 7 days
SELECT
    query,
    user_email,
    total_bytes_billed / POW(1024, 4) AS tib_billed,
    ROUND(total_slot_ms / 1000 / 3600, 2) AS slot_hours,
    creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND job_type = 'QUERY' AND state = 'DONE'
ORDER BY total_bytes_billed DESC
LIMIT 20;
```

```sql
-- Snowflake: credit consumption per warehouse per day
SELECT warehouse_name, DATE(start_time) AS usage_date,
       SUM(credits_used) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name, usage_date
ORDER BY credits DESC;
```

Two or three queries usually explain most of the bill: a handful of dashboards scanning raw tables, a backfill re-reading history, and an oversized always-on warehouse. Find those first.

[Table of Contents](#Cost-Optimization)

## How do you reduce warehouse and lake query costs?

Start by reducing data scanned: use columnar formats, partition pruning, clustering/sort keys, and selective projections. Then reduce repeated compute by materializing expensive shared transformations. Finally, set workload controls such as query limits, warehouse auto-suspend, reservations, and alerts.

| Lever | Typical saving | Effort |
|---|---|---|
| Stop scanning unused columns | 30-95% of bytes | low |
| Partition pruning on filter columns | 50-99% of bytes | medium |
| Cluster/sort within partitions | 20-70% of bytes | medium |
| Materialize repeated joins/aggregations | 40-90% of compute | medium-high |
| Auto-suspend and right-size warehouses | 20-60% of credits | low |
| Query guardrails and quotas | bounds the tail | low-medium |

```sql
-- Expensive: every column, all history, filter applied late
SELECT * FROM raw.events_json WHERE event_date >= DATE '2026-10-01';

-- Cheap: three columns, partition-key filter pushed down
SELECT event_date, user_id, COUNT(*) AS events
FROM curated.events
WHERE event_date >= DATE '2026-10-01' AND event_date < DATE '2026-10-08'
GROUP BY event_date, user_id;
```

```bash
# BigQuery: estimate bytes scanned without executing the query
bq query --dry_run --use_legacy_sql=false \
  'SELECT event_date, COUNT(*) FROM `acme.curated.events`
   WHERE event_date = DATE "2026-10-04" GROUP BY event_date'
```

On Snowflake, inspect the query profile and its partition-pruning percentage before and after a change.

**Failure mode:** micro-optimizing a cheap query while one dashboard scans a raw table every 15 minutes. Rank by total spend (frequency x unit cost), not single-query cost.

[Table of Contents](#Cost-Optimization)

## How do you explain cost trade-offs in a data architecture interview?

Frame cost as a product of storage, compute, scan volume, orchestration frequency, and operational complexity. A cheap pipeline that is impossible to debug is not truly cheap. A more expensive serving table may be worth it if it prevents hundreds of dashboard queries from recomputing the same logic.

Example trade-off:

+ raw-only lake: cheap storage, expensive repeated queries
+ curated marts: extra storage and ETL, cheaper and faster BI
+ streaming pipeline: low latency, higher operational cost
+ daily batch: lower cost, higher latency

Quantify it. If 200 analysts run 30 ad-hoc queries a day over a 40 TB raw table, but the pre-aggregated mart is 2 TB:

| Option | Scan per query | Daily scan | Notes |
|---|---|---|---|
| Raw table | ~35 TB | ~210 PB/day | unusable, dominates the bill |
| Pre-aggregated mart | ~40 GB | ~240 TB/day | ~99.9% less scan |
| Mart build cost | - | one 6 TB scan/day | ~3% overhead |

The answer in an interview is a **breakeven statement**: "materializing the mart costs one full scan a day and saves about 200 full scans, so it pays back within hours as long as the mart is reused a few times per day."

Do not optimize away observability (a bad publish costs more than the check), isolation (mixing a backfill with interactive BI hurts everyone), or reproducibility (deleting raw history makes incident recovery impossible - tier it to cheap object storage instead).

[Table of Contents](#Cost-Optimization)

## What are the main cost drivers in data platforms?

Typical drivers include:

+ compute time (clusters, warehouses, serverless slots)
+ bytes scanned and shuffles
+ storage growth (raw + derived + duplicates)
+ data movement (egress, cross-region transfers)
+ operational overhead (frequent backfills, retries)

| Driver | Metric | Typical control |
|---|---|---|
| Warehouse compute | credits or slot-hours | auto-suspend, right-size, budgets |
| Serverless scan | bytes billed | partitioning, clustering, dry runs |
| Spark/cluster compute | DBU or node-hours | right-size, spot, adaptive execution |
| Storage | TB-month by layer | lifecycle to cold tiers, compaction |
| Data movement | GB egress | co-locate compute and storage |
| Orchestration | task-minutes, retries | fewer, larger tasks; idempotent reruns |

Time travel and failsafe are easy to forget because they are billed storage:

```sql
-- Snowflake: storage by schema, separating active from time-travel bytes
SELECT table_schema, table_name,
       ROUND(active_bytes / POW(1024, 3), 2)      AS active_gb,
       ROUND(time_travel_bytes / POW(1024, 3), 2) AS time_travel_gb,
       ROUND(failsafe_bytes / POW(1024, 3), 2)    AS failsafe_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE active_bytes > 100 * POW(1024, 3)
ORDER BY active_bytes DESC
LIMIT 50;
```

If a table retains 10 TB of active data and 40 TB of time travel, reducing retention is a direct cost fix that no query tuning will find.

[Table of Contents](#Cost-Optimization)

## How does partitioning affect cost and performance?

Good partitioning reduces scanned data by enabling partition pruning. Bad partitioning creates too many small partitions, increasing metadata overhead and small files. Partitioning should match common query filters and data distribution, and be reevaluated as workloads evolve.

Guidelines: partition on the columns that appear in `WHERE` clauses, usually a date; keep cardinality moderate (thousands, not hundreds of thousands); do not partition on high-cardinality ids; and recheck that filters do not wrap the partition column in a function.

```sql
-- A function on the partition column defeats pruning
SELECT COUNT(*) FROM curated.events WHERE DATE(event_ts) = DATE '2026-10-04';

-- Pruning-friendly: filter the raw partition column directly
SELECT COUNT(*) FROM curated.events
WHERE event_ts >= TIMESTAMP '2026-10-04 00:00:00'
  AND event_ts <  TIMESTAMP '2026-10-05 00:00:00';
```

```sql
-- Confirm the result: actual bytes processed and slot time
SELECT total_bytes_processed / POW(1024, 3) AS gb_processed,
       total_slot_ms / 1000 / 3600 AS slot_hours
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'job_abc123';
```

Partition **and cluster**: partitioning prunes partitions, while clustering sorts within them so row-group and micro-partition pruning can skip more. On Snowflake that is `CLUSTER BY`, on BigQuery a cluster key, on Iceberg a sort order. Revisit the scheme every few months, because a stale partition choice quietly becomes a full-scan generator.

[Table of Contents](#Cost-Optimization)

## What is the small files problem and why does it increase cost?

Small files increase scheduling and metadata overhead and reduce scan efficiency. Engines spend more time opening and planning files than processing data. Small files often appear from streaming writes or overly granular partitions and typically require compaction or clustering to fix.

The cost is threefold: **metadata/planning** (each file is an open plus a footer parse), **compute** (tiny tasks waste slot time), and **storage** (per-object overhead). A partition with 50,000 one-MB files can be slower than the same data in 50 files of 1 GB.

```sql
-- Iceberg: transactional compaction instead of hand-rewriting files
CALL catalog.system.rewrite_data_files(
    table => 'curated.orders',
    options => map('target-file-size-bytes', '268435456')
);
```

```bash
# Count and size files in a prefix to spot a small-files partition
aws s3api list-objects-v2 --bucket acme-curated --prefix orders/ds=2026-10-04/ \
  --query 'Contents[].Size' --output text | tr '\t' '\n' | sort -n | tail -5
```

**Failure mode:** compacting without controlling the writer. If a streaming job produces one-second micro-batches, compaction runs forever and costs more than it saves. Increase the trigger interval or buffer first, then compact history. Iceberg and Delta make this safe by rewriting files under a transaction; doing it by hand on plain Parquet can corrupt readers mid-swap.

[Table of Contents](#Cost-Optimization)

## How do you choose a target file size for Parquet tables?

You choose a size that balances parallelism and overhead. Too small increases file count and planning cost; too large reduces parallelism and can slow selective queries. Many teams target hundreds of MB per file, but the correct value depends on the engine, storage, and query patterns.

A practical starting point:

+ **Batch lake tables:** 128-512 MB per file, up to 1 GB for append-only facts.
+ **Small dimension tables:** a single file is fine.
+ **Wide/nested tables:** row groups around 128 MB, files under ~1 GB.
+ **Streaming with frequent commits:** a few MB per file, compacted more often.

The math matters more than the number: aim for at least one file per CPU core you want to parallelize across, and at most a few thousand files per query. For a 500 GB partition on a 200-core cluster, 200-500 files of 1-2.5 GB is reasonable; 30 files of 16 GB serializes work, and 200,000 files of 2.5 MB wastes the cluster on planning.

```python
# PySpark: size the write deliberately instead of inheriting the shuffle count
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("right-size-write").getOrCreate()
TARGET_BYTES = 256 * 1024 * 1024
data = spark.read.parquet("s3://acme-curated/orders/")
total_bytes = 900 * 1024 ** 3                 # from S3 inventory / table metadata
files = max(1, total_bytes // TARGET_BYTES)

(
    data.repartition(int(files))
    .write.mode("overwrite")
    .option("parquet.block.size", str(128 * 1024 * 1024))
    .parquet("s3://acme-curated/orders_compact/")
)

spark.conf.set("spark.sql.files.openCostInBytes", str(TARGET_BYTES))
spark.conf.set("spark.sql.files.maxPartitionBytes", str(TARGET_BYTES))
```

`spark.sql.files.openCostInBytes` tells Spark how expensive opening a file is relative to scanning bytes; raising it makes the planner pack more files per task and avoids one tiny task per file.

[Table of Contents](#Cost-Optimization)

## How do you detect and fix data skew in distributed processing?

Skew happens when some partitions have much more data than others, causing straggler tasks. Detect it via task duration distributions and partition size metrics. Fixes include salting keys, using skew-aware joins, repartitioning, or changing the join strategy (broadcast when possible).

Detect it in the Spark UI (one task taking 10x the median) and confirm by counting keys:

```python
from pyspark.sql import functions as F

orders = spark.read.parquet("s3://acme-curated/orders/")
orders.groupBy("customer_id").count().orderBy(F.desc("count")).show(20, truncate=False)
```

Fix options, cheapest first: broadcast the small side; let Adaptive Query Execution handle skew joins; filter early; salt heavy keys; or use two-stage aggregation.

```python
# Salting: spread a heavy key across N buckets, aggregate, then combine
SALT = 16

salt = (
    orders.withColumn("salt", (F.rand() * SALT).cast("int"))
    .withColumn("salted_key", F.concat_ws("#", "customer_id", "salt"))
)
partial = salt.groupBy("salted_key").agg(F.sum("amount").alias("partial_amount"))
final = (
    partial.withColumn("customer_id", F.split("salted_key", "#")[0])
    .groupBy("customer_id")
    .agg(F.sum("partial_amount").alias("amount"))
)
final.show()
```

```python
# Prefer AQE skew handling when the join is the problem - often no code change
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5")
```

**Failure mode:** salting every key "just in case". It adds a shuffle stage and can slow an already balanced job. Measure first and prefer AQE unless you are on an older engine.

[Table of Contents](#Cost-Optimization)

## What is shuffle and how do you reduce it in Spark?

Shuffle is data redistribution across executors (for joins, group by, distinct). It is expensive due to network IO and disk spills. You reduce shuffle by using proper partitioning, avoiding wide transformations, filtering early, broadcasting small tables, and tuning shuffle partitions.

The cost is roughly `data_size x (serialize + write + network + read)`, and spills multiply it. Ask whether the shuffle can be avoided entirely:

+ Replace `groupByKey` with `reduceByKey`/`agg` so partial aggregation happens first.
+ Broadcast a small dimension instead of shuffling the large side.
+ Filter and project **before** the join or group-by.
+ Bucket tables on the join key at write time so reads are shuffle-free.
+ Tune shuffle partitions for the actual data size.

```python
from pyspark.sql import functions as F

orders = spark.read.parquet("s3://acme-curated/orders/")
customers = spark.read.parquet("s3://acme-dim/customers/")   # ~5 MB

slow = orders.join(customers, "customer_id")                 # full shuffle
fast = orders.join(F.broadcast(customers), "customer_id")    # no large shuffle

by_country = (
    orders.filter(F.col("order_date") >= "2026-10-01")
    .groupBy("country")
    .agg(F.sum("amount").alias("revenue"))
)
```

Then set `spark.sql.adaptive.enabled=true` and `spark.sql.adaptive.advisoryPartitionSizeInBytes=128m` so AQE coalesces shuffle partitions to the real data size instead of the default 200.

**Failure mode:** too many shuffle partitions. 10,000 partitions over 20 GB produces thousands of tiny tasks with scheduling and file-open overhead, which shows up in wall-clock and the cluster bill. AQE's partition coalescing usually fixes this automatically.

[Table of Contents](#Cost-Optimization)

## When should you pre-aggregate or materialize tables?

Materialize when many downstream queries reuse expensive computations or when interactive BI requires low latency. Avoid over-materialization because it increases storage and refresh complexity. A good approach is to materialize stable, high-value marts and keep exploratory logic as views.

Use this test: is the transformation **expensive**, **reused**, **stable**, and does it have a clear **grain and owner**? Three or more "yes" answers mean materialize; exploratory logic that changes weekly belongs in a view.

```sql
-- Snowflake: a dynamic table materializes and refreshes on its own
CREATE OR REPLACE DYNAMIC TABLE marts.revenue_daily
  TARGET_LAG = '1 hour'
  WAREHOUSE = transform_wh
AS
SELECT order_date, country, SUM(amount) AS revenue, COUNT(DISTINCT order_id) AS orders
FROM curated.fct_orders
GROUP BY order_date, country;
```

```yaml
# dbt: an incremental model only processes new partitions
# models/marts/revenue_daily.sql
# {{ config(materialized='incremental', unique_key='order_date',
#           partition_by={'field': 'order_date', 'data_type': 'date'},
#           cluster_by=['country']) }}
```

**Failure mode:** materializing everything "for speed". Each extra table adds storage, a refresh job, a failure mode, and a lineage edge. Watch the refresh fan-out too: 500 hourly incremental models can cost more in orchestration and small scans than one well-partitioned daily mart.

[Table of Contents](#Cost-Optimization)

## How do you prevent runaway queries and protect shared clusters?

Use workload management: query timeouts, concurrency limits, resource quotas, and separate compute for heavy workloads. Enforce best practices with guardrails (linting, cost alerts) and educate users with profiling tools. Multi-tenant platforms typically need isolation to prevent one team from impacting others.

Layer controls from cheapest to strictest: budgets and alerts, byte limits, statement timeouts, concurrency caps, separate warehouses/pools, and query tagging for attribution.

```sql
-- Snowflake: suspend a warehouse at a credit threshold
CREATE OR REPLACE RESOURCE MONITOR limit_transform_wh WITH
  CREDIT_QUOTA = 500
  TRIGGERS ON 80 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND
           ON 110 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE transform_wh SET RESOURCE_MONITOR = limit_transform_wh;
```

```bash
# CI guardrail: fail the pull request if a model would scan more than 500 GB
bq query --dry_run --use_legacy_sql=false --format=json < models/revenue.sql \
  | jq -e '.statistics.query.totalBytesProcessed < 500000000000'
```

**Failure mode:** quotas with no runbook. A suspended warehouse at 03:00 blocks the tier-1 pipeline, and on-call must know who to call and how to raise the limit. Pair every hard limit with an alert and an escalation path, and keep batch-critical workloads in a monitored window rather than competing with ad-hoc analysis.

[Table of Contents](#Cost-Optimization)

## How do you optimize joins in large-scale analytics?

You optimize joins by ensuring join keys are clean and well-distributed, filtering before joins, and choosing appropriate join strategies (broadcast vs shuffle). You also reduce the size of join inputs (select only needed columns) and consider pre-joining into curated marts when joins are repeated.

| Join shape | Strategy | Why |
|---|---|---|
| Huge x tiny (< 10 MB) | broadcast | no shuffle of the large side |
| Huge x medium | broadcast if safe, else bucket | avoids the shuffle |
| Huge x huge, filterable | filter/project, then shuffle | moves less data |
| Huge x huge, repeated daily | pre-join into a mart | pay once, reuse |
| Skewed keys | AQE skew join or salting | avoids stragglers |

```sql
-- Reduce both sides before the join: project, filter, then join
WITH recent_orders AS (
    SELECT order_id, customer_id, amount, order_date
    FROM curated.fct_orders
    WHERE order_date >= DATE '2026-10-01'
),
active_customers AS (
    SELECT customer_id, country, segment
    FROM curated.dim_customers
    WHERE is_active = TRUE
)
SELECT c.country, c.segment, SUM(o.amount) AS revenue
FROM recent_orders AS o
JOIN active_customers AS c USING (customer_id)
GROUP BY c.country, c.segment;
```

```python
# PySpark: project and filter before broadcasting the dimension
from pyspark.sql import functions as F

orders = spark.read.parquet("s3://acme-curated/orders/").select(
    "order_id", "customer_id", "amount", "order_date"
)
customers = spark.read.parquet("s3://acme-dim/customers/").select(
    "customer_id", "country", "segment"
)

result = (
    orders.filter(F.col("order_date") >= "2026-10-01")
    .join(F.broadcast(customers), "customer_id")
    .groupBy("country", "segment")
    .agg(F.sum("amount").alias("revenue"))
)
```

**Failure mode:** broadcast joins that outgrow memory. If the "small" side grows past the broadcast threshold, the driver can OOM. Set `spark.sql.autoBroadcastJoinThreshold` deliberately and monitor it rather than assuming a dimension stays small forever.

[Table of Contents](#Cost-Optimization)

## How do you plan and estimate the cost of a backfill?

Estimate based on data volume, compute requirements, and expected scan/shuffle behavior. Run on a small sample window to measure throughput and extrapolate. Backfills should be staged, monitored, and preferably run in off-peak windows, with a clear rollback plan.

A defensible estimate has four numbers: bytes scanned, shuffle bytes, cluster/warehouse hours, and wall-clock. Measure one representative partition, then multiply.

```sql
-- Cost of rebuilding one day: bytes and slot time, then extrapolate
SELECT total_bytes_billed / POW(1024, 4) AS tib_billed,
       total_slot_ms / 1000 / 3600 AS slot_hours
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = 'backfill_orders_2026_09_01' AND state = 'DONE';
```

```python
# 1 day measured -> 90 days planned, with a safety margin
per_day_bytes = 1.2 * 1024 ** 4
per_day_slot_hours = 2.5
days, margin = 90, 1.3

print("scan TiB:", round(per_day_bytes * days / 1024 ** 4, 1))
print("slot-hours:", round(per_day_slot_hours * days * margin, 1))
```

```bash
# Off-peak backfill with bounded concurrency
airflow dags backfill revenue_daily \
  --start-date 2026-07-01 --end-date 2026-09-30 \
  --max-active-runs 2 --reset-dagruns
```

Controls that keep a backfill from becoming an incident: run it on a **separate warehouse/cluster**, cap concurrency, checkpoint progress per partition, and stop if cumulative spend crosses a threshold. Publish the estimate and the expected metric change to stakeholders beforehand.

[Table of Contents](#Cost-Optimization)

## What metrics would you track for FinOps in data engineering?

Common metrics include cost by team/project, cost per pipeline, bytes scanned per query, cluster utilization, storage growth by layer, and top expensive datasets/queries. You also track trend changes (week-over-week) and tie cost to value (usage, criticality).

A useful dashboard has four rows: **spend** (by warehouse/project, with budget burn), **efficiency** (cost per dashboard refresh, per 1,000 queries), **waste** (idle warehouse time, failed-job spend, time-travel storage, unqueried tables), and **value** (spend versus query volume by team).

```sql
-- Cost per pipeline, attributed by query tag (Snowflake)
SELECT REGEXP_SUBSTR(query_tag, 'pipeline=([^;]+)', 1, 1, 'e', 1) AS pipeline,
       COUNT(*) AS queries,
       ROUND(SUM(bytes_scanned) / POW(1024, 4), 2) AS tib_scanned
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  AND query_tag ILIKE '%pipeline=%'
GROUP BY pipeline
ORDER BY tib_scanned DESC
LIMIT 25;
```

```sql
-- Waste: storage for tables not queried in 90 days
SELECT t.table_schema, t.table_name,
       ROUND(t.active_bytes / POW(1024, 3), 1) AS active_gb,
       MAX(q.start_time) AS last_queried
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS AS t
LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY AS q
  ON q.query_text ILIKE '%' || t.table_name || '%'
GROUP BY t.table_schema, t.table_name, t.active_bytes
HAVING last_queried IS NULL OR last_queried < DATEADD('day', -90, CURRENT_TIMESTAMP())
ORDER BY active_gb DESC;
```

Pair every metric with a **target and an owner** ("p95 bytes scanned per dashboard query < 50 GB, owned by BI platform"). Without a target, a FinOps dashboard is just a second bill. Review cost in the same ritual as reliability and treat a sustained budget breach as an incident with a root cause.

[Table of Contents](#Cost-Optimization)

## Real world use cases for Cost Optimization

### 1. E-commerce: cutting a BigQuery bill with partitioning and clustering

A retailer's on-demand BigQuery bill reached ~$68k/month because the top dashboards scanned raw event tables every hour. Daily event volume is ~2 TB and the fact table holds 300 TB.

```sql
-- After: partition by day, cluster by country; the same query scans ~1/50th
CREATE OR REPLACE TABLE curated.events
PARTITION BY DATE(event_ts)
CLUSTER BY country, event_type
AS SELECT * FROM raw.events_json;

SELECT country, SUM(amount) AS revenue
FROM curated.events
WHERE event_ts >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY country;
```

**Why this design:** on-demand pricing is linear in bytes scanned, so partition pruning plus clustering was the highest-leverage change and needed no query rewrites beyond removing the `DATE()` wrapper. A CI dry-run gate stops the regression from returning.

### 2. Snowflake: right-sizing warehouses and killing idle time

A SaaS company ran a single XL warehouse 24/7 for all workloads; ETL and analyst queries contended, so both were slow and the warehouse rarely suspended.

```sql
CREATE WAREHOUSE etl_wh   WAREHOUSE_SIZE = LARGE  AUTO_SUSPEND = 60  AUTO_RESUME = TRUE;
CREATE WAREHOUSE bi_wh    WAREHOUSE_SIZE = MEDIUM AUTO_SUSPEND = 300 AUTO_RESUME = TRUE;
CREATE WAREHOUSE adhoc_wh WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60  AUTO_RESUME = TRUE;

ALTER WAREHOUSE bi_wh SET MIN_CLUSTER_COUNT = 1 MAX_CLUSTER_COUNT = 4 SCALING_POLICY = 'ECONOMY';
```

**Why this design:** separating ETL from BI removed contention, let each warehouse match its workload, and aggressive auto-suspend eliminated idle hours. Multi-cluster BI keeps analyst latency predictable while billing only for clusters actually used.

### 3. Fintech: controlling a Spark backfill that would have cost a month of budget

A payments team needed to reprocess 18 months of transactions (~180 TB) after a currency-conversion bug. A naive full reprocess on on-demand clusters would have cost tens of thousands of dollars.

```python
# Spot instances, dynamic allocation, and per-month checkpoints
spark = (
    SparkSession.builder.appName("fx-reprocess-2026")
    .config("spark.executor.instances", "40")
    .config("spark.dynamicAllocation.enabled", "true")
    .config("spark.sql.adaptive.enabled", "true")
    .getOrCreate()
)

for month in month_range("2025-01", "2026-06"):
    if checkpoint_done(month):
        continue                                   # restartable: skip completed months
    (spark.read.parquet(f"s3://acme-raw/txn/month={month}/")
          .transform(convert_currency)
          .write.mode("overwrite")
          .parquet(f"s3://acme-curated/txn/month={month}/"))
    checkpoint_mark(month)
```

**Why this design:** spot capacity with dynamic allocation cut the compute rate, per-month checkpoints meant a preemption lost at most one month, and a one-month pilot validated the per-month cost before committing to all 18.

### 4. Multi-tenant SaaS: taming streaming small files

A platform ingests 5 TB/day via Kafka into S3 using 30-second micro-batches, producing ~300,000 small Parquet files per day. Query planning dominated runtime and S3 request charges dominated storage cost.

```python
# Longer trigger interval reduces file creation at the source
(
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "events")
    .load()
    .writeStream
    .format("iceberg")
    .option("checkpointLocation", "s3://acme-checkpoints/events/")
    .trigger(processingTime="10 minutes")
    .toTable("lake.events")
)
```

```sql
-- Then compact history transactionally and expire old snapshots
CALL lake.system.rewrite_data_files(
    table => 'lake.events',
    options => map('target-file-size-bytes', '268435456', 'min-input-files', '5')
);
CALL lake.system.expire_snapshots(table => 'lake.events', older_than => TIMESTAMP '2026-10-01 00:00:00');
```

**Why this design:** compaction alone would have run forever while the writer kept producing tiny files, so the pipeline first increased the commit interval and then used Iceberg's transactional compaction and snapshot expiry. Expiring snapshots also cut metastore size, which had become a planning bottleneck.

[Table of Contents](#Cost-Optimization)
