## [Main title](../README.md)
### [Interview questions](full.md)

# ClickHouse
+ [What is ClickHouse and how is it architected?](#What-is-ClickHouse-and-how-is-it-architected)
+ [How does MergeTree store parts partitions and ORDER BY?](#How-does-MergeTree-store-parts-partitions-and-ORDER-BY)
+ [How do the sparse primary index and skipping indexes work?](#How-do-the-sparse-primary-index-and-skipping-indexes-work)
+ [What are projections and when should you use them?](#What-are-projections-and-when-should-you-use-them)
+ [Which MergeTree engine variants exist?](#Which-MergeTree-engine-variants-exist)
+ [How do the Distributed and Replicated engines work?](#How-do-the-Distributed-and-Replicated-engines-work)
+ [How does TTL manage the data lifecycle?](#How-does-TTL-manage-the-data-lifecycle)
+ [How do materialized views do incremental aggregation?](#How-do-materialized-views-do-incremental-aggregation)
+ [How do you ingest from Kafka with the Kafka engine?](#How-do-you-ingest-from-Kafka-with-the-Kafka-engine)
+ [How do async inserts batch inserts and Kafka Connect differ?](#How-do-async-inserts-batch-inserts-and-Kafka-Connect-differ)
+ [How do codecs and compression work?](#How-do-codecs-and-compression-work)
+ [Which column types matter and what are the Nullable caveats?](#Which-column-types-matter-and-what-are-the-Nullable-caveats)
+ [How do ClickHouse JOIN algorithms work?](#How-do-ClickHouse-JOIN-algorithms-work)
+ [How do dictionaries speed up lookups?](#How-do-dictionaries-speed-up-lookups)
+ [How do you read EXPLAIN output and optimize queries?](#How-do-you-read-EXPLAIN-output-and-optimize-queries)
+ [How do you deduplicate with ReplacingMergeTree and FINAL?](#How-do-you-deduplicate-with-ReplacingMergeTree-and-FINAL)
+ [How do you build real-time analytics pipelines?](#How-do-you-build-real-time-analytics-pipelines)
+ [How does ClickHouse compare with Druid BigQuery and Snowflake?](#How-does-ClickHouse-compare-with-Druid-BigQuery-and-Snowflake)
+ [What operational concerns matter in production?](#What-operational-concerns-matter-in-production)
+ [Real world use cases for ClickHouse](#Real-world-use-cases-for-ClickHouse)

## What is ClickHouse and how is it architected?
ClickHouse is a column-oriented OLAP database built for real-time analytics. It is shared-nothing: each node has local disks and its own CPU, and there is no single leader in the data path. A query can be sent to any node, and a `Distributed` table fans it out to shards.

+ **Table engine** - storage and behavior are chosen per table. `MergeTree` and its variants are the foundation; `Distributed` and `Replicated*` add scale and durability.
+ **Parts and partitions** - inserts create immutable parts; background merges combine them inside a partition.
+ **ClickHouse Keeper** - a Raft-based coordination service that replaces ZooKeeper for replication and distributed DDL.
+ **Clusters** - shards (horizontal data split) and replicas (copies of a shard), defined in `remote_servers` with per-node `macros`.

```text
config.d/remote_servers.xml
<clickhouse>
  <remote_servers>
    <analytics_cluster>
      <shard><replica><host>ch-1</host><port>9000</port></replica><replica><host>ch-2</host><port>9000</port></replica></shard>
      <shard><replica><host>ch-3</host><port>9000</port></replica><replica><host>ch-4</host><port>9000</port></replica></shard>
    </analytics_cluster>
  </remote_servers>
  <macros><shard>01</shard><replica>ch-1</replica></macros>
</clickhouse>
```

ClickHouse favors wide, append-only, denormalized tables with high insert throughput. It is not an OLTP database: there are no efficient single-row updates or foreign keys, and joins are a secondary operation rather than the primary access path.

[Table of Contents](#ClickHouse)

## How does MergeTree store parts partitions and ORDER BY?
`MergeTree` sorts rows by the `ORDER BY` expression, splits data into partitions, writes each insert as a part, and merges parts in the background. The `PRIMARY KEY` is the sparse index prefix and, when omitted, defaults to `ORDER BY`.

```sql
CREATE TABLE analytics.events
(
    event_time  DateTime,
    user_id     UInt64,
    country     LowCardinality(String),
    event_type  LowCardinality(String),
    amount      Decimal(18, 2)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(event_time)
ORDER BY (country, event_time, user_id)
SETTINGS index_granularity = 8192;

INSERT INTO analytics.events VALUES
    (now(), 101, 'DE', 'purchase', 42.50),
    (now(), 102, 'FR', 'view', 0);
```

Inspect the resulting layout with `SELECT partition, name, rows FROM system.parts WHERE table = 'events' AND active`.

Design rules:

+ `ORDER BY` should lead with the lowest-cardinality column you filter on, then the timestamp, then the high-cardinality key. Sorted data is what makes range scans fast.
+ Keep monthly or daily partitions for time-series data; too many tiny partitions hurt merges and metadata.
+ `PRIMARY KEY` must be a prefix of `ORDER BY`. Set it explicitly only when you want a shorter sparse index than the sort key.
+ A part is the unit of merging and each insert creates one part, so insert less often with more rows per insert.

[Table of Contents](#ClickHouse)

## How do the sparse primary index and skipping indexes work?
The primary index is sparse: it stores one mark per granule of `index_granularity` rows (8192 by default) rather than one entry per row. A range scan finds the first matching granule and reads forward, which keeps the index small enough to stay in memory. Skipping indexes add secondary pruning for columns that are not in the sort key.

```sql
ALTER TABLE analytics.events
    ADD INDEX idx_type event_type TYPE set(100) GRANULARITY 4,
    ADD INDEX idx_amount amount TYPE minmax GRANULARITY 2,
    ADD INDEX idx_message message TYPE tokenbf_v1(8192, 3, 0) GRANULARITY 4;

ALTER TABLE analytics.events MATERIALIZE INDEX idx_type;

EXPLAIN indexes = 1
SELECT count() FROM analytics.events
WHERE event_type = 'purchase' AND amount > 1000;
```

The output reports which granules each index skipped:

```text
PrimaryKey  Keys: event_type, event_time, user_id   Granules: 116/1024
Skip        Name: idx_amount (minmax)               Granules: 32/116
```

Index guidance: `minmax` for numeric ranges, `set` for a bounded number of values, `bloom_filter` for equality on high-cardinality strings, and `tokenbf_v1` or `ngrambf_v1` for text search. Every index costs storage and merge time, so add one only after a query shows up in `system.query_log` as a full scan.

[Table of Contents](#ClickHouse)

## What are projections and when should you use them?
A projection is an alternative physical ordering of the same data, stored inside the table. It lets one table serve two access patterns without a second table or a materialized view.

```sql
ALTER TABLE analytics.events
    ADD PROJECTION by_user (
        SELECT user_id, event_time, event_type, amount
        ORDER BY (user_id, event_time)
    );

ALTER TABLE analytics.events MATERIALIZE PROJECTION by_user;

EXPLAIN indexes = 1
SELECT user_id, count() FROM analytics.events WHERE user_id = 101;
```

The planner selects a projection automatically when it fits the query. Use projections for a second common sort order or for pre-aggregated rollups on the same table. They cost extra disk and merge work, so keep the number small and materialize only what queries use. For rollups that must be shared and queried by name, a `MaterializedView` over `AggregatingMergeTree` is usually clearer.

[Table of Contents](#ClickHouse)

## Which MergeTree engine variants exist?
The MergeTree family changes what happens during a merge. Choosing the right variant removes the need for application-side deduplication or rollup jobs.

| Engine | Merge behavior | Use case |
|---|---|---|
| `MergeTree` | keeps all rows | append-only facts and events |
| `ReplacingMergeTree` | keeps one row per sort key | upserts and CDC mirrors |
| `SummingMergeTree` | sums numeric columns per key | additive counters |
| `AggregatingMergeTree` | merges aggregate states | exact rollups with `uniq`, `avg`, `quantile` |
| `CollapsingMergeTree` | cancels rows by `sign` | streaming updates without versions |
| `VersionedCollapsingMergeTree` | cancels by `sign` and version | out-of-order updates |

```sql
CREATE TABLE analytics.orders_rt
(
    order_id   UInt64,
    status     LowCardinality(String),
    amount     Decimal(18, 2),
    updated_at DateTime
)
ENGINE = ReplacingMergeTree(updated_at)
ORDER BY order_id;

-- SummingMergeTree follows the same shape: ENGINE = SummingMergeTree((hits, bytes))
```

`ReplacingMergeTree` deduplicates only during merges, so duplicates remain visible until a merge runs; `FINAL` or an `argMax` aggregation is required for correctness. `SummingMergeTree` keeps one row per key after merging, so a pre-merge sum can differ from the post-merge value.

[Table of Contents](#ClickHouse)

## How do the Distributed and Replicated engines work?
`Replicated*MergeTree` keeps each shard's data on multiple nodes through ClickHouse Keeper. `Distributed` is a thin table that routes reads and writes across shards of a cluster.

```sql
CREATE TABLE analytics.events_local ON CLUSTER analytics_cluster
(
    event_time DateTime,
    user_id    UInt64,
    country    LowCardinality(String),
    amount     Decimal(18, 2)
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/analytics/events', '{replica}')
PARTITION BY toYYYYMM(event_time)
ORDER BY (country, event_time);

CREATE TABLE analytics.events ON CLUSTER analytics_cluster AS analytics.events_local
ENGINE = Distributed('analytics_cluster', 'analytics', 'events_local', rand());

SELECT country, sum(amount) FROM analytics.events GROUP BY country;
```

Rules that avoid surprises: use `rand()` or a high-cardinality key for even distribution; use `GLOBAL JOIN` or `distributed_product_mode` for joins across `Distributed` tables; and write to a `Distributed` table only when you accept that the sharding key decides placement.

[Table of Contents](#ClickHouse)

## How does TTL manage the data lifecycle?
TTL statements run during merges to delete, move, or aggregate old data. Retention becomes part of the table definition instead of a batch job.

```sql
CREATE TABLE analytics.logs
(
    log_time DateTime,
    service  LowCardinality(String),
    level    LowCardinality(String),
    message  String
)
ENGINE = MergeTree()
PARTITION BY toDate(log_time)
ORDER BY (service, log_time)
TTL log_time + INTERVAL 30 DAY DELETE,
    log_time + INTERVAL 7 DAY TO VOLUME 'cold';

-- Aggregating TTL: keep hourly error rollups longer than raw rows
ALTER TABLE analytics.logs
    MODIFY TTL
        log_time + INTERVAL 7 DAY DELETE,
        log_time + INTERVAL 7 DAY GROUP BY toStartOfHour(log_time), service, level
            SET message = '', hits = count()
        WHERE level = 'error';
```

TTL is applied on merge, not on a wall clock, so a partition can briefly outlive its TTL. Pair `DELETE` TTLs with partition-level `DROP PARTITION` for hard guarantees, and use `TO VOLUME` or `TO DISK` with a storage policy that defines hot and cold tiers.

[Table of Contents](#ClickHouse)

## How do materialized views do incremental aggregation?
A ClickHouse materialized view is a trigger on inserts, not a cached query result. It reads the inserted block and writes to a target table, which makes it the standard tool for incremental aggregation.

```sql
CREATE TABLE analytics.daily_country
(
    day     Date,
    country LowCardinality(String),
    users   AggregateFunction(uniq, UInt64),
    revenue SimpleAggregateFunction(sum, Decimal(18, 2)),
    events  SimpleAggregateFunction(sum, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (day, country);

CREATE MATERIALIZED VIEW analytics.mv_daily_country TO analytics.daily_country AS
SELECT
    toDate(event_time) AS day,
    country,
    uniqState(user_id) AS users,
    sum(amount)        AS revenue,
    count()            AS events
FROM analytics.events
GROUP BY day, country;
```

Only rows inserted after the view is created are processed, so create the target table and view before backfilling raw data, or backfill the target explicitly. Use `AggregateFunction` for exact distinct or quantiles and `SimpleAggregateFunction` for plain `sum`, `min`, `max`, and `any`.

[Table of Contents](#ClickHouse)

## How do you ingest from Kafka with the Kafka engine?
The Kafka table engine turns a topic into a table. Reads consume messages, and a materialized view on top of it is the usual way to land data into a `MergeTree` target.

```sql
CREATE TABLE analytics.events_kafka
(
    event_time DateTime,
    user_id    UInt64,
    country    LowCardinality(String),
    amount     Decimal(18, 2)
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka-1:9092,kafka-2:9092',
    kafka_topic_list = 'events',
    kafka_group_name = 'clickhouse-events',
    kafka_format = 'JSONEachRow',
    kafka_num_consumers = 4,
    kafka_max_block_size = 65536,
    kafka_skip_broken_messages = 100;

CREATE MATERIALIZED VIEW analytics.mv_events_kafka TO analytics.events AS
SELECT event_time, user_id, country, amount
FROM analytics.events_kafka;
```

The Kafka engine table is a cursor, not storage, so never query it for analytics directly. Duplicate consumption is normal, so make the target idempotent or use `ReplacingMergeTree`. A parse error blocks the consumer unless `kafka_skip_broken_messages` is set.

[Table of Contents](#ClickHouse)

## How do async inserts batch inserts and Kafka Connect differ?
ClickHouse is built for bulk inserts. Row-by-row `INSERT ... VALUES` is the classic anti-pattern, because every insert creates a part and many small parts trigger merge pressure.

Async inserts let the server buffer small writes and form larger blocks, which suits many clients that each send a row at a time. Batch inserts are better when the client controls the flow.

```sql
INSERT INTO analytics.events SETTINGS
    async_insert = 1,
    wait_for_async_insert = 1,
    async_insert_max_data_size = 10485760,
    async_insert_busy_timeout_ms = 1000
VALUES (now(), 101, 'DE', 'purchase', 42.50);
```

```python
import clickhouse_connect

client = clickhouse_connect.get_client(host="ch-1", port=8123, database="analytics")

rows = [
    ("2026-10-04 10:00:00", 101, "DE", "purchase", 42.50),
    ("2026-10-04 10:00:01", 102, "FR", "view", 0.00),
]

client.insert(
    "events",
    rows,
    column_names=["event_time", "user_id", "country", "event_type", "amount"],
    settings={"async_insert": 1, "wait_for_async_insert": 1, "max_insert_threads": 4},
)
```

`max_insert_block_size` (default 1048576 rows) caps the block the server forms, `min_insert_block_size_rows` and `min_insert_block_size_bytes` control squashing before parts are written, `input_format_parallel_parsing` speeds up large file loads, and `async_insert_deduplicate` deduplicates identical buffered inserts on retries. Aim for at least 10k to 100k rows per part on a busy table.

The ClickHouse Kafka Connect sink is the alternative when you already run Kafka Connect and want exactly-once delivery and connector management in one place.

```json
{
  "name": "clickhouse-events-sink",
  "config": {
    "connector.class": "com.clickhouse.kafka.connect.ClickHouseSinkConnector",
    "tasks.max": "4",
    "topics": "events",
    "hostname": "ch-1",
    "port": "8443",
    "database": "analytics",
    "username": "ingest",
    "ssl": "true",
    "exactlyOnce": "true",
    "topic2TableMap": "events=events_raw"
  }
}
```

```bash
curl -s -X POST -H 'Content-Type: application/json' \
  --data @clickhouse-sink.json http://connect:8083/connectors
```

The Kafka engine is lower-latency and lives inside ClickHouse, but offsets and parse errors are managed by the server. Kafka Connect gives exactly-once semantics and DLQ handling at the cost of another service to operate. Both write into the same `MergeTree` targets.

[Table of Contents](#ClickHouse)

## How do codecs and compression work?
ClickHouse compresses every column independently and lets you choose a codec per column. Codecs exploit the column's value pattern, which is why the columnar layout compresses far better than row storage.

```sql
CREATE TABLE analytics.metrics
(
    ts          DateTime CODEC(DoubleDelta, ZSTD(3)),
    device_id   UInt64 CODEC(Delta, ZSTD(3)),
    temperature Float32 CODEC(Gorilla, ZSTD(3)),
    status      LowCardinality(String) CODEC(ZSTD(3)),
    raw         String CODEC(NONE)
)
ENGINE = MergeTree()
PARTITION BY toDate(ts)
ORDER BY (device_id, ts);

SELECT name, formatReadableSize(sum(data_uncompressed_bytes) / sum(data_compressed_bytes)) AS ratio
FROM system.columns WHERE table = 'metrics' GROUP BY name;
```

`Delta` and `DoubleDelta` are excellent for monotonically increasing timestamps and counters, `Gorilla` for slowly changing floats, `T64` for small integer ranges, and `ZSTD` as the general-purpose backstop. Higher ZSTD levels save storage but cost insert CPU. Check the real ratio in `system.columns` rather than assuming, and leave already-compressed payloads as `NONE`.

[Table of Contents](#ClickHouse)

## Which column types matter and what are the Nullable caveats?
Type choice drives both compression and query speed. The biggest wins come from replacing generic strings with specialized types.

```sql
CREATE TABLE analytics.sessions
(
    session_id  UUID,
    user_id     UInt64,
    country     LowCardinality(String),
    device      Enum8('desktop' = 1, 'mobile' = 2, 'tablet' = 3),
    started_at  DateTime64(3, 'UTC'),
    duration_ms UInt32,
    revenue     Decimal(18, 2),
    tags        Array(LowCardinality(String)),
    props       Map(String, String)
)
ENGINE = MergeTree()
ORDER BY (country, started_at);
```

+ `LowCardinality(String)` dictionary-encodes a column with fewer than roughly 10k distinct values. It saves space and speeds up grouping and filtering, but hurts if cardinality is actually high.
+ `Enum8` or `Enum16` is cheaper than `LowCardinality(String)` when the value set is fixed and known.
+ `Array`, `Map`, and `Tuple` are first-class, and array functions avoid the row explosion that join-then-group would cause.

`Nullable(T)` stores a separate null mask, blocks some optimizations, and cannot be used efficiently in the sort key, so prefer a default or an explicit sentinel.

```sql
-- Prefer a plain column with a default over Nullable on the hot path
CREATE TABLE analytics.events_no_null
(event_time DateTime, country LowCardinality(String) DEFAULT 'unknown')
ENGINE = MergeTree() ORDER BY (country, event_time);
```

Avoid `Nullable` inside `AggregateFunction` states and in join keys; `LowCardinality(Nullable(String))` is supported but compounds the cost. Keep one or two `Nullable` columns at the edges of a table, not across the sort key.

[Table of Contents](#ClickHouse)

## How do ClickHouse JOIN algorithms work?
Joins in ClickHouse are hash-based by default and the build side is the right-hand table. Distribution, memory, and algorithm all matter more than in a row-store.

```sql
SET join_algorithm = 'hash';
SET max_bytes_in_join = 20000000000;
SET join_use_nulls = 1;

SELECT e.country, d.region, count()
FROM analytics.events AS e
LEFT JOIN analytics.dict_country AS d ON e.country = d.country
GROUP BY e.country, d.region;
```

+ `hash` (default) - builds a hash table from the right side. Fast when the right side fits in memory.
+ `grace_hash` - hash join that spills to disk; the safest choice for large joins.
+ `parallel_hash` - parallel build and probe, good for large right sides on many cores.
+ `partial_merge` and `full_sorting_merge` - sort-merge joins that avoid a full hash table.
+ `direct` - uses the right table's storage order directly, with no hash table.
+ `GLOBAL JOIN` - required when joining two `Distributed` tables so the right side is sent to each shard once.

Keep the right-hand table small, watch `max_bytes_in_join` and `join_algorithm` in `system.query_log`, and prefer dictionaries over joins for repeated lookups.

[Table of Contents](#ClickHouse)

## How do dictionaries speed up lookups?
Dictionaries are key-value lookups loaded into memory or partly on SSD and refreshed on a lifetime. They replace a repeated join with a function call.

```sql
CREATE DICTIONARY analytics.country_region
(
    country String,
    region  String,
    manager String
)
PRIMARY KEY country
SOURCE(CLICKHOUSE(host 'ch-1' port 9000 db 'analytics' table 'country_reference' user 'default'))
LAYOUT(HASHED())
LIFETIME(MIN 300 MAX 600);

SELECT e.country,
       dictGet('analytics.country_region', 'region', e.country) AS region,
       count() AS events
FROM analytics.events AS e
WHERE e.event_time >= today() - 1
GROUP BY e.country, region
ORDER BY events DESC;
```

Layouts: `FLAT` for small numeric keys, `HASHED` for general keys, `COMPLEX_KEY_HASHED` for composite keys, `RANGE_HASHED` for time-bounded attributes, and `CACHE` or `SSD_CACHE` when the reference data is too large for memory. An unloaded or stale dictionary shows up in `system.dictionaries` as `status = 'NOT_LOADED'` or with an old `last_successful_update_time`, so monitor it like a job.

[Table of Contents](#ClickHouse)

## How do you read EXPLAIN output and optimize queries?
`EXPLAIN` has several modes, and `indexes = 1` is the one that tells you whether the query prunes data or scans everything.

```sql
EXPLAIN PIPELINE SELECT country, count() FROM analytics.events GROUP BY country;
EXPLAIN indexes = 1 SELECT count() FROM analytics.events WHERE country = 'DE';
```

Then confirm with the query log:

```sql
SELECT query_duration_ms,
       read_rows,
       read_bytes,
       memory_usage,
       ProfileEvents['SelectedMarks'] AS marks
FROM system.query_log
WHERE type = 'QueryFinish' AND query LIKE '%analytics.events%'
ORDER BY event_time DESC
LIMIT 10;
```

Optimization checklist:

+ Filter on the leading `ORDER BY` column so `PrimaryKey` granules are skipped.
+ Add a skipping index only for a column that appears in slow queries.
+ Reduce `SelectedMarks`; if it equals total marks, the sort key does not match the filter.
+ Replace `SELECT *` with explicit columns, because wide tables read many column files.
+ Prefer `uniqCombined` for approximate distinct counts and `AggregatingMergeTree` for repeated rollups.
+ Use `max_threads`, `max_memory_usage`, and `max_execution_time` as per-query guardrails, tracked in `system.processes`.

[Table of Contents](#ClickHouse)

## How do you deduplicate with ReplacingMergeTree and FINAL?
`ReplacingMergeTree` keeps the row with the greatest version per sort key during a merge. Because merges are asynchronous, duplicates remain queryable until then, and `FINAL` resolves them at read time.

```sql
CREATE TABLE analytics.users_rt
(
    user_id    UInt64,
    plan       LowCardinality(String),
    email      String,
    updated_at DateTime,
    is_deleted UInt8 DEFAULT 0
)
ENGINE = ReplacingMergeTree(updated_at, is_deleted)
ORDER BY user_id;
```

Three ways to read the deduplicated state:

```sql
-- Correct but merges everything at query time
SELECT * FROM analytics.users_rt FINAL WHERE is_deleted = 0;

-- Faster on large tables: aggregate at query time
SELECT user_id,
       argMax(plan, updated_at) AS plan,
       argMax(email, updated_at) AS email
FROM analytics.users_rt
GROUP BY user_id
HAVING argMax(is_deleted, updated_at) = 0;

-- Force a merge now, then query without FINAL
OPTIMIZE TABLE analytics.users_rt FINAL;
```

`FINAL` cost is controlled by `max_final_threads` and `do_not_merge_across_partitions_select_final`. For a steady-state production table, prefer the `argMax` pattern or partition by a key so `FINAL` only merges within one partition.

[Table of Contents](#ClickHouse)

## How do you build real-time analytics pipelines?
A real-time pipeline on ClickHouse is usually a raw table, one or more incremental materialized views, and a query layer over aggregated tables.

```sql
-- Raw events land in a short-lived MergeTree with TTL (see the TTL section)
CREATE TABLE analytics.events_minute
(
    minute  DateTime,
    country LowCardinality(String),
    events  SimpleAggregateFunction(sum, UInt64),
    revenue SimpleAggregateFunction(sum, Decimal(18, 2)),
    users   AggregateFunction(uniq, UInt64)
)
ENGINE = AggregatingMergeTree()
PARTITION BY toDate(minute)
ORDER BY (country, minute);

CREATE MATERIALIZED VIEW analytics.mv_events_minute TO analytics.events_minute AS
SELECT
    toStartOfMinute(event_time) AS minute,
    country,
    count()            AS events,
    sum(amount)        AS revenue,
    uniqState(user_id) AS users
FROM analytics.events_raw
GROUP BY minute, country;

SELECT country, sum(events) AS events, sum(revenue) AS revenue, uniqMerge(users) AS users
FROM analytics.events_minute
WHERE minute >= now() - INTERVAL '60' MINUTE
GROUP BY country
ORDER BY revenue DESC;
```

Patterns worth copying: keep raw data short-lived and rollups long-lived; make every stage idempotent because Kafka ingestion is at-least-once; and use `ReplacingMergeTree` for dimensions that change, with a periodic `OPTIMIZE` for readers that cannot tolerate duplicates.

[Table of Contents](#ClickHouse)

## How does ClickHouse compare with Druid BigQuery and Snowflake?
| System | Storage and compute | Strength | Trade-off |
|---|---|---|---|
| ClickHouse | tightly coupled per node, shared-nothing | sub-second queries on high-volume event data, self-managed or cloud | operational effort, limited multi-statement transactions |
| Druid | separated, segment-based | pre-aggregated time-series with rollup at ingestion | complex ingestion specs, weaker general SQL |
| BigQuery | fully separated, serverless | elastic scale, zero operations, big ecosystem | cost per query, less control over physical layout |
| Snowflake | separated, virtual warehouses | concurrency isolation, mature governance, SQL breadth | cost, higher latency for high-frequency small queries |

```text
Choose ClickHouse for high-volume append-only events with sub-second aggregation
targets and a team that can operate a cluster; choose BigQuery or Snowflake when
operations, governance, and elasticity matter more than hardware-level control.
```

ClickHouse also handles workloads the separated systems do not: `clickhouse-local` for ad-hoc files, S3 and Iceberg table functions for querying a lake in place, and materialized views that keep rollups fresher than a scheduled warehouse job.

[Table of Contents](#ClickHouse)

## What operational concerns matter in production?
ClickHouse rewards proactive operations. Three areas cause most incidents.

**Merges.** Merge throughput must keep up with insert rate, or parts accumulate and reads slow down.

```sql
SELECT database, table, elapsed, progress, num_parts FROM system.merges ORDER BY elapsed DESC;
```

**Keeper and replication.** Replication correctness depends on ClickHouse Keeper being healthy and quorum-connected.

```sql
SELECT * FROM system.replicas WHERE is_readonly OR absolute_delay > 60;
SELECT * FROM system.replication_queue ORDER BY create_time LIMIT 20;
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/tables';
```

**Mutations, backups, and guardrails.** `ALTER TABLE ... UPDATE` and `DELETE` are asynchronous rewrites, not point updates.

```sql
ALTER TABLE analytics.events DELETE WHERE event_time < today() - 365;
SELECT * FROM system.mutations WHERE is_done = 0;
BACKUP TABLE analytics.events TO Disk('backups', 'events.zip');
```

Configure storage policies for hot and cold volumes, cap concurrency and memory with `max_concurrent_queries`, `max_memory_usage`, and `max_threads`, and monitor `system.errors`, `system.events`, and disk free space, because `MergeTree` stops accepting inserts when a disk fills. Run DDL with `ON CLUSTER` so every node stays in sync.

[Table of Contents](#ClickHouse)

## Real world use cases for ClickHouse

### 1. Real-time product analytics

A consumer app streams click and purchase events through Kafka. A materialized view keeps per-minute rollups, and dashboards query the rollup table with sub-second latency while raw events stay for three days.

```sql
SELECT toStartOfMinute(event_time) AS minute,
       country,
       uniqMerge(users) AS users,
       sum(revenue)     AS revenue
FROM analytics.events_minute
WHERE minute >= now() - INTERVAL '6' HOUR
  AND country = 'DE'
GROUP BY minute
ORDER BY minute;
```

Why ClickHouse: incremental materialized views mean the dashboard never scans raw events, and the columnar engine aggregates millions of rows per query without a pre-computation job.

### 2. Observability and log analytics with retention tiers

A platform stores structured application logs, keeps 7 days on fast SSD and 90 days on cheaper storage, and searches messages with a token index.

```sql
CREATE TABLE observability.logs
(
    log_time DateTime,
    service  LowCardinality(String),
    level    LowCardinality(String),
    message  String CODEC(ZSTD(3)),
    INDEX idx_message message TYPE tokenbf_v1(8192, 3, 0) GRANULARITY 4
)
ENGINE = MergeTree()
PARTITION BY toDate(log_time)
ORDER BY (service, level, log_time)
TTL log_time + INTERVAL 7 DAY TO VOLUME 'hot',
    log_time + INTERVAL 90 DAY DELETE;
```

Why ClickHouse: TTL storage policies implement retention without a batch job, and skipping indexes keep free-text queries inside interactive latency.

### 3. CDC mirror of an operational database

Debezium events land in a `ReplacingMergeTree` keyed by primary key. A periodic `OPTIMIZE` keeps the table compact, and readers that need a fully deduplicated view use `FINAL` or `argMax` as described above.

```sql
CREATE TABLE cdc.customers_rt
(
    customer_id UInt64,
    name        String,
    email       String,
    updated_at  DateTime,
    is_deleted  UInt8 DEFAULT 0
)
ENGINE = ReplacingMergeTree(updated_at, is_deleted)
ORDER BY customer_id;
```

Why ClickHouse: `ReplacingMergeTree` gives last-write-wins semantics without a merge-on-read table format, and the columnar layout still answers analytical questions over the mirrored data.

### 4. Querying a lakehouse in place

A data team keeps Parquet and Iceberg tables in S3. Instead of loading everything, they query the lake directly with the `iceberg` and `s3` table functions from the same cluster that serves dashboards.

```sql
SELECT country, count() AS events, sum(amount) AS revenue
FROM iceberg('s3://acme-warehouse/analytics/events/', 'access_key', 'secret_key')
WHERE event_date = '2026-10-04'
GROUP BY country
ORDER BY revenue DESC;
```

Why ClickHouse: the same engine that serves real-time dashboards can scan object storage without a separate ingestion pipeline, which shortens the path from raw files to an answer.

### 5. Multi-tenant usage metering and billing

A SaaS platform meters API calls per customer per hour, sums counters with `SummingMergeTree`, and reconciles invoices with the same rollup table.

```sql
SELECT tenant_id,
       sum(calls) AS calls,
       round(sum(errors) / nullIf(sum(calls), 0), 4) AS error_rate
FROM billing.usage_hourly
WHERE hour >= toStartOfMonth(now())
GROUP BY tenant_id
ORDER BY calls DESC;
```

Why ClickHouse: `SummingMergeTree` keeps additive counters compact and merge-friendly, and the same rollup serves both live usage dashboards and month-end reconciliation.

[Table of Contents](#ClickHouse)
