import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from kafka_common import HELPERS, INTRO, SETUP_PIP
from nbtools import build, run

PATH = "notebooks/topics/kafka/kafka-01-log-and-partitions.ipynb"
SPEC = f"""%% md
# Kafka 1: The log and partitions

A Kafka topic is an append-only log split into partitions. This lesson shows what that means for the order you can
rely on, how a record's key picks its partition, why two client libraries can disagree about that choice, and how
a retained log lets any reader replay history.

{INTRO}

{SETUP_PIP}
%% md
## Setup and sample data

The next cell starts the mock cluster and defines two helpers used throughout the Kafka lessons: `produce` sends
`(key, value)` pairs and returns where each record landed, and `consume` reads records back with a consumer group.
Topics are created automatically on first use, with four partitions each.

{HELPERS}
%% md
## Topics, partitions and offsets

A **topic** is a named stream of records, such as `orders`. Each topic is split into **partitions**, and each
partition is a separate append-only log on a broker. When a record is appended, the partition gives it the next
**offset**: 0, 1, 2 and so on. An offset identifies a record only together with its partition: "partition 2,
offset 5" is an address; "offset 5" on its own is not.

The producer's delivery report says where each record went. Here six order events for three orders are sent with
the order ID as the key.

**Where it matters**

Every replay, lag metric and consumer checkpoint is expressed as partition-plus-offset, so reading delivery reports
and consumer positions starts here.

**Watch out for**

Offsets are not timestamps and do not line up across partitions: offset 3 in partition 0 may be older or newer than
offset 1 in partition 2. There is no global order across a topic.
%% code
events = [
    ("order-10", "placed"),
    ("order-11", "placed"),
    ("order-10", "paid"),
    ("order-12", "placed"),
    ("order-11", "cancelled"),
    ("order-10", "shipped"),
]
for partition, offset, key, value in produce("orders", events):
    print(f"partition {{partition}} offset {{offset}}: {{key}} {{value}}")
%% md
**What to notice:** Each partition numbers its own records from 0. Orders 10 and 12 hash to partition 3, so their
four records take offsets 0 to 3 there, while order 11's two records start again at offset 0 in partition 1.
Partitions 0 and 2 received nothing: with only three keys, some partitions stay empty.
%% md
## Keys decide the partition, and the partition decides the order

The producer hashes the key to choose a partition, so every record with the same key lands in the same partition.
Kafka guarantees order **within a partition** only. Together these give the guarantee most pipelines rely on:
**all events for one key are read in the order they were written**.

The consumer below reads the topic back. Grouping by key shows each order's history in sequence, even though the
records of different orders interleave.

**Where it matters**

Choose the key so that events which must be applied in order share it: an order ID for an order's status changes,
an account ID for balance updates, a primary key for change-data-capture rows.

**Watch out for**

Records without a key are spread across partitions for throughput, so they have no order relative to each other.
Changing the number of partitions later changes which partition a key hashes to, which breaks per-key order for
records written across the change.
%% code
history = {{}}
for partition, offset, key, value in consume("orders", group="history", expected=len(events)):
    history.setdefault(key, []).append(value)
for key, values in sorted(history.items()):
    print(key, "->", values)
%% md
**What to notice:** Each order's events come back in the order they were produced (`placed`, `paid`, `shipped` for
order 10) because they share one partition. Nothing in Kafka orders order 10's events relative to order 11's.
%% md
## Partitioners must match across clients

The function that maps a key to a partition is the **partitioner**. The Java client, Kafka Streams and Kafka Connect
use **murmur2**. librdkafka, which underlies `confluent-kafka` for Python, Go and .NET, defaults to
`consistent_random`, a CRC32 hash. The same key can therefore land in different partitions depending on which
library produced it.

**Where it matters**

A topic written by a Python service and a Java service, or a Python producer feeding a Kafka Streams join, must agree
on partitions, or records for one key split across partitions and lose their order.

**Watch out for**

The mismatch is silent: both producers succeed. Set `partitioner: murmur2_random` in librdkafka clients that share
topics with Java clients.
%% code
keys = ["order-10", "order-11", "order-12", "order-13"]
for partitioner in ["consistent_random", "murmur2_random"]:
    placed = produce(f"orders-{{partitioner}}", [(key, "placed") for key in keys], partitioner=partitioner)
    print(f"{{partitioner:>17}}:", {{key: partition for partition, _, key, _ in placed}})
%% md
**What to notice:** Orders 12 and 13 happen to land in the same partition under both hash functions, but orders 10
and 11 move (from 3 to 2 and from 1 to 2). A consumer or join that assumes murmur2 placement would look for them in
the wrong partition.
%% md
## Retention and replay

Reading does not remove records. A topic keeps records for its **retention** period (for example seven days) or up
to a size limit, whichever comes first, and every consumer group tracks its own position. A new group starts from
the beginning or the end, as `auto.offset.reset` says, and any reader can **seek** to a chosen offset and read
forward again.

`read_from` below assigns one partition directly, without a group, and reads it from a given offset to the end.

**Where it matters**

Replay is how you rebuild a downstream table after a bug fix, backfill a new consumer, or reprocess a bad hour,
without asking the source system to send the data again.

**Watch out for**

Replay only reaches as far back as retention. Records older than that are deleted for good, so a consumer that is
down for longer than the retention period cannot catch up from Kafka alone.
%% code
def read_from(topic, partition, offset):
    reader = Consumer({{"bootstrap.servers": BOOTSTRAP, "group.id": "replay", "enable.auto.commit": False}})
    _, end = reader.get_watermark_offsets(TopicPartition(topic, partition), timeout=10)
    reader.assign([TopicPartition(topic, partition, offset)])
    records = []
    while offset < end:
        msg = reader.poll(1.0)
        if msg is not None and not msg.error():
            records.append((msg.offset(), text(msg.key()), text(msg.value())))
            offset = msg.offset() + 1
    reader.close()
    return records


print("a second group reads everything again:", len(consume("orders", group="audit", expected=len(events))))
print("partition 3 from offset 2:", read_from("orders", partition=3, offset=2))
%% md
**What to notice:** The `audit` group reads all six records even though `history` already read them: positions are
per group. Seeking partition 3 to offset 2 skips the first two records there and returns only the last two:
order 12's `placed` and order 10's `shipped`.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Prove per-key order

**Difficulty:** Easy · about 10 min

Produce five events for `customer-7` interleaved with events for `customer-8` to a new topic `profile-changes`.
Read the topic back and show that `customer-7`'s events arrive in the order you sent them.
%% code
# Try your solution here.
%% solution
changes = [("customer-7", f"v{{i}}") for i in range(1, 6)]
changes = [record for pair in zip(changes, [("customer-8", "noise")] * 5) for record in pair]
produce("profile-changes", changes)
received = [value for _, _, key, value in consume("profile-changes", group="ex1", expected=10) if key == "customer-7"]
print(received)
print("in order:", received == [f"v{{i}}" for i in range(1, 6)])
%% md
### Exercise 2: Replay one partition

**Difficulty:** Easy · about 10 min

Find the partition that holds `order-11` in the `orders` topic and replay it from offset 1.
%% code
# Try your solution here.
%% solution
partition = next(p for p, _, key, _ in consume("orders", group="ex2", expected=len(events)) if key == "order-11")
print("order-11 lives in partition", partition)
print(read_from("orders", partition=partition, offset=1))
%% md
### Exercise 3: Check a mixed-language topic

**Difficulty:** Medium · about 10 min

A Java service and a Python service both write `invoice-*` keys to one topic. For keys `invoice-1` to `invoice-6`,
which keys would land in different partitions if the Python producer kept the default partitioner?
%% code
# Try your solution here.
%% solution
invoices = [f"invoice-{{i}}" for i in range(1, 7)]
default = {{k: p for p, _, k, _ in produce("invoices-default", [(k, "x") for k in invoices])}}
java_like = {{k: p for p, _, k, _ in produce("invoices-murmur2", [(k, "x") for k in invoices], partitioner="murmur2_random")}}
print("would split:", [key for key in invoices if default[key] != java_like[key]])
%% md
## Key takeaways

- A topic is a set of partitions; each partition is an append-only log, and an offset is only meaningful with its
  partition.
- Kafka orders records within a partition, never across a topic. Pick the key so that events that must stay in
  order share it.
- Producers in different languages must use the same partitioner. Set `murmur2_random` in librdkafka clients that
  share topics with Java.
- Reading does not consume records: each group keeps its own position, and any reader can seek back as far as
  retention allows.
%% md
**Next:** [Kafka 2: Producers, batching and retries](kafka-02-producers.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
