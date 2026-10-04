## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Avro

**Notebook:** [`notebooks/topics/avro.ipynb`](../notebooks/topics/avro.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is Apache Avro?](#What-is-Apache-Avro)
+ [What Avro Offers?](#What-Avro-Offers)
+ [State some Key Points about Apache Avro?](#State-some-Key-Points-about-Apache-Avro)
+ [Explain Avro schemas?](#Explain-Avro-schemas)
+ [What do you mean by schema declaration?](#What-do-you-mean-by-schema-declaration)
+ [What is the way of creating Avro Schemas?](#What-is-the-way-of-creating-Avro-Schemas)
+ [Name some primitive types of Data Types which Avro Supports.](#Name-some-primitive-types-of-Data-Types-which-Avro-Supports)
+ [Name some complex types of Data Types which Avro Supports.](#Name-some-complex-types-of-Data-Types-which-Avro-Supports)
+ [Explain Thrift and Protocol Buffers and Avro?](#Explain-Thrift-and-Protocol-Buffers-and-Avro)
+ [Why Avro?](#Why-Avro)
+ [What are best features of Apache Avro?](#What-are-best-features-of-Apache-Avro)
+ [Explain some advantages of Avro.](#Explain-some-advantages-of-Avro)
+ [Explain some disadvantages of Avro.](#Explain-some-disadvantages-of-Avro)
+ [Explain the term Serialization?](#Explain-the-term-Serialization)
+ [Name some Avro Reference Apis?](#Name-some-Avro-Reference-Apis)
+ [How to use Avro?](#How-to-use-Avro)
+ [Explain sort order in brief?](#Explain-sort-order-in-brief)
+ [What do you mean by Schema Resolution?](#What-do-you-mean-by-Schema-Resolution)
+ [How does Avro schema evolution work?](#How-does-Avro-schema-evolution-work)
+ [What are Avro compatibility modes and how does a schema registry enforce them?](#What-are-Avro-compatibility-modes-and-how-does-a-schema-registry-enforce-them)
+ [How do aliases work in Avro schema evolution?](#How-do-aliases-work-in-Avro-schema-evolution)
+ [What are common Avro schema evolution pitfalls?](#What-are-common-Avro-schema-evolution-pitfalls)
+ [Explain the Avro Sasl profile?](#Explain-the-Avro-Sasl-profile)
+ [Why is Avro useful in streaming and CDC pipelines?](#Why-is-Avro-useful-in-streaming-and-CDC-pipelines)
+ [When to use Avro?](#When-to-use-Avro)
+ [Who is intended audience to Learn Avro?](#Who-is-intended-audience-to-Learn-Avro)
+ [What are prerequisites to learn Avro?](#What-are-prerequisites-to-learn-Avro)
+ [What is the advantage of Hadoop Over Java Serialization?](#What-is-the-advantage-of-Hadoop-Over-Java-Serialization)
+ [What are the disadvantages of Hadoop Serialization?](#What-are-the-disadvantages-of-Hadoop-Serialization)
+ [Real world use cases for Apache Avro](#Real-world-use-cases-for-Apache-Avro)

## What is Apache Avro?
An open source project which offers data serialization as well as data exchange services, originally for Apache Hadoop, is what we call Apache Avro. It is possible to use these services together or independently. Programs can efficiently serialize data into files or into messages with the serialization service, and data storage is very compact and efficient because the data definition (the schema) is written in JSON while the data itself is stored in a binary format.

An Avro schema is a JSON document that declares a record name, a namespace, and typed fields:

```json
{
  "type": "record",
  "name": "OrderEvent",
  "namespace": "com.example.orders",
  "doc": "One order lifecycle event emitted by the orders service.",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "status", "type": {"type": "enum", "name": "OrderStatus", "symbols": ["CREATED", "PAID", "CANCELLED", "REFUNDED"]}},
    {"name": "amount", "type": {"type": "bytes", "logicalType": "decimal", "precision": 12, "scale": 2}},
    {"name": "currency", "type": "string", "default": "USD"},
    {"name": "event_time", "type": {"type": "long", "logicalType": "timestamp-millis"}}
  ]
}
```

The schema is the contract: a writer always serializes with a writer schema, and a reader always resolves the bytes with a reader schema. In an Avro Object Container File (`.avro`) the writer schema plus a sync marker are stored in the header, so the file is self-describing. In Kafka, the schema usually travels separately through a schema registry and only a small schema ID is embedded in each message.

Key interview point: Avro is *schema-on-write* with *schema evolution*. Unlike JSON there is no field name repeated for every record, which is why Avro payloads are typically several times smaller than equivalent JSON.

[Table of Contents](#Apache-Avro)

## What Avro Offers?
Avro offers:
+ Rich data structures (records, arrays, maps, unions, enums, fixed).
+ A compact, fast, binary data format.
+ A container file (`.avro`) to store persistent data with the schema embedded.
+ Remote procedure calls (RPC) through its own protocol definition.
+ Schema evolution through writer/reader schema resolution.

Example: the same order event as JSON versus Avro on the wire.

```text
JSON (field names repeated in every record, ~220 bytes):
{"order_id":"O-1001","customer_id":"C-7","status":"PAID","amount":42.50,"currency":"USD","event_time":"2026-10-04T15:03:02Z"}

Avro binary (no field names, ~35 bytes + 5-byte registry header):
05 O-1001 05 C-7 01 <8-byte decimal> 06 USD <8-byte long>
```

That size difference compounds at scale: 1 billion events per day at 220 bytes of JSON is roughly 220 GB/day before compression; the same stream in Avro is closer to 35 GB/day.

[Table of Contents](#Apache-Avro)

## State some Key Points about Apache Avro?
Some key points are:
+ Avro is a data serialization system.
+ It uses JSON-based schemas.
+ It uses RPC calls to send data.
+ During data exchange the schema is sent (or referenced), not repeated per record.
+ Avro is language-neutral: Java, Python, C, C++, C#, Go, Ruby, and others can read the same data.
+ Field identity is by name and (in newer schema designs) by aliases; Avro does not use numeric field IDs the way Protocol Buffers does.

[Table of Contents](#Apache-Avro)

## Explain Avro schemas?
Mainly, Avro heavily depends on its schema. Basically, it permits every datum to be written with no prior knowledge of the schema at read time, because the writer schema is available in the file header or from the schema registry. We can say Avro serializes fast and the data resulting after serialization is least in size with schemas.

Every Avro schema also has a canonical form used to detect whether two schemas are textually the same. Two schemas that differ only in whitespace, field order in JSON, `doc`, or `aliases` produce the same parsing canonical form, which is why a schema registry can tell you "this is the same schema, reuse it" instead of registering a new version.

```json
{
  "type": "record",
  "name": "PageView",
  "namespace": "com.example.web",
  "fields": [
    {"name": "user_id", "type": "string"},
    {"name": "url", "type": "string"},
    {"name": "ts", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "props", "type": {"type": "map", "values": "string"}, "default": {}},
    {"name": "experiments", "type": {"type": "array", "items": "string"}, "default": []}
  ]
}
```

Interview note: defaults are not optional metadata. A field with no `default` is required, and a union that includes `null` should normally declare `"default": null` so old readers of old data do not fail.

[Table of Contents](#Apache-Avro)

## What do you mean by schema declaration?
In JSON, a Schema is represented by one of:
+ A JSON string, such as `"string"` or `"com.example.orders.OrderEvent"`.
+ A JSON object, such as `{"type": "record", "name": "Order", "fields": [...]}`.
+ `{"type": "typename", ...attributes...}` for a type with extra attributes.
+ A JSON array, which declares a union, such as `["null", "string"]`.

Examples:

```json
"string"
```

```json
{"type": "array", "items": "long"}
```

```json
["null", {"type": "record", "name": "Address", "fields": [
  {"name": "city", "type": "string"},
  {"name": "postcode", "type": ["null", "string"], "default": null}
]}]
```

A named type is declared once and then referenced by its fully qualified name, for example `"com.example.orders.OrderEvent"`.

[Table of Contents](#Apache-Avro)

## What is the way of creating Avro Schemas?
In the format "lightweight text-based data interchange", JavaScript Object Notation (JSON), the Avro schema gets created. We can make it in various ways:
+ A JSON string
+ A JSON object
+ A JSON array (union)

In practice there are four ways to produce a schema:

```text
1. Hand-write the JSON schema (small, stable events).
2. Generate it from code: Java SpecificData / Avro Maven plugin, or Python avro.schema.
3. Reflect it from an existing type: Java ReflectData, or Pydantic/dataclass converters.
4. Convert from another contract: Avro IDL (.avdl) or a SQL DDL mapping in a CDC connector.
```

Avro IDL is a higher-level syntax when hand-writing JSON gets unwieldy:

```text
@namespace("com.example.orders")
protocol Orders {
  enum OrderStatus { CREATED, PAID, CANCELLED, REFUNDED }
  record OrderEvent {
    string order_id;
    string customer_id;
    OrderStatus status;
    decimal(12,2) amount;
    union { null, string } coupon_code = null;
  }
}
```

Compile it with `avro-tools idl2schemata orders.avdl out/` or `avro-tools compile protocol orders.avdl out.jar` in a build step.

[Table of Contents](#Apache-Avro)

## Name some primitive types of Data Types which Avro Supports.
Avro supports a wide range of primitive datatypes:
+ Null: no value
+ Boolean: a binary value
+ Int: 32-bit signed integer
+ Long: 64-bit signed integer
+ Float: single precision (32-bit) IEEE 754 floating-point number
+ Double: double precision (64-bit) IEEE 754 floating-point number
+ Bytes: the sequence of 8-bit unsigned bytes
+ String: Unicode character sequence

Avro also defines logical types that annotate primitives with a meaning, while keeping the underlying primitive on the wire:

```json
{
  "type": "record",
  "name": "Payment",
  "fields": [
    {"name": "payment_id", "type": "string"},
    {"name": "amount", "type": {"type": "bytes", "logicalType": "decimal", "precision": 18, "scale": 2}},
    {"name": "created_at", "type": {"type": "long", "logicalType": "timestamp-micros"}},
    {"name": "value_date", "type": {"type": "int", "logicalType": "date"}},
    {"name": "latency_ms", "type": {"type": "int", "logicalType": "time-millis"}},
    {"name": "external_id", "type": {"type": "string", "logicalType": "uuid"}}
  ]
}
```

Interview caution: a reader that does not understand a logical type still reads the primitive, but it loses the meaning (a decimal becomes raw bytes, a timestamp becomes a long). Always confirm that the consumer engine supports the logical types you choose.

[Table of Contents](#Apache-Avro)

## Name some complex types of Data Types which Avro Supports.
There are six kinds of complex types which Avro supports:
+ Records
+ Enums
+ Arrays
+ Maps
+ Unions
+ Fixed

A single schema that exercises all of them:

```json
{
  "type": "record",
  "name": "Envelope",
  "namespace": "com.example.common",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "kind", "type": {"type": "enum", "name": "Kind", "symbols": ["ORDER", "PAYMENT", "REFUND"]}},
    {"name": "tags", "type": {"type": "array", "items": "string"}, "default": []},
    {"name": "attributes", "type": {"type": "map", "values": "string"}, "default": {}},
    {"name": "payload", "type": ["null", "com.example.orders.OrderEvent"], "default": null},
    {"name": "checksum", "type": {"type": "fixed", "name": "Md5", "size": 16}}
  ]
}
```

Points worth making in an interview:
+ A union is an ordered list of types; on write the branch is chosen by the value's type, and on read the reader's first matching branch wins.
+ A field default must match the first branch of a union, so put `null` first when you want `"default": null`; the union does not otherwise require `null` to be first.
+ Named complex types must be defined before they are referenced by name within the same schema.
+ Maps always have string keys; use an array of records if keys are not strings.
+ `fixed` is sized bytes with a name, used for checksums and keys.

[Table of Contents](#Apache-Avro)

## Explain Thrift and Protocol Buffers and Avro?
The most competent libraries with Avro are Thrift and Protocol Buffers. The difference between them is: as per the need, Avro supports both dynamic and static types. Basically, to specify schemas and their types, Protocol Buffers and Thrift use Interface Definition Languages (IDLs). Avro is built in the Hadoop ecosystem, while Thrift and Protocol Buffers are not.

Additional trade-offs:

+ Protocol Buffers and Thrift use numeric field tags, so renames are free but tags must never be reused.
+ Avro uses field names, so a rename is a breaking change unless you add an `aliases` entry.
+ Avro embeds (or resolves) the full writer schema, which makes dynamic/self-describing reads easy but message headers slightly larger in registry-based setups.
+ Protocol Buffers' `oneof` maps naturally to an Avro union; Protobuf's strict `required` was removed in proto3, while Avro leans on defaults.

Interview framing: "All three are binary and schema-driven. Choose Avro when Kafka and Hadoop/Spark compatibility and schema-registry-driven evolution matter most; choose Protobuf for gRPC service APIs; choose Thrift when you already run a Thrift service stack."

[Table of Contents](#Apache-Avro)

## Why Avro?
Some features where Avro differs from other systems are:
+ Dynamic typing.
+ Untagged data (no per-record field tags or field names).
+ No manually assigned field IDs.
+ Schema travels with the data, so any reader can decode it.

Avro therefore supports two usage styles:

```python
# 1. Dynamic / generic: decode with the writer schema read from the file.
from fastavro import reader

with open("orders.avro", "rb") as src:
    for record in reader(src, reader_schema=None):
        print(record)  # dict, no generated class needed
```

```python
# 2. Static / generated: compile the schema to a Python class or Java class first.
# Java: avro-tools compile schema orders.avsc out/
# Python: dataclasses-avroschema or a hand-written dataclass plus fastavro schemaless writer
```

The dynamic path is what makes Avro pleasant for ETL: a generic job can consume any topic whose schema is registered, without shipping a generated class per topic.

[Table of Contents](#Apache-Avro)

## What are best features of Apache Avro?
Some of the best features of Avro are:
+ Schema evolution
+ Untagged data
+ Language support
+ Transparent compression
+ Dynamic typing
+ Native support in MapReduce
+ Rich data structures

Compression and splitting are the two features interviewers dig into. Avro container files store compressed blocks plus a sync marker every N bytes, so a block is the unit of compression:

```python
from fastavro import writer

with open("orders.avro", "wb") as out:
    writer(
        out,
        parsed_schema,
        events,
        codec="zstandard",          # null, deflate, snappy, zstandard, bzip2, xz
        sync_interval=64 * 1024,    # sync marker roughly every 64 KiB
    )
```

Because each block starts after a sync marker, a distributed reader can seek to a block boundary and split the file across Spark tasks, which is exactly why Avro is splittable while an opaque gzip file is not.

[Table of Contents](#Apache-Avro)

## Explain some advantages of Avro.
Pros of Avro are:
+ The smallest size.
+ It compresses block at a time; split table.
+ Maintained object structure.
+ Supports reading old data with a new schema.
+ Schema is machine-readable, so it can drive CI compatibility checks and documentation.

```python
import io
from fastavro import writer, reader

buf = io.BytesIO()
writer(buf, parsed_schema, events)
raw = buf.getvalue()

# Self-describing: the writer schema travels in the header.
buf.seek(0)
print(reader(buf).writer_schema["name"])  # com.example.orders.OrderEvent (fastavro stores the full name)
```

[Table of Contents](#Apache-Avro)

## Explain some disadvantages of Avro.
Cons of Avro are:
+ It must use .NET 4.5, in the case of C# Avro, to make the best use of it.
+ Potentially slower serialization than hand-rolled binary formats.
+ In order to read/write data, you need a schema.
+ The binary payload is not human-readable, so debugging needs tooling such as `avro-tools tojson`.
+ Reusing one schema for many event types leads to wide records and poor evolution hygiene.

```bash
# Inspect an Avro file from the command line.
java -jar avro-tools.jar tojson --pretty orders.avro | head -3
java -jar avro-tools.jar getschema orders.avro
```

[Table of Contents](#Apache-Avro)

## Explain the term Serialization?
To transport the data over the network or to store it on some persistent storage, the process of translating data structures or object state into binary or textual form is what we call Serialization. In other words, serialization is also known as marshaling and deserialization is known as unmarshalling.

A complete fastavro round trip:

```python
from decimal import Decimal
from fastavro import writer, reader, parse_schema

schema = parse_schema({
    "type": "record",
    "name": "OrderEvent",
    "namespace": "com.example.orders",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "customer_id", "type": "string"},
        {"name": "status", "type": "string"},
        {"name": "amount", "type": {"type": "bytes", "logicalType": "decimal", "precision": 12, "scale": 2}},
        {"name": "currency", "type": "string", "default": "USD"},
        {"name": "event_time", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    ],
})

events = [
    {
        "order_id": "O-1001",
        "customer_id": "C-7",
        "status": "PAID",
        "amount": Decimal("42.50"),
        "currency": "USD",
        "event_time": 1791138182000,
    }
]

with open("orders.avro", "wb") as out:
    writer(out, schema, events)

with open("orders.avro", "rb") as src:
    for record in reader(src):
        print(record)
```

[Table of Contents](#Apache-Avro)

## Name some Avro Reference Apis?
The classes and methods which we use in the serialization, as well as deserialization, of Avro schemas are:

Java:
+ `SpecificDatumWriter`
+ `SpecificDatumReader`
+ `DataFileWriter`
+ `DataFileReader`
+ `Schema.Parser`
+ `GenericRecord`
+ `GenericData.Record`

Python and other languages:
+ `fastavro.writer`, `fastavro.reader`, `fastavro.parse_schema`, `fastavro.schemaless_writer`
+ `avro.schema.parse`, `avro.io.DatumReader`, `avro.io.DatumWriter`, `avro.datafile.DataFileReader`
+ `confluent_kafka.schema_registry.avro.AvroSerializer` / `AvroDeserializer` for Kafka

```python
from fastavro import parse_schema, schemaless_writer, schemaless_reader
import io

schema = parse_schema({"type": "record", "name": "Ping", "fields": [{"name": "ts", "type": "long"}]})

buf = io.BytesIO()
schemaless_writer(buf, schema, {"ts": 1791138182000})   # no header, for Kafka payloads
buf.seek(0)
print(schemaless_reader(buf, schema))
```

[Table of Contents](#Apache-Avro)

## How to use Avro?
The workflow to use Avro is:
1. Create or obtain the schema.
2. Read the schema into your program, either by generating a class with a parser/library or by parsing it dynamically.
3. Serialize using the serialization API.
4. Deserialize using the deserialization API, supplying the writer schema if it is not embedded.

PySpark reads and writes Avro with the `spark-avro` package (`--packages org.apache.spark:spark-avro_2.12:3.5.1`):

```python
orders = (
    spark.read
    .format("avro")
    .load("s3://company-raw/orders/")
)

orders.write.format("avro").mode("append").save("s3://company-curated/orders/")
```

Kafka producer with the Confluent serializer (schema registry assigns and stores the writer schema; the message carries a 5-byte magic byte + schema ID prefix):

```python
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

order_schema_str = """
{
  "type": "record",
  "name": "OrderEvent",
  "namespace": "com.example.orders",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "status", "type": "string"},
    {"name": "amount", "type": "double"}
  ]
}
"""

registry = SchemaRegistryClient({"url": "https://schema-registry.example.com"})
serializer = AvroSerializer(registry, order_schema_str)

producer = Producer({"bootstrap.servers": "kafka-1:9092,kafka-2:9092"})
producer.produce(
    topic="orders.events.v1",
    key="O-1001",
    value=serializer(
        {"order_id": "O-1001", "status": "PAID", "amount": 42.50},
        SerializationContext("orders.events.v1", MessageField.VALUE),
    ),
)
producer.flush()
```

[Table of Contents](#Apache-Avro)

## Explain sort order in brief?
There is a standard sort order for data in Avro which allows data written by one system to be efficiently sorted by another system. As sort order comparisons are sometimes the most frequent per-object operation, it can be an important optimization.

Every type has a defined ordering, and a schema can override it per field:

```json
{
  "type": "record",
  "name": "LeaderboardEntry",
  "fields": [
    {"name": "player_id", "type": "string"},
    {"name": "score", "type": "long", "order": "descending"},
    {"name": "updated_at", "type": {"type": "long", "logicalType": "timestamp-millis"}, "order": "ignore"}
  ]
}
```

+ Default ordering for records is field-by-field in declaration order, using each field's `order`.
+ `ascending` (default), `descending`, and `ignore` are the allowed values.
+ Unions order by branch index first, which is why `["null", "string"]` and `["string", "null"]` are different schemas.
+ Avro does not ship a distributed sort; the point is that two systems agree on *how* to compare, not that either sorts for you.

[Table of Contents](#Apache-Avro)

## What do you mean by Schema Resolution?
Whether from an RPC or a file, a reader of Avro data can always parse that data since its schema is offered. Yet it is possible that the schema may not be exactly the schema we expect, so for that purpose we use Schema Resolution.

Resolution rules that matter in interviews:

+ Fields are matched by name (or alias) between writer and reader schema.
+ A reader field with a default is filled in when the writer did not write it.
+ A writer field absent from the reader schema is skipped.
+ Numeric promotion is allowed in the widening direction: `int` to `long`, `float`, or `double`; `long` to `float` or `double`; `float` to `double`.
+ Union resolution matches the writer's branch against a reader branch; the writer's branch must be present in the reader union (unless it can be promoted).
+ An enum symbol unknown to the reader needs a reader-side default (`"default": "UNKNOWN"` on the enum) or resolution fails.

```python
import io
from fastavro import parse_schema, schemaless_writer, schemaless_reader

writer_schema = parse_schema({
    "type": "record",
    "name": "Order",
    "fields": [{"name": "order_id", "type": "string"}],
})

reader_schema = parse_schema({
    "type": "record",
    "name": "Order",
    "fields": [
        {"name": "order_id", "type": "string"},
        {"name": "currency", "type": "string", "default": "USD"},
    ],
})

buf = io.BytesIO()
schemaless_writer(buf, writer_schema, {"order_id": "O-1001"})
buf.seek(0)

# Old bytes, new reader schema: 'currency' comes from the default.
print(schemaless_reader(buf, writer_schema, reader_schema))
```

[Table of Contents](#Apache-Avro)

## How does Avro schema evolution work?
Avro supports compatible schema changes when readers and writers can resolve differences. Common compatible changes include adding a field with a default value, removing a field that readers do not require, or widening some types depending on compatibility rules. Breaking changes include renaming a field without aliases or changing a type incompatibly.

Compatibility by change type:

| Change | Backward (new reader, old data) | Forward (old reader, new data) | Full |
|---|---|---|---|
| Add field with `default` | Yes | Yes | Yes |
| Add field without `default` | No | Yes | No |
| Remove field with `default` | Yes | Yes | Yes |
| Remove required field | Yes | No | No |
| Widen `int` to `long` | Yes | No | No |
| Rename field + add `aliases` | Yes | No | No |
| Change `string` to `int` | No | No | No |
| Reorder union branches | No | No | No |

Aliases are applied by rewriting the *writer's* schema using aliases from the *reader's* schema, so adding an alias to the new schema makes the rename backward compatible; it is not forward compatible unless the old reader also carries an alias for the new name (or the old field has a default).

Example: adding a field safely.

```json
{"name": "currency", "type": "string", "default": "USD"}
```

Because old messages do not contain `currency`, the default lets new readers handle old data. In production, schema compatibility should be enforced in CI or by a schema registry:

```bash
# Confluent Schema Registry: set and check the topic-level compatibility policy.
curl -s -X PUT -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data '{"compatibility": "BACKWARD"}' \
  https://schema-registry.example.com/config/orders.events.v1

# CI gate: test a candidate schema before merge.
curl -s -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data "{\"schema\": $(python -c 'import json;print(json.dumps(open("orders_v2.avsc").read()))')}" \
  https://schema-registry.example.com/compatibility/subjects/orders.events.v1-value/versions/latest
```

[Table of Contents](#Apache-Avro)

## What are Avro compatibility modes and how does a schema registry enforce them?
A schema registry stores versioned schemas per subject (usually `<topic>-value`) and rejects a new version that violates the subject's compatibility policy. The four modes interviewers expect:

+ `BACKWARD`: new schema can read data written with the previous schema. This is the default and the safest for consumers-first upgrades.
+ `FORWARD`: previous schema can read data written with the new schema. Safe when producers upgrade before consumers.
+ `FULL`: both directions. Restrictive but the safest for rolling deployments.
+ `NONE`: no checks. Use only for greenfield topics where you control both ends.

```yaml
# Debezium / Kafka Connect sink connector referencing the registry.
name: orders-avro-sink
config:
  connector.class: io.confluent.connect.s3.S3SinkConnector
  topics: orders.events.v1
  s3.bucket.name: company-curated
  format.class: io.confluent.connect.s3.format.avro.AvroFormat
  schema.compatibility: FULL
  value.converter: io.confluent.connect.avro.AvroConverter
  value.converter.schema.registry.url: https://schema-registry.example.com
  key.converter: org.apache.kafka.connect.storage.StringConverter
```

Interview note: the registry's mode is a policy, not a guarantee. It only checks schemas that are actually registered; a producer that bypasses the registry can still write incompatible bytes.

[Table of Contents](#Apache-Avro)

## How do aliases work in Avro schema evolution?
`aliases` let a reader treat one name as another, which is how you rename a field or record without breaking existing data.

```json
{
  "type": "record",
  "name": "OrderCreated",
  "aliases": ["OrderEvent"],
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "gross_amount", "type": "double", "aliases": ["amount"]}
  ]
}
```

Rules:
+ Aliases are applied only during resolution (read), so old files and old messages keep working.
+ Renaming a record means you should also update the subject name or keep the previous name as an alias.
+ Aliases also let a reader pull a field from a renamed record, but they do not fix type changes.
+ Adding `aliases` does not change the parsing canonical form, so a registry treats it as the same schema for parsing purposes but as a new version for resolution.

[Table of Contents](#Apache-Avro)

## What are common Avro schema evolution pitfalls?
+ Adding a required field (no default) breaks backward compatibility for every existing reader.
+ Writing `null` into a union that does not declare `null` fails at serialization time, not at read time.
+ Removing `null` from `["null", "string"]` after data was written with nulls makes old data unreadable.
+ Using a bare `double` for money and later wanting `decimal` is a breaking type change; design money as decimal from day one.
+ Putting logically distinct events in one schema produces dozens of optional fields; prefer one topic/schema per event type with a shared envelope.
+ Relying on default `double`/`float` for IDs loses precision above 2^53.
+ Forgetting that a schema registry subject per topic means a rename of the record also changes the resolved schema everywhere.
+ Using `doc` or field descriptions as the only documentation; they are stripped from the canonical form and not enforced.

[Table of Contents](#Apache-Avro)

## Explain the Avro Sasl profile?
Basically, SASL offers a framework for authentication and security of network protocols. In Avro also we use SASL Profile for authentication and security purposes.

Avro RPC uses SASL for the handshake, and the common mechanisms are `PLAIN`, `DIGEST-MD5`, `GSSAPI` (Kerberos), and `ANONYMOUS` for trusted networks only. In a modern Kafka pipeline, SASL is configured on the Kafka broker/client side rather than in Avro itself:

```yaml
# Kafka Connect worker properties: SASL_SSL plus Avro serialization via the registry.
security.protocol: SASL_SSL
sasl.mechanism: SCRAM-SHA-512
sasl.jaas.config: >-
  org.apache.kafka.common.security.scram.ScramLoginModule required
  username="svc-cdc" password="${file:/opt/kafka/secrets/cdc.password}";
value.converter: io.confluent.connect.avro.AvroConverter
value.converter.schema.registry.url: https://schema-registry.example.com
value.converter.basic.auth.credentials.source: USER_INFO
value.converter.basic.auth.user.info: svc-cdc:${file:/opt/kafka/secrets/sr.password}
```

[Table of Contents](#Apache-Avro)

## Why is Avro useful in streaming and CDC pipelines?
Avro is compact, schema-based, and well suited for record-oriented data. It is commonly used with Kafka because producers and consumers can exchange small binary messages while a schema registry manages compatibility. This helps pipelines evolve without every consumer breaking when a new optional field is added.

Example schema:

```json
{
  "type": "record",
  "name": "OrderEvent",
  "fields": [
    {"name": "order_id", "type": "string"},
    {"name": "amount", "type": ["null", "double"], "default": null},
    {"name": "event_time", "type": "string"}
  ]
}
```

The key interview point is that Avro stores data with a schema contract. This is safer than passing ungoverned JSON between teams when fields and types change over time.

In CDC specifically, Debezium emits a well-known envelope (before/after/op/source) and its `AvroConverter` registers that envelope in the registry:

```json
{
  "name": "orders-avro-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "pg-primary.internal",
    "database.port": "5432",
    "database.dbname": "orders",
    "table.include.list": "public.orders,public.order_items",
    "plugin.name": "pgoutput",
    "topic.prefix": "cdc",
    "key.converter": "io.confluent.connect.avro.AvroConverter",
    "key.converter.schema.registry.url": "https://schema-registry.example.com",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "value.converter.schema.registry.url": "https://schema-registry.example.com",
    "decimal.handling.mode": "precise",
    "time.precision.mode": "adaptive_time_microseconds",
    "tombstones.on.delete": "true",
    "heartbeat.interval.ms": "10000"
  }
}
```

[Table of Contents](#Apache-Avro)

## When to use Avro?
Mainly, for two purposes, we use Avro, like:
+ Data serialization
+ RPC (Remote procedure call) protocol

Although, some key points are:
+ We are able to read the data from disk with applications written in other languages besides Java or the JVM.
+ Avro allows us to transfer data across a remote system without the overhead of Java serialization.
+ We use Avro when we need to store a large set of data on disk, as it conserves space.
+ By using Avro for RPC, we get better remote data transfer.

Choose Avro when:
+ Kafka is the backbone and a schema registry is available.
+ Row-oriented files matter more than columnar scan performance (Avro beats Parquet for full-row streaming and write-heavy landing zones).
+ You need a self-describing container file for archival or handoff.

Do not choose Avro when:
+ The workload is analytical and scan-heavy by a few columns: Parquet or ORC will be much faster and smaller.
+ Humans need to read the payload directly.
+ You need random access or column pruning.

[Table of Contents](#Apache-Avro)

## Who is intended audience to Learn Avro?
Those people who want to learn the basics of Big Data Analytics by using the Hadoop Framework, and also those who aspire to become a successful Hadoop developer, can go for Avro. Further, those aspirants who want to use Avro for data serialization and deserialization can also learn Avro. In practice the audience today is mostly streaming and data-platform engineers: Kafka producers/consumers, CDC pipeline owners, Spark and Flink developers, and platform teams governing schemas.

[Table of Contents](#Apache-Avro)

## What are prerequisites to learn Avro?
Those who want to learn Avro must know Hadoop's architecture and APIs before learning Avro. Also, they must know Java with experience in writing basic applications before going for Avro. For a modern streaming role, the more useful prerequisites are: JSON, a Kafka producer/consumer, one of the Avro libraries (`fastavro`, `avro-python3`, or Java `avro`), and the concept of a schema registry.

[Table of Contents](#Apache-Avro)

## What is the advantage of Hadoop Over Java Serialization?
As with the help of the Writable objects, Hadoop Writable-based serialization is able to reduce object-creation overhead, which is not possible with the Java native serialization framework; that is why using the Hadoop one is an advantage.

Comparison:

+ Java serialization writes class names, field metadata, and object graph information with every stream, which is large and not portable.
+ Hadoop `Writable` is compact and reusable (`write`/`readFields` into the same object), but it is Java-only and tightly coupled to a specific class.
+ Avro goes one step further: it is compact, cross-language, and schema-governed, so Hive, Spark, and Python can all read the same files.

[Table of Contents](#Apache-Avro)

## What are the disadvantages of Hadoop Serialization?
The only disadvantage of Hadoop Serialization is that the Writable and Sequence files have only a Java API. Hence, to solve this issue, Avro comes in the picture.

A simple Avro file written by Python and read by Spark demonstrates the portability that `Writable` lacks:

```python
from fastavro import writer, reader

schema = {
    "type": "record",
    "name": "Metric",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "value", "type": "double"},
        {"name": "ts", "type": "long"},
    ],
}
writer(open("metrics.avro", "wb"), schema, [{"name": "cpu", "value": 0.42, "ts": 1791138182000}])

for row in reader(open("metrics.avro", "rb")):
    print(row)
```

```python
# The same file, read by Spark.
metrics = spark.read.format("avro").load("file:///data/metrics.avro")
metrics.show()
```

[Table of Contents](#Apache-Avro)

## Real world use cases for Apache Avro

### 1. E-commerce order events on Kafka

Business context: the checkout service publishes an `OrderEvent` for every state change, and five downstream teams (fulfilment, fraud, analytics, notifications, data lake) consume it. Volume: 40 million events/day at peak 3,000 events/second, roughly 120 bytes per event.

Architecture: producer serializes with `AvroSerializer`; the schema lives in a registry under subject `orders.events.v1-value` with `BACKWARD` compatibility; consumers use `AvroDeserializer`; a Kafka Connect S3 sink writes Avro object container files to a raw zone.

```yaml
name: orders-avro-s3-sink
config:
  connector.class: io.confluent.connect.s3.S3SinkConnector
  topics: orders.events.v1
  tasks.max: "6"
  s3.bucket.name: company-raw
  s3.part.size: "67108864"
  flush.size: "50000"
  storage.class: io.confluent.connect.s3.storage.S3Storage
  format.class: io.confluent.connect.s3.format.avro.AvroFormat
  value.converter: io.confluent.connect.avro.AvroConverter
  value.converter.schema.registry.url: https://schema-registry.example.com
```

Why this design: Avro keeps per-event overhead low at thousands of messages per second, the registry blocks a producer from shipping a required field that would break the five consumers, and Avro container files remain splittable so the nightly Spark job over the raw zone parallelizes cleanly.

### 2. Fintech ledger CDC into a lakehouse

Business context: a payments platform must replicate its PostgreSQL ledger to an S3 warehouse with exact amounts and audit-ready ordering. Volume: 12 million ledger rows, 8,000 updates/second during settlement windows, decimal amounts that must not lose precision.

Architecture: Debezium reads the Postgres WAL and emits the Avro envelope (`before`, `after`, `op`, `source.lsn`, `source.txId`); the topic is compacted by primary key; Spark Structured Streaming deduplicates on `(ledger_id)` ordered by `source.lsn` and merges into Iceberg.

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

raw = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-1:9092")
    .option("subscribe", "cdc.public.ledger")
    .option("startingOffsets", "earliest")
    .load()
)

envelope = (
    raw.select(F.from_avro(F.col("value"), ledger_envelope_schema).alias("e"))
    .select("e.after.*", "e.op", "e.source.lsn", "e.source.ts_ms")
)

window = Window.partitionBy("ledger_id").orderBy(F.col("lsn").desc(), F.col("ts_ms").desc())
deduped = (
    envelope.withColumn("rn", F.row_number().over(window))
    .where(F.col("rn") == 1)
    .drop("rn")
)
```

Why this design: Avro's `decimal(18,2)` logical type preserves exact money values, `source.lsn` gives a monotonic ordering key so replays are deterministic, and the raw Avro topic is the immutable audit trail while the Iceberg table is the queryable current state.

### 3. Multi-tenant SaaS event ingestion

Business context: a B2B SaaS platform ingests product telemetry for 2,000 tenants, each with slightly different custom properties. Volume: 300 million events/day, and tenant schemas change independently.

Architecture: a shared `EventEnvelope` Avro schema carries `tenant_id`, `event_name`, `occurred_at`, and a `map<string,string>` for tenant-specific properties; per-tenant subjects (`telemetry.tenant-42.properties-value`) version the custom dimension schema; a generic Avro consumer decodes the envelope dynamically.

```python
from fastavro import parse_schema, schemaless_reader
import io

envelope_schema = parse_schema({
    "type": "record",
    "name": "EventEnvelope",
    "namespace": "com.example.telemetry",
    "fields": [
        {"name": "tenant_id", "type": "string"},
        {"name": "event_name", "type": "string"},
        {"name": "occurred_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
        {"name": "props", "type": {"type": "map", "values": "string"}, "default": {}},
    ],
})

def decode(payload: bytes) -> dict:
    return schemaless_reader(io.BytesIO(payload), envelope_schema)
```

Why this design: one stable core schema plus a free-form map avoids 2,000 registered schemas for the hot path, while a per-tenant subject still governs the optional typed extensions. Avro's `map` is string-keyed, which is exactly what tenant properties are.

### 4. GDPR-safe customer events with tokenized PII

Business context: a European retailer must keep analytics events while ensuring raw email and phone never land in the lake. Volume: 5 million events/day, 90-day retention on raw tokens, 3-year retention on aggregates.

Architecture: the ingestion service stores PII in a vault and replaces it with a deterministic token before serializing. The Avro schema marks the token field and carries no raw PII; a `logicalType` uuid keeps tokens compact.

```python
from fastavro import writer

gdpr_events = [
    {
        "customer_token": "3f9c1b6e-6b1c-4f5e-9c1a-2f4d7e8a0b12",
        "event_type": "checkout_started",
        "occurred_at": 1791138182000,
    }
]
writer(open("gdpr_events.avro", "wb"), gdpr_schema, gdpr_events)
```

Why this design: because the PII never enters the Avro payload, a deletion request only needs the vault mapping removed and the token rows in the lake become meaningless. The schema documents the contract so a producer cannot quietly add an `email` field without a registry compatibility review.

### 5. Cross-language ML feature logging

Business context: an ML platform logs features and predictions for training-set reconstruction and drift monitoring. Volume: 2 TB/day compressed, read back months later by Python, Scala, and Java jobs.

Architecture: online services (Go, Java) write Avro container files; offline Spark and Python read the same files; the schema is stored alongside the model artifact with the git commit SHA so a model reproduces against the exact feature contract.

```json
{
  "type": "record",
  "name": "FeatureLog",
  "namespace": "com.example.ml",
  "fields": [
    {"name": "request_id", "type": "string"},
    {"name": "model_version", "type": "string"},
    {"name": "features", "type": {"type": "map", "values": "double"}},
    {"name": "prediction", "type": "double"},
    {"name": "logged_at", "type": {"type": "long", "logicalType": "timestamp-millis"}}
  ]
}
```

Why this design: Avro container files are self-describing and splittable, so a six-month-old file still decodes without the service that wrote it; the schema-in-git pairing makes training data reproducible; and the map keeps the feature set flexible without a new schema per model.

[Table of Contents](#Apache-Avro)
