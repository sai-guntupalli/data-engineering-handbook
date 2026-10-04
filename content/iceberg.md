## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Iceberg
+ [What is Apache Iceberg?](#What-is-Apache-Iceberg)
+ [How do you enable Iceberg in PySpark?](#How-do-you-enable-Iceberg-in-PySpark)
+ [How do you create and write to an Iceberg table in PySpark?](#How-do-you-create-and-write-to-an-Iceberg-table-in-PySpark)
+ [How does Iceberg improve data lake table management?](#How-does-Iceberg-improve-data-lake-table-management)
+ [What problems does Iceberg solve compared to plain Parquet datasets?](#What-problems-does-Iceberg-solve-compared-to-plain-Parquet-datasets)
+ [What is hidden partitioning in Iceberg and how do you enable it in PySpark?](#What-is-hidden-partitioning-in-Iceberg-and-how-do-you-enable-it-in-PySpark)
+ [What is partition evolution and how do you change partitions in PySpark?](#What-is-partition-evolution-and-how-do-you-change-partitions-in-PySpark)
+ [How does schema evolution work and how do you apply it in PySpark?](#How-does-schema-evolution-work-and-how-do-you-apply-it-in-PySpark)
+ [What is a snapshot in Iceberg and how do you inspect it in PySpark?](#What-is-a-snapshot-in-Iceberg-and-how-do-you-inspect-it-in-PySpark)
+ [What is time travel and how do you use it in PySpark?](#What-is-time-travel-and-how-do-you-use-it-in-PySpark)
+ [How does Iceberg handle concurrent writes?](#How-does-Iceberg-handle-concurrent-writes)
+ [What are equality deletes and positional deletes, and how do you use deletes in PySpark?](#What-are-equality-deletes-and-positional-deletes-and-how-do-you-use-deletes-in-PySpark)
+ [How do upserts and merges work with Iceberg in PySpark?](#How-do-upserts-and-merges-work-with-Iceberg-in-PySpark)
+ [Why does the small files problem happen and how do you mitigate it in PySpark?](#Why-does-the-small-files-problem-happen-and-how-do-you-mitigate-it-in-PySpark)
+ [What maintenance operations are common for Iceberg tables in PySpark?](#What-maintenance-operations-are-common-for-Iceberg-tables-in-PySpark)
+ [What is an Iceberg catalog and how do you configure one for PySpark?](#What-is-an-Iceberg-catalog-and-how-do-you-configure-one-for-PySpark)
+ [How would you migrate an existing Parquet dataset to Iceberg with PySpark?](#How-would-you-migrate-an-existing-Parquet-dataset-to-Iceberg-with-PySpark)
+ [Iceberg vs Delta Lake: what is the difference with examples?](#Iceberg-vs-Delta-Lake-what-is-the-difference-with-examples)
+ [How do you make a Delta table Iceberg-compatible?](#How-do-you-make-a-Delta-table-Iceberg-compatible)
+ [How do you access a PySpark-created Iceberg table in Snowflake?](#How-do-you-access-a-PySpark-created-Iceberg-table-in-Snowflake)
+ [Iceberg vs Delta vs Hudi: when would you choose Iceberg?](#Iceberg-vs-Delta-vs-Hudi-when-would-you-choose-Iceberg)
+ [Real world use cases for Apache Iceberg](#Real-world-use-cases-for-Apache-Iceberg)

## What is Apache Iceberg?
Apache Iceberg is an open table format for large analytical datasets. It is not a compute engine by itself. PySpark, Spark SQL, Flink, Trino, Snowflake, and other engines use Iceberg metadata to read and write the same table consistently.

In a PySpark data platform, the usual shape is:

```text
PySpark job -> Iceberg catalog -> Iceberg table metadata -> Parquet files in S3/GCS/ADLS/HDFS
```

Iceberg manages table metadata, snapshots, manifests, schema evolution, partition evolution, row-level deletes, and transaction commits. The data files are commonly Parquet.

Real-world example: a Databricks PySpark job writes `main.analytics.orders` every hour, Trino or another Iceberg REST client serves ad-hoc SQL, and Snowflake reads the same Unity Catalog-managed Iceberg table for BI. Iceberg is the shared table layer that makes that possible.

[Table of Contents](#Apache-Iceberg)

## How do you enable Iceberg in PySpark?
In Databricks with Unity Catalog enabled, you normally do not manually configure a Spark catalog for day-to-day PySpark notebooks/jobs. You use Unity Catalog's three-level namespace:

```text
catalog.schema.table
```

Example:

```python
spark.sql("create schema if not exists main.analytics")

orders = spark.table("main.analytics.orders")
```

If your Databricks workspace supports Unity Catalog-managed Iceberg tables, create Iceberg tables directly in Unity Catalog:

```python
spark.sql("""
create table if not exists main.analytics.orders (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  status string,
  amount decimal(12, 2)
) using iceberg
""")
```

Outside Databricks, or when connecting external Spark to Unity Catalog, you configure the Iceberg REST catalog endpoint for Unity Catalog. That is an interoperability setup; inside Databricks, prefer native Unity Catalog table names like `main.analytics.orders`.

[Table of Contents](#Apache-Iceberg)

## How do you create and write to an Iceberg table in PySpark?
Use `spark.sql` for table DDL and PySpark DataFrameWriterV2 (`writeTo`) for table-aware writes.

Create a schema and table:

```python
spark.sql("create schema if not exists main.analytics")

spark.sql("""
create table if not exists main.analytics.orders (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  status string,
  amount decimal(12, 2)
) using iceberg
partitioned by (days(order_ts))
""")
```

Append a DataFrame:

```python
from pyspark.sql import functions as F

orders_df = (
    spark.read.json("s3://company-raw/orders/ds=2026-10-04/")
    .select(
        F.col("order_id").cast("bigint"),
        F.col("customer_id").cast("bigint"),
        F.col("order_ts").cast("timestamp"),
        F.col("status").cast("string"),
        F.col("amount").cast("decimal(12,2)"),
    )
)

orders_df.writeTo("main.analytics.orders").append()
```

Overwrite a single business day safely:

```python
(
    orders_df
    .writeTo("main.analytics.orders")
    .overwrite(
        "order_ts >= timestamp '2026-10-04 00:00:00' "
        "and order_ts < timestamp '2026-10-05 00:00:00'"
    )
)
```

Interview point: `writeTo` is preferred over path-based writes because it writes through the Iceberg table abstraction and participates in Iceberg commits.

[Table of Contents](#Apache-Iceberg)

## How does Iceberg improve data lake table management?
Plain object storage has files, but not table semantics. Iceberg adds metadata so PySpark can plan queries from table metadata instead of recursively listing directories and guessing table state.

Inspect metadata from PySpark:

```python
spark.table("main.analytics.orders.snapshots").show(truncate=False)
spark.table("main.analytics.orders.files").select(
    "file_path", "record_count", "file_size_in_bytes"
).show(truncate=False)
spark.table("main.analytics.orders.history").show(truncate=False)
```

Real-world example: if a PySpark write job fails halfway through, readers still see the last committed snapshot. The failed job may leave orphan files, but those files are not visible as table data until a successful Iceberg commit references them.

[Table of Contents](#Apache-Iceberg)

## What problems does Iceberg solve compared to plain Parquet datasets?
A plain Parquet dataset usually relies on folder layout and conventions. This causes problems with partial writes, concurrent jobs, schema changes, partition changes, deletes, updates, and slow file listing.

Path-based Parquet read:

```python
plain_orders = spark.read.parquet("s3://company-lake/orders/")
```

Iceberg table read:

```python
iceberg_orders = spark.table("main.analytics.orders")
```

With Iceberg, PySpark asks the catalog and Iceberg metadata which files belong to the current snapshot. With plain Parquet, Spark mostly sees files and folders. That difference matters when multiple jobs update the same dataset.

[Table of Contents](#Apache-Iceberg)

## What is hidden partitioning in Iceberg and how do you enable it in PySpark?
Hidden partitioning means users filter on logical columns, while Iceberg stores partition transforms in table metadata. You enable it with partition transforms in table DDL.

Create a table partitioned by day of `event_ts`:

```python
spark.sql("""
create table if not exists main.analytics.events (
  event_id string,
  user_id string,
  event_ts timestamp,
  event_type string
) using iceberg
partitioned by (days(event_ts))
""")
```

Query using the original timestamp column:

```python
daily_counts = (
    spark.table("main.analytics.events")
    .where(
        (F.col("event_ts") >= F.lit("2026-10-04 00:00:00").cast("timestamp"))
        & (F.col("event_ts") < F.lit("2026-10-05 00:00:00").cast("timestamp"))
    )
    .groupBy("event_type")
    .count()
)
```

You do not need to create or filter on a separate `event_date` folder column. Iceberg maps the timestamp filter to the `days(event_ts)` transform and prunes files.

Other useful transforms:

```python
spark.sql("""
create table if not exists main.analytics.customer_events (
  event_id string,
  customer_id string,
  region string,
  event_ts timestamp
) using iceberg
partitioned by (
  days(event_ts),
  bucket(32, customer_id),
  truncate(8, region)
)
""")
```

Real-world choice:

+ `days(order_ts)`: common daily reporting and backfills
+ `bucket(32, customer_id)`: frequent customer-keyed deletes, joins, or merges
+ `truncate(8, region)`: prefix-style grouping for string fields with many values

[Table of Contents](#Apache-Iceberg)

## What is partition evolution and how do you change partitions in PySpark?
Partition evolution lets you change the partition spec for new data without rewriting all old files. Historical files keep their old partition spec; new files use the new spec.

Add a bucket partition:

```python
spark.sql("""
alter table main.analytics.orders
add partition field bucket(32, customer_id)
""")
```

Drop a partition field for future writes:

```python
spark.sql("""
alter table main.analytics.orders
drop partition field days(order_ts)
""")
```

Then continue writing normally:

```python
new_orders_df.writeTo("main.analytics.orders").append()
```

Important: altering the partition spec does not rewrite old data. If you want old files to be physically reorganized with the new spec from an external Spark Iceberg client, run a rewrite/compaction job. The example below assumes your external Spark catalog alias is `uc` and its warehouse is the Unity Catalog catalog `main`.

```python
spark.sql("""
call uc.system.rewrite_data_files(
  table => 'analytics.orders'
)
""")
```

Real-world workflow: identify slow queries, change the partition spec, monitor new writes, then rewrite older data only if the performance gain is worth the cost.

[Table of Contents](#Apache-Iceberg)

## How does schema evolution work and how do you apply it in PySpark?
Iceberg tracks columns by stable field IDs, not only names. This makes add, drop, rename, and compatible type changes safer than unmanaged Parquet.

Add a column:

```python
spark.sql("alter table main.analytics.orders add column currency string")
```

Rename a column:

```python
spark.sql("alter table main.analytics.orders rename column amount to gross_amount")
```

Change a compatible type:

```python
spark.sql("""
alter table main.analytics.orders
alter column gross_amount type decimal(18, 2)
""")
```

Drop a column:

```python
spark.sql("alter table main.analytics.orders drop column currency")
```

Read after schema evolution:

```python
orders = spark.table("main.analytics.orders")
orders.printSchema()
```

Interview guidance: additive columns are usually safest. Renames are safer in Iceberg than path-based Parquet, but downstream BI tools, dbt models, and notebooks still need to handle the new name.

[Table of Contents](#Apache-Iceberg)

## What is a snapshot in Iceberg and how do you inspect it in PySpark?
A snapshot is a committed table version. Every successful append, overwrite, merge, delete, or schema change creates a new table state.

Inspect snapshots:

```python
snapshots = spark.table("main.analytics.orders.snapshots")
snapshots.select("committed_at", "snapshot_id", "operation", "summary").show(truncate=False)
```

Inspect history:

```python
spark.table("main.analytics.orders.history").orderBy(F.desc("made_current_at")).show(truncate=False)
```

Inspect files in the current table:

```python
spark.table("main.analytics.orders.files").select(
    "content", "file_path", "record_count", "file_size_in_bytes"
).show(truncate=False)
```

Real-world use: after a bad PySpark deployment, find the snapshot from before the deployment and compare row counts or metrics.

[Table of Contents](#Apache-Iceberg)

## What is time travel and how do you use it in PySpark?
Time travel queries a table as it existed at a previous snapshot or timestamp. Use it for debugging, audits, regression checks, and reproducing reports.

Read by snapshot ID:

```python
old_orders = (
    spark.read
    .option("snapshot-id", "1234567890123456789")
    .format("iceberg")
    .load("main.analytics.orders")
)
```

Read by timestamp:

```python
orders_as_of = (
    spark.read
    .option("as-of-timestamp", "1791098400000")
    .format("iceberg")
    .load("main.analytics.orders")
)
```

Compare old and current statuses:

```python
current_orders = spark.table("main.analytics.orders").select("order_id", "status")
old_orders = old_orders.select(
    "order_id",
    F.col("status").alias("old_status"),
)

changed = (
    current_orders.alias("c")
    .join(old_orders.alias("o"), "order_id")
    .where(F.col("c.status") != F.col("o.old_status"))
)
```

Operational note: time travel only works while old snapshots and files are retained. If maintenance expires old snapshots and removes old files, very old versions are no longer queryable.

[Table of Contents](#Apache-Iceberg)

## How does Iceberg handle concurrent writes?
Iceberg uses optimistic concurrency control. A writer plans changes from a base snapshot, writes new files, then tries to commit new metadata. If another writer committed a conflicting change first, the commit fails or retries instead of silently corrupting the table.

Example scenario:

```text
PySpark job A reads snapshot 10 and prepares append
PySpark job B reads snapshot 10 and commits snapshot 11
PySpark job A attempts commit; Iceberg checks whether A can safely commit on top of snapshot 11
```

Practical PySpark guidance:

+ keep batch jobs partition-scoped where possible
+ avoid two jobs rewriting the same table partition at the same time
+ make merge jobs idempotent
+ retry commit conflicts at the orchestration layer when safe
+ compact after heavy updates/deletes

For append-only workloads, retries are usually easier. For overlapping `merge`, `delete`, and overwrite workloads, conflicts are more likely.

[Table of Contents](#Apache-Iceberg)

## What are equality deletes and positional deletes, and how do you use deletes in PySpark?
Iceberg supports row-level deletes by writing delete files instead of immediately rewriting every affected data file.

+ Equality deletes mark rows as deleted based on column values, such as `order_id = 1001`.
+ Positional deletes mark specific row positions in specific data files.

Most PySpark users do not manually create delete files. They use SQL commands or `MERGE INTO`, and the engine writes the appropriate Iceberg files.

Delete old cancelled orders:

```python
spark.sql("""
delete from main.analytics.orders
where status = 'cancelled'
  and order_ts < timestamp '2026-01-01 00:00:00'
""")
```

Delete a customer for a privacy request:

```python
customer_id = "C123"
spark.sql(f"""
delete from main.analytics.customer_events
where customer_id = '{customer_id}'
""")
```

Configure merge-on-read delete/update behavior:

```python
spark.sql("""
alter table main.analytics.orders
set tblproperties (
  'write.delete.mode' = 'merge-on-read',
  'write.update.mode' = 'merge-on-read',
  'write.merge.mode' = 'merge-on-read'
)
""")
```

Operational note: merge-on-read can make writes faster, but many delete files can slow reads. Follow heavy delete/update workloads with compaction.

[Table of Contents](#Apache-Iceberg)

## How do upserts and merges work with Iceberg in PySpark?
Use `MERGE INTO` from PySpark through `spark.sql`. Deduplicate CDC input first so each target key has one winning source record.

Deduplicate CDC input:

```python
from pyspark.sql.window import Window

cdc = spark.table("main.bronze.orders_cdc")

window = Window.partitionBy("order_id").orderBy(
    F.col("source_lsn").desc(),
    F.col("ingested_at").desc(),
)

deduped = (
    cdc
    .withColumn("rn", F.row_number().over(window))
    .where(F.col("rn") == 1)
    .drop("rn")
)

deduped.createOrReplaceTempView("orders_cdc_deduped")
```

Merge into the Iceberg table:

```python
spark.sql("""
merge into main.analytics.orders as target
using orders_cdc_deduped as source
on target.order_id = source.order_id
when matched and source.op = 'D' then delete
when matched then update set
  customer_id = source.customer_id,
  order_ts = source.order_ts,
  status = source.status,
  amount = source.amount
when not matched and source.op <> 'D' then insert (
  order_id, customer_id, order_ts, status, amount
) values (
  source.order_id, source.customer_id, source.order_ts, source.status, source.amount
)
""")
```

Real-world guidance:

+ merge on stable business keys
+ dedupe CDC input before merge
+ include delete/tombstone logic
+ compact after large merge jobs
+ monitor both data files and delete files

[Table of Contents](#Apache-Iceberg)

## Why does the small files problem happen and how do you mitigate it in PySpark?
Small files happen when many jobs write small batches, streaming jobs commit frequently, partitioning is too granular, or Spark uses too many writer tasks.

Set target file size:

```python
spark.sql("""
alter table main.analytics.orders
set tblproperties (
  'write.target-file-size-bytes' = '536870912'
)
""")
```

Control write parallelism before append:

```python
(
    orders_df
    .repartition(32, F.to_date("order_ts"))
    .writeTo("main.analytics.orders")
    .append()
)
```

Compact small files:

```python
spark.sql("""
call uc.system.rewrite_data_files(
  table => 'analytics.orders',
  options => map('target-file-size-bytes', '536870912')
)
""")
```

Interview answer: prevention is better than cleanup. Choose sane partitioning, batch enough data per commit, and tune Spark writer parallelism.

[Table of Contents](#Apache-Iceberg)

## What maintenance operations are common for Iceberg tables in PySpark?
Iceberg tables need periodic maintenance after streaming writes, merges, deletes, and frequent schema/partition changes.

The examples below assume an external Spark Iceberg REST catalog alias named `uc` pointed at the Unity Catalog catalog `main`. If you are running directly inside Databricks, use the platform-supported maintenance commands and policies for your table type/runtime.

Compact data files:

```python
spark.sql("""
call uc.system.rewrite_data_files(
  table => 'analytics.orders'
)
""")
```

Rewrite manifests:

```python
spark.sql("""
call uc.system.rewrite_manifests(
  table => 'analytics.orders'
)
""")
```

Expire old snapshots:

```python
spark.sql("""
call uc.system.expire_snapshots(
  table => 'analytics.orders',
  older_than => timestamp '2026-09-01 00:00:00',
  retain_last => 10
)
""")
```

Remove orphan files:

```python
spark.sql("""
call uc.system.remove_orphan_files(
  table => 'analytics.orders',
  older_than => timestamp '2026-09-01 00:00:00'
)
""")
```

Real-world schedule:

+ compact high-write tables daily or hourly depending on volume
+ expire snapshots after the required rollback/audit period
+ remove orphan files carefully after confirming no active jobs need them
+ monitor metadata size, file counts, and planning latency

[Table of Contents](#Apache-Iceberg)

## What is an Iceberg catalog and how do you configure one for PySpark?
An Iceberg catalog stores namespaces and the pointer to each table's current metadata file. It is how PySpark finds and commits to tables.

In Databricks, Unity Catalog is the default recommended catalog for governed Delta and Iceberg tables. You use three-part names:

```text
main.analytics.orders
prod_lake.finance.fact_revenue
```

Create and use a Unity Catalog schema/table from PySpark:

```python
spark.sql("create schema if not exists main.analytics")

spark.sql("""
create table if not exists main.analytics.orders (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  amount decimal(12, 2)
) using iceberg
""")
```

For external Iceberg-compatible engines, Unity Catalog exposes an Iceberg REST catalog interface. A non-Databricks Spark job connecting through that REST interface would use Spark catalog configuration similar to:

```python
spark = (
    SparkSession.builder
    .config("spark.sql.catalog.uc", "org.apache.iceberg.spark.SparkCatalog")
    .config("spark.sql.catalog.uc.type", "rest")
    .config("spark.sql.catalog.uc.uri", "https://<databricks-workspace>/api/2.1/unity-catalog/iceberg-rest")
    .config("spark.sql.catalog.uc.rest.auth.type", "oauth2")
    .config("spark.sql.catalog.uc.oauth2-server-uri", "https://<databricks-workspace>/oidc/v1/token")
    .config("spark.sql.catalog.uc.credential", "<oauth-client-id>:<oauth-client-secret>")
    .config("spark.sql.catalog.uc.warehouse", "main")
    .config("spark.sql.catalog.uc.scope", "all-apis")
    .getOrCreate()
)
```

Other catalog choices still exist, such as Hive metastore, AWS Glue, Apache Polaris, Hadoop catalog, REST catalog, and Nessie. But if your platform is Databricks-centered, use Unity Catalog first because it centralizes governance, permissions, lineage, and external Iceberg REST access.

Interview point: catalog choice affects authorization, interoperability, disaster recovery, and how many engines can safely share the same tables.

[Table of Contents](#Apache-Iceberg)

## How would you migrate an existing Parquet dataset to Iceberg with PySpark?
The safest approach is usually to create a new Iceberg table and rewrite the data into it. This lets you enforce schema, clean bad records, and choose partitioning deliberately.

Read legacy Parquet:

```python
legacy = spark.read.parquet("s3://company-lake/legacy/orders/")
```

Create the Iceberg target:

```python
spark.sql("""
create table if not exists main.analytics.orders_iceberg (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  status string,
  amount decimal(12, 2)
) using iceberg
partitioned by (days(order_ts))
""")
```

Clean and write:

```python
cleaned = legacy.select(
    F.col("order_id").cast("bigint"),
    F.col("customer_id").cast("bigint"),
    F.col("order_ts").cast("timestamp"),
    F.col("status").cast("string"),
    F.col("amount").cast("decimal(12,2)"),
)

cleaned.writeTo("main.analytics.orders_iceberg").append()
```

Validate:

```python
legacy_count = legacy.count()
iceberg_count = spark.table("main.analytics.orders_iceberg").count()

legacy_amount = legacy.select(F.sum("amount")).first()[0]
iceberg_amount = spark.table("main.analytics.orders_iceberg").select(F.sum("amount")).first()[0]
```

Cutover strategy:

+ backfill historical data into Iceberg
+ validate row counts, sums, keys, and sample records
+ pause or dual-write source ingestion briefly
+ apply incremental changes
+ switch readers to the Iceberg table
+ keep the old dataset read-only until confidence is high

[Table of Contents](#Apache-Iceberg)

## Iceberg vs Delta Lake: what is the difference with examples?
Iceberg and Delta Lake both make data lake tables more reliable than plain Parquet, but they make different ecosystem and interoperability trade-offs.

Create the same orders table as Iceberg:

```python
spark.sql("""
create table if not exists main.analytics.orders_iceberg (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  amount decimal(12, 2)
) using iceberg
partitioned by (days(order_ts))
""")

orders_df.writeTo("main.analytics.orders_iceberg").append()
```

Create the same orders table as Delta:

```python
(
    orders_df
    .write
    .format("delta")
    .mode("append")
    .partitionBy("order_date")
    .save("s3://company-lake/delta/orders")
)
```

Key practical differences:

+ Iceberg focuses on open, multi-engine table interoperability with hidden partitioning and strong partition evolution.
+ Delta Lake is deeply integrated with the Delta/Databricks ecosystem and has mature Delta-specific optimization features.
+ Iceberg partitioning is metadata-driven, so users can filter `order_ts` while Iceberg prunes `days(order_ts)`.
+ Traditional Delta partitioning often exposes physical partition columns like `order_date`, though Delta UniForm can expose Delta tables to Iceberg readers.

Example interview answer:

```text
If Spark writes the table, Trino reads it, Snowflake also needs access, and the organization wants an open table format across engines, Iceberg is a strong fit.

If the organization is standardized on Databricks/Delta Live Tables and most readers are Delta-native, Delta may be simpler operationally.
```

[Table of Contents](#Apache-Iceberg)

## How do you make a Delta table Iceberg-compatible?
The common modern approach is Delta UniForm, which lets a Delta table generate Iceberg-compatible metadata so Iceberg readers can read it. The Delta table remains a Delta table; Iceberg clients should treat it as read-only unless your platform explicitly supports more.

Create or alter a Delta table with UniForm enabled from PySpark:

```python
spark.sql("""
create table if not exists delta.`s3://company-lake/delta/orders_uniform` (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  order_date date,
  amount decimal(12, 2)
) using delta
tblproperties (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg'
)
partitioned by (order_date)
""")
```

Or enable it on an existing Delta table:

```python
spark.sql("""
alter table delta.`s3://company-lake/delta/orders_uniform`
set tblproperties (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg'
)
""")
```

Write data normally as Delta:

```python
(
    orders_df
    .withColumn("order_date", F.to_date("order_ts"))
    .write
    .format("delta")
    .mode("append")
    .save("s3://company-lake/delta/orders_uniform")
)
```

What happens next:

+ Delta remains the source of truth.
+ UniForm asynchronously generates Iceberg-compatible metadata.
+ Iceberg engines can read the table using the generated Iceberg metadata.
+ Do not assume Iceberg writers can safely mutate the table; treat Iceberg access as read-oriented unless your vendor/runtime explicitly supports otherwise.

If you need a true native Iceberg table instead of a Delta table exposed as Iceberg, rewrite the Delta table into Iceberg:

```python
delta_orders = spark.read.format("delta").load("s3://company-lake/delta/orders_uniform")

spark.sql("""
create table if not exists main.analytics.orders_iceberg (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  order_date date,
  amount decimal(12, 2)
) using iceberg
partitioned by (days(order_ts))
""")

delta_orders.writeTo("main.analytics.orders_iceberg").append()
```

[Table of Contents](#Apache-Iceberg)

## How do you access a PySpark-created Iceberg table in Snowflake?
A typical pattern is:

1. Databricks PySpark writes an Iceberg table registered in Unity Catalog.
2. A Databricks service principal is granted access to the Unity Catalog catalog/schema/table.
3. Snowflake creates an Iceberg REST catalog integration that points to the Databricks Unity Catalog Iceberg REST endpoint.
4. Snowflake creates a catalog-linked database that syncs Unity Catalog namespaces and Iceberg tables.
5. Snowflake queries the Iceberg table without copying the data.

Databricks PySpark side: create a Unity Catalog-managed Iceberg table:

```python
spark.sql("create schema if not exists main.analytics")

spark.sql("""
create table if not exists main.analytics.orders (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  amount decimal(12, 2)
) using iceberg
partitioned by (days(order_ts))
""")

orders_df.writeTo("main.analytics.orders").append()
```

Databricks permissions side: grant the Snowflake service principal the relevant Unity Catalog privileges. The exact principal name depends on how your Databricks service principal is represented.

```sql
GRANT USE CATALOG ON CATALOG main TO `<application_id>`;
GRANT USE SCHEMA ON SCHEMA main.analytics TO `<application_id>`;
GRANT EXTERNAL USE SCHEMA ON SCHEMA main.analytics TO `<application_id>`;
GRANT SELECT ON TABLE main.analytics.orders TO `<application_id>`;
```

Snowflake side: create a catalog integration that connects to the Databricks Unity Catalog Iceberg REST endpoint:

```sql
CREATE OR REPLACE CATALOG INTEGRATION databricks_uc_iceberg
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<databricks-workspace-url>/api/2.1/unity-catalog/iceberg-rest'
    CATALOG_NAME = 'main'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_TOKEN_URI = 'https://<databricks-workspace-url>/oidc/v1/token'
    OAUTH_CLIENT_ID = '<databricks-service-principal-application-id>'
    OAUTH_CLIENT_SECRET = '<databricks-service-principal-secret>'
    OAUTH_ALLOWED_SCOPES = ('all-apis')
  )
  ENABLED = TRUE;
```

Then create a catalog-linked database:

```sql
CREATE DATABASE databricks_uc
  LINKED_CATALOG = (
    CATALOG = 'databricks_uc_iceberg'
    BLOCKED_NAMESPACES = ('information_schema')
  );
```

After sync, Snowflake exposes Unity Catalog schemas and Iceberg tables under the linked database. For example, `main.analytics.orders` in Unity Catalog can appear under the Snowflake catalog-linked database as an `analytics.orders` table, depending on the sync and naming configuration.

Important operational points:

+ PySpark and Snowflake must point to the same Unity Catalog Iceberg table metadata.
+ With catalog-vended credentials, Unity Catalog can provide Snowflake temporary scoped credentials to access the underlying data.
+ Keep ownership clear. If Databricks owns writes, treat Snowflake primarily as a reader unless you intentionally configure bidirectional/write access.
+ Grant only the Unity Catalog privileges Snowflake needs.
+ Run table maintenance from the owning platform so metadata, snapshots, and data files stay healthy.

[Table of Contents](#Apache-Iceberg)

## Iceberg vs Delta vs Hudi: when would you choose Iceberg?
Choose Iceberg when you need an open, engine-neutral table format with strong metadata handling, hidden partitioning, partition evolution, schema evolution, time travel, and multi-engine access.

Example strong Iceberg fit:

```text
PySpark writes curated tables
Trino serves ad-hoc queries
Snowflake reads selected tables for BI
Flink writes streaming updates
Data lives in S3
Governance uses Databricks Unity Catalog and its Iceberg REST catalog interface
```

Choose carefully:

+ Iceberg: multi-engine lakehouse, open table standard, hidden partitioning, partition/schema evolution
+ Delta: strong fit in Delta/Databricks-centered environments, with UniForm when external Iceberg readers are needed
+ Hudi: strong fit for CDC-heavy ingestion and incremental pull patterns

Interview answer: do not say one is universally better. Tie the choice to engines, governance, update/delete needs, streaming requirements, operational tooling, and team experience.

[Table of Contents](#Apache-Iceberg)

## Real world use cases for Apache Iceberg

### 1. Multi-engine lakehouse on object storage

A retailer keeps one copy of curated data in S3 as Iceberg. Spark writes it, Trino serves ad-hoc analytics, Athena powers a serverless dashboard, and Snowflake reads selected tables for finance - all against the same files and the same snapshot.

```python
spark.sql("""
    CREATE TABLE IF NOT EXISTS lakehouse.orders (
        order_id     STRING,
        customer_id  STRING,
        order_ts     TIMESTAMP,
        amount       DECIMAL(18, 2),
        status       STRING
    )
    USING iceberg
    PARTITIONED BY (days(order_ts), bucket(16, customer_id))
""")

(
    spark.read.parquet("s3://acme-raw/orders/ds=2026-10-04/")
    .writeTo("lakehouse.orders")
    .append()
)
```

Why Iceberg: hidden partitioning means readers do not need to know the partition layout, and partition evolution lets the layout change without rewriting history. A single format removes the copy-per-engine pattern.

### 2. Streaming CDC with upserts and deletes

Flink or Spark Structured Streaming consumes Debezium events and applies them to Iceberg with `MERGE`. Equality deletes let a streaming job mark rows deleted without rewriting whole partitions.

```sql
MERGE INTO lakehouse.customers AS t
USING cdc_batch AS s
ON t.customer_id = s.customer_id
WHEN MATCHED AND s.op = 'd' THEN DELETE
WHEN MATCHED THEN UPDATE SET name = s.name, email = s.email, updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, name, email, updated_at)
VALUES (s.customer_id, s.name, s.email, s.updated_at);
```

Why Iceberg: row-level deletes and ACID commits make the lakehouse table behave like a mutable database table without nightly full rebuilds.

### 3. GDPR deletion and right-to-be-forgotten

A deletion request must remove one customer's rows from a 500 TB table. Rewriting every partition is unacceptable, so the pipeline deletes by predicate and then expires the old snapshots that still contain the data.

```python
spark.sql("DELETE FROM lakehouse.events WHERE customer_id = 'C-12345'")

# physically remove files that are no longer referenced
spark.sql("CALL prod.system.rewrite_data_files(table => 'lakehouse.events')")
spark.sql("CALL prod.system.expire_snapshots(table => 'lakehouse.events', older_than => TIMESTAMP '2026-10-01 00:00:00')")
```

Why Iceberg: predicate deletes plus snapshot expiry give an auditable path to true removal, which copy-on-write-parquet pipelines cannot offer without rewriting everything.

### 4. Reproducible reporting and incident recovery

A finance report must be reproducible as of its publication date. Each successful load tags a snapshot; the reporting job pins that snapshot, and a bad deployment is rolled back by pointing the table at the previous snapshot.

```python
spark.sql("ALTER TABLE lakehouse.orders CREATE TAG finance_close_2026_09 AS OF CURRENT_TIMESTAMP")

# read exactly what finance signed off on
finance = spark.read.option("snapshot-id", tag_id).table("lakehouse.orders")

# roll back a bad publish
spark.sql("CALL prod.system.rollback_to_snapshot('lakehouse.orders', 1234567890)")
```

Why Iceberg: snapshot isolation gives point-in-time reads and fast rollback that do not depend on restoring backups.

### 5. Migration from Hive and Parquet with a zero-downtime cutover

A team migrates partitioned Parquet tables in place, keeping the same storage paths, and dual-runs readers during a validation window.

```sql
-- register existing Parquet files as an Iceberg table without moving data
CALL prod.system.migrate('analytics.orders_parquet');
```

```python
# validate row counts across the old and new access paths before cutover
old = spark.read.parquet("s3://lakehouse/analytics/orders/")
new = spark.table("lakehouse.orders")
assert old.count() == new.count()
```

Why Iceberg: in-place migration avoids a second copy, and snapshot isolation makes the validation window safe for existing readers.

[Table of Contents](#Apache-Iceberg)
