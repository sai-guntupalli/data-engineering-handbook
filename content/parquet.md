## [Main title](../README.md)
### [Interview questions](full.md)

# Parquet

Apache Parquet is a columnar, typed file format for analytics, and the default storage format for Spark, Trino, Athena, and lakehouse tables.

+ [What is Apache Parquet?](#What-is-Apache-Parquet)
+ [Why is Parquet better than CSV or JSON for analytics?](#Why-is-Parquet-better-than-CSV-or-JSON-for-analytics)
+ [How do you write and read Parquet with PySpark?](#How-do-you-write-and-read-Parquet-with-PySpark)
+ [How do columnar storage and predicate pushdown make queries faster?](#How-do-columnar-storage-and-predicate-pushdown-make-queries-faster)
+ [What are row groups, file sizes, and the small files problem?](#What-are-row-groups-file-sizes-and-the-small-files-problem)
+ [How does partitioning interact with Parquet?](#How-does-partitioning-interact-with-Parquet)
+ [What compression and encoding should you use?](#What-compression-and-encoding-should-you-use)
+ [How do nested types work in Parquet?](#How-do-nested-types-work-in-Parquet)
+ [How does schema evolution work with Parquet?](#How-does-schema-evolution-work-with-Parquet)
+ [What are common Parquet mistakes in production?](#What-are-common-Parquet-mistakes-in-production)
+ [How do you inspect Parquet metadata and file layout?](#How-do-you-inspect-Parquet-metadata-and-file-layout)
+ [Parquet vs ORC vs Avro: when do you choose which?](#Parquet-vs-ORC-vs-Avro-when-do-you-choose-which)
+ [Real world use cases for Parquet](#Real-world-use-cases-for-Parquet)

## What is Apache Parquet?

Apache Parquet is an open-source columnar file format designed for analytical workloads. Values are stored by column inside row groups, each column chunk carries statistics (min, max, null count), and a footer holds the schema and metadata. Query engines read only the columns and row groups they need, which is why Parquet scans are cheaper than row-oriented files.

Example: a query that selects `customer_id` and `amount` never touches a large `description` or `payload` column, and a filter on `order_date` can skip row groups whose min/max range cannot match.

```python
# Minimal shape of a Parquet dataset written by Spark
# s3://acme-curated/orders/ds=2026-10-04/part-00000-....snappy.parquet
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("parquet-demo").getOrCreate()

orders = spark.read.json("s3://acme-raw/orders/ds=2026-10-04/")

orders.write.mode("overwrite").parquet("s3://acme-curated/orders/ds=2026-10-04/")
```

Parquet is a file format, not a table format. It has no transactions, no row-level deletes, and no catalog. Iceberg, Delta Lake, and Hudi add those table semantics on top of Parquet files.

[Table of Contents](#Parquet)

## Why is Parquet better than CSV or JSON for analytics?

CSV and JSON are row-oriented text formats. They are human-readable but expensive: every query parses every row, every column, and often every byte. Parquet is binary, typed, columnar, compressed, and splittable, so engines like Spark, Hive, Athena, BigQuery external tables, Trino, and DuckDB scan far less data.

A realistic comparison for the same 200 GB of order events:

| Aspect | JSON / CSV | Parquet |
|---|---|---|
| Storage size | 200 GB | 40-70 GB with Snappy, less with Zstd |
| Scan for 2 of 30 columns | reads every column | reads those 2 column chunks |
| Filter on one date | full scan, no skipping | skips row groups via min/max statistics |
| Schema | inferred per run | embedded in the footer |
| Splittable | often not (gzip CSV) | yes, splittable per row group |
| Nested fields | re-parsed as text | native struct/array/map types |

The practical result: converting a JSON landing zone to partitioned Parquet commonly cuts both storage and warehouse scan cost, and removes a whole class of type-inference bugs.

```python
# Compare the same data as JSON and as Parquet
events = spark.read.json("s3://acme-raw/events/2026/10/04/")

events.write.mode("overwrite").json("s3://acme-cmp/events_json/")
events.write.mode("overwrite").parquet("s3://acme-cmp/events_parquet/")

# Query only two columns and filter by date: Parquet reads a fraction of the bytes
parquet_scan = spark.read.parquet("s3://acme-cmp/events_parquet/")
parquet_scan.select("customer_id", "amount").where("event_date = '2026-10-04'").explain("cost")
```

[Table of Contents](#Parquet)

## How do you write and read Parquet with PySpark?

Ask questions about `mode`, `partitionBy`, compression, and file count in interviews. The snippet below is a production-shaped write:

```python
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("orders-parquet").getOrCreate()

orders = (
    spark.read.json("s3://acme-raw/orders/")
    .withColumn("order_date", F.to_date("created_at"))
    .filter(F.col("order_date") == "2026-10-04")
)

# One logical partition per day, deterministic writes, compressed
(
    orders.repartition("order_date")
    .write.mode("overwrite")
    .partitionBy("order_date")
    .option("compression", "snappy")
    .parquet("s3://acme-curated/orders/")
)

# Read it back and let the engine prune partitions and row groups
curated = spark.read.parquet("s3://acme-curated/orders/")
(
    curated.filter(F.col("order_date") == "2026-10-04")
    .groupBy("country")
    .agg(F.sum("amount").alias("revenue"), F.count("*").alias("orders"))
    .show()
)
```

Mode rules that matter:

+ `overwrite` replaces the whole target (and with `partitionBy`, only the touched partitions under dynamic partition overwrite).
+ `append` is cheap but creates duplicates if a task reruns, which is why idempotency belongs to the table format or to a partition-replace pattern.
+ `repartition(col)` yields one file per partition value; use `coalesce(n)` for the opposite (fewer files, no shuffle) when the data is already small.

[Table of Contents](#Parquet)

## How do columnar storage and predicate pushdown make queries faster?

Parquet stores each column contiguously, so a scan is proportional to the columns selected, not the rows. On top of that, Parquet metadata enables three levels of skipping:

1. **Partition pruning** - the engine skips whole directories from the partition path (`ds=2026-10-03/`).
2. **Row-group skipping** - the footer stores per-column min/max and null counts, so a row group is skipped when the filter cannot match.
3. **Page/dictionary filtering** - finer-grained statistics and bloom filters can skip pages inside a row group.

The `explain()` output is the interview evidence: look for `PushedFilters` and `PartitionFilters` rather than a full scan.

```python
curated = spark.read.parquet("s3://acme-curated/orders/")

filtered = curated.filter("order_date = '2026-10-04' AND country = 'DE'")
filtered.explain("formatted")
# Look for:
#   PartitionFilters: [isnotnull(order_date#..), (order_date#.. = 2026-10-04)]
#   PushedFilters:    [IsNotNull(country), EqualTo(country,DE)]
```

The same idea in a SQL engine (Athena over S3, or Trino):

```sql
SELECT country, SUM(amount) AS revenue
FROM parquet_scan('s3://acme-curated/orders/*/*.parquet')
WHERE order_date = DATE '2026-10-04'
  AND country = 'DE'
GROUP BY country;
```

Two design levers make skipping effective: **partition on the columns you filter most**, and **sort or cluster within files on the next most selective column** so that min/max ranges are tight. If a file mixes all dates, no row group can be skipped.

[Table of Contents](#Parquet)

## What are row groups, file sizes, and the small files problem?

A Parquet file is split into row groups (commonly 128 MB by default in Spark), and each row group contains one column chunk per column. Size choices trade off:

+ Larger row groups: better compression and fewer reads, but coarser skipping and more memory per read.
+ Smaller row groups: finer skipping, more overhead and worse compression.

The bigger production problem is file count. Thousands of tiny files per partition hurt every engine: each file means one open, one footer parse, and one task.

```text
bad layout:  s3://acme-curated/orders/ds=2026-10-04/part-00000 ... part-04800  (KB-sized files)
good layout: s3://acme-curated/orders/ds=2026-10-04/part-00000 ... part-00007  (~128-512 MB files)
```

```python
# Compact small files into fewer, larger ones (read, coalesce, rewrite)
small = spark.read.parquet("s3://acme-curated/orders/ds=2026-10-04/")
target_files = 8
(
    small.coalesce(target_files)
    .write.mode("overwrite")
    .parquet("s3://acme-curated/orders/ds=2026-10-04-compacted/")
)

# Tune the write side so compaction is needed less often
spark.conf.set("spark.sql.files.maxRecordsPerFile", 5_000_000)
spark.conf.set("spark.sql.files.openCostInBytes", 128 * 1024 * 1024)
```

On table formats, do not hand-compact: Iceberg and Delta expose maintenance (`rewrite_data_files`, `OPTIMIZE`) plus snapshot expiry, which is safer than rewriting files underneath a live table.

[Table of Contents](#Parquet)

## How does partitioning interact with Parquet?

The partition key becomes a directory level (`orders/ds=2026-10-04/country=DE/part-....parquet`), and the value is also stored in the file for safety. Partitioning is the highest-leverage performance decision and the easiest one to get wrong.

Guidelines:

+ Partition on low-to-medium cardinality columns used in filters: date, region, tenant, status.
+ Keep partition count manageable. A few thousand partitions per table is fine; hundreds of thousands is not.
+ Do not partition on high-cardinality keys such as `user_id` or millisecond timestamps - each partition becomes a tiny file.
+ Prefer one date grain: `ds=YYYY-MM-DD` for daily, `hour=` only when volume truly needs it.
+ For low-cardinality columns (like `country`), consider clustering or sorting inside files instead of an extra directory level.

```python
# Over-partitioned: 120k directories, tiny files, slow metadata operations
orders.write.partitionBy("order_date", "hour", "customer_id").parquet("s3://acme-bad/orders/")

# Right-sized: day grain, country clustered inside files
(
    orders.repartition("order_date")
    .sortWithinPartitions("country", "order_id")
    .write.partitionBy("order_date")
    .parquet("s3://acme-good/orders/")
)
```

Hidden partitioning in Iceberg removes most of this manual reasoning: you declare `days(ts)` or `bucket(16, user_id)` and the engine handles pruning without exposing directory columns in queries.

[Table of Contents](#Parquet)

## What compression and encoding should you use?

Parquet compresses per column chunk and chooses encodings from the data type (dictionary encoding for repeated strings, run-length encoding for sorted values, delta encodings for timestamps). Codec choice is the knob you control:

| Codec | Ratio | Speed | Splittable | Typical use |
|---|---|---|---|---|
| Snappy | moderate | fast | yes | Spark default; balanced hot path |
| Zstd | high | medium | yes | cold storage, cost-sensitive lakes |
| Gzip | high | slow | yes | legacy; splits at row groups, but decompression is CPU-heavy |
| LZ4 | low-moderate | fastest | yes | latency-critical reads |
| None | 1x | fastest CPU | yes | already compressed payloads |

```python
# Per-write codec choice
orders.write.option("compression", "zstd").parquet("s3://acme-cold/orders/")

# Change it globally for a session
spark.conf.set("spark.sql.parquet.compression.codec", "zstd")
```

Also reduce the data itself: cast wide strings, drop unused columns before writing, and avoid storing raw JSON blobs as string columns. Encoding cannot fix a schema that stores 2 KB of unused JSON per row.

[Table of Contents](#Parquet)

## How do nested types work in Parquet?

Parquet natively represents `struct`, `array`, and `map`, and Spark maps DataFrames onto them directly. Two rules keep nested writes efficient:

+ Read only the nested leaves you need with dot notation (`customer.country`) so the engine can skip the other sub-columns.
+ Do not `explode` large arrays earlier than necessary; exploding multiplies rows and destroys the columnar advantage.

```python
from pyspark.sql import functions as F

events = spark.read.json("s3://acme-raw/events/")
events.printSchema()
# root
#  |-- event_id: string
#  |-- customer: struct (customer_id, country, tier)
#  |-- items: array<struct (sku, qty, price)>

# Project only the nested leaves required for the report
events.select(
    "event_id",
    "customer.country",
    F.explode("items").alias("item"),
).select("event_id", "country", "item.sku", "item.qty").show(5)

# Write the nested shape without flattening it
events.write.mode("overwrite").parquet("s3://acme-curated/events/")
```

[Table of Contents](#Parquet)

## How does schema evolution work with Parquet?

Parquet is schema-on-read: the schema lives in the file footer, and readers reconcile files with different schemas. Adding a nullable column at the end is safe. Removing or renaming columns, or changing a type incompatibly, needs care.

```python
# Batch read: merge schemas across files in the path
events = spark.read.option("mergeSchema", "true").parquet("s3://acme-curated/events/")

# Session-wide default, convenient for near-real-time readers
spark.conf.set("spark.sql.parquet.mergeSchema", "true")
```

Rules that avoid incidents:

+ Add columns as nullable; never reuse a column name with a new meaning.
+ `mergeSchema` on every read slows planning for wide schemas; prefer catalog-driven tables (Iceberg/Delta/Hive metastore) over schema inference in production.
+ Renames are migrations, not evolutions. Write the new name and backfill, or use a view that maps old to new.
+ Parquet has no schema registry. If producers change types freely, add Avro + a registry in the ingestion path, or enforce a contract in the table format.

[Table of Contents](#Parquet)

## What are common Parquet mistakes in production?

+ **Writing thousands of small files.** Use fewer, larger files and schedule compaction.
+ **Over-partitioning.** Every extra partition column multiplies directories and shrinks files.
+ **Partitioning by a column you never filter on.** You pay metadata cost and get no pruning.
+ **Non-splittable codecs.** A single gzip CSV cannot be split; gzip Parquet reads can still bottleneck.
+ **No sort/clustering inside files.** Wide min/max ranges make row-group skipping useless.
+ **Blind `append`.** Retries and backfills duplicate rows; make loads idempotent or use a merge.
+ **Storing everything as string.** You lose statistics quality, encoding, and type safety.
+ **Using Parquet for upserts.** Use Iceberg, Delta, or Hudi when records change.
+ **Forgetting timezone semantics.** Store timestamps consistently (UTC) and document it; naive timestamps across engines cause off-by-hours bugs.
+ **Reading with schema inference in production.** It is slow and can silently change types; pass an explicit schema.

[Table of Contents](#Parquet)

## How do you inspect Parquet metadata and file layout?

Being able to inspect a file is what separates a working pipeline from a debuggable one.

```python
# pyarrow: row groups, sizes, statistics, compression
import pyarrow.parquet as pq

pf = pq.ParquetFile("orders/ds=2026-10-04/part-00000.snappy.parquet")
print(pf.metadata.num_rows, pf.metadata.num_row_groups)
print(pf.schema_arrow)

rg = pf.metadata.row_group(0)
for i in range(rg.num_columns):
    col = rg.column(i)
    stats = col.statistics
    print(col.path_in_schema, col.compression, stats.min if stats else None, stats.max if stats else None)
```

```bash
# File counts and sizes per partition - the first check for small-file problems
aws s3 ls s3://acme-curated/orders/ds=2026-10-04/ --recursive --human-readable --summarize

# One-line schema and row-group summary
python -c "import pyarrow.parquet as pq; print(pq.ParquetFile('part-00000.snappy.parquet').metadata)"
```

[Table of Contents](#Parquet)

## Parquet vs ORC vs Avro: when do you choose which?

| Format | Orientation | Strengths | Best for | Watch out for |
|---|---|---|---|---|
| Parquet | columnar | ecosystem, nested types, predicate pushdown | lakehouse and Spark/Trino/Athena analytics | no row-level updates on its own |
| ORC | columnar | Hive integration, ACID in Hive, strong compression | Hive-centric warehouses | smaller ecosystem outside Hive |
| Avro | row | compact, schema registry, fast row writes | Kafka topics, landing/streaming, record-at-a-time | poor for analytical scans |
| JSON/CSV | row text | debuggable, universal | raw landing, small inputs | size, parsing cost, no types |

A common lakehouse pattern uses both: Avro or JSON for the streaming/landing layer, Parquet for the curated analytical layer, with Iceberg or Delta providing transactions and time travel.

[Table of Contents](#Parquet)

## Real world use cases for Parquet

### 1. Event lake on S3 queried by Athena and Spark

Clickstream events land as JSON, a batch job converts them to partitioned Parquet, and analysts query with Athena. Daily partitions (`ds=YYYY-MM-DD`) allow partition pruning; hourly partitions are added only for the two highest-volume flows.

```python
(
    spark.read.json("s3://acme-raw/clicks/ds=2026-10-04/")
    .select("event_id", "user_id", "url", "event_ts", "device.country")
    .withColumn("ds", F.lit("2026-10-04"))
    .repartition(16)
    .write.mode("overwrite")
    .option("compression", "zstd")
    .parquet("s3://acme-curated/clicks/ds=2026-10-04/")
)
```

Why Parquet: Athena bills by bytes scanned, so columnar projection plus partition pruning is a direct cost lever.

### 2. Offloading a warehouse to object storage

A fintech exports large cold fact tables from Snowflake to Parquet monthly, keeping only recent months in the warehouse. Historical analysis runs on Spark or Trino against S3 at a fraction of the cost.

```sql
-- Snowflake: unload one month as partitioned Parquet
COPY INTO @acme_stage/orders/month=2026-09/
FROM analytics.orders
WHERE order_date >= '2026-09-01' AND order_date < '2026-10-01'
FILE_FORMAT = (TYPE = PARQUET COMPRESSION = ZSTD)
PARTITION_BY = (order_date)
HEADER = TRUE;
```

Why Parquet: it is portable across engines, so the cold copy is not locked into one vendor.

### 3. Training snapshots for machine learning

A feature platform materializes a daily training snapshot as Parquet so training jobs read a stable, immutable dataset with the same schema for every experiment.

```python
features = spark.read.parquet("s3://acme-features/training/ds=2026-10-04/")
features.select("user_id", "label", "days_since_signup", "orders_30d").write.mode("overwrite").parquet(
    "s3://acme-ml/snapshots/ds=2026-10-04/"
)
```

Why Parquet: immutable snapshots make experiments reproducible, and column projection keeps training reads fast even with hundreds of features.

### 4. CDC landing zone feeding a lakehouse table

Debezium writes change events to Kafka; a sink writes micro-batch Parquet into a landing prefix; a merge job applies changes to an Iceberg table. Parquet is the transport format, Iceberg is the queryable table.

```python
landing = spark.read.parquet("s3://acme-landing/customers/dt=2026-10-04/")
landing.createOrReplaceTempView("stg_customers")

spark.sql("""
    MERGE INTO iceberg.customers AS t
    USING stg_customers AS s
    ON t.customer_id = s.customer_id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")
```

Why this split: Parquet is cheap to write and engine-neutral, while the table format provides ACID merges, snapshot isolation, and time travel.

### 5. Log analytics with selective columns

A SaaS platform stores 5 TB/day of application logs. Only a few columns are queried regularly, so the pipeline writes Parquet with a compact set of typed columns plus a compressed `payload` string, and separates high-volume debug logs into a Zstd-compressed cold prefix.

Why Parquet: projection and compression turn an unaffordable full-text scan into a targeted, cheap query, and the same files are readable by Spark, Trino, and DuckDB.

[Table of Contents](#Parquet)
