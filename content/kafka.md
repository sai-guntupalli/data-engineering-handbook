## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Kafka

**Notebook:** [`notebooks/topics/kafka.ipynb`](../notebooks/topics/kafka.ipynb) - runnable version of this topic with self-checking exercises.

Apache Kafka is a distributed, partitioned, replicated commit log: producers append events to topics, consumers read them at their own pace, and retention is decoupled from consumption.

+ [What is Apache Kafka?](#What-is-Apache-Kafka)
+ [What is the traditional method of transferring messages?](#What-is-the-traditional-method-of-transferring-messages)
+ [What are the benefits of Apache Kafka over the traditional technique?](#What-are-the-benefits-of-Apache-Kafka-over-the-traditional-technique)
+ [What is the meaning of broker in Apache Kafka?](#What-is-the-meaning-of-broker-in-Apache-Kafka)
+ [What is the maximum size of a message that Kafka can receive?](#What-is-the-maximum-size-of-a-message-that-Kafka-can-receive)
+ [What is Zookeeper's role in Kafka's ecosystem and can we use Kafka without Zookeeper?](#What-is-Zookeepers-role-in-Kafkas-ecosystem-and-can-we-use-Kafka-without-Zookeeper)
+ [How are messages consumed by a consumer in Apache Kafka?](#How-are-messages-consumed-by-a-consumer-in-Apache-Kafka)
+ [How do Kafka partitions affect ordering and scalability?](#How-do-Kafka-partitions-affect-ordering-and-scalability)
+ [How do you define a partitioning key?](#How-do-you-define-a-partitioning-key)
+ [What is the role of the offset in Kafka?](#What-is-the-role-of-the-offset-in-Kafka)
+ [How do you design Kafka consumers for reliability?](#How-do-you-design-Kafka-consumers-for-reliability)
+ [How can you improve the throughput of a remote consumer?](#How-can-you-improve-the-throughput-of-a-remote-consumer)
+ [How can we get exactly-once messaging from Kafka during data production?](#How-can-we-get-exactly-once-messaging-from-Kafka-during-data-production)
+ [What is In-Sync Replicas (ISR) in Apache Kafka?](#What-is-In-Sync-Replicas-ISR-in-Apache-Kafka)
+ [How can we reduce churn (frequent changes) in ISR?](#How-can-we-reduce-churn-frequent-changes-in-ISR)
+ [When does a broker leave ISR?](#When-does-a-broker-leave-ISR)
+ [What does it indicate if a replica stays out of ISR for a long time?](#What-does-it-indicate-if-a-replica-stays-out-of-ISR-for-a-long-time)
+ [What happens if the preferred replica is not in the ISR list?](#What-happens-if-the-preferred-replica-is-not-in-the-ISR-list)
+ [What is the purpose of replication in Apache Kafka?](#What-is-the-purpose-of-replication-in-Apache-Kafka)
+ [Is it possible to get the message offset after producing to a topic?](#Is-it-possible-to-get-the-message-offset-after-producing-to-a-topic)
+ [What is log compaction in Kafka?](#What-is-log-compaction-in-Kafka)
+ [What is Kafka Connect and when do you use it?](#What-is-Kafka-Connect-and-when-do-you-use-it)
+ [How do you manage schemas with a schema registry?](#How-do-you-manage-schemas-with-a-schema-registry)
+ [How do you monitor Kafka consumer lag and cluster health?](#How-do-you-monitor-Kafka-consumer-lag-and-cluster-health)
+ [What is the difference between Apache Kafka, Apache Storm, and Apache Flink?](#What-is-the-difference-between-Apache-Kafka-Apache-Storm-and-Apache-Flink)
+ [List the various components in Kafka?](#List-the-various-components-in-Kafka)
+ [Can you explain the concept of leader and follower in the Kafka ecosystem?](#Can-you-explain-the-concept-of-leader-and-follower-in-the-Kafka-ecosystem)
+ [In the Producer, when does QueueFullException occur?](#In-the-Producer-when-does-QueueFullException-occur)
+ [Can you please explain the role of the Kafka Producer API?](#Can-you-please-explain-the-role-of-the-Kafka-Producer-API)
+ [How do you size a Kafka cluster for a real workload?](#How-do-you-size-a-Kafka-cluster-for-a-real-workload)
+ [Real world use cases for Kafka](#Real-world-use-cases-for-Kafka)

## What is Apache Kafka?

Apache Kafka is a distributed, partitioned, replicated commit log developed by Apache and written in Java and Scala. Producers append messages to topics, consumers pull them, and Kafka keeps the log for a configurable retention period independent of who has read it. That single design choice - a durable, replayable log - is why it is used both as a messaging system and as the ingestion backbone of streaming platforms.

```text
producers -> topic (partitions + replicas) -> consumer groups
                 |
                 +-- retention (time/size) or compaction (latest value per key)
```

[Table of Contents](#Apache-Kafka)

## What is the traditional method of transferring messages?

The traditional methods are:

+ **Queuing** - a pool of consumers reads from a queue and each message goes to exactly one of them.
+ **Publish-Subscribe** - every subscriber receives every message.

Kafka generalizes both with the **consumer group**: many consumers in one group share the partitions (queue semantics), while separate groups each get the full stream (publish-subscribe semantics).

```text
orders topic, 6 partitions
  group "fraud-detector"   -> 3 consumers, each owns 2 partitions (work sharing)
  group "lake-writer"      -> 2 consumers, each owns 3 partitions (independent copy)
```

[Table of Contents](#Apache-Kafka)

## What are the benefits of Apache Kafka over the traditional technique?

+ **Scalability** - add brokers to spread partitions and throughput horizontally.
+ **Performance** - sequential disk writes, zero-copy reads, and batching deliver very high throughput.
+ **Durability and reliability** - replication across brokers with configurable `acks` and `min.insync.replicas`.
+ **Fault tolerance** - partitions fail over to an in-sync follower automatically.
+ **Real-time processing** - consumers see records with milliseconds of latency.
+ **Decoupling** - producers do not know who consumes, and consumers do not know who produces.
+ **Replayability** - retention (or compaction) lets new consumers reprocess history.
+ **High availability** - the cluster keeps serving through individual broker failures.

The practical benefit is architectural: a new consumer can be added against an existing topic without touching any producer, and a broken consumer can be rewound and replayed.

[Table of Contents](#Apache-Kafka)

## What is the meaning of broker in Apache Kafka?

A broker is a server in the Kafka cluster that stores topic partitions and serves producer and consumer requests. Each partition has one leader broker and zero or more follower brokers. Brokers handle replication, and the cluster controller coordinates partition leadership.

```bash
# What a broker is doing, in one command
kafka-topics.sh --bootstrap-server broker1:9092 --describe --topic orders
```

[Table of Contents](#Apache-Kafka)

## What is the maximum size of a message that Kafka can receive?

Kafka's limit is controlled by `message.max.bytes` on the broker and `max.message.bytes` on the topic (default about 1 MB). Both can be raised, but large messages are an anti-pattern: they break batching, increase memory pressure, and slow replication.

```text
# Topic-level override (CLI) - prefer the smallest value that fits the payload
max.message.bytes=5242880

# Better answer for large payloads:
# put the blob in S3/GCS and publish a small reference message
{"event_id": "e-1", "s3_uri": "s3://acme-blobs/events/e-1.parquet", "size_bytes": 8421337}
```

Frameworks like Spark and Flink also have their own fetch limits (`fetch.max.bytes`, `max.partition.fetch.bytes`) which must be raised together with the broker setting.

[Table of Contents](#Apache-Kafka)

## What is Zookeeper's role in Kafka's ecosystem and can we use Kafka without Zookeeper?

Historically Zookeeper stored cluster metadata: broker membership, controller election, topic configuration, and ACLs. Modern Kafka uses **KRaft** (Kafka Raft Metadata mode), where a quorum of controller nodes manages metadata internally.

```bash
# KRaft: format storage and start a combined broker+controller
kafka-storage.sh random-uuid
kafka-storage.sh format -t <cluster-uuid> -c config/kraft/server.properties
kafka-server-start.sh config/kraft/server.properties
```

Why it matters in an interview: KRaft removes a second distributed system to operate, scales metadata better for very large clusters, and is the path for Kafka 4.x where ZooKeeper support is removed.

[Table of Contents](#Apache-Kafka)

## How are messages consumed by a consumer in Apache Kafka?

Consumption is pull-based. A consumer subscribes to topics, polls the broker for records, and tracks its position per partition as an **offset**. Offsets are committed to the `__consumer_offsets` topic (or stored externally), so a restart resumes where the group left off.

```python
from confluent_kafka import Consumer, KafkaError

consumer = Consumer({
    "bootstrap.servers": "broker1:9092,broker2:9092",
    "group.id": "orders-lake-writer",
    "auto.offset.reset": "earliest",     # only used when the group has no committed offset
    "enable.auto.commit": False,         # commit after processing succeeds
})

consumer.subscribe(["orders"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            raise RuntimeError(msg.error())
        write_to_lake(msg.key(), msg.value())
        consumer.commit(asynchronous=False)
finally:
    consumer.close()
```

[Table of Contents](#Apache-Kafka)

## How do Kafka partitions affect ordering and scalability?

A topic is split into partitions. Kafka guarantees order **within a partition**, not across the topic. More partitions mean more parallelism, but also more open files, longer rebalances, and a higher controller workload.

```text
key = customer_id  -> all events for one customer land in the same partition -> per-customer order
different customers -> different partitions -> processed in parallel
```

Rules of thumb: choose a partition count that is a small multiple of the expected consumer count, and never change the partitioning key mid-stream unless you accept reordering. Increasing a topic's partition count is allowed; decreasing it is not.

[Table of Contents](#Apache-Kafka)

## How do you define a partitioning key?

The key decides the partition: Kafka hashes it (`murmur2`) and maps it to a partition, unless you supply a custom partitioner. A good key is stable, reasonably high-cardinality, and aligned with the ordering your consumers need.

```python
def partition_key(order):
    # stable, high-cardinality key: events for one customer stay ordered together
    return order["customer_id"].encode("utf-8")

producer.produce("orders", key=partition_key(order), value=order_json)
```

Anti-patterns: `None` keys (round-robin, no ordering), a low-cardinality key that creates hot partitions (for example `country`), or a key that changes over the life of an entity (it breaks per-entity ordering).

[Table of Contents](#Apache-Kafka)

## What is the role of the offset in Kafka?

An offset is the unique, monotonically increasing position of a record inside a partition. Consumers commit offsets to mark progress; lag is `log-end offset - committed offset`. Offsets are per partition and per consumer group, which is why two groups can be at completely different positions on the same topic.

```bash
# See current offsets and lag for every partition of a group
kafka-consumer-groups.sh --bootstrap-server broker1:9092 \
  --describe --group orders-lake-writer
```

[Table of Contents](#Apache-Kafka)

## How do you design Kafka consumers for reliability?

Four rules cover most production incidents:

+ Commit offsets **after** the downstream write succeeds (`enable.auto.commit=false`).
+ Make writes **idempotent** (upsert on a business key) because crashes between write and commit replay records.
+ Handle **rebalances**: finish or abandon work before partitions are revoked; use cooperative rebalancing and static membership to reduce churn.
+ Send unrecoverable failures to a **dead-letter topic** with context instead of blocking the partition forever.

```python
def on_assign(consumer, partitions):
    # called on rebalance: seek to committed offsets explicitly when you manage state
    print("assigned:", [p.partition for p in partitions])

consumer.subscribe(["orders"], on_assign=on_assign)
```

This is at-least-once delivery. Exactly-once is a property of the whole pipeline (Kafka transactions plus an idempotent sink), not of the consumer alone.

[Table of Contents](#Apache-Kafka)

## How can you improve the throughput of a remote consumer?

+ **Increase fetch size** - raise `fetch.min.bytes`, `fetch.max.wait.ms`, and `max.partition.fetch.bytes` so each round trip returns more data.
+ **Scale out partitions and consumers** - throughput is bounded by partition count per group.
+ **Batch writes downstream** - buffer records and flush in batches instead of one remote write per record.
+ **Compress** - use `zstd` or `lz4` so fewer bytes cross the network.
+ **Use efficient serialization** - Avro/Protobuf with a registry instead of verbose JSON.
+ **Fix network topology** - keep consumers in the same region/AZ as the brokers.
+ **Cache reference data** - avoid a lookup per record for slowly changing dimensions.
+ **Run the sink in the consumer** - a Spark/Flink job that writes Parquet directly avoids a second hop.

```python
consumer = Consumer({
    "bootstrap.servers": "broker1:9092",
    "group.id": "remote-consumer",
    "fetch.min.bytes": 1048576,     # wait for ~1 MB before returning
    "fetch.max.wait.ms": 500,
    "max.partition.fetch.bytes": 4194304,
})
```

[Table of Contents](#Apache-Kafka)

## How can we get exactly-once messaging from Kafka during data production?

Exactly-once **within Kafka** is achieved with an idempotent producer plus transactions:

1. **Enable idempotence** - `enable.idempotence=true` adds a producer id and sequence numbers, so retries cannot duplicate records.
2. **Use transactions** - set `transactional.id`, then wrap a batch in `begin_transaction()` / `commit_transaction()` / `abort_transaction()`. For consume-transform-produce, pass the consumer's offsets to `send_offsets_to_transaction()`.
3. **Set durability correctly** - `acks=all` plus `min.insync.replicas=2` so an acknowledged write survives a broker failure.
4. **Keep ordering** - with idempotence, `max.in.flight.requests.per.connection` can be up to 5 without reordering; do not raise it blindly.
5. **Make the sink idempotent** - transactions cannot cover a database outside Kafka, so the downstream merge still needs a key.

```python
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "broker1:9092",
    "transactional.id": "orders-etl-1",
    "enable.idempotence": True,
    "acks": "all",
})

producer.init_transactions()
producer.begin_transaction()
try:
    for order in batch:
        producer.produce("orders", key=order["customer_id"], value=order["json"])
    producer.commit_transaction()
except Exception:
    producer.abort_transaction()
    raise
```

[Table of Contents](#Apache-Kafka)

## What is In-Sync Replicas (ISR) in Apache Kafka?

ISR is the set of replicas that are fully caught up with the leader within `replica.lag.time.max.ms`. The leader serves reads and writes; followers in the ISR are eligible to be elected leader. With `acks=all`, a write is acknowledged only after every ISR replica has it, which is why `min.insync.replicas` is the real durability control.

```text
orders-0: leader=broker1  replicas=[1,2,3]  isr=[1,2,3]        healthy
orders-0: leader=broker1  replicas=[1,2,3]  isr=[1,2]          one follower lagging
orders-0: isr=[1] with min.insync.replicas=2 -> producers fail (UnderReplicated)
```

[Table of Contents](#Apache-Kafka)

## How can we reduce churn (frequent changes) in ISR?

+ **Fix the network** - unstable links and saturated NICs make followers fall behind.
+ **Tune `replica.lag.time.max.ms`** - too tight causes false evictions; too loose hides real lag.
+ **Give brokers resources** - replication shares CPU, disk, and page cache with serving traffic.
+ **Separate replication traffic** - dedicated NICs or rack-aware placement reduce contention.
+ **Cap producer load** - use quotas (`kafka-configs.sh --alter --add-config 'producer_byte_rate=...')`) to stop one client from starving replication.
+ **Watch disk health** - a slow disk shows up as ISR churn long before it fails.

[Table of Contents](#Apache-Kafka)

## When does a broker leave ISR?

+ **Falling behind** - the follower does not fetch/catch up within `replica.lag.time.max.ms`.
+ **Broker failure** - crash, network partition, or an unclean shutdown removes its replicas.
+ **Unclean leader election settings** - with `unclean.leader.election.enable=true`, an out-of-sync replica can become leader, trading durability for availability.
+ **Manual intervention** - an operator can reassign or remove replicas, but this should be a deliberate maintenance action.

[Table of Contents](#Apache-Kafka)

## What does it indicate if a replica stays out of ISR for a long time?

It means that replica cannot keep up with the leader's append rate. Persistent causes are slow disks, insufficient network bandwidth, an overloaded broker, or a JVM/GC problem. The risks are reduced fault tolerance (fewer replicas can take over) and, with `acks=all` and `min.insync.replicas` set to the replica count, failed writes.

```bash
# Check ISR and under-replicated partitions
kafka-topics.sh --bootstrap-server broker1:9092 --describe --under-replicated-partitions
```

[Table of Contents](#Apache-Kafka)

## What happens if the preferred replica is not in the ISR list?

The preferred replica is the first replica in the assignment list, normally the leader. If it is out of the ISR, a different in-sync replica leads instead. Kafka does not route clients to an out-of-sync broker; the controller simply keeps leadership on a healthy replica. Once the preferred replica catches up, you can move leadership back with `kafka-leader-election.sh` to rebalance load.

```bash
kafka-leader-election.sh --bootstrap-server broker1:9092 \
  --election-type preferred --topic orders --partition 0
```

[Table of Contents](#Apache-Kafka)

## What is the purpose of replication in Apache Kafka?

Replication provides durability and availability: every partition exists on multiple brokers, so a broker failure does not lose data or stop the partition from being served. The replication factor plus `min.insync.replicas` define the failure model.

```text
replication.factor=3, min.insync.replicas=2, acks=all
-> tolerate 1 broker failure with no data loss and no write interruption
-> tolerate 2 broker failures only for reads, writes fail (safer than silent data loss)
```

[Table of Contents](#Apache-Kafka)

## Is it possible to get the message offset after producing to a topic?

Yes. The delivery report callback returns the topic, partition, and offset assigned by the leader.

```python
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "broker1:9092", "acks": "all"})

def on_delivery(err, msg):
    if err is not None:
        raise RuntimeError(f"produce failed: {err}")
    print(f"stored {msg.topic()}[{msg.partition()}] at offset {msg.offset()}")

producer.produce("orders", key="C123", value=b'{"amount": 42}', callback=on_delivery)
producer.flush()
```

You can also read the offset from the record metadata on the Java client (`RecordMetadata.offset()`) or fetch it later with `kafka-console-consumer.sh --property print.offset=true`.

[Table of Contents](#Apache-Kafka)

## What is log compaction in Kafka?

Compaction keeps at least the latest value for every key and eventually removes older records with the same key. The topic becomes a changelog that can rebuild state - ideal for configuration, user profiles, and CDC streams where only the current row matters.

```bash
kafka-topics.sh --bootstrap-server broker1:9092 \
  --create --topic customer-profile \
  --partitions 12 --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.1 \
  --config segment.ms=3600000
```

```text
before compaction:  C123:v1  C456:v1  C123:v2  C123:v3(deleted tombstone)
after compaction:   C456:v1  C123:v3
```

Compaction is not the same as retention: a `delete` policy drops data by age or size regardless of key, while `compact` preserves the latest state per key indefinitely.

[Table of Contents](#Apache-Kafka)

## What is Kafka Connect and when do you use it?

Kafka Connect is a framework for moving data into and out of Kafka with declarative connectors instead of custom producer/consumer code. Use it for source/sink integrations (Postgres CDC, S3, Snowflake, Elasticsearch, Iceberg) when you do not need custom transformation logic.

```json
{
  "name": "orders-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "pg-primary",
    "database.dbname": "orders",
    "topic.prefix": "cdc",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState"
  }
}
```

```bash
curl -X POST -H "Content-Type: application/json" \
  --data @orders-cdc.json http://connect:8083/connectors
```

Reach for custom code when the transformation is complex; Connect Single Message Transforms (SMTs) are deliberately limited.

[Table of Contents](#Apache-Kafka)

## How do you manage schemas with a schema registry?

A schema registry stores versioned Avro, Protobuf, or JSON schemas and enforces compatibility rules so producers cannot break consumers. Messages carry a short schema id instead of the full schema, which keeps payloads small.

```python
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

registry = SchemaRegistryClient({"url": "http://schema-registry:8081"})
serializer = AvroSerializer(registry, schema_str=order_schema_str)

producer.produce(
    "orders",
    key=order["customer_id"],
    value=serializer(order, SerializationContext("orders", MessageField.VALUE)),
)
```

Compatibility modes (`BACKWARD` is the common default) decide what a producer may change: add optional fields with defaults, never rename or retype a field in place.

[Table of Contents](#Apache-Kafka)

## How do you monitor Kafka consumer lag and cluster health?

The signals that matter:

+ **Consumer lag per group/partition** - growing lag means the consumer cannot keep up.
+ **Under-replicated and offline partitions** - replication problems are the leading indicator of an incident.
+ **ISR shrink rate** - churn predicts failover risk.
+ **Request latency (produce/fetch p99) and request queue size** - saturation.
+ **Disk usage and page cache** - retention plus throughput decides capacity.
+ **Controller and broker count** - a flapping controller destabilizes the cluster.

```bash
# Per-partition lag
kafka-consumer-groups.sh --bootstrap-server broker1:9092 --describe --group orders-lake-writer

# Under-replicated partitions
kafka-topics.sh --bootstrap-server broker1:9092 --describe --under-replicated-partitions
```

Export JMX metrics to Prometheus/Grafana and alert on lag trend, not on a single sample.

[Table of Contents](#Apache-Kafka)

## What is the difference between Apache Kafka, Apache Storm, and Apache Flink?

+ **Kafka** is the durable log and transport layer: it stores streams, decouples producers and consumers, and can do lightweight stream processing with Kafka Streams.
+ **Storm** is a low-latency, record-at-a-time stream processor, historically popular for simple real-time pipelines; its stateful processing story is weaker than Flink's.
+ **Flink** is a full stream-processing engine with event-time semantics, exactly-once stateful processing, windowing, and checkpointing, and it can also run batch jobs.

The usual production combination is Kafka for ingestion and Flink (or Spark Structured Streaming) for stateful transformations - the log buffers and the engine computes.

[Table of Contents](#Apache-Kafka)

## List the various components in Kafka?

+ **Topic** - a named, partitioned, replicated log.
+ **Producer** - appends records, choosing the partition via the key.
+ **Broker** - a server storing partitions and serving clients.
+ **Consumer** - pulls records; consumers in a group share partitions.
+ **Consumer group** - the unit of parallelism and offset tracking.
+ **Controller** - elects partition leaders and manages cluster metadata (KRaft quorum in modern Kafka).
+ **Partition** - the unit of ordering, replication, and parallelism.
+ **Offset** - position of a record in a partition.
+ **Rebalance** - reassignment of partitions when group membership changes.

[Table of Contents](#Apache-Kafka)

## Can you explain the concept of leader and follower in the Kafka ecosystem?

Each partition has one leader and several followers. Producers and consumers talk to the leader; followers replicate the leader's log. If the leader fails, the controller elects a new leader from the ISR.

```text
orders-0  leader=broker1  followers=[broker2, broker3]
   broker2, broker3 fetch from broker1 and append in the same order
   broker1 fails -> controller promotes broker2 (it is in the ISR) -> clients reconnect
```

For availability across racks/regions, place replicas on separate failure domains with `broker.rack`, so a single rack outage cannot take all replicas.

[Table of Contents](#Apache-Kafka)

## In the Producer, when does QueueFullException occur?

`QueueFullException` (Java) or `BufferError: Local: Queue full` (librdkafka) happens when the application produces faster than the producer can send and the in-memory buffer (`buffer.memory` / `queue.buffering.max.messages`) fills. Production options:

+ Slow down or batch the producer input (`linger.ms` and larger batches).
+ Increase `buffer.memory` (temporary relief, more heap pressure).
+ Scale brokers/partitions so the cluster can absorb the rate.
+ Handle the error explicitly instead of dropping messages.

```python
try:
    producer.produce("orders", key=key, value=value)
except BufferError:
    producer.poll(1.0)          # let the client drain and retry
    producer.produce("orders", key=key, value=value)
```

Ignoring this error is how pipelines silently lose records.

[Table of Contents](#Apache-Kafka)

## Can you please explain the role of the Kafka Producer API?

The Producer API sends record streams to topics. It handles partition selection, batching, compression, retries, and acknowledgements, and exposes both synchronous and asynchronous styles: `send()` returns a future you can block on (sync) or attach a callback to (async).

```python
from confluent_kafka import Producer

producer = Producer({
    "bootstrap.servers": "broker1:9092",
    "acks": "all",
    "enable.idempotence": True,
    "linger.ms": 20,
    "batch.size": 262144,
    "compression.type": "zstd",
})

def report(err, msg):
    if err is not None:
        raise RuntimeError(err)

# async: fire many records, then flush
for order in orders:
    producer.produce("orders", key=order["customer_id"], value=order["json"], callback=report)
producer.flush()      # flush blocks until all buffered records are delivered or failed
```

The consumer side has the analogous Consumer API, plus `commit()`, `subscribe()`, `assign()`, and `seek()`.

[Table of Contents](#Apache-Kafka)

## How do you size a Kafka cluster for a real workload?

Sizing is arithmetic: peak throughput, replication overhead, retention, and headroom.

```text
Given: 50 MB/s peak ingest, replication factor 3, retention 7 days, 30% headroom

raw daily data      = 50 MB/s * 86,400 s           ~= 4.3 TB/day
with replication    = 4.3 TB * 3                   ~= 13 TB/day
7-day retention     = 13 TB * 7                    ~= 91 TB usable
with 30% headroom   = 91 TB / 0.7                  ~= 130 TB usable

partitions: target ~10-50 MB/s per partition for healthy parallelism
           50 MB/s / 20 MB/s per partition         ~= 3+ partitions minimum;
           choose 24-48 for growth and consumer parallelism

brokers:   spread ~4-8 TB usable per broker with fast NVMe
           ~20 brokers for storage, plus replication CPU/network headroom
```

Also account for consumer fan-out (each consumer group reads the data again), compaction topics, and the impact of a broker loss: with RF=3 you must still meet `min.insync.replicas` after losing one broker.

[Table of Contents](#Apache-Kafka)

## Real world use cases for Kafka

### 1. CDC from operational databases into a lakehouse

Debezium reads the Postgres WAL and publishes change events per table with the primary key as the message key, preserving per-row order. A consumer (or Kafka Connect sink) merges them into Iceberg/Delta.

```python
# Spark Structured Streaming: Kafka -> Iceberg with checkpointed exactly-once progress
stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "cdc.public.orders")
    .option("startingOffsets", "earliest")
    .load()
)

parsed = stream.selectExpr(
    "CAST(key AS STRING) AS order_id",
    "from_json(CAST(value AS STRING), 'op STRING, after STRUCT<order_id STRING, amount DOUBLE, status STRING>') AS payload",
)

(
    parsed.select("order_id", "payload.op", "payload.after.*")
    .writeStream.format("iceberg")
    .option("checkpointLocation", "s3://acme-checkpoints/cdc-orders/")
    .outputMode("append")
    .toTable("lakehouse.orders_cdc")
)
```

Why Kafka: the WAL is captured once, and every downstream system (lakehouse, cache, search index) consumes the same ordered stream independently.

### 2. Event-driven microservices

Order, payment, and notification services communicate through topics instead of synchronous calls. The order service publishes `order.created`; payment consumes it and publishes `payment.settled`; fulfillment reacts.

```text
order-service --order.created--> [orders] --payment-service--> [payments] --fulfillment
                                    |
                                    +-- analytics consumer (independent group)
```

Why Kafka: services scale and deploy independently, failures are buffered by the log, and new consumers can be added without changing producers.

### 3. Real-time fraud detection

Transactions are produced with `account_id` as the key so each account's events are ordered. A Flink job keeps per-account state and raises an alert when velocity or amount thresholds are crossed within a window.

```python
# Keying by account keeps state and ordering local to each account
transactions = stream.key_by(lambda txn: txn.account_id)
alerts = (
    transactions.window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .process(VelocityDetector())
)
alerts.sink_to(KafkaSink(topic="fraud.alerts"))
```

Why Kafka: sub-second latency with replayable history for tuning and backtesting the detection rules.

### 4. Log and metric aggregation

Application and infrastructure logs are shipped to topics, then consumed by an Elasticsearch sink and an S3 archiver. Retention is short on the hot topic and long in object storage.

Why Kafka: one ingestion path decouples many producers from many sinks, and a burst of logs cannot take down the search cluster because Kafka absorbs the spike.

### 5. IoT telemetry at the edge

Gateways batch sensor readings into Kafka; a stream job downsamples raw readings into 1-minute aggregates and writes them to a time-series store.

```python
# Compress aggressively: telemetry is repetitive and high volume
producer = Producer({
    "bootstrap.servers": "edge-broker:9092",
    "compression.type": "zstd",
    "linger.ms": 50,
})
```

Why Kafka: it handles high-volume, append-only telemetry with configurable retention, and the same data feeds dashboards, alerts, and ML feature pipelines.

[Table of Contents](#Apache-Kafka)
