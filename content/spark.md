## [Main title](../README.md)
### [Interview questions](full.md)

# PySpark

**Notebook:** [`notebooks/topics/spark.ipynb`](../notebooks/topics/spark.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is PySpark and where does it fit in a data platform?](#What-is-PySpark-and-where-does-it-fit-in-a-data-platform)
+ [How do you create a SparkSession in PySpark?](#How-do-you-create-a-SparkSession-in-PySpark)
+ [How do you read data with explicit schemas in PySpark?](#How-do-you-read-data-with-explicit-schemas-in-PySpark)
+ [How do DataFrames differ from RDDs in PySpark?](#How-do-DataFrames-differ-from-RDDs-in-PySpark)
+ [What are transformations and actions in PySpark?](#What-are-transformations-and-actions-in-PySpark)
+ [How does lazy evaluation work in PySpark?](#How-does-lazy-evaluation-work-in-PySpark)
+ [How do you use Spark SQL and temp views from PySpark?](#How-do-you-use-Spark-SQL-and-temp-views-from-PySpark)
+ [How do you clean and standardize data in PySpark?](#How-do-you-clean-and-standardize-data-in-PySpark)
+ [What are common PySpark data manipulation examples?](#What-are-common-PySpark-data-manipulation-examples)
+ [How do you join data in PySpark?](#How-do-you-join-data-in-PySpark)
+ [How do you aggregate data in PySpark?](#How-do-you-aggregate-data-in-PySpark)
+ [How do window functions work in PySpark?](#How-do-window-functions-work-in-PySpark)
+ [How do you handle nested JSON and arrays in PySpark?](#How-do-you-handle-nested-JSON-and-arrays-in-PySpark)
+ [How do you write PySpark tables in Databricks Unity Catalog?](#How-do-you-write-PySpark-tables-in-Databricks-Unity-Catalog)
+ [How do you build an incremental PySpark pipeline?](#How-do-you-build-an-incremental-PySpark-pipeline)
+ [How do you test PySpark transformations?](#How-do-you-test-PySpark-transformations)
+ [How do you handle bad records and data quality checks in PySpark?](#How-do-you-handle-bad-records-and-data-quality-checks-in-PySpark)
+ [How do you use UDFs safely in PySpark?](#How-do-you-use-UDFs-safely-in-PySpark)
+ [How do you process streaming data with PySpark Structured Streaming?](#How-do-you-process-streaming-data-with-PySpark-Structured-Streaming)
+ [How do you monitor and debug PySpark jobs?](#How-do-you-monitor-and-debug-PySpark-jobs)
+ [What should you say in a PySpark interview answer?](#What-should-you-say-in-a-PySpark-interview-answer)
+ [Real world use cases for PySpark](#Real-world-use-cases-for-PySpark)

## What is PySpark and where does it fit in a data platform?
PySpark is the Python API for Apache Spark. It lets you write distributed data processing jobs in Python while Spark executes the work across a cluster.

In a modern lakehouse, PySpark is often used for:

+ Reading raw files from S3, ADLS, GCS, Kafka, or relational sources
+ Cleaning and standardizing semi-structured data
+ Joining large fact data with dimensions
+ Writing Delta, Iceberg, or Parquet tables for analytics
+ Running batch pipelines, streaming pipelines, and feature engineering jobs

Typical production flow:

```text
raw source files -> PySpark bronze job -> PySpark silver job -> Unity Catalog gold tables -> BI / ML / reverse ETL
```

Real-world example: an orders pipeline lands JSON in S3 every 15 minutes. A PySpark job reads the raw JSON, enforces a schema, deduplicates by `order_id`, joins customer data, and writes a governed table such as `main.gold.fact_order`.

[Table of Contents](#PySpark)

## How do you create a SparkSession in PySpark?
`SparkSession` is the main entry point for DataFrame, SQL, catalog, and streaming operations. In Databricks notebooks, `spark` is usually already available. In jobs, tests, or local development, you create it explicitly.

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("orders-pipeline")
    .config("spark.sql.shuffle.partitions", "200")
    .config("spark.sql.adaptive.enabled", "true")
    .getOrCreate()
)
```

In Databricks with Unity Catalog, you normally refer to tables with a three-part name:

```python
orders = spark.table("main.silver.orders")
```

Interview point: `SparkSession` replaced older entry points like `SQLContext` for most DataFrame and SQL work. `SparkContext` still exists underneath, but most production PySpark code should use `SparkSession` and DataFrames.

[Table of Contents](#PySpark)

## How do you read data with explicit schemas in PySpark?
Explicit schemas make pipelines safer and faster. If you let Spark infer schemas from files, the schema may change based on a small sample, a malformed record, or a new partition.

```python
from pyspark.sql import types as T

order_schema = T.StructType([
    T.StructField("order_id", T.StringType(), False),
    T.StructField("customer_id", T.StringType(), True),
    T.StructField("order_ts", T.TimestampType(), True),
    T.StructField("status", T.StringType(), True),
    T.StructField("amount", T.DecimalType(12, 2), True),
])

orders_raw = (
    spark.read
    .schema(order_schema)
    .option("mode", "PERMISSIVE")
    .json("s3://company-raw/orders/ds=2026-10-04/")
)
```

For CSV, be explicit about headers, delimiters, quotes, and bad-record handling:

```python
customers = (
    spark.read
    .schema("customer_id string, email string, created_at timestamp")
    .option("header", "true")
    .option("escape", '"')
    .csv("s3://company-raw/customers/")
)
```

Real-world example: if `amount` is accidentally delivered as `"N/A"` in one file, schema inference can degrade the column to string. With an explicit decimal schema, invalid rows become visible as quality failures instead of silently changing the table contract.

[Table of Contents](#PySpark)

## How do DataFrames differ from RDDs in PySpark?
DataFrames are structured, schema-aware distributed datasets. Spark can optimize DataFrame operations using Catalyst and Tungsten. RDDs are lower-level distributed collections where Spark sees less structure and has fewer optimization opportunities.

Prefer DataFrames for most data engineering work:

```python
from pyspark.sql import functions as F

paid_orders = (
    spark.table("main.silver.orders")
    .where(F.col("status") == "paid")
    .select("order_id", "customer_id", "amount", "order_ts")
)
```

Use RDDs only when you truly need record-level custom distributed logic that DataFrame APIs cannot express:

```python
line_lengths = spark.sparkContext.textFile("s3://company-raw/logs/").map(len)
```

Interview answer: DataFrames are usually better for production pipelines because they support SQL optimization, column pruning, predicate pushdown, better execution planning, and integration with table formats.

[Table of Contents](#PySpark)

## What are transformations and actions in PySpark?
Transformations build a logical plan. Actions trigger execution.

Transformations:

```python
from pyspark.sql import functions as F

daily_revenue = (
    spark.table("main.silver.orders")
    .where(F.col("status").isin("paid", "shipped"))
    .withColumn("order_date", F.to_date("order_ts"))
    .groupBy("order_date")
    .agg(F.sum("amount").alias("revenue"))
)
```

No cluster job has to run yet. An action triggers execution:

```python
daily_revenue.count()
daily_revenue.write.mode("overwrite").saveAsTable("main.gold.daily_revenue")
```

Common transformations include `select`, `where`, `withColumn`, `join`, `groupBy`, `agg`, `distinct`, and `dropDuplicates`. Common actions include `count`, `collect`, `show`, `take`, `write`, and `foreachBatch`.

[Table of Contents](#PySpark)

## How does lazy evaluation work in PySpark?
Lazy evaluation means Spark waits until an action before executing the plan. This lets Spark optimize the whole plan instead of executing every line immediately.

```python
orders = spark.table("main.silver.orders")

result = (
    orders
    .where("order_ts >= timestamp '2026-10-01'")
    .select("order_id", "customer_id", "amount")
    .where("amount > 0")
)

result.explain("formatted")
```

Spark can combine filters, prune unused columns, push predicates to Parquet/Delta/Iceberg readers, and choose join strategies before running tasks.

Real-world example: if you read a 2 TB orders table but select only `order_id` and `amount`, Spark can avoid reading unused columns from Parquet files. That optimization is possible because the plan is declarative.

[Table of Contents](#PySpark)

## How do you use Spark SQL and temp views from PySpark?
PySpark and Spark SQL work together. DataFrames can be registered as temporary views, and SQL results come back as DataFrames.

```python
orders = spark.table("main.silver.orders")
orders.createOrReplaceTempView("orders")

daily = spark.sql("""
select
  date(order_ts) as order_date,
  count(*) as order_count,
  sum(amount) as revenue
from orders
where status in ('paid', 'shipped')
group by date(order_ts)
""")
```

For governed production tables, use Unity Catalog names directly:

```python
spark.sql("""
create or replace table main.gold.daily_revenue as
select
  date(order_ts) as order_date,
  sum(amount) as revenue
from main.silver.orders
where status in ('paid', 'shipped')
group by date(order_ts)
""")
```

Interview point: PySpark DataFrame code and Spark SQL usually compile into the same execution engine. Choose the style that is clearer for the team and workload.

[Table of Contents](#PySpark)

## How do you clean and standardize data in PySpark?
Use built-in column functions instead of Python row loops. Built-ins run inside Spark's optimized execution engine.

```python
from pyspark.sql import functions as F

clean_customers = (
    spark.table("main.bronze.customers")
    .select(
        F.trim(F.lower("email")).alias("email"),
        F.upper(F.trim("country_code")).alias("country_code"),
        F.to_timestamp("created_at").alias("created_at"),
        F.regexp_replace("phone", r"[^0-9]", "").alias("phone_digits"),
    )
    .where(F.col("email").contains("@"))
)
```

For reusable business logic, wrap DataFrame transformations in plain Python functions:

```python
def standardize_orders(df):
    return (
        df
        .withColumn("status", F.lower(F.trim("status")))
        .withColumn("order_date", F.to_date("order_ts"))
        .where(F.col("order_id").isNotNull())
    )

orders = standardize_orders(spark.table("main.bronze.orders"))
```

This style is testable, readable, and avoids hiding Spark logic inside side-effect-heavy notebooks.

[Table of Contents](#PySpark)

## What are common PySpark data manipulation examples?
Most PySpark pipeline work is ordinary data manipulation: parsing timestamps, deriving dates, handling nulls, standardizing strings, splitting arrays, and creating business flags. Prefer `pyspark.sql.functions` because those expressions stay inside Spark's optimizer.

Start with a realistic orders DataFrame:

```python
from pyspark.sql import functions as F

orders = spark.table("main.bronze.orders")
```

Date and timestamp manipulation:

```python
orders_with_dates = (
    orders
    .withColumn("order_ts", F.to_timestamp("order_ts"))
    .withColumn("order_date", F.to_date("order_ts"))
    .withColumn("order_month", F.date_trunc("month", "order_ts"))
    .withColumn("order_year", F.year("order_ts"))
    .withColumn("order_week", F.weekofyear("order_ts"))
    .withColumn("ship_by_date", F.date_add("order_date", 2))
    .withColumn("days_since_order", F.datediff(F.current_date(), "order_date"))
)
```

Timezone conversion is common when sources emit UTC but reporting is local:

```python
localized = (
    orders
    .withColumn("order_ts_utc", F.to_timestamp("order_ts"))
    .withColumn(
        "order_ts_chicago",
        F.from_utc_timestamp("order_ts_utc", "America/Chicago"),
    )
    .withColumn("order_date_chicago", F.to_date("order_ts_chicago"))
)
```

String cleanup:

```python
clean_customers = (
    spark.table("main.bronze.customers")
    .withColumn("email", F.lower(F.trim("email")))
    .withColumn("first_name", F.initcap(F.trim("first_name")))
    .withColumn("phone_digits", F.regexp_replace("phone", r"[^0-9]", ""))
    .withColumn("email_domain", F.element_at(F.split("email", "@"), -1))
)
```

Null handling and default values:

```python
orders_filled = (
    orders
    .withColumn("discount_amount", F.coalesce("discount_amount", F.lit(0.0)))
    .withColumn("status", F.coalesce("status", F.lit("unknown")))
    .fillna({"country_code": "US", "currency": "USD"})
)
```

Type casting and safe derived columns:

```python
typed_orders = (
    orders
    .withColumn("amount", F.col("amount").cast("decimal(12,2)"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn(
        "unit_price",
        F.when(F.col("quantity") > 0, F.col("amount") / F.col("quantity")),
    )
)
```

Conditional business flags:

```python
classified = (
    orders
    .withColumn(
        "order_size",
        F.when(F.col("amount") >= 1000, "enterprise")
         .when(F.col("amount") >= 100, "mid_market")
         .otherwise("small"),
    )
    .withColumn(
        "is_completed",
        F.col("status").isin("paid", "shipped", "delivered"),
    )
)
```

Array and nested field manipulation:

```python
events = spark.table("main.bronze.events")

items = (
    events
    .select(
        "event_id",
        F.col("user.id").alias("user_id"),
        F.explode_outer("items").alias("item"),
    )
    .select(
        "event_id",
        "user_id",
        F.col("item.sku").alias("sku"),
        F.col("item.quantity").alias("quantity"),
    )
)
```

Parsing JSON strings:

```python
payload_schema = "source string, campaign struct<id:string,name:string>"

parsed = (
    events
    .withColumn("payload", F.from_json("payload_json", payload_schema))
    .select(
        "event_id",
        F.col("payload.source").alias("source"),
        F.col("payload.campaign.id").alias("campaign_id"),
    )
)
```

Deduplicating records:

```python
deduped_orders = (
    orders
    .dropDuplicates(["order_id"])
)
```

For CDC or late-arriving updates, use a window so you keep the newest record by source ordering:

```python
from pyspark.sql import Window

w = Window.partitionBy("order_id").orderBy(
    F.col("source_lsn").desc(),
    F.col("ingested_at").desc(),
)

latest_orders = (
    orders
    .withColumn("rn", F.row_number().over(w))
    .where("rn = 1")
    .drop("rn")
)
```

Real-world guidance: if the transformation is expressible with built-in functions, use built-in functions. They are easier for Spark to optimize than Python loops or UDFs.

[Table of Contents](#PySpark)

## How do you join data in PySpark?
A join combines DataFrames by key. The most important production questions are key uniqueness, null handling, data skew, and whether Spark should shuffle both sides or broadcast the small side.

```python
orders = spark.table("main.silver.orders")
customers = spark.table("main.silver.customers")

enriched = (
    orders.alias("o")
    .join(customers.alias("c"), on="customer_id", how="left")
    .select(
        "o.order_id",
        "o.customer_id",
        "c.customer_segment",
        "o.order_ts",
        "o.amount",
    )
)
```

If the dimension is small enough, broadcast it:

```python
from pyspark.sql.functions import broadcast

enriched = orders.join(broadcast(customers), "customer_id", "left")
```

Real-world example: broadcasting a 20 MB customer segment dimension can avoid a large shuffle when joining it to a 3 TB orders fact table. Do not broadcast a dimension just because it is called a dimension; verify its size.

[Table of Contents](#PySpark)

## How do you aggregate data in PySpark?
Aggregations summarize records by one or more grouping columns. They usually create a shuffle because rows with the same key must be brought together.

```python
from pyspark.sql import functions as F

daily_product_sales = (
    spark.table("main.gold.fact_order_line")
    .groupBy("order_date", "product_id")
    .agg(
        F.countDistinct("order_id").alias("orders"),
        F.sum("quantity").alias("units"),
        F.sum("net_amount").alias("revenue"),
    )
)
```

For conditional metrics, use expressions:

```python
customer_metrics = (
    spark.table("main.gold.fact_order")
    .groupBy("customer_id")
    .agg(
        F.sum("amount").alias("lifetime_value"),
        F.sum(F.when(F.col("status") == "refunded", F.col("amount")).otherwise(0)).alias("refunded_amount"),
        F.max("order_ts").alias("last_order_ts"),
    )
)
```

Interview point: aggregations often need tuning because they shuffle data. Check the Spark UI for skewed shuffle partitions, spilled memory, and long-running reduce tasks.

[Table of Contents](#PySpark)

## How do window functions work in PySpark?
Window functions calculate values across related rows without collapsing the result like `groupBy` does.

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("customer_id").orderBy(F.col("order_ts").desc())

latest_order = (
    spark.table("main.silver.orders")
    .withColumn("rn", F.row_number().over(w))
    .where(F.col("rn") == 1)
    .drop("rn")
)
```

Common window use cases:

+ Deduplicating CDC records by latest sequence number
+ Finding the latest row per business key
+ Calculating rolling metrics
+ Ranking products or customers within a segment

CDC example:

```python
w = Window.partitionBy("order_id").orderBy(
    F.col("source_lsn").desc(),
    F.col("ingested_at").desc(),
)

deduped_cdc = (
    spark.table("main.bronze.orders_cdc")
    .withColumn("rn", F.row_number().over(w))
    .where("rn = 1")
    .drop("rn")
)
```

[Table of Contents](#PySpark)

## How do you handle nested JSON and arrays in PySpark?
Nested data is common in event, clickstream, API, and CDC payloads. Use struct and array functions instead of converting rows to Python dictionaries.

```python
from pyspark.sql import functions as F

events = spark.read.json("s3://company-raw/events/")

flattened = events.select(
    F.col("event_id"),
    F.col("user.id").alias("user_id"),
    F.col("device.os").alias("device_os"),
    F.explode_outer("items").alias("item"),
)

items = flattened.select(
    "event_id",
    "user_id",
    F.col("item.sku").alias("sku"),
    F.col("item.quantity").alias("quantity"),
)
```

If a payload column contains JSON strings, parse it with `from_json`:

```python
payload_schema = "event_type string, campaign struct<id:string,name:string>"

parsed = (
    spark.table("main.bronze.raw_events")
    .withColumn("payload", F.from_json("payload_json", payload_schema))
    .select("event_id", "payload.event_type", "payload.campaign.id")
)
```

Interview point: `explode` can multiply rows. Always know the expected array size and watch for unexpected row explosions.

[Table of Contents](#PySpark)

## How do you write PySpark tables in Databricks Unity Catalog?
With Unity Catalog, prefer managed table names like `catalog.schema.table` over raw paths in application code. This keeps governance, lineage, discovery, and permissions at the table layer.

```python
spark.sql("create schema if not exists main.gold")

(
    daily_product_sales
    .write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("main.gold.daily_product_sales")
)
```

For partitioned Delta tables:

```python
(
    daily_product_sales
    .write
    .format("delta")
    .mode("overwrite")
    .partitionBy("order_date")
    .saveAsTable("main.gold.daily_product_sales")
)
```

For table-format-aware writes, use `writeTo` when the target table already exists:

```python
(
    daily_product_sales
    .writeTo("main.gold.daily_product_sales")
    .append()
)
```

Real-world guidance: do not scatter hard-coded S3 paths throughout jobs. Use table names in PySpark transformations, and reserve physical storage paths for ingestion boundaries, external locations, or infrastructure configuration.

[Table of Contents](#PySpark)

## How do you build an incremental PySpark pipeline?
An incremental pipeline processes only new or changed records. The usual pattern is to use a watermark, ingestion timestamp, source sequence number, or table change feed.

Simple batch watermark example:

```python
from pyspark.sql import functions as F

last_loaded_ts = (
    spark.table("main.ops.pipeline_watermarks")
    .where(F.col("pipeline_name") == "orders_silver")
    .select(F.max("loaded_until_ts").alias("ts"))
    .first()["ts"]
)

new_orders = (
    spark.table("main.bronze.orders")
    .where(F.col("ingested_at") > F.lit(last_loaded_ts))
)
```

Merge into the target table:

```python
new_orders.createOrReplaceTempView("new_orders")

spark.sql("""
merge into main.silver.orders as target
using new_orders as source
on target.order_id = source.order_id
when matched then update set *
when not matched then insert *
""")
```

Interview point: a reliable incremental job needs idempotency. If the job retries the same batch, the target should end in the same state, not duplicate data.

[Table of Contents](#PySpark)

## How do you test PySpark transformations?
Keep business transformations as functions that accept and return DataFrames. Then create small test DataFrames and compare outputs.

Transformation:

```python
from pyspark.sql import functions as F

def add_order_date(df):
    return df.withColumn("order_date", F.to_date("order_ts"))
```

Test example:

```python
from datetime import datetime

input_df = spark.createDataFrame(
    [("o1", datetime(2026, 10, 4, 12, 30, 0))],
    ["order_id", "order_ts"],
)

actual = add_order_date(input_df).select("order_id", "order_date").collect()

assert str(actual[0]["order_date"]) == "2026-10-04"
```

For real projects, use `pytest`, fixtures for the Spark session, and small deterministic inputs. Test data should cover nulls, duplicate keys, late-arriving data, invalid records, and boundary timestamps.

[Table of Contents](#PySpark)

## How do you handle bad records and data quality checks in PySpark?
Bad records should be isolated, measurable, and visible. Do not silently drop them unless the product owner agrees that loss is acceptable.

```python
from pyspark.sql import functions as F

orders = spark.table("main.bronze.orders")

valid_orders = orders.where(
    F.col("order_id").isNotNull()
    & F.col("customer_id").isNotNull()
    & (F.col("amount") >= 0)
)

invalid_orders = orders.subtract(valid_orders).withColumn(
    "rejected_at", F.current_timestamp()
)

invalid_orders.write.mode("append").saveAsTable("main.ops.rejected_orders")
valid_orders.write.mode("append").saveAsTable("main.silver.orders")
```

A more explicit rule-based pattern:

```python
checked = (
    orders
    .withColumn(
        "quality_error",
        F.when(F.col("order_id").isNull(), "missing_order_id")
         .when(F.col("amount") < 0, "negative_amount")
    )
)

checked.where("quality_error is null").write.mode("append").saveAsTable("main.silver.orders")
checked.where("quality_error is not null").write.mode("append").saveAsTable("main.ops.orders_quarantine")
```

Interview point: quality checks should happen before publishing gold tables. A dashboard should not discover broken data before the pipeline does.

[Table of Contents](#PySpark)

## How do you use UDFs safely in PySpark?
Use Spark built-in functions first. Python UDFs often move data between the JVM and Python worker, which can be slower and harder for Spark to optimize.

Prefer this:

```python
from pyspark.sql import functions as F

cleaned = customers.withColumn(
    "email_domain",
    F.element_at(F.split(F.lower("email"), "@"), -1),
)
```

Instead of this:

```python
from pyspark.sql import functions as F, types as T

@F.udf(T.StringType())
def email_domain(email):
    if email is None or "@" not in email:
        return None
    return email.lower().split("@")[-1]

cleaned = customers.withColumn("email_domain", email_domain("email"))
```

If you need Python logic for vectorized numeric or ML work, consider Pandas UDFs, but measure performance and memory behavior.

```python
import pandas as pd
from pyspark.sql import functions as F, types as T

@F.pandas_udf(T.DoubleType())
def cap_score(score: pd.Series) -> pd.Series:
    return score.clip(lower=0.0, upper=1.0)

scored = users.withColumn("capped_score", cap_score("score"))
```

[Table of Contents](#PySpark)

## How do you process streaming data with PySpark Structured Streaming?
Structured Streaming lets you express streaming logic with DataFrame APIs. Spark runs the query continuously or in micro-batches.

```python
from pyspark.sql import functions as F

events = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .schema("event_id string, user_id string, event_ts timestamp, event_type string")
    .load("s3://company-raw/events/")
)

clean_events = (
    events
    .withWatermark("event_ts", "30 minutes")
    .dropDuplicates(["event_id"])
)

query = (
    clean_events.writeStream
    .format("delta")
    .option("checkpointLocation", "s3://company-checkpoints/events_silver/")
    .trigger(processingTime="5 minutes")
    .toTable("main.silver.events")
)
```

Real-world points:

+ Checkpoint locations are required for fault tolerance.
+ Watermarks define how late data can arrive before Spark drops state.
+ Deduplication needs a stable event key.
+ Streaming writes must be idempotent or carefully checkpointed.

[Table of Contents](#PySpark)

## How do you monitor and debug PySpark jobs?
Start with the Spark UI. It shows jobs, stages, tasks, shuffle read/write, spilled memory, input size, executor failures, and SQL plans.

Useful PySpark checks:

```python
df.explain("formatted")
print(df.rdd.getNumPartitions())
spark.conf.get("spark.sql.shuffle.partitions")
```

Common symptoms:

+ One task runs much longer than others: likely skew
+ Huge shuffle read/write: expensive join, aggregation, or repartition
+ Spilled memory: insufficient executor memory or too-wide shuffle
+ Many tiny tasks: small files or too many partitions
+ Driver out of memory: collecting too much data to the driver

For production jobs, log record counts at each pipeline boundary:

```python
input_count = orders.count()
output_count = valid_orders.count()

spark.createDataFrame(
    [("orders_silver", input_count, output_count)],
    ["pipeline_name", "input_count", "output_count"],
).write.mode("append").saveAsTable("main.ops.pipeline_metrics")
```

For deeper performance methods, see [Spark Tuning](spark-tuning.md).

[Table of Contents](#PySpark)

## What should you say in a PySpark interview answer?
A strong PySpark interview answer should include the API, the execution model, and the production concern.

Example answer for "How do you deduplicate orders?":

```python
from pyspark.sql import Window, functions as F

w = Window.partitionBy("order_id").orderBy(F.col("source_updated_at").desc())

deduped = (
    spark.table("main.bronze.orders")
    .withColumn("rn", F.row_number().over(w))
    .where("rn = 1")
    .drop("rn")
)
```

Then explain:

+ `row_number` keeps one row per business key.
+ Ordering must use source metadata, not random ingestion order.
+ The result should be merged into the target for idempotency.
+ If one key is extremely hot, this window can skew and needs tuning.

That answer shows that you know PySpark syntax and the operational behavior behind it.

[Table of Contents](#PySpark)

## Real world use cases for PySpark

### 1. Nightly batch ELT into a partitioned lake

Raw JSON lands in object storage, a Spark job cleans and types it, and the curated layer is written as partitioned Parquet for downstream engines.

```python
from pyspark.sql import functions as F

orders = spark.read.schema(order_schema).json("s3://acme-raw/orders/ds=2026-10-04/")

(
    orders.where("amount_cents > 0")
    .withColumn("amount", F.col("amount_cents") / 100)
    .repartition("order_date")            # one file family per day
    .sortWithinPartitions("country")      # tight min/max for skipping
    .write.mode("overwrite")
    .option("compression", "zstd")
    .partitionBy("order_date")
    .parquet("s3://acme-curated/orders/")
)
```

Why Spark: a few minutes of distributed CPU replaces hours of single-node scripting, and explicit schemas remove inference surprises. Enable Adaptive Query Execution (`spark.sql.adaptive.enabled=true`) so skewed joins and partition counts self-tune.

### 2. Structured Streaming from Kafka into a lakehouse table

A streaming job decodes Kafka events, applies the same transformations as the batch path, and merges micro-batches into an Iceberg or Delta table.

```python
from pyspark.sql import functions as F

(
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")
    .load()
    .select(F.from_json(F.col("value").cast("string"), order_schema).alias("o"))
    .select("o.*")
    .writeStream
    .foreachBatch(merge_into_lakehouse)          # idempotent MERGE per batch
    .option("checkpointLocation", "s3://acme-checkpoints/orders/")
    .trigger(processingTime="1 minute")
    .start()
)
```

Why Spark: the batch and streaming APIs share transformations, so there is one business-logic implementation. Checkpointing plus an idempotent merge gives end-to-end exactly-once.

### 3. Feature engineering for machine learning

Feature tables are built with broadcast joins to small dimensions and vectorized pandas UDFs instead of row-at-a-time Python UDFs.

```python
import pandas as pd
from pyspark.sql import functions as F
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()

features = (
    events.join(F.broadcast(products), "product_id")   # small dimension
    .groupBy("customer_id")
    .agg(F.count("*").alias("orders_30d"), F.sum("amount").alias("spend_30d"))
    .withColumn("spend_z", zscore("spend_30d"))
)

features.write.mode("overwrite").parquet("s3://acme-features/customer/ds=2026-10-04/")
```

Why Spark: the same feature definitions can be applied to historical training data and to daily scoring runs, which reduces train/serve skew.

### 4. Log and event processing with messy input

Semi-structured logs break schema assumptions. Read permissively, quarantine bad rows, and evolve the schema deliberately.

```python
raw = (
    spark.read.option("mode", "PERMISSIVE")
    .option("columnNameOfCorruptRecord", "_bad")
    .json("s3://acme-raw/logs/ds=2026-10-04/")
)

good = raw.filter("_bad is null").drop("_bad")
bad = raw.filter("_bad is not null")

good.write.mode("append").parquet("s3://acme-curated/logs/")
bad.write.mode("append").json("s3://acme-quarantine/logs/")
```

Why Spark: quarantine plus schema-on-read lets ingestion continue while the platform team fixes the producer, instead of failing the whole day.

### 5. Backfills and reprocessing without duplicating data

A bug fix requires reprocessing September. With dynamic partition overwrite, only the partitions you touch are replaced.

```python
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

(
    reprocessed.withColumn("order_date", F.to_date("created_at"))
    .write.mode("overwrite")
    .partitionBy("order_date")
    .parquet("s3://acme-curated/orders/")
)
```

Why Spark: the same job that handles daily loads can reprocess a month, and dynamic overwrite makes the rerun idempotent at partition granularity - the property that makes backfills safe.

[Table of Contents](#PySpark)
