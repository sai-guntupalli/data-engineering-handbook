## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Hudi

**Notebook:** [`notebooks/topics/hudi.ipynb`](../notebooks/topics/hudi.ipynb) - runnable version of this topic with self-checking exercises.

Apache Hudi (Hadoop Upserts Deletes and Incrementals) is an open table format and lakehouse framework that brings database-like primitives to object storage: record-level upserts, deletes, incremental pulls, and pluggable table services. It was created at Uber in 2016 to keep petabyte-scale trip tables fresh without rebuilding partitions.
+ [What is Apache Hudi?](#What-is-Apache-Hudi)
+ [What problems does Hudi solve in a data lake?](#What-problems-does-Hudi-solve-in-a-data-lake)
+ [What are Hudi's table types and physical file layout?](#What-are-Hudis-table-types-and-physical-file-layout)
+ [How does Hudi handle upserts and deletes?](#How-does-Hudi-handle-upserts-and-deletes)
+ [How does Hudi support upserts?](#How-does-Hudi-support-upserts)
+ [What is a record key, partition path, and precombine field?](#What-is-a-record-key-partition-path-and-precombine-field)
+ [How do you write and upsert data with Hudi in PySpark?](#How-do-you-write-and-upsert-data-with-Hudi-in-PySpark)
+ [What indexes does Hudi use to find records quickly?](#What-indexes-does-Hudi-use-to-find-records-quickly)
+ [What is the difference between Copy-on-Write and Merge-on-Read in Hudi?](#What-is-the-difference-between-Copy-on-Write-and-Merge-on-Read-in-Hudi)
+ [What is the difference between Copy-on-Write (COW) and Merge-on-Read (MOR)?](#What-is-the-difference-between-Copy-on-Write-COW-and-Merge-on-Read-MOR)
+ [How do you choose between COW and MOR?](#How-do-you-choose-between-COW-and-MOR)
+ [What are the Hudi query types and how do you run an incremental pull?](#What-are-the-Hudi-query-types-and-how-do-you-run-an-incremental-pull)
+ [What is compaction in Hudi?](#What-is-compaction-in-Hudi)
+ [What is clustering in Hudi and when do you need it?](#What-is-clustering-in-Hudi-and-when-do-you-need-it)
+ [Why does the small files problem happen and how do you mitigate it in Hudi?](#Why-does-the-small-files-problem-happen-and-how-do-you-mitigate-it-in-Hudi)
+ [What table services does Hudi run and how do you schedule them?](#What-table-services-does-Hudi-run-and-how-do-you-schedule-them)
+ [How do you handle CDC with Hudi?](#How-do-you-handle-CDC-with-Hudi)
+ [What are common operational metrics for Hudi tables?](#What-are-common-operational-metrics-for-Hudi-tables)
+ [When would you choose Hudi vs Iceberg vs Delta?](#When-would-you-choose-Hudi-vs-Iceberg-vs-Delta)
+ [Real world use cases for Apache Hudi](#Real-world-use-cases-for-Apache-Hudi)

## What is Apache Hudi?
Apache Hudi is an open-source data lakehouse framework that brings database-like capabilities (upserts, deletes, incremental pulls) to data lakes on object storage. It manages table metadata and timelines so batch and streaming engines can write and read consistently. Hudi is not a query engine: Spark, Flink, Trino, Presto, Hive, and BigQuery-style external readers use Hudi metadata to read the same table.

Hudi's differentiators versus a plain Parquet dataset:

+ A **timeline** in `.hoodie/` records every instant (commit, deltacommit, compaction, clean, replacecommit) and lets readers see a consistent snapshot.
+ A **record key index** lets an upsert locate the file group holding a key instead of rewriting the whole table.
+ **Table services** (compaction, clustering, cleaning, archival) run inline or asynchronously to keep the table healthy.
+ **Incremental queries** return only records changed since an instant, which enables streaming-on-batch pipelines.

```text
Spark / Flink / DeltaStreamer
        |
        v
s3://lake/hudi/orders/
  .hoodie/                 table metadata + timeline
    hoodie.properties
    metadata/              metadata table (files + column stats index)
    20261004013000.commit    completed instant
    20261004020000.deltacommit
  order_date=2026-10-04/   partitions
    <fileId>_<token>_<instant>.parquet     base files
```

A first write and read in PySpark:

```python
hudi_options = {
    "hoodie.table.name": "orders_hudi",
    "hoodie.datasource.write.recordkey.field": "order_id",
    "hoodie.datasource.write.partitionpath.field": "order_date",
    "hoodie.datasource.write.precombine.field": "updated_at",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.keygenerator.class": "org.apache.hudi.keygen.SimpleKeyGenerator",
}

(
    orders_df.write.format("hudi")
    .options(**hudi_options)
    .mode("append")
    .save("s3://lake/hudi/orders")
)

orders = spark.read.format("hudi").load("s3://lake/hudi/orders")
```

Interview framing: Hudi is the format you reach for when the dominant workload is continuous upsert/delete ingestion, when you need incremental pull as a first-class read mode, and when you want table services managed inside the write path.

[Table of Contents](#Apache-Hudi)

## What problems does Hudi solve in a data lake?
Hudi enables efficient updates and deletes without rewriting entire datasets, supports incremental processing (read only changes), and helps manage small files and write amplification. It is commonly used for near-real-time ingestion and CDC-style workloads where tables must be kept up-to-date.

Concretely, Hudi solves five recurring data-lake problems:

+ **Updating a small fraction of a large table.** Rewriting 50 TB of Parquet to change 1% of rows is wasteful. Hudi rewrites only the affected file groups.
+ **Deletes and GDPR erasure.** Path-based lakes cannot delete a single customer's rows cheaply. Hudi supports record-level deletes and a delete-marker payload for soft deletes.
+ **Incremental processing.** Extracting "what changed since the last run" from Parquet means scanning and diffing. Hudi's incremental query returns exactly the changed records since an instant.
+ **Small files and write amplification.** Frequent micro-batch ingestion creates thousands of tiny files. Hudi's file-sizing, cleaning, and clustering services bound file counts and file sizes.
+ **Consistency for concurrent readers and writers.** A commit either fully succeeds or is rolled back; readers see the last successful instant even while writers are appending.

Non-goals worth stating in an interview: Hudi is not a compute engine, not a replacement for a warehouse's SQL optimizer, and not a low-latency point-lookup store. It optimizes lake-scale analytical ingestion, not OLTP.

[Table of Contents](#Apache-Hudi)

## What are Hudi's table types and physical file layout?
Hudi has two table types, `COPY_ON_WRITE` (COW) and `MERGE_ON_READ` (MOR), and a file-group abstraction shared by both.

+ A **file group** is identified by a stable `fileId` and lives in one partition. All versions of a record's data land in the same file group, which is what makes the index lookup cheap.
+ A **base file** is a columnar file, usually Parquet, named `<fileId>_<writeToken>_<instantTime>.parquet`.
+ A **log file** (MOR only) is an Avro-encoded delta log named `.<fileId>_<baseInstantTime>.log.<version>_<writeToken>`; it holds changes until compaction folds them into a new base file.
+ The **`.hoodie` directory** holds `hoodie.properties` (table config), the active timeline, archived timeline, and the optional metadata table.

```text
s3://lake/hudi/orders/
  .hoodie/
    hoodie.properties
    20261004013000.commit
    20261004020000.commit.requested
    metadata/
      files/            file listing index
      column_stats/     column statistics index
  order_date=2026-10-04/
    7f3a2c1b-...-0_20261004013000.parquet
    .7f3a2c1b-...-0_20261004013000.log.1_20261004020000
```

Timeline actions you should be able to name:

| Action | Meaning |
|---|---|
| `commit` | A completed COW write |
| `deltacommit` | A completed MOR write that appended log files |
| `replacecommit` | Atomically replaces file groups; used by clustering and insert-overwrite |
| `compaction` | Folds MOR log files into new base files |
| `clean` | Deletes old file versions and log files beyond retention |
| `rollback` | Removes a failed or aborted instant's files |
| `savepoint` | Pins a file version so cleaning cannot remove it |

Inspect the layout from Spark:

```python
meta = spark.read.format("hudi").load("s3://lake/hudi/orders")
meta.select("_hoodie_commit_time", "_hoodie_file_name", "_hoodie_partition_path").show(5, truncate=False)
```

Every Hudi record carries hidden metadata columns: `_hoodie_commit_time`, `_hoodie_commit_seqno`, `_hoodie_record_key`, `_hoodie_partition_path`, and `_hoodie_file_name`. They are how Hudi tracks record provenance per row.

[Table of Contents](#Apache-Hudi)

## How does Hudi handle upserts and deletes?
Hudi manages record-level changes on a data lake table using a record key, precombine field, and table timeline. It can apply inserts, updates, and deletes efficiently compared with rewriting an entire dataset.

The mechanics of one upsert batch:

1. Hudi reads the input records, computes each record key, and resolves duplicates using the precombine field.
2. The index maps each key to an existing file group, or tags the record as an insert for a new file group.
3. Hudi groups records by file group, reads only those base files (plus log files on MOR), merges the new records, and writes the result.
4. A new instant is committed to the timeline; readers atomically switch to the new snapshot.

Deletes come in two flavours:

+ **Hard delete**: the record is physically removed via the `delete` operation, which targets the file groups holding the keys.
+ **Soft delete**: the record is written with a null ordering value (or a delete marker), so readers filter it out while the row remains for audit. Hudi's `DefaultHoodieRecordPayload` treats a record whose precombine value is null as a delete.

```python
# Hard delete of two orders
spark.createDataFrame([("order-1001",), ("order-1002",)], ["order_id"]) \
    .write.format("hudi") \
    .option("hoodie.table.name", "orders_hudi") \
    .option("hoodie.datasource.write.recordkey.field", "order_id") \
    .option("hoodie.datasource.write.partitionpath.field", "order_date") \
    .option("hoodie.datasource.write.operation", "delete") \
    .option("hoodie.datasource.write.keygenerator.class", "org.apache.hudi.keygen.NonpartitionedKeyGenerator") \
    .mode("append") \
    .save("s3://lake/hudi/orders_nopartition")
```

Failure modes to mention: late-arriving events with an older precombine value are ignored (correctly), but events without a reliable ordering column produce non-deterministic results. Duplicate keys inside one batch are resolved by precombine, so choose a column that is monotonic and never null for real updates.

[Table of Contents](#Apache-Hudi)

## How does Hudi support upserts?
Hudi indexes records by key and can locate existing records to update them. On upsert, it writes new versions and updates the timeline/metadata so readers see a consistent view. Correctness depends on stable keys and proper handling of late and duplicate events.

The value of the index is asymmetric cost: without it, Spark would have to shuffle the entire table against the incoming batch. With it, Hudi reads only the file groups that contain touched keys.

```text
incoming batch (1M changed orders)
    -> key generation (order_id)
    -> index lookup (bloom filter / HFile / bucket)
    -> touched file groups (2,000 of 500,000)
    -> merge + write 2,000 new base files
```

Guidance for reliable upserts:

+ Choose a stable, immutable record key. If the key changes when the business entity changes, you get duplicates instead of updates.
+ Provide a precombine field that reflects event time (`updated_at`, `source_lsn`) rather than ingestion time; otherwise replays and late events win incorrectly.
+ Keep record keys evenly distributed so the shuffle and the index do not create a single hot task.
+ Control the `hoodie.upsert.shuffle.parallelism` to roughly match data volume; too few tasks cause long, memory-heavy merges.
+ Use `bulk_insert` for the initial historical load and `upsert` only for incremental changes; bulk insert skips the index and is far faster for empty tables.

[Table of Contents](#Apache-Hudi)

## What is a record key, partition path, and precombine field?
Record key identifies a row uniquely (like a primary key). Partition path controls how data is grouped for storage and pruning. Precombine field is used to resolve multiple records for the same key in a batch (for example choose the latest by `updated_at`) to ensure deterministic upserts.

```text
record key: order_id
precombine field: updated_at
partition path: order_date
```

```python
{
    "hoodie.datasource.write.recordkey.field": "order_id",
    "hoodie.datasource.write.precombine.field": "updated_at",
    "hoodie.datasource.write.partitionpath.field": "order_date",
    "hoodie.datasource.write.keygenerator.class": "org.apache.hudi.keygen.SimpleKeyGenerator",
}
```

Practical rules:

+ The partition path must be derivable from the record or supplied as a literal string. A partition column with thousands of values (for example `order_id`) creates tiny partitions and destroys file sizing.
+ Composite record keys are supported with `ComplexKeyGenerator` and a comma-separated list, for example `"tenant_id,order_id"`.
+ Timestamp-derived partitions use `TimestampBasedKeyGenerator` with `hoodie.keygen.timebased.timestamp.type` and format options.
+ The precombine comparison is per key. Ties (equal ordering values) are resolved deterministically by the payload, but you should not depend on arbitrary tie-breaking; make the ordering value unique per event where possible.
+ Non-partitioned tables use `NonpartitionedKeyGenerator` and live entirely at the table root, which is fine for small tables but loses pruning on large ones.

[Table of Contents](#Apache-Hudi)

## How do you write and upsert data with Hudi in PySpark?
A Hudi write is a normal `DataFrameWriter` with Hudi options. The options decide table type, operation, key semantics, indexing, and table services. This is the example most interviews ask you to produce from memory.

```python
hudi_options = {
    "hoodie.table.name": "orders_hudi",
    "hoodie.datasource.write.recordkey.field": "order_id",
    "hoodie.datasource.write.partitionpath.field": "order_date",
    "hoodie.datasource.write.precombine.field": "updated_at",
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.datasource.write.keygenerator.class": "org.apache.hudi.keygen.SimpleKeyGenerator",
    "hoodie.datasource.write.hive_style_partitioning": "true",
    "hoodie.index.type": "BLOOM",
    "hoodie.upsert.shuffle.parallelism": "200",
    "hoodie.parquet.max.file.size": "134217728",
    "hoodie.parquet.small.file.limit": "104857600",
    "hoodie.metadata.enable": "true",
    "hoodie.clean.automatic": "true",
    "hoodie.cleaner.policy": "KEEP_LATEST_COMMITS",
    "hoodie.cleaner.commits.retained": "10",
    "hoodie.compact.inline": "true",
    "hoodie.compact.inline.max.delta.commits": "5",
}

(
    orders_df.write.format("hudi")
    .options(**hudi_options)
    .mode("append")
    .save("s3://lake/hudi/orders")
)
```

Initial historical load with bulk insert (no index lookup, fastest path into an empty table):

```python
bulk_options = dict(hudi_options, **{
    "hoodie.datasource.write.operation": "bulk_insert",
    "hoodie.bulkinsert.shuffle.parallelism": "400",
    "hoodie.bulkinsert.user.defined.partitioner.class": "org.apache.hudi.execution.bulkinsert.RDDCustomColumnsSortPartitioner",
    "hoodie.bulkinsert.user.defined.partitioner.sort.columns": "order_id",
})

history_df.write.format("hudi").options(**bulk_options).mode("overwrite").save("s3://lake/hudi/orders")
```

Insert-overwrite for a full partition replacement (for example reprocessing one business day):

```python
reprocess_options = dict(hudi_options, **{
    "hoodie.datasource.write.operation": "insert_overwrite",
    "hoodie.datasource.write.partitionpath.field": "order_date",
})

(
    corrected_day_df.write.format("hudi")
    .options(**reprocess_options)
    .mode("append")
    .save("s3://lake/hudi/orders")
)
```

Interview notes:

+ `operation=upsert` with `mode("append")` is the normal incremental path; `mode("overwrite")` on an existing table is usually wrong and can wipe history.
+ `hoodie.datasource.write.table.type` is fixed when the table is created. Converting COW to MOR requires a rewrite or a migration job.
+ In Databricks you can register the Hudi table in Unity Catalog with `CREATE TABLE ... USING hudi LOCATION ...`, but check runtime support for the Hudi version you depend on.
+ Keep the Hudi bundle version aligned with the Spark version (`hudi-spark3.5-bundle_2.12` for Spark 3.5), because Hudi and Spark internals are tightly coupled.

[Table of Contents](#Apache-Hudi)

## What indexes does Hudi use to find records quickly?
Hudi's index maps record keys to file groups so an upsert only touches affected files. The index choice is one of the biggest levers on upsert latency and write amplification.

| Index | How it works | Best for |
|---|---|---|
| `BLOOM` (default) | Bloom filter per base file, probed by the incoming keys | Large partitioned tables, most upsert workloads |
| `SIMPLE` | Keeps a full key-to-file map in memory | Small tables that fit in executor memory |
| `GLOBAL_BLOOM` | Bloom filter across all partitions | Global uniqueness when keys can move partitions |
| `HFILE` | Stores the key map in an HFile per file group | Large tables where a persistent, fast lookup beats recomputing blooms |
| `BUCKET` | Hash of the key determines the file group; no lookup at all | Streaming ingestion with a fixed bucket count |

```python
{
    "hoodie.index.type": "BLOOM",
    "hoodie.bloom.index.parallelism": "100",
    "hoodie.bloom.index.prune.by.runtime.filter": "true",
    "hoodie.bloom.index.update.partition.path": "true",
    "hoodie.metadata.enable": "true",
}
```

```python
# Bucket index removes the lookup entirely but fixes the file layout at creation time.
{
    "hoodie.index.type": "BUCKET",
    "hoodie.index.bucket.engine": "CONSISTENT_HASHING",
    "hoodie.bucket.index.num.buckets": "64",
    "hoodie.storage.layout.partitioner.class": "org.apache.hudi.table.action.commit.SparkBucketIndexPartitioner",
}
```

Trade-offs interviewers look for:

+ Bloom indexes trade memory and CPU on every upsert for flexibility; bucket indexes trade flexibility for near-zero lookup cost.
+ `BLOOM` can produce false positives, which only cause an unnecessary file read, never a wrong result.
+ Global indexes cost more because the key space spans partitions; use local indexes unless keys genuinely move between partitions.
+ The metadata table (`hoodie.metadata.enable=true`) stores the files index and column statistics index, which speeds up query planning by avoiding repeated object-store listing. It is effectively mandatory on cloud object storage.

[Table of Contents](#Apache-Hudi)

## What is the difference between Copy-on-Write and Merge-on-Read in Hudi?
Copy-on-Write rewrites columnar files during updates, making reads simpler and faster but writes heavier. Merge-on-Read writes changes to log files and compacts later, making ingestion faster but reads more complex until compaction occurs.

In COW, an upsert reads the affected base file, merges the records, and writes a brand-new base file. There are no log files, so every reader sees fully materialized Parquet. File versioning plus cleaning keeps storage bounded.

```text
COW upsert of 1 record in a 500 MB file:
  read 500 MB + write 500 MB  ->  read amplification on writes, zero merge cost on reads
```

In MOR, an upsert appends an Avro log file and returns quickly. Readers either read the base files only (`read_optimized`, stale but fast) or merge base plus logs (`snapshot`, fresh but more CPU).

```text
MOR upsert of 1 record:
  append a few KB to a log file  ->  fast write, read-time merge until compaction
```

Example choice:

+ Copy-on-Write: BI table with frequent reads and moderate updates
+ Merge-on-Read: high-volume CDC ingestion where write latency matters

The best choice depends on read latency, write frequency, compaction operations, and query engine support. COW also interacts better with some engines that cannot read Hudi log files, so verify engine capability before choosing MOR.

[Table of Contents](#Apache-Hudi)

## What is the difference between Copy-on-Write (COW) and Merge-on-Read (MOR)?
COW stores data in columnar files and rewrites them on updates, optimizing read performance at the cost of write amplification. MOR stores base files plus delta log files and merges them at read time (or during compaction), optimizing write performance at the cost of more complex reads.

| Dimension | COW | MOR |
|---|---|---|
| Upsert write cost | Rewrites affected base files | Appends small log files |
| Read cost (snapshot) | Low, pure columnar | Higher, merges base + logs |
| Read cost (read_optimized) | Same as snapshot | Ignores logs, may be stale |
| Storage overhead | Multiple file versions until cleaning | Versions plus log files |
| Compaction requirement | None | Essential; backlog degrades reads |
| Streaming ingestion | Higher latency | Low latency |
| Engine compatibility | Broadest | Requires Hudi-aware readers for logs |
| Typical partition size | Moderate to large | Large, write-heavy |

Config snapshots of each table type:

```python
cow = {
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.parquet.max.file.size": "134217728",
}

mor = {
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.compact.inline": "true",
    "hoodie.compact.inline.max.delta.commits": "5",
    "hoodie.logfile.max.size": "1073741824",
}
```

Interview trap: MOR with a large compaction backlog looks fast to write and terrible to read. Always pair MOR with an explicit compaction SLA and alerting on delta-commit lag.

[Table of Contents](#Apache-Hudi)

## How do you choose between COW and MOR?
Choose COW when read latency and query simplicity are most important and updates are moderate. Choose MOR when write throughput and near-real-time updates are critical, and you can manage compaction and read-time merges. The choice also depends on engine support and operational constraints.

A decision checklist:

+ If updates touch a small fraction of rows and reads dominate, COW is usually cheaper end to end.
+ If ingestion is a continuous stream and a 5-15 minute freshness SLA matters, MOR ingests faster and compacts on a schedule.
+ If downstream engines cannot read Hudi log files, COW avoids a whole class of compatibility problems.
+ If write amplification is the bottleneck (network or object-store PUT limits), MOR is the escape valve.
+ If your team cannot operate a compaction job reliably, prefer COW; an unmanaged MOR table degrades continuously.

```python
# Heuristic: pick MOR for streaming, COW for batch + BI.
def pick_table_type(rows_per_hour: int, readers: int, freshness_minutes: int) -> str:
    if freshness_minutes <= 15 and readers < 5:
        return "MERGE_ON_READ"
    return "COPY_ON_WRITE"


print(pick_table_type(rows_per_hour=2_000_000, readers=1, freshness_minutes=5))
print(pick_table_type(rows_per_hour=50_000, readers=40, freshness_minutes=60))
```

Cost note: MOR reduces write cost but can increase read cost and storage until cleaning runs. The honest answer is often "COW for the curated BI table, MOR for the bronze ingestion table."

[Table of Contents](#Apache-Hudi)

## What are the Hudi query types and how do you run an incremental pull?
Hudi exposes three query types from Spark, selected with `hoodie.datasource.query.type`.

+ `snapshot` (default): the latest committed view. On MOR it merges base files with log files at read time.
+ `read_optimized`: base files only. On COW it is identical to snapshot; on MOR it returns the last compacted state and can be stale.
+ `incremental`: only records committed in a given instant range, which powers incremental pipelines and CDC sinks.

```python
# Snapshot read (latest data, merges MOR logs)
snapshot_df = (
    spark.read.format("hudi")
    .option("hoodie.datasource.query.type", "snapshot")
    .load("s3://lake/hudi/orders")
)

# Read-optimized read (fast, base files only)
ro_df = (
    spark.read.format("hudi")
    .option("hoodie.datasource.query.type", "read_optimized")
    .load("s3://lake/hudi/orders")
)
```

Incremental pull with a saved checkpoint:

```python
begin = "20261004000000000"   # last processed Hudi instant
end = "20261005000000000"     # inclusive upper bound; omit for "up to now"

changes = (
    spark.read.format("hudi")
    .option("hoodie.datasource.query.type", "incremental")
    .option("hoodie.datasource.read.begin.instanttime", begin)
    .option("hoodie.datasource.read.end.instanttime", end)
    .option("hoodie.datasource.read.incr.fallback.fulltablescan.enable", "false")
    .load("s3://lake/hudi/orders")
)

changes.write.mode("append").parquet("s3://lake/silver/orders_changes/")
```

Notes:

+ Persist the last committed instant in a control table; Hudi instants are the checkpoint. Reusing the same begin instant replays changes, so downstream must be idempotent.
+ Incremental queries on MOR pick up records from log files, which is why they are the standard CDC fan-out mechanism.
+ `read_optimized` is the right choice for dashboards that tolerate staleness but need predictable latency.
+ `_hoodie_commit_time` on each row tells you when that record version was committed, useful for debugging replay.

[Table of Contents](#Apache-Hudi)

## What is compaction in Hudi?
Compaction merges delta log files into base columnar files (mostly relevant for MOR tables). It improves read performance and reduces the overhead of reading many log files. Compaction must be scheduled and monitored to avoid backlog.

Compaction has two phases: a **planning** phase that writes a `compaction.requested` instant, and an **execution** phase that writes new base files and commits a `commit` that retires the log files.

Inline compaction (simple, but competes with ingestion):

```python
{
    "hoodie.compact.inline": "true",
    "hoodie.compact.inline.max.delta.commits": "5",
    "hoodie.compact.inline.trigger.strategy": "NUM_COMMITS",
}
```

Async or scheduled compaction from a separate job, using Spark SQL procedures:

```python
spark.sql("call run_compaction(op => 'schedule', table => 'orders_hudi')")
spark.sql("call run_compaction(op => 'run', table => 'orders_hudi')")
```

Or schedule then run as a standalone Spark job:

```bash
spark-submit \
  --class org.apache.hudi.utilities.HoodieCompactor \
  --packages org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0 \
  --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
  /opt/hudi/hudi-utilities-bundle.jar \
  --base-path s3://lake/hudi/orders \
  --table-name orders_hudi \
  --instant-time 20261005000000000 \
  --parallelism 100 \
  --spark-memory 4g
```

Operational guidance:

+ Give compaction its own resources so a large compaction does not starve ingestion.
+ Choose the trigger by delta-commit count or time, and alert on `hoodie.compaction.lag` in instants.
+ Compaction reads log files and rewrites base files, so it is I/O heavy; run it off-peak for large tables.
+ A compaction that keeps failing means readers keep merging an ever-growing log set, which is the classic MOR read-latency incident.

[Table of Contents](#Apache-Hudi)

## What is clustering in Hudi and when do you need it?
Clustering reorganizes data files to improve layout (file sizes, sorting, locality) and query performance. You use clustering to combat small files, improve pruning, or optimize for common access patterns (for example sorting by event time).

Clustering rewrites selected file groups into better-shaped ones and commits the swap atomically as a `replacecommit`, so readers never see a partial state.

```python
{
    "hoodie.clustering.inline": "true",
    "hoodie.clustering.inline.max.commits": "4",
    "hoodie.clustering.plan.strategy.target.file.max.bytes": "1073741824",
    "hoodie.clustering.plan.strategy.small.file.limit": "314572800",
    "hoodie.clustering.plan.strategy.sort.columns": "order_date,updated_at",
}
```

Scheduled clustering with procedures or the standalone job:

```python
spark.sql("call run_clustering(table => 'orders_hudi')")
```

```bash
spark-submit \
  --class org.apache.hudi.utilities.HoodieClusteringJob \
  --packages org.apache.hudi:hudi-spark3.5-bundle_2.12:0.15.0 \
  /opt/hudi/hudi-utilities-bundle.jar \
  --base-path s3://lake/hudi/orders \
  --table-name orders_hudi \
  --mode scheduleAndExecute \
  --parallelism 50
```

When clustering pays off:

+ After many small streaming commits, to consolidate hundreds of tiny files.
+ To sort data by a high-selectivity column so Parquet min/max statistics prune more row groups.
+ To change file sizing as data volume grows, without rewriting the whole table.
+ To fix skewed partitions, though a better partition key is usually the real fix.

Trade-offs: clustering is expensive (it rewrites data and can be GBs per run), it creates a new file version that cleaning must eventually remove, and inline clustering adds latency to the ingestion job. Schedule it rather than running it inline on busy pipelines.

[Table of Contents](#Apache-Hudi)

## Why does the small files problem happen and how do you mitigate it in Hudi?
It happens when writers commit frequently with small batches or when partitions are highly granular. Mitigations include tuning write parallelism and file sizing, using clustering/compaction, and adjusting partitioning strategy to reduce tiny partitions.

Root causes:

+ Micro-batch streaming commits every minute, each writing a few MB.
+ Too many shuffle partitions, so each Spark task writes a tiny file.
+ Over-partitioning, for example by `order_id` or by hour on low-volume data.
+ `bulk_insert` with parallelism far higher than the data volume.

File-sizing and parallelism options:

```python
{
    "hoodie.parquet.max.file.size": "134217728",
    "hoodie.parquet.small.file.limit": "104857600",
    "hoodie.parquet.compression.ratio": "0.35",
    "hoodie.insert.shuffle.parallelism": "200",
    "hoodie.upsert.shuffle.parallelism": "200",
    "hoodie.bulkinsert.shuffle.parallelism": "200",
    "hoodie.copyonwrite.insert.split.size": "500000",
}
```

Mitigation strategy, in order of preference:

1. Write fewer, larger commits: a 5-minute micro-batch of 500 MB is far healthier than a 1-minute batch of 100 MB.
2. Set `hoodie.parquet.small.file.limit` so Hudi merges new records into existing small files instead of creating new ones.
3. Right-size shuffle parallelism: target roughly `data_size / 128 MB` tasks, not a fixed 200.
4. Coarsen partitioning. Daily partitions with 2-5 GB each are usually better than hourly partitions with 100 MB each.
5. Run clustering to consolidate existing files and sort them for pruning.
6. Schedule cleaning so old file versions do not inflate file counts and storage.

Interview answer: prevention is better than cleanup. Choose sane partitioning, batch enough data per commit, and tune Spark writer parallelism before reaching for clustering.

[Table of Contents](#Apache-Hudi)

## What table services does Hudi run and how do you schedule them?
Hudi table services are background operations that keep the table healthy. They can run inline inside a write or asynchronously in separate jobs.

| Service | Purpose | Key config |
|---|---|---|
| Compaction | Fold MOR log files into base files | `hoodie.compact.inline`, `hoodie.compact.inline.max.delta.commits` |
| Clustering | Reorganize file sizes and sort order | `hoodie.clustering.inline`, `hoodie.clustering.plan.strategy.sort.columns` |
| Cleaning | Delete old file versions and log files | `hoodie.clean.automatic`, `hoodie.cleaner.policy`, `hoodie.cleaner.commits.retained` |
| Archival | Move old timeline instants out of the active timeline | `hoodie.archivelog.folder`, `hoodie.keep.min.commits` |
| Indexing | Maintain the metadata table and stats index | `hoodie.metadata.enable`, `hoodie.metadata.index.column.stats.enable` |
| Rollback | Remove files from failed instants | automatic on failure |
| Savepoint | Pin a version so cleaning cannot delete it | `call create_savepoint(...)` |

Cleaning and metadata configuration:

```python
{
    "hoodie.clean.automatic": "true",
    "hoodie.cleaner.policy": "KEEP_LATEST_COMMITS",
    "hoodie.cleaner.commits.retained": "10",
    "hoodie.metadata.enable": "true",
    "hoodie.metadata.index.column.stats.enable": "true",
    "hoodie.archivelog.folder": "archived",
}
```

Run services from SQL procedures (Hudi 0.14+):

```python
spark.sql("call run_compaction(op => 'schedule', table => 'orders_hudi')")
spark.sql("call run_clean(table => 'orders_hudi', retain_commits => 10)")
spark.sql("call run_clustering(table => 'orders_hudi')")
spark.sql("call show_commits(table => 'orders_hudi', limit => 10)")
```

Scheduling guidance:

+ Keep inline services for small tables and simple pipelines; move them async once ingestion is continuous or tables exceed a few TB.
+ Give async services their own Spark job and resources so ingestion SLAs are unaffected.
+ Monitor service lag, not just success: a clean or compaction job that runs but cannot keep up is still an incident.
+ Take a savepoint before risky schema or partition changes so you can roll back to a known instant.

[Table of Contents](#Apache-Hudi)

## How do you handle CDC with Hudi?
Hudi can ingest CDC events and apply them as upserts/deletes to maintain a current-state table. You typically standardize event ordering and deduplication (record key + precombine field) and monitor lag/compaction. Some setups also keep an append-only log for auditing alongside the current-state table.

Typical ingestion paths:

+ **DeltaStreamer** reads Kafka or a source table, deduplicates by record key and precombine, and upserts into Hudi.
+ **Kafka Connect Hudi sink** writes connector output directly into a Hudi table.
+ **Flink Hudi connector** consumes a changelog stream and supports `changelog` mode for `INSERT`/`UPDATE_BEFORE`/`UPDATE_AFTER`/`DELETE`.
+ **Spark Structured Streaming** with `foreachBatch` calling the Hudi datasource per micro-batch.

```python
def upsert_micro_batch(batch_df, batch_id: int) -> None:
    deduped = batch_df.dropDuplicates(["order_id"])

    (
        deduped.write.format("hudi")
        .option("hoodie.table.name", "orders_hudi")
        .option("hoodie.datasource.write.recordkey.field", "order_id")
        .option("hoodie.datasource.write.partitionpath.field", "order_date")
        .option("hoodie.datasource.write.precombine.field", "source_lsn")
        .option("hoodie.datasource.write.operation", "upsert")
        .option("hoodie.datasource.write.table.type", "MERGE_ON_READ")
        .option("hoodie.datasource.write.keygenerator.class", "org.apache.hudi.keygen.SimpleKeyGenerator")
        .mode("append")
        .save("s3://lake/hudi/orders")
    )


(
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "orders.cdc")
    .load()
    .selectExpr("CAST(value AS STRING) AS json")
    .select(from_json("json", schema).alias("r"))
    .select("r.*")
    .writeStream
    .foreachBatch(upsert_micro_batch)
    .option("checkpointLocation", "s3://lake/checkpoints/orders_cdc/")
    .trigger(processingTime="5 minutes")
    .start()
)
```

CDC guidance and failure modes:

+ Order by a source log sequence number (`source_lsn`, `binlog_pos`) rather than wall-clock time; clock skew across shards breaks precombine ordering.
+ Handle tombstones explicitly: a delete event must either use `operation=delete` or carry a null ordering value for soft deletion.
+ Deduplicate within a micro-batch before the upsert, otherwise Hudi resolves duplicates by precombine and you lose the ability to log them.
+ Keep an append-only bronze table of raw CDC events for replay and audit; the Hudi current-state table should be reproducible from it.
+ Watch end-to-end lag: Kafka consumer lag plus commit latency plus compaction backlog.

[Table of Contents](#Apache-Hudi)

## What are common operational metrics for Hudi tables?
Common metrics include commit/compaction backlog, file counts per partition, average file size, write latency, failed commits, and query scan metrics. Operational alerts often focus on increasing small files and compaction lag.

Concrete signals to instrument:

+ **Commit duration and rate**: time from batch start to commit on the timeline; alert on p95 regression.
+ **Compaction lag**: number of delta commits since the last compaction, and pending compaction instants. This is the single most important MOR metric.
+ **Clean backlog**: number of file versions beyond retention, and archive timeline growth.
+ **File metrics**: file count per partition, average and p95 file size, small-file ratio, and file-group count.
+ **Write amplification**: bytes read versus bytes written per upsert batch; a ratio near 10x means the index or partition strategy is wrong.
+ **Failed and rolled-back instants**: any rollback deserves investigation.
+ **Metadata table health**: metadata table size and files index freshness.
+ **Read metrics**: scan bytes, snapshot versus read-optimized latency, and query planning time (which improves with the metadata table).

Enable metrics reporters:

```python
{
    "hoodie.metrics.on": "true",
    "hoodie.metrics.reporter.type": "PROMETHEUS",
    "hoodie.metrics.pushgateway.host": "pushgateway.internal",
    "hoodie.metrics.pushgateway.port": "9091",
    "hoodie.metrics.executor.enable": "true",
}
```

Inspect the timeline and file layout directly:

```python
spark.sql("call show_commits(table => 'orders_hudi', limit => 20)").show(truncate=False)
spark.sql("call show_fsview_all(table => 'orders_hudi')").show(truncate=False)

files = (
    spark.read.format("hudi")
    .load("s3://lake/hudi/orders")
    .select("_hoodie_partition_path", "_hoodie_file_name")
    .groupBy("_hoodie_partition_path")
    .count()
)
```

Alerting that works in practice: page on compaction lag exceeding SLA, page on failed commits, and warn on a rising small-file ratio or a growing write-amplification ratio.

[Table of Contents](#Apache-Hudi)

## When would you choose Hudi vs Iceberg vs Delta?
Hudi is often chosen for CDC-heavy and upsert/delete workloads with near-real-time ingestion requirements. Iceberg is often chosen for engine-agnostic open tables with strong metadata and evolution features. Delta is often chosen when you are aligned with the Delta ecosystem and its tooling. The best choice depends on engines, governance, and operational capabilities.

| Dimension | Hudi | Iceberg | Delta Lake |
|---|---|---|---|
| Primary strength | Upserts, incremental pull, table services | Open multi-engine standard, hidden partitioning | Delta/Databricks ecosystem maturity |
| Update model | Indexed upsert; COW or MOR | Merge-on-read deletes; copy-on-write rewrite | Copy-on-write plus deletion vectors |
| Incremental read | First-class incremental query | Incremental append via snapshots/changelog | Change Data Feed |
| Partition evolution | Clustering, limited spec change | Strong partition evolution | Limited; requires rewrite |
| Streaming ingestion | Strong (DeltaStreamer, Flink, Connect) | Good (Flink, Spark) | Strong within Databricks |
| Engine interoperability | Good, but logs need Hudi-aware readers | Broadest | Broad, Iceberg via UniForm |
| Operational burden | Table services (compaction/clustering) to manage | Maintenance (compaction, expire snapshots) | Maintenance/optimize jobs |

Choose Hudi when the pipeline is defined by continuous CDC and the requirement is "current state fast, plus what changed since last run." Choose Iceberg when the table must be shared across many engines with the least coupling to one vendor. Choose Delta when the platform is Databricks-first and the team wants the most integrated tooling.

Interview answer: do not declare a universal winner. Tie the choice to update patterns, read freshness, engine mix, governance, and who will operate the table services. It is common and defensible to run Hudi for bronze ingestion and Iceberg or Delta for the curated layer.

[Table of Contents](#Apache-Hudi)

## Real world use cases for Apache Hudi

### 1. E-commerce order events with late-arriving updates
Business context: a marketplace needs a near-real-time order table that reflects cancellations, refunds, and late-arriving status events. Volume: ~40M order events/day (~120 GB/day), peak 15k events/s, freshness target 5 minutes.

```text
Kafka orders.cdc -> Spark Structured Streaming (5 min micro-batch)
  -> Hudi MOR table, record key order_id, precombine source_lsn
  -> read_optimized for BI dashboards, incremental pull for the silver layer
  -> compaction every 5 delta commits, clustering nightly
```

```python
{
    "hoodie.table.name": "orders_hudi",
    "hoodie.datasource.write.recordkey.field": "order_id",
    "hoodie.datasource.write.partitionpath.field": "order_date",
    "hoodie.datasource.write.precombine.field": "source_lsn",
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.compact.inline": "true",
    "hoodie.compact.inline.max.delta.commits": "5",
    "hoodie.parquet.max.file.size": "134217728",
}
```

Why this design: MOR absorbs the streaming write rate without rewriting Parquet on every event, `source_lsn` makes out-of-order events deterministic, and read-optimized queries keep dashboards fast between compactions. The incremental pull feeds the silver layer without rescanning history.

### 2. Fintech ledger with soft deletes and audit
Business context: a payments ledger must reflect reversals and account closures while retaining an auditable record. Volume: ~8M ledger entries/day, ~2 KB each, strict correctness.

```text
CDC (Debezium) -> bronze raw CDC table (append-only, immutable)
                -> Hudi COW ledger table: hard delete for erasure, soft delete for reversals
                -> incremental pull to regulatory reporting
```

```python
# Soft delete: null ordering value marks the record as deleted for readers.
soft_delete = spark.createDataFrame(
    [("txn-9001", "2026-10-04", None)], ["txn_id", "txn_date", "updated_at"]
)

(
    soft_delete.write.format("hudi")
    .option("hoodie.table.name", "ledger_hudi")
    .option("hoodie.datasource.write.recordkey.field", "txn_id")
    .option("hoodie.datasource.write.partitionpath.field", "txn_date")
    .option("hoodie.datasource.write.precombine.field", "updated_at")
    .option("hoodie.datasource.write.operation", "upsert")
    .mode("append")
    .save("s3://lake/hudi/ledger")
)
```

Why this design: COW gives the strongest read semantics for audit queries, the bronze CDC log makes the ledger reproducible, and soft deletes preserve history for regulators while `_hoodie_is_deleted`-style filtering hides reversed entries from operational reads. A separate hard-delete job handles GDPR erasure.

### 3. IoT telemetry current-state and incremental analytics
Business context: 200k devices emit readings every 30 seconds; operations needs the latest device state and analytics needs only changed rows. Volume: ~600M events/day (~90 GB/day).

```text
MQTT -> Kafka -> DeltaStreamer -> Hudi MOR device_telemetry
                                    |-> snapshot/read_optimized: current device state
                                    |-> incremental pull (checkpointed) -> silver aggregates
```

```bash
spark-submit --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
  --packages org.apache.hudi:hudi-utilities-bundle_2.12:0.15.0 \
  /opt/hudi/hudi-utilities-bundle.jar \
  --table-type MERGE_ON_READ \
  --source-class org.apache.hudi.utilities.sources.JsonKafkaSource \
  --source-ordering-field event_ts \
  --target-base-path s3://lake/hudi/device_telemetry \
  --target-table device_telemetry \
  --props /opt/hudi/deltastreamer.properties \
  --schemaprovider-class org.apache.hudi.utilities.schema.FilebasedSchemaProvider \
  --continuous
```

Why this design: one Hudi table serves both the low-latency current-state read and the change feed, removing the need to duplicate data. DeltaStreamer handles Kafka offset commit and schema registry integration, and incremental pulls keep the silver aggregation job cheap.

### 4. Multi-tenant SaaS activity lake with tenant isolation
Business context: a B2B SaaS platform ingests customer activity into one governed lake and must serve per-tenant queries with cost attribution. Volume: 500 tenants, ~150M events/day, uneven tenant sizes.

```text
activity API -> Kafka -> Hudi COW table partitioned by event_date,
              record key tenant_id,event_id, precombine ingestion_ts
              GSI-equivalent read patterns via Spark predicate pushdown on tenant_id
```

```python
{
    "hoodie.table.name": "activity_hudi",
    "hoodie.datasource.write.recordkey.field": "tenant_id,event_id",
    "hoodie.datasource.write.keygenerator.class": "org.apache.hudi.keygen.ComplexKeyGenerator",
    "hoodie.datasource.write.partitionpath.field": "event_date",
    "hoodie.datasource.write.precombine.field": "ingestion_ts",
    "hoodie.datasource.write.table.type": "COPY_ON_WRITE",
    "hoodie.metadata.index.column.stats.enable": "true",
}
```

Why this design: COW keeps tenant-facing queries simple and fast, composite keys prevent cross-tenant collisions, and date partitioning with column statistics lets Spark prune to a tenant's slices. Column stats in the metadata table keep planning fast despite the file count. Very large tenants can later be split into their own table to avoid skew.

### 5. CDC into a lakehouse bronze layer
Business context: an enterprise replicating 30 operational databases into one lakehouse wants a single upsert-capable bronze table per source before building conformed silver models. Volume: ~1.2B change events/day across sources.

```text
Debezium -> Kafka -> per-source Hudi MOR bronze tables (key = source PK, precombine = lsn)
                  -> incremental pull -> Spark/dbt silver models (Iceberg or Delta)
                  -> compaction + clustering scheduled outside ingestion windows
```

```python
bronze_options = {
    "hoodie.table.name": "crm_accounts_hudi",
    "hoodie.datasource.write.recordkey.field": "account_id",
    "hoodie.datasource.write.precombine.field": "source_lsn",
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
    "hoodie.datasource.write.operation": "upsert",
    "hoodie.metadata.enable": "true",
    "hoodie.clean.automatic": "true",
    "hoodie.cleaner.commits.retained": "20",
}
```

Why this design: Hudi absorbs high-volume CDC cheaply at the bronze layer, keeps a replayable current state per source, and exports only changed records downstream. Iceberg or Delta remains the team's choice for the curated layer, which is a normal and interview-defensible hybrid rather than a format war.

[Table of Contents](#Apache-Hudi)
