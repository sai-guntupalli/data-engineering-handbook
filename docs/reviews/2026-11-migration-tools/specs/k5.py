import sys

sys.path.insert(0, "/private/tmp/claude-501/-Users-sai-WS-data-engineering-handbook/1f47be1b-1880-4d6b-87ef-e637e7c9e78a/scratchpad/tools2")
from kafka_common import HELPERS, INTRO
from nbtools import build, run

PATH = "notebooks/topics/kafka/kafka-05-connect-and-schemas.ipynb"
SPEC = f"""%% md
# Kafka 5: Connect, schemas and change events

Most data in Kafka arrives through connectors, as change events from databases, encoded against a schema. This
lesson replays a change-data-capture stream into a table, shows what log compaction keeps, encodes records with Avro
the way a schema registry does, tests which schema changes are safe, and reads a Kafka Connect configuration.

{INTRO}
%% code
# Setup: install notebook dependencies in Colab.
!pip install -q confluent-kafka~=2.16 fastavro
%% md
## Setup and sample data

The next cell starts the mock cluster and defines the helpers from Kafka 1. The sample data is a change stream for a
`customers` table in the shape Debezium produces: an operation code, the row before and after the change, and the
primary key as the record key.

{HELPERS}
import json

changes = [
    ("1", {{"op": "c", "before": None, "after": {{"id": 1, "email": "ana@example.com", "tier": "basic"}}}}),
    ("2", {{"op": "c", "before": None, "after": {{"id": 2, "email": "ben@example.com", "tier": "basic"}}}}),
    ("1", {{"op": "u", "before": {{"id": 1, "tier": "basic"}}, "after": {{"id": 1, "email": "ana@example.com", "tier": "plus"}}}}),
    ("2", {{"op": "d", "before": {{"id": 2, "email": "ben@example.com", "tier": "basic"}}, "after": None}}),
    ("2", None),  # tombstone: no value, so compaction can eventually drop key 2
]
log = produce("dbserver.public.customers", [(key, json.dumps(value) if value else None) for key, value in changes])
print(len(log), "change records in partitions", sorted({{partition for partition, *_ in log}}))
%% md
## Change events and the envelope

A CDC connector such as Debezium reads the database's transaction log and publishes one record per row change.
Each value carries `op` (`c` create, `u` update, `d` delete, `r` read during the initial snapshot) and the row
`before` and `after` the change. The key is the table's primary key, so all changes to one row stay in one
partition and in order.

A delete is followed by a **tombstone**: a record with the same key and no value. Consumers that materialize the
table treat it as "this key is gone", and compaction uses it to remove the key.

**Where it matters**

Replicating an operational database into a warehouse or lake, building caches and search indexes, and feeding the
SCD Type 2 history from the data-modeling lessons all start by applying a change stream like this one.

**Watch out for**

Apply changes in log order per key, and handle `d` and tombstones explicitly; a consumer that only reads `after`
resurrects deleted rows as nulls. Updates may carry only changed columns in `before`, depending on the database's
replica identity settings.
%% code
table = {{}}
for _, offset, key, value in consume("dbserver.public.customers", group="replica", expected=len(changes)):
    if value is None:
        table.pop(key, None)  # tombstone
        continue
    event = json.loads(value)
    if event["op"] in ("c", "r", "u"):
        table[key] = event["after"]
    elif event["op"] == "d":
        table.pop(key, None)
print(table)
%% md
**What to notice:** After five records the replica holds only customer 1, at tier `plus`. Customer 2 was created and
then deleted, and the tombstone confirmed the delete. Because each customer's changes share a key, they were applied
in the order the database committed them.
%% md
## Log compaction keeps the latest value per key

A topic with `cleanup.policy=compact` is not trimmed by age. Instead the broker periodically rewrites old segments,
keeping only the **latest record for each key**. A tombstone is kept for `delete.retention.ms` so slow consumers see
the delete, and then removed with its key. A compacted topic is therefore a durable, replayable snapshot of a table.

The mock cluster does not run compaction, so the cell below computes what compaction would leave from the log you
just produced.

**Where it matters**

Kafka Connect's own offset and config topics, CDC topics and reference-data topics are compacted, so a new consumer can
rebuild the current state without reading years of history.

**Watch out for**

Compaction runs in the background on closed segments: until it runs, consumers still see every version, so they must
handle duplicates per key anyway. Never use compaction on a topic whose records are independent events with
repeating keys, such as clicks keyed by user.
%% code
latest = {{}}
for partition, offset, key, value in log:
    latest[key] = (offset, value)
survivors = {{key: json.loads(value)["after"]["tier"] if value else "tombstone" for key, (offset, value) in latest.items()}}
print("records before compaction:", len(log))
print("after compaction:", survivors)
%% md
**What to notice:** Compaction would keep two of the five records: customer 1's latest update and customer 2's
tombstone. Once `delete.retention.ms` passes, the tombstone goes too, and key 2 disappears from the topic entirely.
%% md
## Schemas and the wire format

Plain JSON repeats every field name in every record and lets any producer change the shape silently. Most teams
encode values with **Avro** (or Protobuf or JSON Schema) and keep schemas in a **schema registry**. Each record
then starts with the Confluent wire format: a zero **magic byte**, a 4-byte **schema ID**, then the compact binary
body. A consumer reads the ID, fetches that schema once from the registry, and decodes.

The cell below encodes one customer with `fastavro` and frames it as a registry-aware serializer would, using schema
ID 42.

**Where it matters**

The schema ID lets producers and consumers deploy independently: each record says which schema wrote it, and the
registry refuses new schema versions that would break existing readers.

**Watch out for**

A consumer must use the deserializer that matches the producer's serializer. Reading Avro bytes as JSON, or JSON
as Avro, fails on the first record, and a mixed topic is very hard to clean up.
%% code
import io
import struct

from fastavro import parse_schema, schemaless_reader, schemaless_writer

customer_v1 = parse_schema(
    {{
        "type": "record",
        "name": "Customer",
        "fields": [
            {{"name": "id", "type": "long"}},
            {{"name": "email", "type": "string"}},
            {{"name": "tier", "type": "string"}},
        ],
    }}
)


def encode(record, schema, schema_id):
    body = io.BytesIO()
    schemaless_writer(body, schema, record)
    return b"\\x00" + struct.pack(">I", schema_id) + body.getvalue()


def decode(payload, reader_schema, writer_schema):
    magic, schema_id = payload[0], struct.unpack(">I", payload[1:5])[0]
    return schema_id, schemaless_reader(io.BytesIO(payload[5:]), writer_schema, reader_schema)


row = {{"id": 1, "email": "ana@example.com", "tier": "plus"}}
payload = encode(row, customer_v1, schema_id=42)
print("Avro record:", len(payload), "bytes | same row as JSON:", len(json.dumps(row)), "bytes")
print("first five bytes:", payload[:5].hex(" "))
print("decoded:", decode(payload, customer_v1, customer_v1))
%% md
**What to notice:** The Avro record is 27 bytes against 53 for the same row in JSON, because field names live in the
schema, not in each record. The first five bytes are the magic byte `00` and schema ID 42 (`00 00 00 2a`).
%% md
## Schema evolution and compatibility

Schemas change: a column is added, renamed or dropped. Avro resolves a record written with one schema against the
reader's schema by field name, and the registry checks each new version against a **compatibility** rule:

```text
BACKWARD   new readers can read old data   (add fields with defaults, delete fields)   default in the registry
FORWARD    old readers can read new data   (add fields, delete fields that have defaults)
FULL       both                            (add or delete only fields with defaults)
```

**Where it matters**

With `BACKWARD`, upgrade consumers first and producers second. Choose the rule per topic from who deploys first, and
let the registry enforce it in CI rather than discovering a break in production.

**Watch out for**

Renaming a field is a delete plus an add, so it breaks readers unless you use Avro `aliases`. Changing a field's type
(string to long) is rarely compatible in either direction.
%% code
customer_v2 = parse_schema(
    {{
        "type": "record",
        "name": "Customer",
        "fields": [
            {{"name": "id", "type": "long"}},
            {{"name": "email", "type": "string"}},
            {{"name": "tier", "type": "string"}},
            {{"name": "country", "type": "string", "default": "unknown"}},
        ],
    }}
)
customer_v2_strict = parse_schema(
    {{
        "type": "record",
        "name": "Customer",
        "fields": customer_v2["fields"][:3] + [{{"name": "country", "type": "string"}}],
    }}
)

print("v2 reader, v1 data:", decode(payload, customer_v2, customer_v1)[1])
try:
    decode(payload, customer_v2_strict, customer_v1)
except Exception as error:
    print("strict v2 reader, v1 data:", type(error).__name__, "-", error)
%% md
**What to notice:** The new reader filled the missing `country` with its default, so adding a field **with** a default
is backward compatible. Without the default, the reader has no value to use for old records and fails: a registry
in `BACKWARD` mode would have rejected that schema version before any producer used it.
%% md
## Kafka Connect

**Kafka Connect** runs connectors as a managed service so you do not write producer or consumer code for common
systems. A **source** connector (Debezium for PostgreSQL, a JDBC source) writes into Kafka; a **sink** connector
(S3, Snowflake, Elasticsearch, JDBC) reads from it. A connector is a JSON configuration posted to the Connect REST
API; Connect splits it into **tasks** spread across workers and stores progress in its own compacted topics.

```json
{{
  "name": "orders-to-s3",
  "config": {{
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "topics": "dbserver.public.orders",
    "tasks.max": "4",
    "s3.bucket.name": "lake-raw",
    "format.class": "io.confluent.connect.s3.format.parquet.ParquetFormat",
    "flush.size": "10000",
    "rotate.interval.ms": "600000",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "http://schema-registry:8081",
    "transforms": "unwrap",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "errors.tolerance": "all",
    "errors.deadletterqueue.topic.name": "dlq.orders-to-s3",
    "errors.deadletterqueue.context.headers.enable": "true"
  }}
}}
```

Read it top to bottom: four tasks (at most one per partition can be busy) write Avro-decoded records to S3 as
Parquet, closing a file every 10,000 records or ten minutes. A **single message transform** (SMT) unwraps the Debezium
envelope to just the `after` row, and records that fail conversion go to a **dead-letter topic** with the error in
their headers instead of stopping the connector.

**Where it matters**

Connect is the standard way to land CDC streams in a lake or warehouse and to fan topics out to search and caches.
Most of the work is choosing converters, file sizes and error handling, not writing code.

**Watch out for**

`errors.tolerance=all` without a dead-letter topic silently drops bad records. And `ExtractNewRecordState` discards
deletes unless you configure how to represent them, which quietly turns a replica into an append-only table.
%% md
## Check yourself

Try each exercise in the empty cell below it, then open the solution cell to compare.

### Exercise 1: Replay a snapshot and new changes

**Difficulty:** Easy · about 10 min

Produce to a new topic a snapshot read (`op: r`) of customer 3 at tier `basic`, then an update to tier `gold`, and
materialize the topic into a table.
%% code
# Try your solution here.
%% solution
more = [
    ("3", {{"op": "r", "before": None, "after": {{"id": 3, "email": "cy@example.com", "tier": "basic"}}}}),
    ("3", {{"op": "u", "before": {{"id": 3, "tier": "basic"}}, "after": {{"id": 3, "email": "cy@example.com", "tier": "gold"}}}}),
]
produce("customers-snapshot", [(k, json.dumps(v)) for k, v in more])
replica = {{}}
for _, _, key, value in consume("customers-snapshot", group="ex1", expected=2):
    event = json.loads(value)
    if event["op"] == "d":
        replica.pop(key, None)
    else:
        replica[key] = event["after"]
print(replica)
%% md
### Exercise 2: Evolve the schema safely

**Difficulty:** Medium · about 15 min

Write a version 3 of the customer schema that adds `signup_year` (an `int`). Make it readable against version 1 data,
and show what it reads for the encoded record.
%% code
# Try your solution here.
%% solution
customer_v3 = parse_schema(
    {{
        "type": "record",
        "name": "Customer",
        "fields": customer_v2["fields"] + [{{"name": "signup_year", "type": ["null", "int"], "default": None}}],
    }}
)
print(decode(payload, customer_v3, customer_v1)[1])
%% md
### Exercise 3: Check forward compatibility

**Difficulty:** Medium · about 15 min

A producer upgrades to `customer_v2` before the consumers. Encode a version 2 record and decode it with the old
`customer_v1` reader. Is adding `country` forward compatible?
%% code
# Try your solution here.
%% solution
new_payload = encode({{**row, "country": "PT"}}, customer_v2, schema_id=43)
schema_id, record = decode(new_payload, customer_v1, customer_v2)
print("schema", schema_id, "read by v1:", record)
print("forward compatible:", "country" not in record and record["tier"] == "plus")
%% md
## Key takeaways

- CDC connectors publish one keyed record per row change with `op`, `before` and `after`. Apply them in order per key
  and handle deletes and tombstones explicitly.
- Compaction keeps the latest record per key, which makes a topic a replayable snapshot of a table, but it runs in the
  background, so consumers still see older versions.
- Registry-aware serializers prefix each record with a magic byte and a schema ID, so producers and consumers can
  evolve independently.
- Add fields with defaults to stay backward compatible, let the registry enforce the rule, and treat renames and type
  changes as breaking.
- A Connect pipeline is mostly configuration: converters, file sizes, transforms and a dead-letter topic for errors.
%% md
**Next:** [Stream processing concepts](../concepts/stream-processing.ipynb)
"""

if __name__ == "__main__":
    build(PATH, SPEC)
    run(PATH)
