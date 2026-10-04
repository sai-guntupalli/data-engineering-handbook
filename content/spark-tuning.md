## [Main title](../README.md)
### [Interview questions](full.md)

# Spark Tuning

**Notebook:** [`notebooks/topics/spark-tuning.ipynb`](../notebooks/topics/spark-tuning.ipynb) - runnable version of this topic with self-checking exercises.

+ [How should you approach Spark tuning in PySpark?](#How-should-you-approach-Spark-tuning-in-PySpark)
+ [How do you read a Spark physical plan?](#How-do-you-read-a-Spark-physical-plan)
+ [What is a shuffle and why is it expensive?](#What-is-a-shuffle-and-why-is-it-expensive)
+ [How do you choose the right number of shuffle partitions?](#How-do-you-choose-the-right-number-of-shuffle-partitions)
+ [How do repartition and coalesce differ in PySpark?](#How-do-repartition-and-coalesce-differ-in-PySpark)
+ [How do you use repartition by column?](#How-do-you-use-repartition-by-column)
+ [How do you fix data skew with salting?](#How-do-you-fix-data-skew-with-salting)
+ [How do you tune joins in PySpark?](#How-do-you-tune-joins-in-PySpark)
+ [How does broadcast join tuning work?](#How-does-broadcast-join-tuning-work)
+ [How does Adaptive Query Execution help performance?](#How-does-Adaptive-Query-Execution-help-performance)
+ [When should you cache or persist DataFrames?](#When-should-you-cache-or-persist-DataFrames)
+ [How do you tune file sizes and avoid small files?](#How-do-you-tune-file-sizes-and-avoid-small-files)
+ [How do you tune partition pruning and predicate pushdown?](#How-do-you-tune-partition-pruning-and-predicate-pushdown)
+ [How do you reduce data before expensive operations?](#How-do-you-reduce-data-before-expensive-operations)
+ [How do you avoid driver memory problems?](#How-do-you-avoid-driver-memory-problems)
+ [How do you tune executor memory and cores?](#How-do-you-tune-executor-memory-and-cores)
+ [How do you tune Structured Streaming jobs?](#How-do-you-tune-Structured-Streaming-jobs)
+ [What Spark tuning checklist should you use in interviews?](#What-Spark-tuning-checklist-should-you-use-in-interviews)
+ [Real world use cases for Spark tuning](#Real-world-use-cases-for-Spark-tuning)

## How should you approach Spark tuning in PySpark?
Spark tuning should start with evidence, not random configuration changes. The usual workflow is:

1. Reproduce the slow job with representative data.
2. Read the Spark UI and `explain("formatted")`.
3. Identify the bottleneck: scan, shuffle, skew, spill, join, small files, driver memory, or sink write.
4. Change one thing.
5. Measure again.

Useful first checks:

```python
df.explain("formatted")
print("partitions:", df.rdd.getNumPartitions())
print("shuffle partitions:", spark.conf.get("spark.sql.shuffle.partitions"))
```

Real-world example: a job that reads 4 TB and then filters to one day may be slow because partition pruning is not working. Increasing executor memory will not fix that. You need to fix table partitioning, predicates, or file layout.

[Table of Contents](#Spark-Tuning)

## How do you read a Spark physical plan?
The physical plan shows how Spark will execute the query. It helps you identify scans, filters, exchanges, joins, aggregations, and code generation stages.

```python
from pyspark.sql import functions as F

orders = spark.table("main.gold.fact_order")
customers = spark.table("main.gold.dim_customer")

result = (
    orders
    .where(F.col("order_date") >= F.lit("2026-10-01"))
    .join(customers, "customer_id")
    .groupBy("customer_segment")
    .agg(F.sum("amount").alias("revenue"))
)

result.explain("formatted")
```

Look for:

+ `FileScan`: what files and columns Spark reads
+ `PushedFilters`: predicates pushed to the reader
+ `PartitionFilters`: partition pruning
+ `Exchange`: shuffle boundary
+ `BroadcastHashJoin`: small side was broadcast
+ `SortMergeJoin`: both sides were shuffled and sorted
+ `AdaptiveSparkPlan`: AQE is enabled

Interview point: if you cannot explain the plan at a high level, you are tuning blind.

[Table of Contents](#Spark-Tuning)

## What is a shuffle and why is it expensive?
A shuffle redistributes data across executors. It usually happens when Spark needs all records with the same key in the same partition.

Common shuffle operations:

+ `groupBy`
+ `distinct`
+ `dropDuplicates`
+ `join` without broadcast
+ `repartition`
+ Window functions with `partitionBy`

Example:

```python
daily_revenue = (
    spark.table("main.silver.orders")
    .groupBy("order_date")
    .agg(F.sum("amount").alias("revenue"))
)
```

This groups all records for the same `order_date` together. If one date has much more data than others, one shuffle partition can become much larger and slower.

How to inspect shuffle symptoms:

+ Spark UI stage has high shuffle read/write.
+ A few tasks are much slower than the rest.
+ Tasks spill to disk.
+ Executor logs show fetch failures or memory pressure.

[Table of Contents](#Spark-Tuning)

## How do you choose the right number of shuffle partitions?
`spark.sql.shuffle.partitions` controls the default number of partitions after many shuffle operations. The default is often `200`, which may be too low for huge jobs or too high for small jobs.

```python
spark.conf.set("spark.sql.shuffle.partitions", "800")
```

Rule of thumb:

+ Too few partitions: large tasks, memory spills, slow reducers
+ Too many partitions: many tiny tasks, scheduling overhead, small output files
+ Better target: partitions large enough to reduce overhead, small enough to avoid spills

Example for a 2 TB aggregation:

```python
spark.conf.set("spark.sql.shuffle.partitions", "2000")

agg = (
    spark.table("main.silver.events")
    .groupBy("event_date", "event_type")
    .agg(F.count("*").alias("events"))
)
```

On Databricks or Spark 3+, enable AQE so Spark can coalesce shuffle partitions at runtime:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

Interview answer: set a reasonable starting value, use AQE, then validate in the Spark UI by checking task sizes, spills, and scheduling overhead.

[Table of Contents](#Spark-Tuning)

## How do repartition and coalesce differ in PySpark?
`repartition` increases or decreases partitions with a full shuffle. `coalesce` usually reduces partitions without a full shuffle.

Use `repartition` when you need an even redistribution:

```python
balanced = orders.repartition(400)
```

Use `coalesce` when reducing partitions after filtering:

```python
small_result = (
    orders
    .where("order_date = date '2026-10-04'")
    .coalesce(24)
)
```

Key difference:

+ `repartition(400)`: expensive, but balances data across 400 partitions
+ `coalesce(24)`: cheaper, but can preserve imbalance from upstream partitions

Real-world example: if a job filters a month of data down to one small day, `coalesce` before writing can reduce small files. If partitions are badly skewed, `repartition` may be better despite the shuffle.

[Table of Contents](#Spark-Tuning)

## How do you use repartition by column?
Column-based repartitioning puts rows with the same key into the same partition. This can help before joins, aggregations, or table writes, but it creates a shuffle.

```python
orders_by_customer = orders.repartition(800, "customer_id")
```

Useful before a key-based operation:

```python
deduped = (
    spark.table("main.bronze.orders_cdc")
    .repartition(800, "order_id")
    .dropDuplicates(["order_id", "source_lsn"])
)
```

Useful before partitioned writes:

```python
(
    daily_orders
    .repartition("order_date")
    .write
    .mode("append")
    .partitionBy("order_date")
    .saveAsTable("main.silver.orders")
)
```

Be careful: repartitioning by a low-cardinality column such as `country_code` can create skew. If 80 percent of rows are `US`, the `US` partition can dominate the job.

[Table of Contents](#Spark-Tuning)

## How do you fix data skew with salting?
Data skew happens when a few keys have much more data than other keys. Salting spreads a hot key across multiple artificial buckets so Spark can process it in parallel.

Skewed join example:

```python
orders = spark.table("main.silver.orders")
promotions = spark.table("main.silver.customer_promotions")

joined = orders.join(promotions, "customer_id")
```

If `customer_id = 'guest'` appears in hundreds of millions of rows, one join partition becomes huge.

Salt the large side:

```python
from pyspark.sql import functions as F

salt_buckets = 32

orders_salted = orders.withColumn(
    "salt",
    (F.rand(seed=42) * salt_buckets).cast("int"),
)
```

Replicate the small side across salts:

```python
salts = spark.range(salt_buckets).withColumnRenamed("id", "salt")

promotions_salted = promotions.crossJoin(salts)
```

Join on the original key plus salt:

```python
joined = (
    orders_salted
    .join(promotions_salted, ["customer_id", "salt"], "left")
    .drop("salt")
)
```

When to use salting:

+ One or a few keys dominate a join or aggregation.
+ Broadcast join is not possible.
+ AQE skew join handling is not enough.

When not to use salting:

+ The small side is not actually small enough to replicate.
+ The key distribution is already even.
+ You have not verified skew in the Spark UI.

Aggregation salting has two phases:

```python
salted = orders.withColumn("salt", (F.rand(seed=7) * 32).cast("int"))

partial = (
    salted
    .groupBy("customer_id", "salt")
    .agg(F.sum("amount").alias("partial_amount"))
)

final = (
    partial
    .groupBy("customer_id")
    .agg(F.sum("partial_amount").alias("total_amount"))
)
```

The first aggregation spreads hot keys. The second aggregation removes the salt and produces the final result.

[Table of Contents](#Spark-Tuning)

## How do you tune joins in PySpark?
Join tuning starts with the size and distribution of both sides.

Typical decisions:

+ Broadcast the small side if it safely fits in executor memory.
+ Repartition both large sides by the join key if both sides are large.
+ Filter and select columns before joining.
+ Deduplicate dimensions before joining to avoid row multiplication.
+ Use salting or AQE skew handling for hot keys.

Good join hygiene:

```python
orders = (
    spark.table("main.silver.orders")
    .where("order_date >= date '2026-10-01'")
    .select("order_id", "customer_id", "amount")
)

customers = (
    spark.table("main.gold.dim_customer")
    .where("is_current = true")
    .select("customer_id", "customer_segment")
    .dropDuplicates(["customer_id"])
)

joined = orders.join(customers, "customer_id", "left")
```

Bad pattern:

```python
joined = spark.table("main.silver.orders").join(
    spark.table("main.gold.dim_customer"),
    "customer_id",
)
```

The bad pattern reads unnecessary columns, may include historical dimension rows, and may multiply facts if the dimension is not unique by `customer_id`.

[Table of Contents](#Spark-Tuning)

## How does broadcast join tuning work?
A broadcast join sends a small DataFrame to every executor, avoiding a shuffle of the large side.

Explicit broadcast:

```python
from pyspark.sql.functions import broadcast

orders = spark.table("main.silver.orders")
calendar = spark.table("main.ref.calendar")

joined = orders.join(broadcast(calendar), "order_date", "left")
```

Configure automatic broadcast threshold:

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)
```

Disable auto broadcast for testing:

```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
```

Use broadcast when:

+ The small side comfortably fits in executor memory.
+ The same dimension is joined to a much larger fact table.
+ You want to avoid a sort-merge join shuffle.

Avoid broadcast when:

+ The dimension is large or underestimated.
+ Executors have tight memory.
+ The broadcast side is produced by an expensive upstream query that will be recomputed.

Validate with:

```python
joined.explain("formatted")
```

Look for `BroadcastHashJoin` and `BroadcastExchange`.

[Table of Contents](#Spark-Tuning)

## How does Adaptive Query Execution help performance?
Adaptive Query Execution, or AQE, lets Spark adjust the physical plan during execution based on runtime statistics.

Enable AQE:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

AQE can:

+ Coalesce small shuffle partitions
+ Split skewed shuffle partitions
+ Switch join strategy at runtime
+ Avoid over-partitioning small outputs

Example:

```python
spark.conf.set("spark.sql.shuffle.partitions", "2000")
spark.conf.set("spark.sql.adaptive.enabled", "true")

result = (
    spark.table("main.silver.orders")
    .groupBy("order_date", "status")
    .agg(F.count("*").alias("orders"))
)
```

Without AQE, Spark may write 2,000 tiny shuffle partitions. With AQE, Spark can coalesce them after seeing runtime sizes.

Interview point: AQE is helpful, but it does not replace good table design, filtering, join hygiene, and skew analysis.

[Table of Contents](#Spark-Tuning)

## When should you cache or persist DataFrames?
Cache only when the same DataFrame is reused multiple times and is expensive to recompute.

Good cache use:

```python
from pyspark import StorageLevel

base = (
    spark.table("main.silver.orders")
    .where("order_date >= date '2026-10-01'")
    .select("order_id", "customer_id", "amount", "order_date")
    .persist(StorageLevel.MEMORY_AND_DISK)
)

high_value = base.where("amount >= 1000").count()
daily = base.groupBy("order_date").agg(F.sum("amount").alias("revenue"))

base.unpersist()
```

Bad cache use:

```python
df = spark.table("main.silver.orders").cache()
df.write.mode("overwrite").saveAsTable("main.tmp.once")
```

If the DataFrame is used once, caching adds overhead. If it is too large for memory, it may evict useful data or spill.

Interview point: caching is a performance tool, not a default habit. Cache after filters and column pruning, materialize it with an action, and unpersist when done.

[Table of Contents](#Spark-Tuning)

## How do you tune file sizes and avoid small files?
Small files slow down Spark because each file creates metadata overhead and often a tiny task. They also hurt table formats because metadata grows.

Small-file symptoms:

+ Thousands of files under a small partition
+ Spark UI shows many tiny input tasks
+ Queries spend time listing files and scheduling tasks
+ Downstream reads are slow even when data volume is modest

Control output partitions before writing:

```python
(
    daily_orders
    .repartition(96, "order_date")
    .write
    .mode("append")
    .partitionBy("order_date")
    .saveAsTable("main.silver.orders")
)
```

For Delta tables on Databricks, compact with `OPTIMIZE`:

```python
spark.sql("optimize main.silver.orders where order_date >= date '2026-10-01'")
```

For Iceberg tables, rewrite data files from an Iceberg-enabled Spark catalog:

```python
spark.sql("""
call uc.system.rewrite_data_files(
  table => 'silver.orders'
)
""")
```

Real-world guidance: target file sizes are workload-dependent, but analytical tables often perform better with files in the hundreds of MB rather than thousands of tiny files.

[Table of Contents](#Spark-Tuning)

## How do you tune partition pruning and predicate pushdown?
Partition pruning skips whole table partitions. Predicate pushdown skips data inside files when file statistics prove rows cannot match.

Good filter:

```python
orders = spark.table("main.silver.orders").where(
    "order_date >= date '2026-10-01' and order_date < date '2026-11-01'"
)
```

Bad filter that can block pruning:

```python
orders = spark.table("main.silver.orders").where(
    "date_format(order_date, 'yyyy-MM') = '2026-10'"
)
```

The bad version wraps the partition column in a function. Spark may not be able to prune partitions efficiently.

Check the plan:

```python
orders.explain("formatted")
```

Look for `PartitionFilters` and `PushedFilters`.

For Unity Catalog tables, keep frequently filtered columns well-modeled. For Delta, consider clustering or liquid clustering where appropriate. For Iceberg, use hidden partition transforms such as `days(event_ts)` or `bucket(32, customer_id)`.

[Table of Contents](#Spark-Tuning)

## How do you reduce data before expensive operations?
Filter rows and select columns before joins, aggregations, and window functions.

Better:

```python
orders = (
    spark.table("main.silver.orders")
    .where("order_date >= date '2026-10-01'")
    .select("order_id", "customer_id", "amount", "order_date")
)

customers = (
    spark.table("main.gold.dim_customer")
    .select("customer_id", "customer_segment")
)

result = orders.join(customers, "customer_id").groupBy("customer_segment").sum("amount")
```

Worse:

```python
result = (
    spark.table("main.silver.orders")
    .join(spark.table("main.gold.dim_customer"), "customer_id")
    .where("order_date >= date '2026-10-01'")
    .groupBy("customer_segment")
    .sum("amount")
)
```

Spark can sometimes push filters and prune columns automatically, but clear code makes intent obvious and helps avoid blockers such as UDFs, complex expressions, or non-deterministic filters.

[Table of Contents](#Spark-Tuning)

## How do you avoid driver memory problems?
The driver coordinates the job. It should not hold the full dataset.

Dangerous patterns:

```python
rows = df.collect()
pdf = df.toPandas()
ids = [row["customer_id"] for row in df.select("customer_id").collect()]
```

Safer alternatives:

```python
df.limit(20).show(truncate=False)
df.write.mode("overwrite").saveAsTable("main.tmp.debug_sample")
```

If you need a Python list for a small dimension, limit it intentionally:

```python
top_ids = [
    row["customer_id"]
    for row in df.select("customer_id").limit(1000).collect()
]
```

Interview point: driver memory failures often come from using Spark like pandas. Keep large data distributed, write results to tables, and collect only bounded samples.

[Table of Contents](#Spark-Tuning)

## How do you tune executor memory and cores?
Executor tuning balances CPU parallelism, memory per task, and cluster utilization. More memory is not always better; too many cores per executor can make each executor run many memory-hungry tasks at once.

Example job configuration:

```python
spark = (
    SparkSession.builder
    .appName("large-orders-aggregation")
    .config("spark.executor.instances", "20")
    .config("spark.executor.cores", "4")
    .config("spark.executor.memory", "16g")
    .config("spark.executor.memoryOverhead", "4g")
    .getOrCreate()
)
```

What to watch:

+ CPU underutilized: not enough partitions or too few cores
+ Frequent GC: executor memory pressure
+ Disk spill: shuffle or aggregation does not fit memory
+ Container killed: memory overhead too low
+ Slow tasks with no spill: skew or remote I/O

Real-world guidance: start with moderate cores per executor, enough memory overhead for Python and off-heap operations, and enough partitions to keep all cores busy. Then tune from Spark UI evidence.

[Table of Contents](#Spark-Tuning)

## How do you tune Structured Streaming jobs?
Streaming tuning focuses on input rate, state size, trigger interval, checkpoint health, and sink throughput.

Example:

```python
events = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("maxFilesPerTrigger", "500")
    .schema("event_id string, user_id string, event_ts timestamp")
    .load("s3://company-raw/events/")
)

query = (
    events
    .withWatermark("event_ts", "30 minutes")
    .dropDuplicates(["event_id"])
    .writeStream
    .option("checkpointLocation", "s3://company-checkpoints/events/")
    .trigger(processingTime="5 minutes")
    .toTable("main.silver.events")
)
```

Tuning levers:

+ Increase trigger interval if each batch cannot finish before the next one starts.
+ Use watermarks to bound state.
+ Control ingestion with `maxFilesPerTrigger` or source-specific rate limits.
+ Avoid expensive `foreachBatch` logic that scans large target tables each batch.
+ Keep checkpoint paths stable and isolated per stream.

Real-world example: a stream that deduplicates by `event_id` without a watermark can keep state forever. The job may run well for a week and then slow down as state grows.

[Table of Contents](#Spark-Tuning)

## What Spark tuning checklist should you use in interviews?
Use this checklist when an interviewer asks, "How would you optimize a slow Spark job?"

+ First inspect the Spark UI and physical plan.
+ Check input size, file count, and partition pruning.
+ Filter rows and select columns early.
+ Avoid Python UDFs unless necessary.
+ Tune joins: broadcast small dimensions, deduplicate dimensions, handle skew.
+ Tune shuffle partitions and enable AQE.
+ Use `repartition` for balancing, `coalesce` for reducing output partitions.
+ Use salting for verified hot keys.
+ Cache only reused expensive DataFrames.
+ Avoid `collect()` and `toPandas()` on large data.
+ Compact small files and write sensible file sizes.
+ Validate improvements with runtime, shuffle metrics, spill metrics, and output correctness.

Strong interview answer: "I would not start by changing executor memory. I would inspect the plan and Spark UI, identify whether the bottleneck is scan, shuffle, skew, join, spill, or output files, then apply the smallest targeted fix and measure again."

[Table of Contents](#Spark-Tuning)

## Real world use cases for Spark tuning

### 1. A nightly job that regressed from 20 minutes to 3 hours

The job was fine until one tenant's data grew. The Spark UI showed stage 7 with one task taking 90% of the time and shuffle spill - classic skew plus too many shuffle partitions.

```python
# Diagnosis: the physical plan and stage metrics told the story
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128m")

# Also stop forcing a huge fixed partition count
spark.conf.set("spark.sql.shuffle.partitions", "auto")
```

Why it worked: AQE coalesced the small post-shuffle partitions and split the skewed join, so runtime dropped back to minutes without changing executor memory at all.

### 2. A join on a hot customer key

One customer produced 40% of all rows, so salting is the targeted fix when AQE skew handling is not enough or the key is used in a non-join shuffle.

```python
from pyspark.sql import functions as F

salt_buckets = 16

large = orders.withColumn("salt", (F.rand() * salt_buckets).cast("int"))
dim = customers.crossJoin(spark.range(salt_buckets).withColumnRenamed("id", "salt"))

joined = large.join(F.broadcast(dim), ["customer_id", "salt"])
```

Why it worked: splitting the hot key into 16 sub-keys lets 16 tasks process it, turning a single straggler task into balanced work. Measure the key distribution first - salting adds a shuffle and is wasted effort if the skew is not real.

### 3. The small-files problem after streaming ingestion

A streaming sink wrote thousands of tiny files per hour. Queries slowed because planning and opening files dominated the scan.

```python
# Compact the partition into fewer, larger files
(
    spark.read.parquet("s3://acme-curated/orders/ds=2026-10-04/")
    .coalesce(8)
    .write.mode("overwrite")
    .parquet("s3://acme-curated/orders_compacted/ds=2026-10-04/")
)

# Prevent the problem at the source where possible
spark.conf.set("spark.sql.files.maxRecordsPerFile", 5_000_000)
spark.conf.set("spark.sql.files.openCostInBytes", 128 * 1024 * 1024)
```

Why it worked: fewer files meant fewer tasks and less per-file overhead. On a table format, run the platform compaction (`OPTIMIZE`, `rewrite_data_files`) instead of rewriting files yourself.

### 4. A broadcast join that stopped broadcasting

A "small" product dimension grew past the broadcast threshold, so every nightly run shuffled both sides.

```python
# Raise the threshold deliberately (and know the driver memory cost)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 64 * 1024 * 1024)

# Or force it when you know the relation is small
joined = events.join(F.broadcast(products), "product_id")
```

Why it worked: a broadcast avoids the shuffle entirely. The trade-off is driver memory and broadcast time - never broadcast a relation you have not checked the size of.

### 5. Streaming latency that kept climbing

A Structured Streaming job fell behind because each micro-batch tried to consume everything available, producing ever-larger batches.

```python
stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "orders")
    .option("maxOffsetsPerTrigger", 500_000)     # bound each micro-batch
    .load()
)

(
    stream.writeStream
    .option("checkpointLocation", "s3://acme-checkpoints/orders/")
    .trigger(processingTime="2 minutes")
    .start()
)
```

Why it worked: `maxOffsetsPerTrigger` caps batch size so each batch finishes before the next arrives, and the fixed trigger makes throughput predictable. Also check watermarking and state-store growth for stateful operators.

### 6. Driver OOM from collecting results

The driver died whenever a job called `collect()` or `toPandas()` on a large DataFrame.

```python
# Before: pulls every row into the driver
rows = df.collect()

# After: aggregate in the cluster and bring back one row
summary = df.agg(F.sum("amount").alias("total")).first()

# For small samples only, cap what crosses the network
sample = df.limit(1000).toPandas()
```

Why it worked: the driver is for coordination, not data. Aggregations and `limit` keep results inside the cluster, and only small results cross to the driver.

[Table of Contents](#Spark-Tuning)
