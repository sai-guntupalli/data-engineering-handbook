## [Main title](../README.md)
### [Interview questions](full.md)

# Delta Lake
+ [What is Delta Lake?](#What-is-Delta-Lake)
+ [How do you create a Delta table in Databricks Unity Catalog with PySpark?](#How-do-you-create-a-Delta-table-in-Databricks-Unity-Catalog-with-PySpark)
+ [How do you write to a Delta table with PySpark?](#How-do-you-write-to-a-Delta-table-with-PySpark)
+ [How does Delta Lake support upserts and CDC merges?](#How-does-Delta-Lake-support-upserts-and-CDC-merges)
+ [How do you use Delta Lake time travel and restore?](#How-do-you-use-Delta-Lake-time-travel-and-restore)
+ [What is VACUUM in Delta Lake and when should you use it?](#What-is-VACUUM-in-Delta-Lake-and-when-should-you-use-it)
+ [What is Change Data Feed in Delta Lake?](#What-is-Change-Data-Feed-in-Delta-Lake)
+ [How do Delta optimization and file compaction work?](#How-do-Delta-optimization-and-file-compaction-work)
+ [How do you make a Delta table Iceberg-compatible with UniForm?](#How-do-you-make-a-Delta-table-Iceberg-compatible-with-UniForm)
+ [Delta Lake vs Iceberg: when would you choose each?](#Delta-Lake-vs-Iceberg-when-would-you-choose-each)
+ [Real world use cases for Delta Lake](#Real-world-use-cases-for-Delta-Lake)

## What is Delta Lake?
Delta Lake is a lakehouse table format that adds ACID transactions, schema enforcement, time travel, efficient updates/deletes, and streaming/batch interoperability to files stored in cloud object storage.

In Databricks, the preferred production pattern is to create governed Delta tables in Unity Catalog:

```text
catalog.schema.table
main.bronze.orders_raw
main.silver.orders
main.gold.daily_revenue
```

Real-world example: a PySpark job lands raw order events in `main.bronze.orders_raw`, cleans and deduplicates them into `main.silver.orders`, and publishes dashboard-ready aggregates into `main.gold.daily_revenue`.

[Table of Contents](#Delta-Lake)

## How do you create a Delta table in Databricks Unity Catalog with PySpark?
Use Unity Catalog three-part names and create schemas/tables through `spark.sql`.

```python
spark.sql("create schema if not exists main.bronze")
spark.sql("create schema if not exists main.silver")
spark.sql("create schema if not exists main.gold")

spark.sql("""
create table if not exists main.silver.orders (
  order_id bigint,
  customer_id bigint,
  order_ts timestamp,
  order_date date,
  status string,
  amount decimal(12, 2)
) using delta
partitioned by (order_date)
""")
```

If you are in Databricks with Unity Catalog, prefer this managed table style over writing directly to paths like `s3://.../orders`. Unity Catalog gives you centralized permissions, lineage, discovery, and table governance.

[Table of Contents](#Delta-Lake)

## How do you write to a Delta table with PySpark?
For managed Unity Catalog tables, use `saveAsTable`, SQL inserts, or DataFrameWriterV2-style table writes where supported.

Example batch write:

```python
from pyspark.sql import functions as F

orders_df = (
    spark.read.json("s3://company-landing/orders/ds=2026-10-04/")
    .select(
        F.col("order_id").cast("bigint"),
        F.col("customer_id").cast("bigint"),
        F.col("order_ts").cast("timestamp"),
        F.to_date("order_ts").alias("order_date"),
        F.col("status").cast("string"),
        F.col("amount").cast("decimal(12,2)"),
    )
)

orders_df.write.mode("append").saveAsTable("main.silver.orders")
```

Example partition overwrite for one day:

```python
(
    orders_df
    .where(F.col("order_date") == F.lit("2026-10-04"))
    .write
    .mode("overwrite")
    .option("replaceWhere", "order_date = '2026-10-04'")
    .saveAsTable("main.silver.orders")
)
```

Interview point: make writes idempotent by partition, batch id, or business key. Avoid blind append when a retry could duplicate records.

[Table of Contents](#Delta-Lake)

## How does Delta Lake support upserts and CDC merges?
Delta supports `MERGE INTO`, which is commonly used for CDC. In PySpark, deduplicate the source changes first, then merge into the target Delta table.

Deduplicate CDC records:

```python
from pyspark.sql import functions as F
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

Merge changes:

```python
spark.sql("""
merge into main.silver.orders as target
using orders_cdc_deduped as source
on target.order_id = source.order_id
when matched and source.op = 'D' then delete
when matched then update set
  customer_id = source.customer_id,
  order_ts = source.order_ts,
  order_date = to_date(source.order_ts),
  status = source.status,
  amount = source.amount
when not matched and source.op <> 'D' then insert (
  order_id, customer_id, order_ts, order_date, status, amount
) values (
  source.order_id, source.customer_id, source.order_ts, to_date(source.order_ts), source.status, source.amount
)
""")
```

Real-world guidance: merge on stable keys, dedupe by source ordering metadata, handle deletes explicitly, and track merge row counts for observability.

[Table of Contents](#Delta-Lake)

## How do you use Delta Lake time travel and restore?
Delta keeps table versions in the transaction log. You can query older versions for debugging, audit, or recovery.

Inspect history:

```python
history = spark.sql("describe history main.silver.orders")
history.select("version", "timestamp", "operation", "operationMetrics").show(truncate=False)
```

Read an older version:

```python
orders_v42 = (
    spark.read
    .option("versionAsOf", 42)
    .table("main.silver.orders")
)
```

Read by timestamp:

```python
orders_yesterday = (
    spark.read
    .option("timestampAsOf", "2026-10-04 10:00:00")
    .table("main.silver.orders")
)
```

Restore a table to an older version:

```python
spark.sql("restore table main.silver.orders to version as of 42")
```

Do not rely on infinite time travel. Retention and `VACUUM` settings determine how far back you can safely query.

[Table of Contents](#Delta-Lake)

## What is VACUUM in Delta Lake and when should you use it?
`VACUUM` removes old data files that are no longer referenced by the current Delta table version. This controls storage cost, but it can reduce time travel history.

Example:

```python
spark.sql("vacuum main.silver.orders retain 168 hours")
```

Use `VACUUM` after retention requirements are clear. For example, if your team needs 30 days of rollback/audit history, do not vacuum with a 7-day retention policy.

[Table of Contents](#Delta-Lake)

## What is Change Data Feed in Delta Lake?
Change Data Feed (CDF) lets downstream jobs read row-level changes from a Delta table instead of scanning the full table each run.

Enable CDF:

```python
spark.sql("""
alter table main.silver.orders
set tblproperties (delta.enableChangeDataFeed = true)
""")
```

Read changes from a starting version:

```python
changes = (
    spark.read
    .format("delta")
    .option("readChangeFeed", "true")
    .option("startingVersion", 42)
    .table("main.silver.orders")
)

changes.select("_change_type", "_commit_version", "order_id", "status").show()
```

Real-world use: update a downstream `main.gold.daily_revenue` aggregate only from changed orders rather than rebuilding all history.

[Table of Contents](#Delta-Lake)

## How do Delta optimization and file compaction work?
Small files slow queries and increase metadata overhead. On Databricks, common tools include optimized writes, auto compaction, `OPTIMIZE`, and optionally Z-ordering where supported.

Optimize a table:

```python
spark.sql("optimize main.silver.orders")
```

Optimize a recent partition:

```python
spark.sql("""
optimize main.silver.orders
where order_date >= date_sub(current_date(), 7)
""")
```

If your workload frequently filters by `customer_id`, clustering or Z-ordering can help depending on your runtime/table features:

```python
spark.sql("optimize main.silver.orders zorder by (customer_id)")
```

The practical answer is: compact files based on query patterns and write volume, not just on a fixed schedule.

[Table of Contents](#Delta-Lake)

## How do you make a Delta table Iceberg-compatible with UniForm?
Delta UniForm can generate Iceberg-compatible metadata for a Delta table, so Iceberg readers can read it. The Delta table remains the source of truth.

Create a Unity Catalog Delta table with Iceberg compatibility enabled:

```python
spark.sql("""
create table if not exists main.silver.orders_uniform (
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

Enable UniForm on an existing table:

```python
spark.sql("""
alter table main.silver.orders_uniform
set tblproperties (
  'delta.enableIcebergCompatV2' = 'true',
  'delta.universalFormat.enabledFormats' = 'iceberg'
)
""")
```

Important: treat Iceberg access to UniForm tables as read-oriented unless your platform explicitly supports writes through multiple formats. In most interview scenarios, Delta owns writes and external Iceberg clients read.

[Table of Contents](#Delta-Lake)

## Delta Lake vs Iceberg: when would you choose each?
Choose Delta Lake when your platform is Databricks-centered and you want tight integration with Unity Catalog, Delta Live Tables, Databricks SQL, Auto Loader, Change Data Feed, and Databricks optimization features.

Choose Iceberg when you need broad multi-engine interoperability as the primary requirement, especially when Spark, Trino, Flink, Snowflake, and other engines need to share open table metadata directly.

Example Delta fit:

```text
Databricks PySpark writes main.silver.orders
Databricks SQL dashboards query main.gold.daily_revenue
Unity Catalog owns permissions and lineage
Change Data Feed powers downstream aggregates
```

Example Iceberg fit:

```text
PySpark writes main.analytics.orders as Iceberg
Snowflake reads through Unity Catalog Iceberg REST
Trino reads through Iceberg REST
Multiple engines need the same open table contract
```

There is overlap. Delta UniForm can expose Delta tables to Iceberg readers, while native Iceberg is often cleaner when Iceberg is the primary table contract from day one.

[Table of Contents](#Delta-Lake)

## Real world use cases for Delta Lake

### 1. Medallion lakehouse on Databricks

Bronze holds raw events, silver holds cleaned and deduplicated entities, gold holds aggregates. Silver and gold are Delta tables maintained with `MERGE` plus scheduled `OPTIMIZE`.

```python
from delta.tables import DeltaTable

# Upsert yesterday's changed orders into silver
(
    DeltaTable.forName(spark, "main.silver.orders")
    .alias("t")
    .merge(
        spark.read.table("main.bronze.order_events").alias("s"),
        "t.order_id = s.order_id",
    )
    .whenMatchedUpdateAll(condition="s.updated_at > t.updated_at")
    .whenNotMatchedInsertAll()
    .execute()
)

# Compact and co-locate for the most common filter
spark.sql("OPTIMIZE main.silver.orders ZORDER BY (customer_id)")
```

Why Delta: ACID merges make incremental silver and gold layers reliable, and time travel gives reproducible reporting without a separate history store.

### 2. Kafka CDC into Delta with exactly-once streaming

A Structured Streaming job consumes Debezium events and merges each micro-batch into Delta. Checkpointing gives exactly-once processing, and `MERGE` makes the write idempotent even if a batch is replayed.

```python
from delta.tables import DeltaTable

def upsert_to_delta(micro_batch_df, batch_id):
    (
        DeltaTable.forName(spark, "main.silver.customers")
        .alias("t")
        .merge(micro_batch_df.alias("s"), "t.customer_id = s.customer_id")
        .whenMatchedDelete(condition="s.op = 'd'")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

(
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "cdc.public.customers")
    .load()
    .selectExpr("CAST(value AS STRING) AS json")
    .writeStream
    .foreachBatch(upsert_to_delta)
    .option("checkpointLocation", "s3://acme-checkpoints/customers/")
    .trigger(availableNow=True)
    .start()
)
```

Why Delta: CDC deletes and updates map directly to `MERGE`, and replaying a batch does not duplicate rows.

### 3. Change Data Feed for downstream aggregates

Gold aggregates only need changed rows, not full rebuilds. Enable CDF and read the change stream to update a metrics table incrementally.

```sql
ALTER TABLE main.silver.orders
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

SELECT order_id, _change_type, order_date, amount
FROM table_changes('main.silver.orders', '2026-10-04T00:00:00', '2026-10-05T00:00:00')
WHERE _change_type IN ('insert', 'update_postimage');
```

Why Delta: incremental propagation keeps the end-to-end SLA short without recomputing the whole warehouse.

### 4. Regulatory reporting, audit, and right-to-be-forgotten

A bank keeps every version of a transactions table for audit, then must also delete one customer's data on request.

```python
# point-in-time report as of the close
spark.read.option("versionAsOf", 42).table("main.gold.fct_transactions")

# delete, then physically remove files that are no longer referenced
spark.sql("DELETE FROM main.gold.fct_transactions WHERE customer_id = 'C-12345'")
spark.sql("VACUUM main.gold.fct_transactions RETAIN 168 HOURS")
```

Why Delta: time travel answers audit questions, and delete plus `VACUUM` removes data for good - but the retention window must stay shorter than the time-travel window your readers depend on.

### 5. One table for streaming and batch

A pipeline ingests continuously and also re-reads history for backfills. Because both paths use the same Delta table, they share one schema, one history, and one permission model.

```python
# batch backfill from a known-good version
backfill = spark.read.option("versionAsOf", 40).table("main.silver.orders")

# recovery: undo a bad publish, then reprocess
spark.sql("RESTORE TABLE main.silver.orders TO VERSION AS OF 40")
```

Why Delta: one storage contract removes the classic streaming-table versus batch-table split, and `RESTORE` makes a bad deployment reversible in seconds.

[Table of Contents](#Delta-Lake)
