## [Main title](../README.md)
### [Interview questions](full.md)

# Change Data Capture (CDC)

**Notebook:** [`notebooks/topics/cdc.ipynb`](../notebooks/topics/cdc.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is CDC (Change Data Capture)?](#What-is-CDC-Change-Data-Capture)
+ [When would you choose CDC over batch ingestion?](#When-would-you-choose-CDC-over-batch-ingestion)
+ [What are common CDC sources (WAL/binlog/triggers) and trade-offs?](#What-are-common-CDC-sources-WALbinlogtriggers-and-trade-offs)
+ [What is the difference between snapshot and incremental CDC?](#What-is-the-difference-between-snapshot-and-incremental-CDC)
+ [How does log-based CDC work in PostgreSQL and MySQL?](#How-does-log-based-CDC-work-in-PostgreSQL-and-MySQL)
+ [How do you configure Debezium for a PostgreSQL source?](#How-do-you-configure-Debezium-for-a-PostgreSQL-source)
+ [What does a typical CDC event look like?](#What-does-a-typical-CDC-event-look-like)
+ [What is the difference between the Debezium envelope and a flat CDC event?](#What-is-the-difference-between-the-Debezium-envelope-and-a-flat-CDC-event)
+ [What delivery semantics exist (at-most-once/at-least-once/exactly-once)?](#What-delivery-semantics-exist-at-most-onceat-least-onceexactly-once)
+ [How do you make CDC ingestion idempotent?](#How-do-you-make-CDC-ingestion-idempotent)
+ [How do you handle deletes in CDC pipelines?](#How-do-you-handle-deletes-in-CDC-pipelines)
+ [How do you handle updates when the source does not provide full row images?](#How-do-you-handle-updates-when-the-source-does-not-provide-full-row-images)
+ [What is ordering and why is it hard in CDC?](#What-is-ordering-and-why-is-it-hard-in-CDC)
+ [What is a watermark/offset and where should it be stored?](#What-is-a-watermarkoffset-and-where-should-it-be-stored)
+ [How do you handle schema evolution with CDC?](#How-do-you-handle-schema-evolution-with-CDC)
+ [What is the outbox pattern and why is it useful?](#What-is-the-outbox-pattern-and-why-is-it-useful)
+ [How do you monitor CDC lag and where can lag come from?](#How-do-you-monitor-CDC-lag-and-where-can-lag-come-from)
+ [How do you design a safe backfill/reprocessing strategy for CDC?](#How-do-you-design-a-safe-backfillreprocessing-strategy-for-CDC)
+ [What are the most common failure modes in CDC pipelines?](#What-are-the-most-common-failure-modes-in-CDC-pipelines)
+ [How do you merge CDC events into a current-state table?](#How-do-you-merge-CDC-events-into-a-current-state-table)
+ [How do you handle late or out-of-order CDC events?](#How-do-you-handle-late-or-out-of-order-CDC-events)
+ [How do you build SCD Type 2 history from CDC?](#How-do-you-build-SCD-Type-2-history-from-CDC)
+ [How do you handle deletion requests and GDPR in a CDC pipeline?](#How-do-you-handle-deletion-requests-and-GDPR-in-a-CDC-pipeline)
+ [How do CDC pipelines fit into bronze, silver, and gold lakehouse layers?](#How-do-CDC-pipelines-fit-into-bronze-silver-and-gold-lakehouse-layers)
+ [How do you replay or rebuild a CDC pipeline?](#How-do-you-replay-or-rebuild-a-CDC-pipeline)
+ [Real world use cases for Change Data Capture](#Real-world-use-cases-for-Change-Data-Capture)

## What is CDC (Change Data Capture)?
CDC is a technique to capture row-level changes (inserts, updates, deletes) from a source system and stream them downstream. In databases, CDC is commonly log-based (reading the WAL/binlog) so it can capture changes without repeatedly scanning full tables. CDC pipelines often feed event logs (append-only) and/or materialized current-state tables.

The three things CDC must get right:

```text
1. Completeness - every committed change reaches the pipeline, including deletes.
2. Ordering     - changes are applied per key in source commit order.
3. Exactly-once effect - retries and rebalances do not change the final result.
```

A minimal mental model:

```text
source DB -> transaction log -> CDC connector -> Kafka topic -> sink/merge -> target table
              (WAL/binlog)      (Debezium)      (keyed, ordered per partition)
```

[Table of Contents](#Change-Data-Capture-CDC)

## When would you choose CDC over batch ingestion?
Choose CDC when you need low-latency updates, continuous incremental processing, or a reliable change history. CDC is also useful when full-table scans are too expensive because the source is large or changes frequently. Batch ingestion is often simpler when latency requirements are relaxed and operational complexity should be minimized.

Practical decision table:

| Requirement | Batch extract | Log-based CDC |
|---|---|---|
| Latency | minutes to hours | seconds to minutes |
| Source load | full scans or high-watermark queries | log read, low overhead |
| Deletes captured | only with soft-delete columns | yes, natively |
| Intermediate states | lost | preserved in order |
| Operational cost | low | connector + broker + merge job |
| Source privileges | SELECT | replication slot / binlog access |

Choose batch when: the source is small, nightly freshness is fine, the source is a SaaS API with no log access, or the team cannot operate a connector and broker.

[Table of Contents](#Change-Data-Capture-CDC)

## What are common CDC sources (WAL/binlog/triggers) and trade-offs?
Common sources are:
+ database logs (WAL/binlog): low overhead and high fidelity, but requires privileges and careful offset handling
+ triggers: can work without log access, but adds write overhead and is easy to break
+ timestamp-based queries: simple but can miss updates or create duplicates if clocks/transactions behave unexpectedly

Log-based CDC is usually preferred for production at scale.

| Source technique | Fidelity | Source overhead | Captures deletes | Notes |
|---|---|---|---|---|
| WAL / binlog | exact, ordered | low | yes | needs replication privileges/slot |
| Triggers + change table | high | per-write cost | yes | DDL on every table, easy to drift |
| Timestamp / `updated_at` poll | partial | query cost | only if soft delete | misses same-second updates |
| Full snapshot diff | exact at snapshot | very high | yes (diff) | not incremental |
| Application dual-write | high if correct | app changes | yes | dual-write failure risk |

Interview note: PostgreSQL logical replication requires `wal_level = logical` and a replication slot; MySQL needs `binlog_format = ROW` and `binlog_row_image = FULL` for full before/after images.

[Table of Contents](#Change-Data-Capture-CDC)

## What is the difference between snapshot and incremental CDC?
A snapshot reads an initial consistent baseline of existing rows. Incremental CDC then streams changes after that baseline using a log position/offset. Many systems require both: snapshot for bootstrap, incremental for ongoing updates.

The hard part is the handoff. If you snapshot first and then start streaming, changes that happened during the snapshot can be missed or duplicated unless the connector records a consistent log position at snapshot start.

```text
t0: record log position P, begin repeatable-read snapshot
t1: stream snapshot rows into the target (marks each with P)
t2: switch to streaming from P (inclusive), de-duplicate rows already at P
```

Debezium does this by default: the initial snapshot and the streaming phase share the same source position, and the Kafka topic carries both `op=r` (read/snapshot) and later `op=c/u/d` events.

[Table of Contents](#Change-Data-Capture-CDC)

## How does log-based CDC work in PostgreSQL and MySQL?
PostgreSQL: a logical decoding plugin (`pgoutput` for the built-in one, or `decoderbufs`/`wal2json`) reads the WAL through a replication slot. The slot advances only when the consumer confirms, which is why an abandoned slot fills the primary's disk.

MySQL: the binary log in ROW format records before and after images per row; the connector reads it as a replica (or via `binlog` client libraries). `binlog_row_image=FULL` is needed for updates and deletes to carry all columns.

```sql
-- PostgreSQL: check logical replication settings and slots.
show wal_level;                        -- must be 'logical'
select slot_name, active, restart_lsn, confirmed_flush_lsn from pg_replication_slots;

-- MySQL: check row-based binlog settings.
show variables like 'binlog_format';       -- ROW
show variables like 'binlog_row_image';    -- FULL
show master status;                        -- file + position
```

Trade-off to mention: a replication slot is a durability contract with the source. If the CDC pipeline is down for a week, the WAL is retained for a week and can exhaust primary disk. Monitor `pg_wal` size and slot lag, and set `max_slot_wal_keep_size` so a broken pipeline does not take down production.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you configure Debezium for a PostgreSQL source?
Kafka Connect submits connectors as JSON. This connector captures two tables with the Avro converters and heartbeat events:

```json
{
  "name": "orders-pg-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "pg-primary.internal",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "${file:/opt/kafka/secrets/pg.password}",
    "database.dbname": "orders",
    "topic.prefix": "cdc",
    "schema.include.list": "public",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_orders",
    "publication.autocreate.mode": "filtered",
    "snapshot.mode": "initial",
    "tombstones.on.delete": "true",
    "heartbeat.interval.ms": "10000",
    "decimal.handling.mode": "precise",
    "time.precision.mode": "adaptive_time_microseconds",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "https://schema-registry.example.com",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "https://schema-registry.example.com",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.drop.tombstones": "false",
    "transforms.unwrap.delete.handling.mode": "rewrite"
  }
}
```

Operational notes:

+ `snapshot.mode=initial` snapshots once; use `schema_only` when the target is already populated, or `no_data` for DDL-only history.
+ `tombstones.on.delete=true` plus log compaction lets downstream consumers remove state for deleted keys.
+ Do not use the `unwrap` SMT if you need before-images or full ordering metadata; keep the full envelope and unwrap in the lakehouse.

[Table of Contents](#Change-Data-Capture-CDC)

## What does a typical CDC event look like?
A CDC event usually contains the operation type, source metadata, and either the row before the change, the row after the change, or both. The metadata is just as important as the row values because it lets you order, deduplicate, audit, and replay events.

Example shape:

```json
{
  "op": "u",
  "source_table": "orders",
  "primary_key": {"order_id": 1001},
  "before": {"order_id": 1001, "status": "created", "amount": 42.50},
  "after": {"order_id": 1001, "status": "paid", "amount": 42.50},
  "source_lsn": "16/B374D848",
  "transaction_id": "781223",
  "event_time": "2026-10-04T15:03:02Z"
}
```

Interview tip: mention that different systems use different names (`lsn`, `binlog_file` + `position`, `scn`, offset), but the purpose is the same: capture a durable source position and event order.

[Table of Contents](#Change-Data-Capture-CDC)

## What is the difference between the Debezium envelope and a flat CDC event?
The real Debezium envelope wraps everything in `before`, `after`, `source`, `op`, `ts_ms`, and `transaction`, and `op` uses single letters. Flattening it loses information you often need later.

```json
{
  "before": {"order_id": 1001, "status": "created", "amount": 42.50},
  "after": {"order_id": 1001, "status": "paid", "amount": 42.50},
  "source": {
    "version": "3.0.0.Final",
    "connector": "postgresql",
    "db": "orders",
    "schema": "public",
    "table": "orders",
    "txId": 781223,
    "lsn": 39123842,
    "ts_ms": 1791138182000
  },
  "op": "u",
  "ts_ms": 1791138182345,
  "transaction": null
}
```

Operation codes:

+ `r` = snapshot read (initial load)
+ `c` = create / insert
+ `u` = update (has both before and after)
+ `d` = delete (before populated, after null)
+ `t` = truncate (message with a `truncated` array)

Interview point: keep `source.lsn` (or `source.file` + `source.pos`) and `source.txId` in the bronze table. Without them you cannot deterministically order or deduplicate after a replay.

[Table of Contents](#Change-Data-Capture-CDC)

## What delivery semantics exist (at-most-once/at-least-once/exactly-once)?
At-most-once can lose messages but avoids duplicates. At-least-once avoids loss but can produce duplicates on retries. Exactly-once is hard end-to-end; many systems implement "effectively once" by combining at-least-once delivery with idempotent writes and deterministic merge logic.

Where each guarantee is usually available:

```text
Source log to Kafka (Debezium):        at-least-once
Kafka to Kafka (transactions/EOS):     exactly-once within Kafka
Kafka to warehouse (merge on PK):      effectively-once with idempotent MERGE
Kafka to object store (append files):  at-least-once, dedupe downstream by offset
```

Flink example of a checkpointed, exactly-once sink:

```python
from pyflink.common import WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.checkpointing_mode import CheckpointingMode
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(4)
env.enable_checkpointing(10_000)
env.get_checkpoint_config().set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
env.get_checkpoint_config().set_min_pause_between_checkpoints(5_000)

kafka_source = (
    KafkaSource.builder()
    .set_bootstrap_servers("kafka-1:9092")
    .set_topics("cdc.public.orders")
    .set_group_id("orders-cdc-flink")
    .set_starting_offsets(KafkaOffsetsInitializer.earliest())
    .set_value_only_deserializer(SimpleStringSchema())
    .build()
)

(
    env.from_source(kafka_source, WatermarkStrategy.no_watermarks(), "orders-cdc")
    .key_by(lambda row: row["order_id"])
    .process(DeduplicateByLsn())
    .sink_to(iceberg_sink)
)

env.execute("orders-cdc-merge")
```

[Table of Contents](#Change-Data-Capture-CDC)

## How do you make CDC ingestion idempotent?
You make downstream writes idempotent by using stable keys (primary key + source LSN/transaction id) and applying deterministic upsert/merge logic. A common pattern is to load changes into an append-only raw log, then build current-state tables using "latest per key" logic. Idempotency must hold across retries and replays.

Three techniques that compose well:

+ Store a natural idempotency key: `(source_table, primary_key, source_lsn)` for events, and reject duplicates on insert.
+ Make the merge a pure function of the source history: rank by source ordering metadata, never by ingestion time.
+ Make the offset commit atomic with the write, or make the write safe to repeat so a non-atomic retry is harmless.

```sql
-- Raw table enforces event-level deduplication.
create table bronze.orders_cdc (
  source_table  string,
  order_id      bigint,
  op            string,
  before_json   string,
  after_json    string,
  source_lsn    bigint,
  source_txid   bigint,
  ingested_at   timestamp
)
using iceberg
tblproperties ('write.merge.mode' = 'merge-on-read');

-- A replay of the same LSN is a no-op.
merge into bronze.orders_cdc as t
using staging.orders_cdc as s
on  t.source_table = s.source_table
and t.order_id = s.order_id
and t.source_lsn = s.source_lsn
when not matched then insert *;
```

[Table of Contents](#Change-Data-Capture-CDC)

## How do you handle deletes in CDC pipelines?
Deletes may appear as explicit delete events, tombstones, or a "before image" without an "after image". Downstream you can:
+ apply hard deletes (remove row)
+ apply soft deletes (is_deleted flag with deleted_at)
+ keep full history (append-only) and compute current state with delete logic

The choice depends on compliance, analytics needs, and downstream consumers.

```sql
-- Soft delete preserves the audit trail and lets you resurrect if the delete was wrong.
merge into silver.orders_current as t
using staged_orders as s
on t.order_id = s.order_id
when matched and s.op = 'd' then update set
  is_deleted = true,
  deleted_at = current_timestamp(),
  last_source_lsn = s.source_lsn
when matched and s.op <> 'd' then update set
  status = s.status,
  amount = s.amount,
  is_deleted = false,
  last_source_lsn = s.source_lsn
when not matched and s.op <> 'd' then insert *;
```

Interview guidance: GDPR erasure usually requires a real delete (or irreversible anonymization), while analytics usually prefers soft delete. Design for both: a soft-deleted current-state table plus a separate compaction/erasure job that hard-deletes on legal request.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you handle updates when the source does not provide full row images?
If updates are partial (only changed columns), you often need to reconstruct the full row by joining against previous state. Some CDC tools can be configured to emit before/after images; if not, current-state reconstruction becomes part of your pipeline. You must also handle out-of-order updates carefully.

```sql
-- Reconstruct the current row from a partial-update log by taking the last non-null value per column.
-- The CASE keeps rows whose value is null from winning the ordering, so the latest non-null value wins.
select
  order_id,
  max_by(status, case when status is not null then source_lsn end)             as status,
  max_by(amount, case when amount is not null then source_lsn end)             as amount,
  max_by(customer_id, case when customer_id is not null then source_lsn end)   as customer_id
from bronze.orders_cdc_partial
where op <> 'd'
group by order_id;
```

`max_by(value, ordering_key)` returns the value associated with the largest ordering key; the `case` guard is needed because a plain `max_by` would return the null of a later partial update. It works in Spark SQL, Trino, and Snowflake; BigQuery needs the equivalent `array_agg(value ignore nulls order by ordering_key desc limit 1)`. In PySpark the equivalent is a windowed `row_number()` or `last(col, ignorenulls=True)`:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

by_key = Window.partitionBy("order_id").orderBy(F.col("source_lsn").asc())
by_key_desc = Window.partitionBy("order_id").orderBy(F.col("source_lsn").desc())

filled = (
    bronze_partial
    .withColumn("status", F.last("status", ignorenulls=True).over(by_key))
    .withColumn("amount", F.last("amount", ignorenulls=True).over(by_key))
    .withColumn("rn", F.row_number().over(by_key_desc))
    .where(F.col("rn") == 1)
)
```

Set the source connector to emit full row images where possible (`binlog_row_image=FULL`, Postgres `REPLICA IDENTITY FULL` for tables without a primary key) because reconstruction is expensive and easy to get subtly wrong.

[Table of Contents](#Change-Data-Capture-CDC)

## What is ordering and why is it hard in CDC?
Ordering means applying changes in the same order they happened in the source. It is hard because events can be partitioned (multiple tables/partitions), delivered out of order, or retried. Correctness often requires per-key ordering (or per-partition ordering) using source transaction metadata.

Sources of disorder:

+ Kafka partitioning by key preserves per-key order, but two keys in the same transaction can be processed by different consumers at different speeds.
+ Connector restarts replay from the last committed offset and can resend a batch.
+ A sink that parallelizes by file rather than by key can interleave updates to the same key.
+ Snapshot rows (`op=r`) and streaming rows can overlap around the handoff point.

Rule of thumb: guarantee order *per primary key*, and use `source.lsn` (plus `txId` for cross-table consistency) as the ordering key. Never order by `ingested_at`, because retries and backfills break that assumption.

[Table of Contents](#Change-Data-Capture-CDC)

## What is a watermark/offset and where should it be stored?
An offset (watermark) is the position in the source log (or stream) up to which changes have been processed. It should be stored durably in the ingestion system (connector state store) and, for reliability, often also in your platform (for example a control table) so you can audit and recover. Offsets must be updated atomically with downstream writes to avoid gaps/duplicates.

```sql
create table ops.cdc_watermarks (
  pipeline_name   string,
  source_table    string,
  kafka_partition int,
  kafka_offset    bigint,
  source_lsn      bigint,
  committed_at    timestamp
)
using iceberg;

merge into ops.cdc_watermarks as t
using staged_watermarks as s
on t.pipeline_name = s.pipeline_name and t.source_table = s.source_table
when matched then update set
  kafka_offset = s.kafka_offset,
  source_lsn = s.source_lsn,
  committed_at = s.committed_at
when not matched then insert *;
```

Interview point: if the offset is committed before the write, a crash causes data loss; if after, it causes duplicates. Either commit them in one transaction (Spark/Flink sinks with transactional commit) or make the write idempotent so duplicates are harmless.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you handle schema evolution with CDC?
You need a strategy for compatible changes (additive columns) and breaking changes (renames, type changes). Common tools include schema registries and compatibility policies, plus strict validation in CI. Downstream tables should tolerate additive fields, and pipelines should alert on breaking changes before production data is corrupted.

Practical pattern: landing tables store the raw payload as a string/struct plus a small set of promoted columns. Additive source columns do not require a migration; breaking changes generate an alert and a new topic version.

```python
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructField, StructType

envelope_fields = [
    StructField("op", StringType()),
    StructField("before", StringType()),
    StructField("after", StringType()),
    StructField("source", StringType()),
    StructField("ts_ms", StringType()),
]
envelope_schema = StructType(envelope_fields)

landing = raw_kafka.select(
    F.col("key").cast("string").alias("kafka_key"),
    F.from_json(F.col("value").cast("string"), envelope_schema).alias("env"),
    F.col("partition"),
    F.col("offset"),
)
```

Register the connector's output schema with `BACKWARD` compatibility so the producer cannot add a required field. When a rename is unavoidable, prefer a dual-write period with both old and new field names (or an alias) rather than a flag-day cutover.

[Table of Contents](#Change-Data-Capture-CDC)

## What is the outbox pattern and why is it useful?
The outbox pattern writes business events into an "outbox" table in the same transaction as the application write. CDC then captures the outbox changes and publishes them reliably. This avoids dual-write problems where the database update succeeds but the event publish fails (or vice versa).

```sql
begin;

update orders
set status = 'paid', paid_at = now()
where order_id = 1001;

insert into outbox (aggregate_type, aggregate_id, event_type, payload, created_at)
values ('Order', '1001', 'OrderPaid', '{"order_id": 1001, "amount": 42.50}', now());

commit;
```

The outbox table is then captured by the same Debezium connector:

```json
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "pg-primary.internal",
    "database.dbname": "orders",
    "database.user": "debezium",
    "database.password": "${file:/opt/kafka/secrets/pg.password}",
    "topic.prefix": "cdc",
    "table.include.list": "public.outbox",
    "plugin.name": "pgoutput",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.route.topic.replacement": "domain.orders.v1",
    "transforms.outbox.table.field.event.key": "aggregate_id",
    "transforms.outbox.table.field.event.payload": "payload",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "https://schema-registry.example.com"
  }
}
```

Trade-offs: the outbox adds a table and a write per event, and rows must be cleaned up after capture (or the outbox becomes a huge history table). In exchange you get an atomic, replayable event stream without a message broker in the request path.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you monitor CDC lag and where can lag come from?
Lag can come from:
+ source: heavy write load, log retention limits
+ connector: slow polling, backpressure, failures
+ broker/stream: throughput limits, partition hotspots
+ downstream: slow merges/compaction, expensive transformations

You monitor lag using source LSN vs processed LSN, consumer offsets, and end-to-end freshness in target tables.

```sql
-- Kafka consumer lag (approximate; pair with broker-side metrics).
select
  "group" as consumer_group,
  topic,
  sum(lag) as total_lag,
  max(lag) as max_partition_lag
from kafka_consumer_lag_snapshot
where "group" = 'cdc-orders-sink'
group by "group", topic;
```

```text
End-to-end freshness is the metric that matters to the business:
  freshness_seconds = now() - max(source.ts_ms) in the target table

Alert on:
+ lag growing monotonically for > 15 min
+ pg_replication_slots lag / retained WAL bytes above a threshold
+ freshness SLO breach per table
+ connector task restarts and dead-letter queue depth
```

[Table of Contents](#Change-Data-Capture-CDC)

## How do you design a safe backfill/reprocessing strategy for CDC?
A safe strategy usually separates raw change storage from derived tables. You keep the raw CDC log (immutable) and rebuild derived current-state/marts from it when needed. For backfills, you often run in a separate environment or commit to new snapshots/versions, then switch consumers after validation.

Concrete steps:

```text
1. Raw events are immutable in bronze (keyed by source LSN), so "backfill" = re-run the merge step.
2. Rebuild into a shadow table (silver.orders_current_v2), not in place.
3. Validate row counts, checksums, and per-key latest LSN against the current table.
4. Use a snapshot/version swap or an alias/view flip so consumers switch atomically.
5. Keep the old table for rollback until the next validation window.
```

Do not re-snapshot the source for a backfill if the raw log still covers the period: replaying the log is cheaper and avoids competing with production. If the raw log retention has expired, you need a fresh snapshot plus a reconciliation for keys that changed during it.

[Table of Contents](#Change-Data-Capture-CDC)

## What are the most common failure modes in CDC pipelines?
Common issues include:
+ duplicates due to retries/rebalances
+ missed events due to offset mismanagement or log retention
+ schema drift/breaking changes
+ incorrect delete handling
+ out-of-order application of updates

Extended list with mitigations:

| Failure | Symptom | Mitigation |
|---|---|---|
| Replication slot grows | primary disk fills | monitor slot lag, `max_slot_wal_keep_size` |
| Snapshot never completes | target stale for hours | throttle, snapshot on a replica |
| Partition hotspot | one Kafka partition lags | re-key or split the topic |
| Schema change breaks sink | pipeline paused, DLQ grows | registry compatibility check in CI |
| Offset committed before write | rows missing after a crash | transactional sink or idempotent merge |
| Delete without tombstone | target keeps deleted rows | enable tombstones, compact topic |
| Poison message | consumer stuck retrying | dead-letter topic + alert |
| Backfill corrupts current state | wrong aggregates | shadow table + validation then swap |

[Table of Contents](#Change-Data-Capture-CDC)

## How do you merge CDC events into a current-state table?
Load CDC events into an immutable raw table first, then merge the latest valid event per primary key into the current-state table. Use source ordering metadata, not ingestion time, to decide which event wins.

Example SQL pattern:

```sql
merge into silver.orders_current as target
using (
  select *
  from (
    select
      order_id,
      status,
      amount,
      op,
      source_lsn,
      row_number() over (
        partition by order_id
        order by source_lsn desc
      ) as rn
    from bronze.orders_cdc
  ) ranked
  where rn = 1
) as source
on target.order_id = source.order_id
when matched and source.op = 'd' then delete
when matched then update set
  status = source.status,
  amount = source.amount,
  last_source_lsn = source.source_lsn
when not matched and source.op <> 'd' then insert (
  order_id, status, amount, last_source_lsn
) values (
  source.order_id, source.status, source.amount, source.source_lsn
);
```

This pattern is easier to reason about than directly mutating targets from the connector because the raw event history remains available for debugging and rebuilds.

The same shape in PySpark with Iceberg:

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

events = spark.table("bronze.orders_cdc")

latest = Window.partitionBy("order_id").orderBy(F.col("source_lsn").desc())

winning = (
    events
    .withColumn("rn", F.row_number().over(latest))
    .where(F.col("rn") == 1)
    .drop("rn")
)

winning.createOrReplaceTempView("orders_latest")

spark.sql("""
merge into silver.orders_current as t
using orders_latest as s
on t.order_id = s.order_id
when matched and s.op = 'd' then delete
when matched then update set
  t.status = s.status,
  t.amount = s.amount,
  t.last_source_lsn = s.source_lsn
when not matched and s.op <> 'd' then insert (
  order_id, status, amount, last_source_lsn
) values (
  s.order_id, s.status, s.amount, s.source_lsn
)
""")
```

[Table of Contents](#Change-Data-Capture-CDC)

## How do you handle late or out-of-order CDC events?
Use source ordering fields and make the merge conditional. If an older event arrives after a newer event, it should not overwrite the current row. In many systems this means storing the latest applied source position or event timestamp per key.

Example rule:

```sql
when matched
  and source.source_lsn > target.last_source_lsn
  and source.op <> 'd'
then update set ...
```

The exact comparison depends on the source database. A single monotonic LSN is convenient; multi-part offsets may require comparing file name plus position, transaction id plus sequence number, or connector-provided ordering fields. For cross-table consistency, transaction boundaries also matter.

```sql
-- Composite ordering key: binlog file + position (MySQL-style).
merge into silver.orders_current as t
using staged as s
on t.order_id = s.order_id
when matched
  and (
    s.binlog_file > t.last_binlog_file
    or (s.binlog_file = t.last_binlog_file and s.binlog_pos > t.last_binlog_pos)
  )
  and s.op <> 'd'
then update set
  t.status = s.status,
  t.amount = s.amount,
  t.last_binlog_file = s.binlog_file,
  t.last_binlog_pos = s.binlog_pos;
```

If you use event-time processing, add a bounded watermark and route events older than the watermark to a quarantine table so the pipeline keeps moving while an operator reconciles them.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you build SCD Type 2 history from CDC?
CDC is the ideal input for SCD2 because the before/after images already describe what changed. The pattern is: close the current version when a tracked attribute changes, then open a new version.

```sql
-- 1. Land every change with valid-from = source commit time.
create table silver.customer_history (
  customer_id  bigint,
  name         string,
  email        string,
  valid_from   timestamp,
  valid_to     timestamp,
  is_current   boolean,
  source_lsn   bigint
)
using iceberg;

-- 2. Close the open version when a tracked attribute changes.
merge into silver.customer_history as t
using staged_customer_changes as s
on  t.customer_id = s.customer_id
and t.is_current = true
and (t.name <> s.name or t.email <> s.email)
when matched then update set
  t.valid_to = s.change_time,
  t.is_current = false;

-- 3. Insert the new open version.
insert into silver.customer_history
select
  s.customer_id, s.name, s.email, s.change_time,
  timestamp '9999-12-31 23:59:59', true, s.source_lsn
from staged_customer_changes s
where s.op <> 'd';
```

Interview note: define the tracked columns explicitly; otherwise every row update (for example a `last_seen_at` column) creates a new SCD2 version and the history table explodes. Deletes are usually modeled as closing the current version and writing a tombstone or a deleted marker, not by removing history.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you handle deletion requests and GDPR in a CDC pipeline?
A deletion request cannot rely on "the row will eventually be soft-deleted" because raw CDC logs and backups keep the old values. You need a deliberate erasure path across all layers.

```text
1. Identify all copies: source DB, raw CDC topic (compacted, retained), bronze files,
   silver current table, SCD2 history, backups, search indexes, exports.
2. Prefer tokenization: if the lake never stored raw PII, erasure is a vault operation.
3. For raw logs: compact the topic with a tombstone, and expire affected bronze partitions.
4. For derived tables: hard-delete the key and rebuild aggregates that included it.
5. Record proof of erasure (audit table with request id, scope, timestamps).
```

```sql
-- Erasure job: delete the subject everywhere it is still identifiable.
delete from silver.customers_current where customer_token = :token;
delete from silver.customer_history where customer_token = :token;

-- Recompute affected aggregates from the now-clean base tables.
insert overwrite gold.customer_ltv
select * from silver.customer_ltv_recomputed;
```

Interview point: deleting from an immutable append-only log is fundamentally awkward. The cleanest answer is "do not put raw PII in the log": tokenize at the application boundary, or isolate raw PII in a short-retention vault table that is not part of the CDC stream.

[Table of Contents](#Change-Data-Capture-CDC)

## How do CDC pipelines fit into bronze, silver, and gold lakehouse layers?
In a lakehouse, CDC usually lands in layers:

+ bronze: raw append-only CDC events with minimal transformation
+ silver: cleaned, deduplicated, typed current-state tables and optional SCD history
+ gold: business-ready marts, metrics, and dimensional models

Example: an `orders` CDC stream lands in `bronze.orders_cdc`, is merged into `silver.orders_current`, then joins `dim_customer` and `dim_date` to produce `gold.fact_orders`. Keeping these layers separate makes replay, quality checks, and downstream contracts much safer.

```text
Kafka cdc.public.orders
   -> bronze.orders_cdc         (append-only, keyed by source_lsn, Avro/JSON)
   -> silver.orders_current     (deduped, typed, latest per order_id)
   -> silver.orders_scd2        (optional full history)
   -> gold.fact_orders          (joined, conformed, partitioned by order_date)
```

Lakehouse specifics worth mentioning: use merge-on-read for the bronze merge if write latency matters, run `rewrite_data_files`/compaction after heavy merges to avoid delete-file buildup, and expire snapshots on the raw layer only after the retention window that compliance requires.

[Table of Contents](#Change-Data-Capture-CDC)

## How do you replay or rebuild a CDC pipeline?
Replay is the ability to reprocess a known range of the source log without touching the source again. It is the single most valuable property of a log-based CDC design.

```bash
# Replay a Kafka range into a separate consumer group / environment.
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --group cdc-orders-replay-2026-10-04 \
  --topic cdc.public.orders \
  --reset-offsets --to-datetime 2026-10-04T00:00:00.000 --execute
```

```sql
-- Rebuild a derived table from the retained raw events.
create or replace table silver.orders_current_v2 using iceberg as
select order_id, status, amount, source_lsn
from (
  select
    order_id, status, amount, source_lsn,
    row_number() over (partition by order_id order by source_lsn desc) as rn
  from bronze.orders_cdc
  where op <> 'd'
) ranked
where rn = 1;
```

Requirements for a working replay: raw events retained long enough, ordering metadata preserved, merge logic deterministic and idempotent, and a way to write to a shadow table and swap. If you flattened the envelope or overwrote bronze in place, you cannot replay.

[Table of Contents](#Change-Data-Capture-CDC)

## Real world use cases for Change Data Capture

### 1. E-commerce order and inventory sync

Business context: an order service on PostgreSQL must keep inventory, search, and the analytics lake in sync within seconds of checkout. Volume: 25 million orders/day, 6,000 order updates/second at flash-sale peaks, 40 GB/day of raw CDC.

Architecture: Debezium on `public.orders` and `public.inventory` -> Kafka (keyed by primary key, log-compacted) -> Spark Structured Streaming merge into Iceberg `silver.orders_current` and `silver.inventory_current`; a separate Flink job updates the search index.

```json
{
  "name": "orders-pg-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "pg-primary.internal",
    "database.dbname": "orders",
    "database.user": "debezium",
    "database.password": "${file:/opt/kafka/secrets/pg.password}",
    "topic.prefix": "cdc",
    "table.include.list": "public.orders,public.inventory",
    "plugin.name": "pgoutput",
    "snapshot.mode": "initial",
    "tombstones.on.delete": "true",
    "heartbeat.interval.ms": "10000"
  }
}
```

Why this design: log-based capture adds no query load to the OLTP database at flash-sale peaks, per-key Kafka ordering gives correct latest-state semantics, and Iceberg merge-on-read keeps the sink fast while compaction keeps reads cheap.

### 2. Fintech ledger CDC with exactly-once effect

Business context: a payments platform needs a queryable ledger copy for finance and fraud while the source remains the system of record. Volume: 12 million ledger rows, 8,000 updates/second during settlement, strict audit and no tolerance for lost or double-applied entries.

Architecture: Debezium reads the Postgres WAL with `decimal.handling.mode=precise`; a Flink job checkpoints every 10 seconds, deduplicates by `(ledger_id, source.lsn)`, and writes to Iceberg with a transactional sink; the raw topic is retained 30 days for replay.

```python
events = (
    raw_kafka
    .select(F.from_json(F.col("value").cast("string"), envelope_schema).alias("e"))
    .select("e.after.*", "e.before.*", "e.op", F.col("e.source.lsn").alias("lsn"))
)

deduped = (
    events
    .withColumn("rn", F.row_number().over(
        Window.partitionBy("ledger_id").orderBy(F.col("lsn").desc())
    ))
    .where(F.col("rn") == 1)
    .drop("rn")
)
```

Why this design: `decimal.handling.mode=precise` preserves exact money values end to end, `source.lsn` makes the merge idempotent across replay and rebalance, and retaining the compacted keyed topic means a bad deployment can be rebuilt without re-reading the source database.

### 3. Multi-tenant SaaS with per-tenant isolation

Business context: a B2B SaaS platform replicates each tenant's PostgreSQL database into a shared lakehouse for tenant-facing analytics. Volume: 2,000 tenants, 500 GB/day total, tenants vary from 1 MB/day to 50 GB/day.

Architecture: one Debezium connector per tenant database writing to a tenant-prefixed topic; a single streaming merge job consumes all topics and routes by `tenant_id`; the lakehouse uses row-level security so a tenant only sees its own rows.

```python
topic_pattern = "cdc.tenant-.*\\.public\\..*"

raw = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-1:9092")
    .option("subscribePattern", topic_pattern)
    .option("startingOffsets", "earliest")
    .load()
)

enriched = raw.withColumn("tenant_id", F.regexp_extract("topic", r"cdc\.(tenant-[^.]+)\.", 1))
```

```sql
-- Lakehouse row-level security for tenant isolation.
create or replace row access policy tenant_isolation as (tenant_id string)
returns boolean ->
  tenant_id = current_user_tenant();

alter table gold.tenant_orders add row access policy tenant_isolation on (tenant_id);
```

Why this design: per-tenant topics and connectors isolate failures (one noisy tenant does not stall the rest), a shared merge job controls cost, and row-level security enforces isolation even though all tenants share physical tables.

### 4. GDPR erasure with a tokenized CDC stream

Business context: a European subscription business must honor erasure requests within 30 days across raw, derived, and serving layers. Volume: 3 million customer records, 20 million change events/day, 400 erasure requests/month.

Architecture: the application writes a `customer_token` (never raw PII) into CDC-captured tables; raw PII lives only in a short-retention vault table excluded from CDC; an erasure orchestrator fans out deletes to current-state, SCD2 history, search, and exports, then writes an audit record.

```sql
-- Vault table is NOT part of the CDC stream.
delete from vault.customer_pii where customer_token = :token;

-- Derived tables are keyed by token, so erasure is a keyed delete.
delete from silver.customers_current where customer_token = :token;
delete from silver.customer_history where customer_token = :token;

insert into ops.gdpr_erasure_log
values (:token, :request_id, current_timestamp(), 'completed');
```

Why this design: tokenizing before the CDC boundary turns erasure from "rewrite an immutable log" into "delete a vault mapping", which is fast, auditable, and does not require expiring the whole raw topic.

### 5. Legacy mainframe to cloud via log scraping plus CDC

Business context: a retailer keeps a legacy DB2 inventory system on-premises and wants near-real-time inventory in the cloud without a costly integration project. Volume: 4 million SKUs, 2,000 updates/minute, batch window unacceptable for e-commerce availability checks.

Architecture: a mainframe log-scraping agent extracts DB2 change records into Kafka; Kafka Connect lands them in S3 as Avro; Spark merges into the cloud lakehouse; a nightly reconciliation compares counts against a batch extract.

```yaml
name: db2-inventory-source
config:
  connector.class: com.example.connect.Db2LogScrapeSource
  kafka.topic: legacy.db2.inventory
  poll.interval.ms: "1000"
  batch.size: "500"
  value.converter: io.confluent.connect.avro.AvroConverter
  value.converter.schema.registry.url: https://schema-registry.example.com
```

Why this design: CDC avoids a nightly batch window and keeps source overhead low; a nightly reconciliation catches drift that log scraping can miss; and keeping the raw Avro topic allows a rebuild if the merge logic changes.

[Table of Contents](#Change-Data-Capture-CDC)
