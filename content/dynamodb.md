## [Main title](../README.md)
### [Interview questions](full.md)

# DynamoDB
+ [How do you model data in DynamoDB?](#How-do-you-model-data-in-DynamoDB)
+ [What are partition keys, sort keys, GSIs, and LSIs?](#What-are-partition-keys-sort-keys-GSIs-and-LSIs)
+ [How do you avoid hot partitions in DynamoDB?](#How-do-you-avoid-hot-partitions-in-DynamoDB)
+ [How do you read and write items with boto3?](#How-do-you-read-and-write-items-with-boto3)
+ [What is the difference between Query and Scan?](#What-is-the-difference-between-Query-and-Scan)
+ [What are DynamoDB capacity modes and how do you control cost?](#What-are-DynamoDB-capacity-modes-and-how-do-you-control-cost)
+ [How do GSI and LSI projections and limits affect design?](#How-do-GSI-and-LSI-projections-and-limits-affect-design)
+ [How do you use conditional writes and optimistic locking?](#How-do-you-use-conditional-writes-and-optimistic-locking)
+ [How do you use DynamoDB transactions?](#How-do-you-use-DynamoDB-transactions)
+ [How do you capture changes with DynamoDB Streams and TTL?](#How-do-you-capture-changes-with-DynamoDB-Streams-and-TTL)
+ [How do you model one-to-many and many-to-many relationships?](#How-do-you-model-one-to-many-and-many-to-many-relationships)
+ [How do you handle throttling, retries, and errors?](#How-do-you-handle-throttling-retries-and-errors)
+ [When should you NOT use DynamoDB?](#When-should-you-NOT-use-DynamoDB)
+ [Real world use cases for DynamoDB](#Real-world-use-cases-for-DynamoDB)

## How do you model data in DynamoDB?
DynamoDB modeling starts with access patterns, not with entities. You write down every query the application must run, then choose a primary key, secondary indexes, and item collections that satisfy those queries. Unlike relational modeling, you denormalize aggressively and design multiple item types in one table. There are no joins and no server-side aggregations beyond `Query` on a key and `Scan` on everything.

A practical process:

1. List access patterns with their frequency and latency target, for example "get order by id (1000/s)" or "list a customer's orders by recency (50/s)".
2. Choose the partition key for even write distribution and the sort key for range queries and item collections.
3. Add a GSI only for access patterns the base key cannot serve.
4. Decide the item types that share the table and give them a key prefix convention.

Item collection (single-table) key pattern:

```text
PK = CUSTOMER#123
SK = PROFILE
SK = ORDER#2026-10-04#999

PK = ORDER#999
SK = ITEM#1
SK = ITEM#2
```

```json
{
  "PK": {"S": "CUSTOMER#123"},
  "SK": {"S": "ORDER#2026-10-04#999"},
  "entity_type": {"S": "order"},
  "order_id": {"S": "999"},
  "status": {"S": "shipped"},
  "amount": {"N": "149.90"},
  "order_ts": {"S": "2026-10-04T12:31:00Z"},
  "GSI1PK": {"S": "CUSTOMER#123#STATUS#shipped"},
  "GSI1SK": {"S": "2026-10-04T12:31:00Z"}
}
```

`PK`/`SK` are generic key attributes that can hold any entity type, and the `CUSTOMER#` prefix makes the value sortable and greppable. Querying `PK = CUSTOMER#123` returns the profile and every order in one request. Adding a GSI on `GSI1PK`/`GSI1SK` answers "all shipped orders for this customer, newest first" without a scan.

Interview guidance:

+ Model for the query you will run thousands of times per second, not for the shape of the CSV you imported once.
+ Prefer a small number of tables in a service. True single-table design is powerful but harder to operate; multi-table is acceptable when access patterns are cleanly separated.
+ If you cannot name the access pattern that a new index serves, do not create it. Every index increases write cost and failure surface.
+ DynamoDB is eventually consistent by default on reads and GSIs; request `ConsistentRead=True` only on the base table when the pattern truly needs it.

[Table of Contents](#DynamoDB)

## What are partition keys, sort keys, GSIs, and LSIs?
The partition key (hash key) is hashed to a physical partition and determines data distribution. The sort key (range key) orders items inside a partition and enables range queries and `begins_with`/`between` conditions. Partition key plus sort key must be unique. A global secondary index (GSI) defines a completely different partition/sort key pair and is maintained asynchronously. A local secondary index (LSI) keeps the table's partition key but uses a different sort key, and must be created with the table.

Example schema for an orders workload:

```text
table key:   customer_id (PK), order_ts (SK)
GSI "by_status":  order_status (PK), order_ts (SK)
LSI "by_amount":  customer_id (PK), amount (SK)
```

```json
{
  "TableName": "orders",
  "KeySchema": [
    {"AttributeName": "customer_id", "KeyType": "HASH"},
    {"AttributeName": "order_ts", "KeyType": "RANGE"}
  ],
  "AttributeDefinitions": [
    {"AttributeName": "customer_id", "AttributeType": "S"},
    {"AttributeName": "order_ts", "AttributeType": "S"},
    {"AttributeName": "order_status", "AttributeType": "S"}
  ],
  "GlobalSecondaryIndexes": [
    {
      "IndexName": "by_status",
      "KeySchema": [
        {"AttributeName": "order_status", "KeyType": "HASH"},
        {"AttributeName": "order_ts", "KeyType": "RANGE"}
      ],
      "Projection": {"ProjectionType": "ALL"}
    }
  ]
}
```

Key differences that interviewers probe:

| Aspect | GSI | LSI |
|---|---|---|
| Partition key | Any attribute, independent of table | Must equal the table partition key |
| Creation | Any time, online | Only at table creation |
| Consistency | Eventually consistent only | Supports strongly consistent reads |
| Capacity | Own RCU/WCU; writes fan out to the index | Shares table throughput |
| Partition limit | No fixed item-collection size limit | 10 GB per partition-key item collection |
| Limit | 20 GSIs per table (default quota) | 5 LSIs per table |

Design notes:

+ Indexes are updated asynchronously. A read immediately after a base-table write can be eventually consistent and, in the case of a GSI, can miss the just-written item for a short window.
+ Use sparse indexes deliberately: if items that should be indexed carry the index key and others omit it, the others never appear in the index, keeping it small and cheap.
+ The 10 GB LSI ceiling is per partition key, not per table. A hot `customer_id` with millions of orders can hit it; a GSI has no equivalent per-key ceiling but can still throttle on its own partition.

[Table of Contents](#DynamoDB)

## How do you avoid hot partitions in DynamoDB?
A hot partition happens when one partition key value receives a disproportionate share of traffic. DynamoDB partitions have throughput limits, and even on-demand tables throttle a single very hot key because the limit is per physical partition, not per table. Common causes are a low-cardinality partition key (a constant tenant, today's date, a status value) and monotonically increasing keys.

Bad versus sharded keys:

```text
bad:    PK = EVENT_DATE#2026-10-04          # every event lands in one partition
better: PK = EVENT_DATE#2026-10-04#BUCKET#07  # 16-64 random buckets spread writes
```

```python
import random

def shard_key(event_date: str, buckets: int = 16) -> str:
    bucket = random.randint(0, buckets - 1)
    return f"EVENT_DATE#{event_date}#BUCKET#{bucket:02d}"
```

The trade-off is that reads must query every bucket and merge results, which multiplies RCU and latency.

Other mitigations:

+ Use write sharding with a random or hash suffix on the hot key and accept fan-out reads.
+ Use a high-cardinality key such as `order_id`, `device_id`, or `customer_id` instead of a status or a date.
+ Cache the hot item (DAX or an application cache) so read traffic does not reach the partition.
+ Move counters to a distributed pattern: write one update per shard, then sum on read, or use DynamoDB Streams plus aggregations.
+ Watch `ThrottledRequests`, `WriteThrottleEvents`, and `ReadThrottleEvents` in CloudWatch, and per-key Contributor Insights to find the offending key.
+ On provisioned tables, `AdaptiveCapacity` automatically shifts capacity toward hot partitions, but it cannot fix a key so hot that it exceeds a single partition's ceiling.

[Table of Contents](#DynamoDB)

## How do you read and write items with boto3?
boto3 offers two styles. The low-level `client` maps directly to the DynamoDB API and uses typed `AttributeValue` JSON. The higher-level `resource` (or `Table`) accepts and returns plain Python values and is easier to write but hides wire details you still need to recognize in interviews.

Low-level client with DynamoDB JSON:

```python
import boto3

client = boto3.client("dynamodb", region_name="us-east-1")

client.put_item(
    TableName="orders",
    Item={
        "PK": {"S": "CUSTOMER#123"},
        "SK": {"S": "ORDER#2026-10-04#999"},
        "order_id": {"S": "999"},
        "status": {"S": "shipped"},
        "amount": {"N": "149.90"},
        "tags": {"SS": ["priority", "gift"]},
        "meta": {"M": {"channel": {"S": "mobile"}}},
    },
    ConditionExpression="attribute_not_exists(PK)",
)

response = client.get_item(
    TableName="orders",
    Key={"PK": {"S": "CUSTOMER#123"}, "SK": {"S": "ORDER#2026-10-04#999"}},
    ConsistentRead=True,
)
item = response.get("Item")
```

Higher-level resource with plain values, plus a typed deserializer if you mix styles:

```python
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb", region_name="us-east-1").Table("orders")

table.put_item(Item={
    "PK": "CUSTOMER#123",
    "SK": "ORDER#2026-10-04#999",
    "status": "shipped",
    "amount": 149.90,
})

page = table.query(
    KeyConditionExpression=Key("PK").eq("CUSTOMER#123") & Key("SK").begins_with("ORDER#"),
    ProjectionExpression="order_id, #s, amount",
    ExpressionAttributeNames={"#s": "status"},
    Limit=25,
)
```

AWS CLI for a quick smoke test:

```bash
aws dynamodb put-item \
  --table-name orders \
  --item '{"PK":{"S":"CUSTOMER#123"},"SK":{"S":"ORDER#2026-10-04#999"},"status":{"S":"shipped"}}'

aws dynamodb get-item \
  --table-name orders \
  --key '{"PK":{"S":"CUSTOMER#123"},"SK":{"S":"ORDER#2026-10-04#999"}}'
```

PartiQL is useful for ad-hoc reads in the console and for teams that want SQL-like syntax:

```sql
SELECT order_id, status, amount
FROM orders
WHERE PK = 'CUSTOMER#123' AND begins_with(SK, 'ORDER#')
```

Notes:

+ `PutItem` replaces the whole item. Use `UpdateItem` with `SET`/`ADD`/`REMOVE` to change individual attributes safely under concurrency.
+ Attribute names that collide with reserved words (`status`, `size`, `timestamp`) must be aliased with `ExpressionAttributeNames`, which is why `#s` appears above.
+ `ProjectionExpression` reduces network and RCU cost by returning only the attributes you need.
+ `boto3` retries transient errors automatically; do not disable that except in tests that need deterministic failure behavior.

[Table of Contents](#DynamoDB)

## What is the difference between Query and Scan?
`Query` seeks directly to one partition (and optionally a sort-key range) using the index, so cost and latency scale with the number of matching items. `Scan` reads the entire table or index and then filters, so cost scales with table size regardless of how many rows you keep. Scan is the classic interview trap: it looks convenient and silently becomes the most expensive operation in the account.

```python
import boto3
from boto3.dynamodb.conditions import Attr, Key

table = boto3.resource("dynamodb", region_name="us-east-1").Table("orders")

# Good: one partition, one sort-key range
resp = table.query(
    KeyConditionExpression=Key("PK").eq("CUSTOMER#123") & Key("SK").between(
        "ORDER#2026-01-01", "ORDER#2026-10-04"
    ),
    FilterExpression=Attr("amount").gt(100),
    ScanIndexForward=False,
)

# Bad by default: full scan with a filter
resp = table.scan(
    FilterExpression=Attr("status").eq("cancelled"),
)
```

Pagination is identical for both and is driven by `LastEvaluatedKey`; a single call returns at most 1 MB:

```python
def query_all(table, **kwargs):
    items = []
    while True:
        resp = table.query(**kwargs)
        items.extend(resp["Items"])
        last = resp.get("LastEvaluatedKey")
        if not last:
            return items
        kwargs["ExclusiveStartKey"] = last
```

Interview notes:

+ `FilterExpression` is applied after the read. You still pay for the items that were read and discarded, so a filter that removes 99% of rows still costs 100%.
+ Use `Limit` for page size, not as a cost control; it caps items scanned per call, not total work.
+ If a scan is genuinely needed (one-off backfill, small config table, analytics export), isolate it, run it off-peak, and consider `ParallelScan` with `TotalSegments`.
+ If you find yourself scanning to answer an access pattern, the model is wrong: add a GSI or restructure keys.

[Table of Contents](#DynamoDB)

## What are DynamoDB capacity modes and how do you control cost?
DynamoDB offers on-demand and provisioned capacity. Cost comes from writes, reads, storage, indexes, backups, and streams, and the read/write unit accounting is the part candidates usually miss.

Unit math to memorize:

+ 1 WCU = 1 write per second for an item up to 1 KB; larger items consume `ceil(size_kb)` WCUs.
+ 1 RCU = 1 strongly consistent read per second for an item up to 4 KB, or 2 eventually consistent reads; larger items consume `ceil(size_kb / 4)`.
+ A GSI multiplies write cost: every base write that changes an indexed attribute writes to the index too.
+ Transactions cost roughly double (prepare plus commit), and transactional reads cost 2 RCUs per 4 KB.

```bash
# On-demand table (no capacity planning, pay per request)
aws dynamodb create-table --table-name orders \
  --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
  --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

# Provisioned table with application auto scaling
aws dynamodb update-table --table-name orders \
  --billing-mode PROVISIONED \
  --provisioned-throughput ReadCapacityUnits=50,WriteCapacityUnits=50
```

```yaml
# Application Auto Scaling target for the orders table
Targets:
  - Id: orders-writes
    ServiceNamespace: dynamodb
    ScalableDimension: dynamodb:table:WriteCapacityUnits
    ResourceId: table/orders
    MinCapacity: 20
    MaxCapacity: 2000
```

Choosing a mode:

+ On-demand is right when traffic is spiky, new, or hard to forecast. It scales immediately and you pay per request; it can be several times more expensive at steady high utilization.
+ Provisioned is right for predictable, sustained traffic. You can reserve capacity for large discounts, and auto scaling reacts within minutes, not instantly.
+ There is also provisioned with reserved capacity for one- or three-year commitments when the baseline is stable.

Cost controls that matter:

+ Reduce item size; RCU/WCU are rounded up per KB, so a 1.1 KB item costs twice a 1.0 KB item's write.
+ Use eventually consistent reads where acceptable, which halves read cost.
+ Project fewer attributes into GSIs; `KEYS_ONLY` and `INCLUDE` cost less than `ALL`.
+ Enable TTL to expire old items for free instead of paying to delete and store them.
+ Avoid scans over large tables; a bad scan can dominate the monthly bill.
+ Turn on DynamoDB Streams only where you consume them, and monitor index storage growth separately.

[Table of Contents](#DynamoDB)

## How do GSI and LSI projections and limits affect design?
Projection decides which attributes are copied into the index. It controls index size, index write cost, and whether a query can be answered without a follow-up read of the base table.

```json
{
  "IndexName": "by_status",
  "KeySchema": [
    {"AttributeName": "order_status", "KeyType": "HASH"},
    {"AttributeName": "order_ts", "KeyType": "RANGE"}
  ],
  "Projection": {
    "ProjectionType": "INCLUDE",
    "NonKeyAttributes": ["amount", "customer_id"]
  }
}
```

Projection types:

+ `KEYS_ONLY`: smallest and cheapest, but every query needs a second `GetItem` (or batch) to fetch other attributes.
+ `INCLUDE`: a limited list of extra attributes; a good middle ground.
+ `ALL`: no follow-up read, but the highest storage and write amplification.

Operational rules:

+ You cannot change an index's key schema later; changing projections requires a new index and a backfill. Plan key schemas carefully up front.
+ You can add a GSI online to a live table, which is the usual migration path when a new access pattern appears.
+ Queries that fetch non-projected attributes turn one request into N follow-up reads (the "N+1" DynamoDB anti-pattern). Prefer `ALL` or `INCLUDE` when the access pattern is hot.
+ Sparse indexes are a feature: only items that contain the index key are projected, so conditional keys keep an index small.
+ A GSI has its own throughput and its own hot-partition behavior; a low-cardinality GSI partition key can throttle even when the base table is healthy.

[Table of Contents](#DynamoDB)

## How do you use conditional writes and optimistic locking?
Conditional writes make an operation atomic and fail with `ConditionalCheckFailedException` when a condition is not met. They are how DynamoDB implements uniqueness, state machines, and optimistic locking without a server-side transaction.

Enforce uniqueness and valid state transitions:

```python
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

table = boto3.resource("dynamodb", region_name="us-east-1").Table("orders")

try:
    table.put_item(
        Item={"PK": "CUSTOMER#123", "SK": "ORDER#2026-10-04#999", "status": "created"},
        ConditionExpression="attribute_not_exists(PK)",
    )
except ClientError as exc:
    if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
        raise ValueError("order already exists") from exc
    raise

table.update_item(
    Key={"PK": "CUSTOMER#123", "SK": "ORDER#2026-10-04#999"},
    UpdateExpression="SET #s = :new, updated_at = :ts",
    ConditionExpression="#s = :expected",
    ExpressionAttributeNames={"#s": "status"},
    ExpressionAttributeValues={":new": "shipped", ":expected": "created", ":ts": "2026-10-04T13:00:00Z"},
)
```

Optimistic locking with a version attribute is the standard pattern for read-modify-write:

```python
def update_with_retry(key: dict, mutate, retries: int = 5) -> None:
    for _ in range(retries):
        item = table.get_item(Key=key, ConsistentRead=True)["Item"]
        new_item = mutate(item)
        new_item["version"] = int(item.get("version", 0)) + 1
        try:
            table.put_item(
                Item=new_item,
                ConditionExpression="version = :v",
                ExpressionAttributeValues={":v": int(item.get("version", 0))},
            )
            return
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
    raise RuntimeError("too much contention on item")
```

Notes:

+ A failed condition still consumes write capacity.
+ Conditions are evaluated atomically against the current item, so they work across concurrent writers without external locks.
+ Do not build distributed locks out of conditional writes unless you own the lease renewal and expiry semantics; a crashed holder can block progress.

[Table of Contents](#DynamoDB)

## How do you use DynamoDB transactions?
`TransactWriteItems` and `TransactGetItems` give all-or-nothing atomicity across up to 100 items, which can span multiple tables in the same account and Region. They are the escape hatch for invariants that cannot be modeled as a single item, such as debiting one account and crediting another.

```python
client = boto3.client("dynamodb", region_name="us-east-1")

client.transact_write_items(
    TransactItems=[
        {
            "Update": {
                "TableName": "ledger",
                "Key": {"PK": {"S": "ACCOUNT#A"}, "SK": {"S": "BALANCE"}},
                "UpdateExpression": "SET balance = balance - :amt",
                "ConditionExpression": "balance >= :amt",
                "ExpressionAttributeValues": {":amt": {"N": "100.00"}},
            }
        },
        {
            "Update": {
                "TableName": "ledger",
                "Key": {"PK": {"S": "ACCOUNT#B"}, "SK": {"S": "BALANCE"}},
                "UpdateExpression": "SET balance = balance + :amt",
                "ExpressionAttributeValues": {":amt": {"N": "100.00"}},
            }
        },
        {
            "Put": {
                "TableName": "ledger",
                "Item": {
                    "PK": {"S": "TXN#20261004#0001"},
                    "SK": {"S": "LEDGER"},
                    "amount": {"N": "100.00"},
                },
                "ConditionExpression": "attribute_not_exists(PK)",
            }
        },
    ],
    ClientRequestToken="txn-20261004-0001",
)
```

Constraints and failure modes:

+ 100 items maximum, 4 MB total, no two operations on the same item in one transaction.
+ Transactions are not supported across Regions or accounts.
+ You cannot run a `Query` inside a transaction; you must know the keys in advance. This pushes reads and business decisions before the transaction, which is when conflicts appear.
+ `TransactionConflictException` means another transaction touched the same item; retry with backoff.
+ Cost is higher: transactional writes roughly double the WCU, and `TransactWriteItems` cannot target a GSI directly.
+ Prefer single-item conditional updates when they suffice; reach for transactions only when the invariant genuinely spans items.

[Table of Contents](#DynamoDB)

## How do you capture changes with DynamoDB Streams and TTL?
DynamoDB Streams records an ordered log of item-level changes (with `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, or `NEW_AND_OLD_IMAGES`) and retains it for 24 hours. It is the standard way to trigger side effects, replicate to another store, and build CDC pipelines into a lakehouse.

```bash
aws dynamodb update-table --table-name orders \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES
```

Lambda consumer that forwards to Kinesis Firehose for lake landing:

```python
import json
import boto3
from decimal import Decimal

firehose = boto3.client("firehose")

def handler(event, context):
    records = []
    for record in event["Records"]:
        if record["eventName"] not in {"INSERT", "MODIFY", "REMOVE"}:
            continue
        image = record["dynamodb"].get("NewImage") or record["dynamodb"].get("OldImage")
        payload = {
            "event_name": record["eventName"],
            "event_id": record["eventID"],
            "keys": record["dynamodb"]["Keys"],
            "image": image,
        }
        records.append({
            "Data": json.dumps(payload, default=lambda o: float(o) if isinstance(o, Decimal) else str(o))
        })
    if records:
        firehose.put_record_batch(DeliveryStreamName="orders-cdc", Records=records)
    return {"forwarded": len(records)}
```

TTL deletes items automatically by comparing a numeric epoch-seconds attribute against the current time:

```bash
aws dynamodb update-time-to-live --table-name sessions \
  --time-to-live-specification "Enabled=true,AttributeName=expires_at"
```

```python
import time
table.put_item(Item={
    "PK": "SESSION#abc",
    "SK": "META",
    "user_id": "123",
    "expires_at": int(time.time()) + 3600,
})
```

Notes:

+ Streams are ordered per partition key, not globally. Downstream consumers must be idempotent and tolerate at-least-once delivery.
+ TTL deletion is free but not immediate; items can linger for up to ~48 hours and the delete appears in the stream with `eventName=REMOVE` and `userIdentity.principalId=dynamodb.amazonaws.com`. Do not rely on TTL for strict data-retention guarantees.
+ `NEW_AND_OLD_IMAGES` costs more and can double stream payload size; choose the smallest view type the consumer needs.
+ For lower latency and fan-out beyond Lambda's concurrency, send the stream to Kinesis Data Streams for DynamoDB and read from there.

[Table of Contents](#DynamoDB)

## How do you model one-to-many and many-to-many relationships?
DynamoDB has no joins, so relationships are modeled by duplicating data and choosing keys that cluster related items. The two core techniques are item collections (one partition key, many sort keys) and the adjacency-list pattern (each relationship becomes an item, queryable from both directions).

One-to-many, for example a customer with orders and each order with line items:

```text
PK = CUSTOMER#123   SK = ORDER#2026-10-04#999
PK = ORDER#999      SK = ITEM#1
PK = ORDER#999      SK = ITEM#2
```

```python
# All line items for an order
table.query(
    KeyConditionExpression=Key("PK").eq("ORDER#999") & Key("SK").begins_with("ITEM#")
)
```

Many-to-many with an adjacency list, for example users and projects with memberships:

```text
PK = USER#u1    SK = PROJECT#p1   role=admin
PK = PROJECT#p1 SK = USER#u1      role=admin
```

Writing both items in one `TransactWriteItems` keeps the relationship consistent, and each direction is a single `Query`. This doubles write cost per relationship but makes both traversals O(1) partitions.

Design rules that interviewers look for:

+ Duplicate the attributes needed by the query so you never need a join; denormalization is expected, and you accept update fan-out as the cost.
+ Use `begins_with` on hierarchical sort keys to model trees, for example `SK = PATH#/a/b/c`.
+ Keep item collections bounded. A single hot partition key cannot exceed one partition's throughput, and LSIs add a 10 GB per-key ceiling.
+ For high-fan-out aggregates (follower counts, likes), use sharded counters and sum on read rather than one hot item.
+ Version or soft-delete related items rather than performing multi-item deletes; then compact them with a background job.

[Table of Contents](#DynamoDB)

## How do you handle throttling, retries, and errors?
The errors you must recognize:

+ `ProvisionedThroughputExceededException` / `ThrottlingException`: capacity or partition-level limit exceeded. Retry with exponential backoff and jitter.
+ `ConditionalCheckFailedException`: a business condition failed; usually do not retry blindly.
+ `TransactionConflictException`: concurrent transaction on the same item; retry the whole transaction.
+ `ItemCollectionSizeLimitExceededException`: an LSI item collection exceeded 10 GB.
+ `ValidationException`: malformed expression, reserved word, or wrong key type.
+ `RequestLimitExceeded`: too many control-plane calls; back off.

Retry with full jitter using boto3's adaptive mode when appropriate:

```python
from botocore.config import Config
import boto3

config = Config(
    retries={"max_attempts": 10, "mode": "adaptive"},
    max_pool_connections=50,
)
client = boto3.client("dynamodb", region_name="us-east-1", config=config)
```

```python
import random
import time
from botocore.exceptions import ClientError

RETRYABLE = {"ProvisionedThroughputExceededException", "ThrottlingException", "RequestLimitExceeded"}

def with_backoff(fn, attempts: int = 8):
    for attempt in range(attempts):
        try:
            return fn()
        except ClientError as exc:
            code = exc.response["Error"]["Code"]
            if code not in RETRYABLE or attempt == attempts - 1:
                raise
            time.sleep(random.uniform(0, min(2 ** attempt, 20)) * 0.1)
```

Operational guidance:

+ Prefer `BatchWriteItem` (25 items) and `BatchGetItem` (100 keys) for throughput, but remember batch calls can partially fail and return `UnprocessedItems`; loop until empty with backoff.
+ Distinguish retryable throttling from a modeling problem. Persistent throttling on one key means the key is hot, not that retries are too few.
+ Add jitter; synchronized retries create thundering herds.
+ Track throttles per table and per index, and use Contributor Insights for per-key visibility.
+ Make consumers idempotent, because at-least-once delivery from Streams, Lambdas, and retries will replay operations.

[Table of Contents](#DynamoDB)

## When should you NOT use DynamoDB?
DynamoDB is excellent at predictable, single-digit-millisecond key-based access at very large scale. It is a poor fit when the query shape is unknown or the data is inherently relational.

Avoid DynamoDB when:

+ You need ad-hoc analytics, joins, or arbitrary `GROUP BY` aggregations. Use a warehouse or an OLAP store, and land DynamoDB data there via Streams or export to S3.
+ Query patterns are still changing weekly. Every new pattern can require a new GSI and a backfill, and index key schemas are immutable.
+ The workload is read-heavy with large scans over a modest table. A relational database with an index will be cheaper and simpler.
+ You need multi-item ACID transactions beyond 100 items, or cross-Region transactions.
+ Strong consistency across the whole dataset is required without design work; DynamoDB is per-item consistent, and GSIs are always eventually consistent.
+ Long, complex queries with server-side aggregation, window functions, or `ORDER BY` over non-key columns are core requirements.
+ The team needs a SQL-first workflow with BI tools pointing directly at the database.

Alternatives and when they fit:

+ Amazon Aurora/PostgreSQL for relational integrity, joins, and moderate scale.
+ Amazon Bigtable or Cassandra for wide-column, high-write time-series workloads with a different operational model.
+ Amazon Redshift, Athena, or an open lakehouse for analytics on the same data.
+ Elasticsearch/OpenSearch for full-text search and flexible filtering.

Interview answer: choose DynamoDB when access patterns are known, keys can be designed for even distribution, and the dominant need is horizontal scale at low latency. Otherwise name the access pattern that breaks it and propose the store that fits.

[Table of Contents](#DynamoDB)

## Real world use cases for DynamoDB

### 1. E-commerce cart and order state (multi-tenant SaaS)
Business context: a marketplace with 8M monthly active buyers needs a cart that survives devices, plus an order state machine. Volume: ~120M cart writes/day at peak 15k writes/s, items under 2 KB.

```text
PK = CART#<tenant>#<user_id>   SK = ITEM#<sku>
PK = ORDER#<order_id>          SK = META
GSI1: GSI1PK = USER#<user_id>#STATUS#<status>, GSI1SK = order_ts
```

`PutItem` with `ConditionExpression` guards item quantity, and `UpdateItem` transitions order status with a condition on the allowed previous state. `cart` uses TTL to expire abandoned carts after 30 days.

Why this design: every hot access pattern is a single-partition `Query`, conditional writes make concurrent device updates safe without a lock, and TTL removes abandoned-cart storage cost automatically. Tenant is part of the partition key so a large tenant cannot starve the others.

### 2. Fintech ledger and idempotent payments
Business context: a payments API must never double-post a transfer and must expose an audit trail. Volume: ~5M transfers/day, ledger item ~1 KB, strict p99 under 20 ms.

```python
client.transact_write_items(
    TransactItems=[
        {"Update": {"TableName": "ledger",
                    "Key": {"PK": {"S": "ACCOUNT#A"}, "SK": {"S": "BALANCE"}},
                    "UpdateExpression": "SET balance = balance - :amt",
                    "ConditionExpression": "balance >= :amt",
                    "ExpressionAttributeValues": {":amt": {"N": "250.00"}}}},
        {"Put": {"TableName": "ledger",
                 "Item": {"PK": {"S": "IDEMPOTENCY#req-7f3a"}, "SK": {"S": "TX"},
                          "response": {"S": "accepted"}},
                 "ConditionExpression": "attribute_not_exists(PK)"}},
    ],
    ClientRequestToken="req-7f3a",
)
```

Why this design: the delete-and-credit pair is atomic, and the idempotency item makes retries safe. The same `ClientRequestToken` lets DynamoDB reject duplicate submissions. Streams feed both the fraud pipeline and a lakehouse audit table.

### 3. IoT telemetry latest-state and alerting
Business context: 250k devices report every 10 seconds; the app needs the latest reading per device and hot-device alerting, while the full time series lives in S3/Timestream. Volume: 2.2B writes/day, ~1 KB per reading.

```text
PK = DEVICE#<device_id>   SK = LATEST
GSI1: GSI1PK = SITE#<site_id>#STATE#<state>, GSI1SK = last_seen
```

Writes overwrite `LATEST` with a conditional `last_seen > :prev` so out-of-order retries cannot regress state. A sparse GSI holds only devices currently in `ALARM`, so alert queries are tiny.

Why this design: overwriting a single item per device keeps storage flat, the sparse index keeps alerting cheap, and the bulk time series is streamed to cheap object storage rather than stored in DynamoDB.

### 4. CDC from DynamoDB into an open lakehouse
Business context: the analytics team needs near-real-time order facts in Iceberg without querying the production table. Volume: 120M change events/day, peak 5 MB/s.

```text
DynamoDB Streams (NEW_AND_OLD_IMAGES)
  -> Lambda (batch 500 records, idempotent by eventID)
  -> Kinesis Firehose (60s buffer)
  -> s3://lake/bronze/dynamodb_orders/  (JSON, partitioned by ingest date)
  -> Spark Structured Streaming MERGE INTO iceberg.analytics.orders
```

Why this design: Streams is push-based and adds no read load to the serving table, Firehose buffers and batches to avoid small files, and the `eventID` gives the lakehouse a natural dedup key for the Spark merge.

### 5. Gaming leaderboard and session store
Business context: 3M daily players need sub-10 ms leaderboard reads and session lookups that expire. Volume: ~50k updates/s at peak during events.

```text
PK = LEADERBOARD#<board_id>   SK = SCORE#<padded_score>#<player_id>
PK = SESSION#<session_id>     SK = META     (TTL expires_at)
```

Scores are zero-padded so `ScanIndexForward=False` returns the top N in score order without sorting server-side. DAX sits in front to absorb repeated leaderboard reads.

Why this design: `Query` with a descending sort on the sort key returns the top players without aggregation, DAX cuts read cost on the hot board, and TTL handles sessions without a cleanup job.

[Table of Contents](#DynamoDB)
