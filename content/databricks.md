## [Main title](../README.md)
### [Interview questions](full.md)

# Databricks

Databricks is a managed lakehouse platform built on Apache Spark, Delta Lake, and Unity Catalog; it is where most Spark-and-Delta interview questions become concrete.

+ [What is Databricks?](#What-is-Databricks)
+ [How does the Databricks architecture work?](#How-does-the-Databricks-architecture-work)
+ [What cluster types exist and when do you use each?](#What-cluster-types-exist-and-when-do-you-use-each)
+ [How do you size and configure a cluster for performance and cost?](#How-do-you-size-and-configure-a-cluster-for-performance-and-cost)
+ [What is Unity Catalog and how does the three-level namespace work?](#What-is-Unity-Catalog-and-how-does-the-three-level-namespace-work)
+ [How do you govern data with Unity Catalog?](#How-do-you-govern-data-with-Unity-Catalog)
+ [How does Delta Lake work on Databricks?](#How-does-Delta-Lake-work-on-Databricks)
+ [How do you run incremental ingestion with Auto Loader?](#How-do-you-run-incremental-ingestion-with-Auto-Loader)
+ [How do you build a medallion pipeline (bronze, silver, gold)?](#How-do-you-build-a-medallion-pipeline-bronze-silver-gold)
+ [What are Lakeflow Declarative Pipelines (Delta Live Tables)?](#What-are-Lakeflow-Declarative-Pipelines-Delta-Live-Tables)
+ [How do you orchestrate jobs and workflows?](#How-do-you-orchestrate-jobs-and-workflows)
+ [How do you manage Databricks resources as code?](#How-do-you-manage-Databricks-resources-as-code)
+ [How do you query data with Databricks SQL?](#How-do-you-query-data-with-Databricks-SQL)
+ [What is Photon and when does it help?](#What-is-Photon-and-when-does-it-help)
+ [How do you tune Delta tables on Databricks?](#How-do-you-tune-Delta-tables-on-Databricks)
+ [How do you handle schema evolution and Change Data Feed?](#How-do-you-handle-schema-evolution-and-Change-Data-Feed)
+ [How do you implement CI/CD for Databricks?](#How-do-you-implement-CICD-for-Databricks)
+ [What security and access-mode concepts matter?](#What-security-and-access-mode-concepts-matter)
+ [How do you control Databricks cost?](#How-do-you-control-Databricks-cost)
+ [How does Databricks compare with Snowflake and BigQuery?](#How-does-Databricks-compare-with-Snowflake-and-BigQuery)
+ [How do you migrate from on-prem Spark and Hive?](#How-do-you-migrate-from-on-prem-Spark-and-Hive)
+ [What is MLflow and how is it used on Databricks?](#What-is-MLflow-and-how-is-it-used-on-Databricks)
+ [What are common Databricks interview traps?](#What-are-common-Databricks-interview-traps)
+ [Real world use cases for Databricks](#Real-world-use-cases-for-Databricks)

## What is Databricks?

Databricks is a managed data platform that packages Apache Spark with Delta Lake, a governance layer (Unity Catalog), a SQL warehouse, workflow orchestration, and ML tooling. The core promise is the **lakehouse**: ACID tables, schema enforcement, and time travel on cheap object storage, with one copy of data serving BI, data science, and streaming.

```text
cloud storage (S3/ADLS/GCS)
        |
   Delta / Iceberg tables          <- open formats, one copy of data
        |
Spark + Photon  |  SQL warehouses  |  MLflow / serving
        |
   Unity Catalog: catalogs.schemas.tables + lineage + grants
```

Interview framing: Databricks is not a database engine you install - it is a control plane plus managed compute on top of your cloud account, with Delta as the table format and Spark as the execution engine.

[Table of Contents](#Databricks)

## How does the Databricks architecture work?

+ **Control plane** - the Databricks-managed layer: workspace UI, notebooks, job scheduler, Unity Catalog metadata, cluster manager. Databricks operates it.
+ **Data plane (compute plane)** - clusters and SQL warehouses that run in your cloud account/network, next to your storage. Data does not have to leave your account.
+ **Serverless compute** - Databricks-managed compute in the Databricks account; no cluster to size, faster startup, per-second billing.
+ **Storage** - object storage in your account (S3, ADLS Gen2, GCS), accessed through Unity Catalog external locations and storage credentials rather than hard-coded keys.
+ **Notebooks and jobs** - interactive work and scheduled production work use the same Spark engine and the same tables.

```text
Workspace (control plane)
   |  REST API / CLI / Terraform / bundles
   v
Compute plane (your cloud account)
   +-- all-purpose cluster (interactive, shared)
   +-- job cluster (ephemeral, per-run)
   +-- SQL warehouse (BI and SQL)
   +-- serverless (Databricks account)
   |
   v
Object storage: s3://acme-lake/bronze|silver|gold
```

[Table of Contents](#Databricks)

## What cluster types exist and when do you use each?

| Cluster | Lifetime | Used for | Cost profile |
|---|---|---|---|
| All-purpose | long-lived, shared | interactive notebooks, exploration, ad-hoc | expensive per DBU; idle cost if not auto-stopped |
| Job cluster | created per job run | production pipelines | cheapest for scheduled work, isolated per run |
| SQL warehouse | managed, auto-stop | BI, dashboards, SQL users | sized by warehouse size and clusters |
| Serverless (jobs/SQL/notebooks) | managed | bursty or latency-sensitive workloads | no cluster management, per-second billing |

Rules of thumb:

+ Run production pipelines on **job clusters** (or serverless jobs), never on a developer's all-purpose cluster.
+ Use **all-purpose** clusters for exploration and pair them with aggressive auto-stop.
+ Use **SQL warehouses** for BI so warehouse sizing and concurrency are independent of Spark jobs.
+ Give each workload its own cluster **access mode** and policy when governance requires isolation.

```json
{
  "cluster_name": "etl-daily",
  "spark_version": "auto:latest-lts",
  "node_type_id": "m5d.4xlarge",
  "autoscale": {"min_workers": 4, "max_workers": 32},
  "aws_attributes": {"availability": "SPOT_WITH_FALLBACK", "zone_id": "auto"},
  "autotermination_minutes": 20,
  "custom_tags": {"team": "data-platform", "cost-center": "analytics"},
  "spark_conf": {"spark.sql.adaptive.enabled": "true"}
}
```

[Table of Contents](#Databricks)

## How do you size and configure a cluster for performance and cost?

+ **Workers** - memory-optimized (r-family) for shuffles and caching; compute-optimized (c-family) for CPU-heavy transformation; storage-optimized (i/d-family) when spilling or caching to local disk matters.
+ **Autoscaling** - scale within a range; it reacts to pending tasks, so it is not a substitute for fixing skew.
+ **Spot instances with fallback** - large savings for batch; avoid for latency-critical or stateful streaming drivers.
+ **Driver size** - the driver collects results and runs the DAG; `collect()` on a large DataFrame still kills the driver.
+ **Photon** - enable it for SQL/DataFrame heavy workloads; it does not accelerate row-at-a-time Python UDFs.
+ **Auto-stop** - set 10-20 minutes on interactive clusters; the biggest source of accidental spend is an idle cluster.

```python
# Check what a job actually used: sizing questions are answered with data, not opinions
display(spark.sql("""
    SELECT usage_metadata.cluster_id AS cluster_id,
           usage_metadata.job_id AS job_id,
           SUM(usage_quantity) AS dbus
    FROM system.billing.usage
    WHERE usage_date >= current_date() - INTERVAL 30 DAYS
    GROUP BY usage_metadata.cluster_id, usage_metadata.job_id
    ORDER BY dbus DESC
    LIMIT 20
"""))
```

[Table of Contents](#Databricks)

## What is Unity Catalog and how does the three-level namespace work?

Unity Catalog is the governance layer for data and AI assets. Objects are addressed with three levels:

```text
catalog.schema.table
acme.silver.orders
acme.gold.fct_orders
acme.bronze.orders_raw
```

+ **Metastore** - one per region (typically); attaches to workspaces.
+ **Catalog** - the top-level container, often per environment (`dev`, `prod`) or per domain.
+ **Schema** - database-level grouping of tables, views, volumes, functions, models.
+ **Volumes** - governed storage for files that are not tables (`/Volumes/acme/landing/orders/`).
+ **External locations and storage credentials** - central place to grant access to cloud storage; notebooks no longer need access keys.

```sql
CREATE CATALOG IF NOT EXISTS acme;
CREATE SCHEMA IF NOT EXISTS acme.silver;

CREATE TABLE IF NOT EXISTS acme.silver.orders (
    order_id      STRING NOT NULL,
    customer_id   STRING,
    order_ts      TIMESTAMP,
    amount        DECIMAL(18, 2),
    status        STRING
)
USING DELTA
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

[Table of Contents](#Databricks)

## How do you govern data with Unity Catalog?

Governance is a first-class interview topic: grants, fine-grained filters, and lineage all live in the catalog.

```sql
-- role-style grants at catalog/schema/table level
GRANT USE CATALOG ON CATALOG acme TO `analytics`;
GRANT USE SCHEMA ON SCHEMA acme.gold TO `analytics`;
GRANT SELECT ON TABLE acme.gold.fct_orders TO `analytics`;

-- column mask: analysts see a hashed email
CREATE FUNCTION acme.security.mask_email(email STRING)
RETURNS STRING
RETURN CASE WHEN is_account_group_member('pii-readers') THEN email
            ELSE sha2(email, 256) END;

ALTER TABLE acme.gold.dim_customer
ALTER COLUMN email SET MASK acme.security.mask_email;

-- row filter: each regional team sees only its region
CREATE FUNCTION acme.security.region_filter(region STRING)
RETURNS BOOLEAN
RETURN is_account_group_member('global-readers')
       OR is_account_group_member(CONCAT('region-', region));

ALTER TABLE acme.gold.fct_orders
SET ROW FILTER acme.security.region_filter ON (region);
```

Also know **attribute-based access** with tags, **lineage** (table -> notebook/job -> dashboard), **audit logs** in `system.access.audit`, and **data contracts** via constraints plus enforced schemas.

[Table of Contents](#Databricks)

## How does Delta Lake work on Databricks?

Delta Lake is the default table format on Databricks: Parquet files plus a transaction log (`_delta_log`) that adds ACID commits, schema enforcement, time travel, and efficient updates/deletes.

```sql
-- time travel and restore
SELECT * FROM acme.silver.orders VERSION AS OF 42;
SELECT * FROM acme.silver.orders TIMESTAMP AS OF '2026-10-01T00:00:00Z';
RESTORE TABLE acme.silver.orders TO VERSION AS OF 42;

-- inspect history and table details
DESCRIBE HISTORY acme.silver.orders;
DESCRIBE DETAIL acme.silver.orders;
```

```python
from delta.tables import DeltaTable

# idempotent upsert from a staging DataFrame
(
    DeltaTable.forName(spark, "acme.silver.orders").alias("t")
    .merge(staged.alias("s"), "t.order_id = s.order_id")
    .whenMatchedUpdateAll(condition="s.updated_at > t.updated_at")
    .whenNotMatchedInsertAll()
    .execute()
)
```

[Table of Contents](#Databricks)

## How do you run incremental ingestion with Auto Loader?

Auto Loader (`cloudFiles`) incrementally discovers new files in cloud storage, tracks them in a RocksDB-backed state store, and handles schema inference and evolution. It is the standard bronze-layer ingestion pattern.

```python
schema_location = "/Volumes/acme/bronze/checkpoints/orders_schema"
checkpoint = "/Volumes/acme/bronze/checkpoints/orders"

raw = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_location)
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.inferColumnTypes", "true")
    .option("cloudFiles.maxFilesPerTrigger", 1000)
    .load("s3://acme-raw/orders/")
)

(
    raw.writeStream
    .option("checkpointLocation", checkpoint)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)          # batch-style catch-up, then stop
    .toTable("acme.bronze.orders_raw")
)
```

Why it matters: no file-listing bookkeeping, exactly-once progress via checkpoints, and new columns do not break the pipeline. `availableNow` gives you scheduled micro-batch behaviour without keeping a streaming cluster alive.

[Table of Contents](#Databricks)

## How do you build a medallion pipeline (bronze, silver, gold)?

The medallion pattern separates raw landing from conformed data from serving tables:

```text
bronze  raw append-only, Auto Loader, no business logic, keeps history
  |
silver  cleaned, deduplicated, typed, conformed keys; MERGE upserts
  |
gold    facts, dimensions, aggregates that BI and ML read
```

```python
# silver: dedupe raw events, then merge into a conformed table
from pyspark.sql import Window, functions as F

raw = spark.readStream.table("acme.bronze.orders_raw")

deduped = (
    raw.withWatermark("ingested_at", "2 hours")
    .dropDuplicates(["order_id"])
)

(
    deduped.writeStream
    .option("checkpointLocation", "/Volumes/acme/checkpoints/silver_orders")
    .trigger(availableNow=True)
    .foreachBatch(merge_into_silver)
    .toTable("acme.silver.orders")
)
```

Keep bronze immutable (replayability), put quality expectations in silver, and keep gold small enough for fast dashboard queries.

[Table of Contents](#Databricks)

## What are Lakeflow Declarative Pipelines (Delta Live Tables)?

Lakeflow Declarative Pipelines (formerly Delta Live Tables) let you declare datasets and expectations; the runtime handles dependency ordering, incremental processing, retries, and data-quality metrics.

```python
import dlt                      # older runtimes expose dlt; newer ones also expose pyspark.pipelines
from pyspark.sql import functions as F

@dlt.table(name="bronze_orders", comment="Raw orders from cloud storage")
def bronze_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/acme/dlt/orders_schema")
        .load("s3://acme-raw/orders/")
    )

@dlt.table(name="silver_orders")
@dlt.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dlt.expect_or_fail("valid_amount", "amount >= 0")
def silver_orders():
    return (
        dlt.read_stream("bronze_orders")
        .withColumn("order_date", F.to_date("order_ts"))
        .dropDuplicates(["order_id"])
    )
```

Interview points: expectations are declared with the table (not in a separate tool), `expect_or_drop` quarantines bad rows while `expect_or_fail` stops the pipeline, and both streaming tables and materialized views are supported.

[Table of Contents](#Databricks)

## How do you orchestrate jobs and workflows?

Databricks Workflows run multi-task DAGs with dependencies, schedules, triggers, retries, and alerts.

```python
# Jobs API: submit a task-based run (simplified)
import requests

payload = {
    "run_name": "daily-orders",
    "tasks": [
        {"task_key": "bronze", "notebook_task": {"notebook_path": "/Repos/prod/notebooks/bronze"}},
        {"task_key": "silver", "depends_on": [{"task_key": "bronze"}],
         "notebook_task": {"notebook_path": "/Repos/prod/notebooks/silver"}},
        {"task_key": "gold", "depends_on": [{"task_key": "silver"}],
         "sql_task": {"warehouse_id": "abc123", "query": {"query_id": "gold-refresh"}}},
    ],
    "schedule": {"quartz_cron_expression": "0 0 3 * * ?", "timezone_id": "UTC"},
    "max_concurrent_runs": 1,
}
requests.post("https://acme.cloud.databricks.com/api/2.1/jobs/create",
              headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=30)
```

Useful features to name: **file-arrival triggers**, **task values** for passing small results between tasks, **retry policies per task**, **job parameters**, **repair runs** (re-run only failed tasks), and **notifications** on failure or duration.

[Table of Contents](#Databricks)

## How do you manage Databricks resources as code?

Databricks Asset Bundles (DABs) package jobs, pipelines, notebooks, and config into a repo deployable with the CLI; Terraform manages workspace-level infrastructure.

```yaml
# databricks.yml
bundle: acme_lakehouse
workspace:
  host: https://acme.cloud.databricks.com
variables:
  catalog:
    default: acme_dev
resources:
  jobs:
    daily_orders:
      name: daily-orders-${bundle.target}
      schedule:
        quartz_cron_expression: "0 0 3 * * ?"
        timezone_id: UTC
      tasks:
        - task_key: bronze
          notebook_task:
            notebook_path: ./notebooks/bronze_orders.py
        - task_key: silver
          depends_on:
            - task_key: bronze
          notebook_task:
            notebook_path: ./notebooks/silver_orders.py
```

```bash
databricks bundle validate -t prod
databricks bundle deploy -t prod
databricks bundle run daily_orders -t prod
```

```hcl
# Terraform for workspace-level resources
resource "databricks_job" "daily_orders" {
  name = "daily-orders"
  task {
    task_key = "bronze"
    notebook_task { notebook_path = "/Repos/prod/notebooks/bronze" }
  }
}
```

[Table of Contents](#Databricks)

## How do you query data with Databricks SQL?

SQL warehouses are separate compute for SQL workloads, with serverless or classic sizing, auto-stop, and query federation to external systems.

```sql
-- cost and performance introspection from system tables
SELECT workspace_id, compute.warehouse_id AS warehouse_id,
       SUM(total_duration_ms) / 1000 AS seconds
FROM system.query.history
WHERE start_time >= current_date() - INTERVAL 7 DAYS
GROUP BY workspace_id, compute.warehouse_id
ORDER BY seconds DESC;

-- liquid clustering + maintenance on a gold table
ALTER TABLE acme.gold.fct_orders CLUSTER BY (order_date, customer_id);
OPTIMIZE acme.gold.fct_orders;
```

Also relevant: **Databricks SQL dashboards and alerts**, **query federation** to other databases, **materialized views** for repeated aggregations, and **Photon** as the default for SQL warehouses.

[Table of Contents](#Databricks)

## What is Photon and when does it help?

Photon is a vectorized C++ query engine that replaces the JVM execution path for supported operations in Spark and SQL workloads.

+ **Helps**: large scans, filters, joins, aggregations, Delta MERGE, SQL warehouses.
+ **Does not help**: Python UDFs and row-at-a-time code, which fall back to the slower path.
+ **Trade-off**: Photon clusters cost more per DBU but are often cheaper per job because they finish faster - validate with the query profile rather than assuming.

```text
Rule of interview thumb: replace Python UDFs with built-in functions, then measure;
Photon cannot rescue row-by-row Python.
```

[Table of Contents](#Databricks)

## How do you tune Delta tables on Databricks?

+ **File size** - target roughly 100 MB-1 GB per file; small files kill scans and metadata.
+ **Liquid clustering** - the current recommended layout strategy: `CLUSTER BY (order_date, customer_id)` lets Databricks manage file layout incrementally and supports changing the keys.
+ **Partitioning** - still valid when a low-cardinality column is always filtered (`date`), but avoid over-partitioning; do not combine manual partitioning with clustering on the same table.
+ **ZORDER** - legacy co-location technique; still works, but liquid clustering is preferred for new tables.
+ **OPTIMIZE / VACUUM** - compact files and reclaim space; VACUUM cannot go inside the time-travel retention window.
+ **Predictive optimization** - Databricks can run OPTIMIZE/VACUUM/ANALYZE automatically for eligible tables.

```sql
ALTER TABLE acme.silver.orders CLUSTER BY (order_date, customer_id);
OPTIMIZE acme.silver.orders;
VACUUM acme.silver.orders RETAIN 168 HOURS;
ANALYZE TABLE acme.silver.orders COMPUTE STATISTICS FOR ALL COLUMNS;
```

[Table of Contents](#Databricks)

## How do you handle schema evolution and Change Data Feed?

```sql
-- merge schema on ingest for new columns
SET spark.databricks.delta.schema.autoMerge.enabled = true;

-- change data feed lets downstream jobs read only changed rows
ALTER TABLE acme.silver.orders SET TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

SELECT order_id, _change_type, _commit_version, order_ts, amount
FROM table_changes('acme.silver.orders', 100)
WHERE _change_type IN ('insert', 'update_postimage');
```

Rules that prevent incidents: add columns as nullable, never reuse a column name for a new meaning, and treat renames as migrations (backfill plus view) rather than schema evolution.

[Table of Contents](#Databricks)

## How do you implement CI/CD for Databricks?

```text
1. Repos: notebooks and jobs live in Git (Databricks Repos or external CI checkout).
2. Validate: databricks bundle validate in each PR; run unit tests with pytest on pure PySpark transforms.
3. Deploy: databricks bundle deploy -t staging|prod from CI, promoting the same artifact.
4. Test on real data: run the job against a staging catalog, then compare row counts and business metrics.
5. Guardrails: Unity Catalog grants, job permissions, and cluster policies are code, reviewed like application code.
```

Key practices: keep transformation logic in importable Python modules under test, parameterize catalogs per environment, and never point CI at the production catalog.

[Table of Contents](#Databricks)

## What security and access-mode concepts matter?

+ **Access modes** - dedicated (formerly single-user), standard (formerly shared), and serverless; the mode determines which Spark features and languages are available and how users are isolated.
+ **Identity** - users, groups, service principals, and managed identities for jobs; avoid personal access tokens in production.
+ **Secrets** - Databricks secret scopes backed by Key Vault/Secrets Manager; never put credentials in notebooks or cluster env vars.
+ **Network** - private link/VNet injection, IP access lists, and no-public-IP clusters for regulated environments.
+ **Audit** - `system.access.audit` records who read, wrote, or changed what.

[Table of Contents](#Databricks)

## How do you control Databricks cost?

```sql
-- top spend by SKU and workspace, from the billing system table
SELECT usage_date, sku_name, SUM(usage_quantity) AS dbus
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 30 DAYS
GROUP BY usage_date, sku_name
ORDER BY dbus DESC;
```

Levers that actually move the bill:

+ Job clusters with auto-termination instead of idle all-purpose clusters.
+ Spot instances with fallback for batch, plus autoscaling ranges that reflect real need.
+ Photon and liquid clustering to finish jobs sooner (DBUs are time-based).
+ Right-sized SQL warehouses and auto-stop; separate warehouses per workload instead of one giant one.
+ Serverless for bursty jobs where cluster startup would otherwise dominate.
+ Tag clusters/jobs by team and cost center, then review the top 20 spenders monthly.

[Table of Contents](#Databricks)

## How does Databricks compare with Snowflake and BigQuery?

| Aspect | Databricks | Snowflake | BigQuery |
|---|---|---|---|
| Engine | Spark + Photon, plus SQL warehouses | proprietary SQL engine | serverless SQL engine |
| Table format | Delta (and Iceberg) on your storage | Snowflake-managed micro-partitions (Iceberg tables available) | BigQuery-managed storage (BigLake/Iceberg available) |
| Strength | large-scale Spark/ML, notebooks, streaming, open formats | SQL analytics, ease of use, governed sharing | serverless simplicity, tight GCP integration |
| Cost model | DBUs + cloud VM/storage | credits + storage | on-demand/edition slots + storage |
| Governance | Unity Catalog | native RBAC + policies | IAM + Dataplex/policy tags |

The honest interview answer: choose Databricks when Spark-scale engineering, streaming, ML, and open table formats matter; choose Snowflake or BigQuery when the workload is mostly SQL analytics and managed simplicity wins. Many companies run two of the three.

[Table of Contents](#Databricks)

## How do you migrate from on-prem Spark and Hive?

+ **Storage first** - copy HDFS/Hive data to object storage (DistCp, cloud transfer service), then register it as external Delta/Iceberg tables or migrate in place.
+ **Metastore** - move Hive metastore objects into Unity Catalog; use the migration tooling to upgrade tables to Delta and fix unsupported types.
+ **Code** - replace `hive`-specific SQL with Spark SQL equivalents, remove `HiveContext`, and convert Python UDFs to built-in functions.
+ **Jobs** - port Oozie/Airflow DAGs to Databricks Workflows or keep Airflow and call Databricks jobs via the operator.
+ **Validate** - compare row counts and checksums between old and new tables, then run both paths in parallel for a period before cutover.

[Table of Contents](#Databricks)

## What is MLflow and how is it used on Databricks?

MLflow tracks experiments, packages models, and manages a model registry. On Databricks it is integrated with the workspace and Unity Catalog.

```python
import mlflow
import mlflow.sklearn

mlflow.set_registry_uri("databricks-uc")

with mlflow.start_run(run_name="churn-baseline"):
    mlflow.log_params({"max_depth": 8, "n_estimators": 200})
    mlflow.log_metric("auc", 0.912)
    mlflow.sklearn.log_model(model, artifact_path="model",
                             registered_model_name="acme.ml.churn_classifier")
```

Data-engineer relevance: feature tables built with Spark feed training jobs; the same features should be served online from a low-latency store, which is why feature consistency and point-in-time correctness come up in interviews.

[Table of Contents](#Databricks)

## What are common Databricks interview traps?

+ Saying "Databricks is just hosted Spark" - it also includes Delta, Unity Catalog, workflows, SQL warehouses, and governance.
+ Running production pipelines on an all-purpose cluster.
+ Using `collect()` or `toPandas()` on large data and blaming the cluster.
+ Calling Python UDFs on huge datasets and expecting Photon to fix it.
+ Over-partitioning a Delta table, then wondering why the file listing is slow.
+ Confusing `VACUUM` retention with time travel: vacuuming inside the retention window breaks time travel.
+ Forgetting that Unity Catalog changes the namespace to three levels, so old two-level paths stop working.
+ Assuming autoscaling fixes skew - it cannot split a single hot partition.

[Table of Contents](#Databricks)

## Real world use cases for Databricks

### 1. Retail lakehouse: raw events to executive dashboards

```text
S3 raw JSON -> Auto Loader (bronze) -> dedupe/type (silver) -> fct/dim (gold) -> SQL warehouse dashboards
```

```python
@dlt.table(name="gold_daily_revenue")
def gold_daily_revenue():
    return (
        dlt.read("silver_orders")
        .groupBy("order_date", "country")
        .agg(F.sum("amount").alias("revenue"), F.count("*").alias("orders"))
    )
```

Why Databricks: one pipeline feeds BI and data science, Delta gives ACID merges and time travel, and Unity Catalog keeps PII governed with masks and row filters.

### 2. Streaming CDC from operational databases

Debezium/Kafka lands change events; a streaming job merges them into Delta silver tables for near-real-time reporting.

```python
(
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "cdc.public.orders")
    .load()
    .select(F.from_json(F.col("value").cast("string"), order_schema).alias("o"))
    .select("o.*")
    .writeStream
    .option("checkpointLocation", "/Volumes/acme/checkpoints/cdc_orders")
    .trigger(processingTime="1 minute")
    .foreachBatch(merge_into_silver)
    .start()
)
```

Why Databricks: structured streaming plus Delta MERGE gives exactly-once ingestion with upserts and deletes in the same platform as batch.

### 3. Migrating an on-prem Hive warehouse

Terabytes of Hive tables move to ADLS/S3, are upgraded to Delta, and Oozie jobs become Databricks Workflows.

Why Databricks: the Spark migration path is direct, Unity Catalog replaces Hive metastore governance, and liquid clustering plus Photon usually beats the old cluster.

### 4. Machine-learning platform with one feature definition

Feature tables in Delta are built nightly, registered in Unity Catalog, and consumed by MLflow-tracked training jobs; serving reads the same features from an online store.

Why Databricks: one governed copy of data, lineage from table to model, and MLflow integrated with the same catalog.

### 5. Cost-optimization program for an existing workspace

The platform team moves all scheduled work to job clusters with spot fallback, enables Photon and liquid clustering on hot tables, rightsizes SQL warehouses, and reviews `system.billing.usage` monthly by cost-center tag.

Why Databricks: cost is controllable when workload isolation, cluster policy, and table layout are treated as engineering, not afterthoughts.

[Table of Contents](#Databricks)
