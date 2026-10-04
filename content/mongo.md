## [Main title](../README.md)
### [Interview questions](full.md)

# MongoDB

**Notebook:** [`notebooks/topics/mongo.ipynb`](../notebooks/topics/mongo.ipynb) - runnable version of this topic with self-checking exercises.

MongoDB is a document database. Records are BSON documents stored in collections, the schema is flexible by default and enforceable with `$jsonSchema`, indexes make the common queries fast, replica sets provide automatic failover, and sharding provides horizontal scale.

+ [What is MongoDB?](#What-is-MongoDB)
+ [How do you model documents in MongoDB?](#How-do-you-model-documents-in-MongoDB)
+ [How do indexes affect MongoDB query performance?](#How-do-indexes-affect-MongoDB-query-performance)
+ [Why use MongoDB?](#Why-use-MongoDB)
+ [What are the Advantages of MongoDB?](#What-are-the-Advantages-of-MongoDB)
+ [When Should You Use MongoDB?](#When-Should-You-Use-MongoDB)
+ [How does MongoDB exactly store the data?](#How-does-MongoDB-exactly-store-the-data)
+ [MongoDB vs. RDBMS: What are the differences?](#MongoDB-vs-RDBMS-What-are-the-differences)
+ [How does mongodb scale?](#How-does-mongodb-scale)
+ [How does mongodb scale horizontally?](#How-does-mongodb-scale-horizontally)
+ [What are the advantages of sharding?](#What-are-the-advantages-of-sharding)
+ [What methods can we use for sharding in mongodb?](#What-methods-can-we-use-for-sharding-in-mongodb)
+ [How does atomicity and transaction word in mongodb?](#How-does-atomicity-and-transaction-word-in-mongodb)
+ [What is an Aggregation Pipeline in mongodb?](#What-is-an-Aggregation-Pipeline-in-mongodb)
+ [Where should I use an index in mongodb?](#Where-should-I-use-an-index-in-mongodb)
+ [How would you choose a indexing strategy in mongo and what are some common considerations we need to care about?](#How-would-you-choose-a-indexing-strategy-in-mongo-and-what-are-some-common-considerations-we-need-to-care-about)
+ [How does MongoDB ensure data consistency and reliability?](#How-does-MongoDB-ensure-data-consistency-and-reliability)
+ [What are MongoDB's backup and restore options?](#What-are-MongoDBs-backup-and-restore-options)
+ [How does MongoDB handle concurrency?](#How-does-MongoDB-handle-concurrency)
+ [What security features does MongoDB offer?](#What-security-features-does-MongoDB-offer)
+ [How does MongoDB manage schema design and changes?](#How-does-MongoDB-manage-schema-design-and-changes)
+ [What are the limitations or disadvantages of MongoDB?](#What-are-the-limitations-or-disadvantages-of-MongoDB)
+ [How do you perform migrations from RDBMS to MongoDB?](#How-do-you-perform-migrations-from-RDBMS-to-MongoDB)
+ [What is MongoDB Atlas and what benefits does it provide?](#What-is-MongoDB-Atlas-and-what-benefits-does-it-provide)
+ [How can you monitor and optimize MongoDB performance?](#How-can-you-monitor-and-optimize-MongoDB-performance)
+ [What is a replica set in MongoDB and how does it work?](#What-is-a-replica-set-in-MongoDB-and-how-does-it-work)
+ [How do change streams work in MongoDB?](#How-do-change-streams-work-in-MongoDB)
+ [How do you handle data integrity in MongoDB?](#How-do-you-handle-data-integrity-in-MongoDB)
+ [How does MongoDB fit into the CAP theorem?](#How-does-MongoDB-fit-into-the-CAP-theorem)
+ [How do you handle large data volumes in MongoDB?](#How-do-you-handle-large-data-volumes-in-MongoDB)
+ [What are the best practices for designing a MongoDB schema?](#What-are-the-best-practices-for-designing-a-MongoDB-schema)
+ [How does MongoDB handle geographic data and geospatial queries?](#How-does-MongoDB-handle-geographic-data-and-geospatial-queries)
+ [What are the trade-offs and when should you not use MongoDB?](#What-are-the-trade-offs-and-when-should-you-not-use-MongoDB)
+ [Real world use cases for MongoDB](#Real-world-use-cases-for-MongoDB)

## What is MongoDB?
MongoDB is a document database built on a horizontal scale-out architecture that uses a flexible schema for storing data. Founded in 2007, MongoDB has a worldwide following in the developer community.

The unit of storage is a BSON document: key/value pairs with nested objects, arrays, and rich types (dates, decimals, ObjectId, binary). Documents with a similar shape live in a collection. There is no fixed table schema, joins are optional (`$lookup`, `$graphLookup`), and scale-out is built in through replica sets and shards rather than bolted on.

```text
// mongosh: switch database, insert, query, project
use shop
db.products.insertOne({
  sku: "A1",
  name: "Espresso Machine",
  price: NumberDecimal("249.00"),
  tags: ["kitchen", "coffee"],
  stock: { warehouse: "DFW", qty: 12 }
})
db.products.find({ tags: "coffee" }, { name: 1, price: 1, _id: 0 }).sort({ price: -1 }).limit(5)
```

Core capabilities an interviewer expects you to name: document model, secondary indexes (single, compound, multikey, text, TTL, geospatial, wildcard, partial), the aggregation framework, multi-document transactions (4.0+), replica sets, sharding, and tunable read/write concern.

[Table of Contents](#MongoDB)

## How do you model documents in MongoDB?
MongoDB modeling depends on access patterns. Embed related data when it is usually read together and has bounded size. Reference related data when it grows independently, is shared by many documents, or would create very large documents.

Example embedded order:

```json
{
  "_id": "order_1001",
  "customer_id": "C123",
  "items": [
    {"sku": "A1", "qty": 2},
    {"sku": "B9", "qty": 1}
  ]
}
```

This is efficient when the application usually reads an order with its items. For large or frequently changing child collections, referencing is safer.

The rule of thumb is one-to-few embeds, one-to-many references, and one-to-squillions (unbounded, such as events or messages) uses a separate collection plus the bucket pattern so a single document never grows without limit. References cost an extra round trip and an application-side join, or a `$lookup` in the pipeline.

```text
// Referenced model: order points at the customer
db.orders.insertOne({ _id: "order_1002", customer_id: "C123", total: NumberDecimal("312.00") })

// Join them when the report needs both
db.orders.aggregate([
  { $match: { _id: "order_1002" } },
  { $lookup: {
      from: "customers",
      localField: "customer_id",
      foreignField: "_id",
      as: "customer"
  } },
  { $unwind: "$customer" },
  { $project: { total: 1, "customer.name": 1, "customer.tier": 1 } }
])
```

Duplicate deliberately when reads dominate and the copied value changes rarely (for example the product name inside an order line). Duplication is a cache: you must decide who owns updates and how stale copies are refreshed.

[Table of Contents](#MongoDB)

## How do indexes affect MongoDB query performance?
Indexes let MongoDB find documents without scanning the whole collection. Compound indexes should match common filters and sort patterns. Too many indexes slow writes and consume storage, so indexes should be tied to real query patterns.

Example:

```text
db.orders.createIndex({ customer_id: 1, created_at: -1 })
```

This helps queries like "latest orders for customer C123." Use explain plans to confirm the index is used.

```text
const plan = db.orders
  .find({ customer_id: "C123" })
  .sort({ created_at: -1 })
  .explain("executionStats")

print(plan.queryPlanner.winningPlan.inputStage.stage)   // IXSCAN, not COLLSCAN
print(plan.executionStats.nTotalDocsExamined)           // should be ~ nReturned
print(plan.executionStats.nReturned)
```

Two numbers matter in an interview: `nReturned` vs `nTotalDocsExamined` (a large ratio means the index is not selective enough) and `totalKeysExamined`. A `COLLSCAN` or an in-memory `SORT` stage in the winning plan is the signal to add or reorder an index. Index types worth naming: compound, multikey (an indexed array), text, TTL (auto-expiry), 2dsphere, partial (`partialFilterExpression`), unique, and wildcard.

[Table of Contents](#MongoDB)

## Why use MongoDB?
As a document database, MongoDB makes it easy for developers to store structured or unstructured data. It uses a JSON-like format to store documents. This format directly maps to native objects in most modern programming languages, making it a natural choice for developers, as they don't need to think about normalizing data. MongoDB can also handle high volume and can scale both vertically or horizontally to accommodate large data loads.

The practical drivers are: one round trip returns a whole aggregate (an order with its lines) instead of a multi-table join; the schema can evolve without a migration window; read scaling and failover are built into a replica set; and sharding extends the same model to multi-terabyte collections.

[Table of Contents](#MongoDB)

## What are the Advantages of MongoDB?
- A Powerful Document-Oriented Database: rich query language, aggregation framework, geospatial and text search, and multi-document transactions.
- Developer User Experience: documents map to objects in application code; no object-relational impedance mismatch during early product iteration.
- Scalability and Transactionality: replica sets for availability, sharding for horizontal scale, and snapshot-isolation transactions across documents and collections.
- Platform and Ecosystem Maturity: official drivers for every major language, Atlas managed service, Compass, BI connectors, and a large operational toolset.
- Flexible Schema: fields can differ per document, which fits evolving and heterogeneous data; validation can be added later where the data needs it.

[Table of Contents](#MongoDB)

## When Should You Use MongoDB?
- Integrating large amounts of diverse data (catalogs with heterogeneous attributes, semi-structured ingestion).
- Describing complex data structures that evolve quickly and would otherwise force constant DDL migrations.
- Delivering data in high-performance applications where one document read replaces several joins.
- Supporting hybrid and multi-cloud applications with replica sets in multiple regions.
- Supporting agile development and collaboration, where a schema change is a code change.

When not to reach for it: heavy multi-entity transactional reporting, applications that need mature SQL analytics and star-schema joins, data that exceeds the 16 MB document limit as a single aggregate, or workloads with thousands of secondary indexes where write amplification dominates.

[Table of Contents](#MongoDB)

## How does MongoDB exactly store the data?
In MongoDB, records are stored as documents in compressed [BSON](https://www.mongodb.com/json-and-bson) files. The documents can be retrieved directly in JSON format, which has many benefits:

- It is a natural form to store data.
- It is human-readable.
- Structured and unstructured information can be stored in the same document.
- You can nest JSON to store complex data objects.
- JSON has a flexible and dynamic schema, so adding fields or leaving a field out is not a problem.
- Documents map to objects in most popular programming languages.

Most developers find it easy to work with JSON because it is a simple and powerful way to describe and store data.

Under the hood the default storage engine is WiredTiger: documents are stored in compressed files (snappy by default for collections, zlib/zstd configurable), each collection has a `_id` index, and the journal (write-ahead log) provides durability. BSON supports types JSON does not, such as `ObjectId`, `Decimal128`, `Date`, `Binary`, and 64-bit integers, which matters for money and timestamps.

```text
// BSON size matters: one document may not exceed 16 MB
const doc = { sku: "A1", tags: ["kitchen", "coffee"], created: new Date() }
print(Object.bsonSize(doc))   // bytes, including field names
```

Two consequences interviewers look for: big arrays make documents grow on update (the document may move on disk, and the Storage engine must rewrite it), and the 16 MB cap is a hard design constraint that pushes unbounded data into a child collection.

[Table of Contents](#MongoDB)

## MongoDB vs. RDBMS: What are the differences?

One of the main differences between MongoDB and RDBMS is that RDBMS is a relational database while MongoDB is nonrelational. Likewise, while most RDBMS systems use SQL to manage stored data, MongoDB uses BSON for data storage.

While RDBMS uses tables and rows, MongoDB uses documents and collections. In RDBMS a table -- the equivalent to a MongoDB collection -- stores data as columns and rows. Likewise, a row in RDBMS is the equivalent of a MongoDB document but stores data as structured data items in a table. A column denotes sets of data values, which is the equivalent to a field in MongoDB.

| Aspect | RDBMS | MongoDB |
|---|---|---|
| Unit | row in a table | BSON document in a collection |
| Schema | fixed, DDL migrations | flexible, optional `$jsonSchema` validation |
| Relationships | foreign keys + joins | embedding, `$lookup`, application joins |
| Transactions | multi-row by default | single-document atomic; multi-document with sessions |
| Scale-out | mostly vertical, read replicas | native sharding + replica sets |
| Query language | SQL | MQL / aggregation pipeline, SQL via Atlas SQL |
| Best fit | strongly relational, reporting | aggregate-oriented, evolving, high write volume |

MongoDB is not "RDBMS without discipline": the schema still exists, it just lives in the application and in validators rather than in foreign-key constraints.

[Table of Contents](#MongoDB)

## How does mongodb scale?
mongo scales the same way as any distributed application would scale, throw more resources at it (`Vertical Scaling`) or distribute the data on multiple physical servers or nodes (`Horizontal Scaling`).

or in other words:

*Vertical Scaling* involves increasing the capacity of a single server, such as using a more powerful CPU, adding more RAM, or increasing the amount of storage space. It is simple but has a ceiling and is often a single point of failure.

*Horizontal Scaling* involves dividing the system dataset and load over multiple servers, adding additional servers to increase capacity as required. Sharding is MongoDB's horizontal mechanism; replica sets scale reads and provide availability but do not split a single collection.

While the overall speed or capacity of a single machine may not be high, each machine handles a subset of the overall workload, potentially providing better efficiency than a single high-speed high-capacity server.

Before sharding, exhaust the cheaper levers: correct indexes, covered queries, read preference `secondaryPreferred` for analytics, projection to avoid fetching large fields, and `$out`/`$merge` rollups so dashboards read small summary collections.

[Table of Contents](#MongoDB)

## How does mongodb scale horizontally?

MongoDB supports *horizontal scaling* through [sharding.](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharding)

Sharding is a method for distributing data across multiple machines. MongoDB uses sharding to support deployments with very large data sets and high throughput operations.

A MongoDB [sharded cluster](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster) consists of the following components:

- [shard](https://www.mongodb.com/docs/manual/core/sharded-cluster-shards/#std-label-shards-concepts): Each shard contains a subset of the sharded data. Each shard must be deployed as a [replica set.](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-replica-set)
- [mongos](https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/): The `mongos` acts as a query router, providing an interface between client applications and the sharded cluster. [`mongos`](https://www.mongodb.com/docs/manual/reference/program/mongos/#mongodb-binary-bin.mongos) can support [hedged reads](https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/#std-label-mongos-hedged-reads) to minimize latencies.
- [config servers](https://www.mongodb.com/docs/manual/core/sharded-cluster-config-servers/#std-label-sharding-config-server): Config servers store metadata and configuration settings for the cluster. As of MongoDB 3.4, config servers must be deployed as a replica set (CSRS).

The following graphic describes the interaction of components within a sharded cluster:

![Diagram of a sample sharded cluster for production purposes.  Contains exactly 3 config servers, 2 or more ``mongos`` query routers, and at least 2 shards. The shards are replica sets.](https://www.mongodb.com/docs/manual/images/sharded-cluster-production-architecture.bakedsvg.svg)

MongoDB shards data at the [collection](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-collection) level, distributing the collection data across the shards in the cluster.

```text
// Enable sharding and pick a shard key (run against mongos)
sh.enableSharding("shop")
sh.shardCollection("shop.orders", { customer_id: "hashed" })

// Inspect balance and chunk distribution
sh.status()
db.orders.getShardDistribution()
```

A sharded cluster needs a shard key chosen up front: queries that include the shard key (or its prefix) are routed to one shard; everything else becomes a scatter-gather across all shards.

[Table of Contents](#MongoDB)

## What are the advantages of sharding?

##### Reads / Writes

MongoDB distributes the read and write workload across the [shards](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-shard) in the [sharded cluster](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster), allowing each shard to process a subset of cluster operations. Both read and write workloads can be scaled horizontally across the cluster by adding more shards.

For queries that include the shard key or the prefix of a [compound](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-compound-index) shard key, [`mongos`](https://www.mongodb.com/docs/manual/reference/program/mongos/#mongodb-binary-bin.mongos) can target the query at a specific shard or set of shards. These [targeted operations](https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/#std-label-sharding-mongos-targeted) are generally more efficient than [broadcasting](https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/#std-label-sharding-mongos-broadcast) to every shard in the cluster.

[`mongos`](https://www.mongodb.com/docs/manual/reference/program/mongos/#mongodb-binary-bin.mongos) can support [hedged reads](https://www.mongodb.com/docs/manual/core/sharded-cluster-query-router/#std-label-mongos-hedged-reads) to minimize latencies.

##### Storage Capacity

[Sharding](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharding) distributes data across the [shards](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-shard) in the cluster, allowing each shard to contain a subset of the total cluster data. As the data set grows, additional shards increase the storage capacity of the cluster.

##### High Availability

The deployment of config servers and shards as replica sets provide increased availability.

Even if one or more shard replica sets become completely unavailable, the sharded cluster can continue to perform partial reads and writes. That is, while data on the unavailable shard(s) cannot be accessed, reads or writes directed at the available shards can still succeed.

The cost of these advantages is operational: more components, a shard key that is expensive or impossible to change later, and the risk of an unbalanced cluster if the key is monotonically increasing (for example an ObjectId or a timestamp) or too coarse.

[Table of Contents](#MongoDB)

## What methods can we use for sharding in mongodb?

MongoDB supports two sharding strategies for distributing data across [sharded clusters.](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-sharded-cluster)

##### Hashed Sharding

Hashed Sharding involves computing a hash of the shard key field's value. Each [chunk](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-chunk) is then assigned a range based on the hashed shard key values. It spreads writes well even for monotonically increasing keys, but range queries on the shard key cannot be targeted and must be broadcast.

##### Ranged Sharding

Ranged sharding involves dividing data into ranges based on the shard key values. Each [chunk](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-chunk) is then assigned a range based on the shard key values. Range queries are targeted, but a monotonically increasing key sends every new write to the last chunk, creating one hot shard.

```text
// Hashed: even write spread, scatter-gather on ranges
sh.shardCollection("shop.events", { tenant_id: "hashed" })

// Ranged compound: target by tenant, keep recent data together
sh.shardCollection("shop.orders", { tenant_id: 1, created_at: 1 })
```

A good shard key is high cardinality, low frequency per value, non-monotonic, and present in the queries you care about. Consider a compound key such as `{ tenant_id: 1, created_at: 1 }` when you need multi-tenant isolation plus recent-data locality.

[Table of Contents](#MongoDB)

## How does atomicity and transaction word in mongodb?

In MongoDB, a write operation is [atomic](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-atomic-operation) on the level of a single document, even if the operation modifies multiple embedded documents *within* a single document.

When a single write operation (e.g. [`db.collection.updateMany()`](https://www.mongodb.com/docs/manual/reference/method/db.collection.updateMany/#mongodb-method-db.collection.updateMany)) modifies multiple documents, the modification of each document is atomic, but the operation as a whole is not atomic.

For situations that require atomicity of reads and writes to multiple documents (in a single or multiple collections), MongoDB supports distributed transactions, including transactions on replica sets and sharded clusters. Transactions require a replica set or sharded cluster, use snapshot isolation, and default to a 60-second lifetime.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
accounts = client.bank.accounts
transfers = client.bank.transfers

with client.start_session() as session:
    with session.start_transaction():
        accounts.update_one({"_id": "A"}, {"$inc": {"balance": -100}}, session=session)
        accounts.update_one({"_id": "B"}, {"$inc": {"balance": 100}}, session=session)
        transfers.insert_one(
            {"from": "A", "to": "B", "amount": 100, "status": "posted"},
            session=session,
        )
```

Because a single-document update is atomic, many "transactions" are avoidable: `$inc`, `$push`, `$addToSet`, `findAndModify`, and upserts each operate atomically on one document. Design the document so the invariant fits inside it, and reach for a multi-document transaction only when it genuinely spans documents.

[Table of Contents](#MongoDB)

## What is an Aggregation Pipeline in mongodb?

An aggregation pipeline consists of one or more [stages](https://www.mongodb.com/docs/manual/reference/operator/aggregation-pipeline/#std-label-aggregation-pipeline-operator-reference) that process documents:

- Each stage performs an operation on the input documents. For example, a stage can filter documents, group documents, and calculate values.
- The documents that are output from a stage are passed to the next stage.
- An aggregation pipeline can return results for groups of documents. For example, return the total, average, maximum, and minimum values.

```text
db.orders.aggregate([
  { $match: { status: "paid", created_at: { $gte: ISODate("2026-10-01") } } },
  { $unwind: "$items" },
  { $group: {
      _id: { day: { $dateTrunc: { date: "$created_at", unit: "day" } }, sku: "$items.sku" },
      revenue: { $sum: { $multiply: ["$items.qty", "$items.price"] } },
      orders: { $sum: 1 },
      avg_qty: { $avg: "$items.qty" }
  } },
  { $sort: { "_id.day": 1, revenue: -1 } },
  { $merge: { into: "daily_sku_revenue", whenMatched: "replace", whenNotMatched: "insert" } }
], { allowDiskUse: true })
```

Put `$match` and `$limit` first so indexes can be used and fewer documents flow through the pipeline. Stage names to know: `$match`, `$project`, `$group`, `$sort`, `$unwind`, `$lookup`, `$facet` (several reports in one pass), `$bucket`, `$setWindowFields` (running totals), and `$merge`/`$out` for materialized views. `$lookup` does not use an index on the foreign collection's join field unless one exists, so index `foreignField`.

[Table of Contents](#MongoDB)

## Where should I use an index in mongodb?

If your application is repeatedly running queries on the same fields, you can create an index on those fields to improve performance.

Although indexes improve query performance, adding an index has negative performance impact for write operations. For collections with a high write-to-read ratio, indexes are expensive because each insert must also update any indexes.

Concretely: index the fields used in equality filters, in sorts, and in the join key of `$lookup`; add a TTL index when data expires; use a text index for search; and use a partial index when only a small slice of documents is queried.

```text
db.sessions.createIndex({ expires_at: 1 }, { expireAfterSeconds: 0 })   // TTL
db.orders.createIndex(
  { tenant_id: 1, status: 1 },                                          // partial
  { partialFilterExpression: { status: "open" } }
)
db.products.createIndex({ name: "text", description: "text" }, { weights: { name: 10 } })
```

[Table of Contents](#MongoDB)

## How would you choose a indexing strategy in mongo and what are some common considerations we need to care about?

The best indexes for your application must take a number of factors into account, including the kinds of queries you expect, the ratio of reads to writes, and the amount of free memory on your system.

The best overall strategy for designing indexes is to profile a variety of index configurations with data sets similar to the ones you'll be running in production to see which configurations perform best. Inspect the current indexes created for your collections to ensure they are supporting your current and planned queries. If an index is no longer used, drop the index.

These are some considerations you need to take for your indexing strategy:

- [Use the ESR (Equality, Sort, Range) Rule](https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-rule/#std-label-esr-indexing-rule)

  The ESR (Equality, Sort, Range) Rule is a guide to creating indexes that support your queries efficiently.

- [Create Indexes to Support Your Queries](https://www.mongodb.com/docs/manual/tutorial/create-indexes-to-support-queries/#std-label-create-indexes-to-support-queries)

  An index supports a query when the index contains all the fields scanned by the query. Creating indexes that support queries results in greatly increased query performance.

- [Use Indexes to Sort Query Results](https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/#std-label-sorting-with-indexes)

  To support efficient queries, use the strategies here when you specify the sequential order and sort order of index fields.

- [Ensure Indexes Fit in RAM](https://www.mongodb.com/docs/manual/tutorial/ensure-indexes-fit-ram/#std-label-indexes-ensure-indexes-fit-ram)

  When your index fits in RAM, the system can avoid reading the index from disk and you get the fastest processing.

- [Create Indexes to Ensure Query Selectivity](https://www.mongodb.com/docs/manual/tutorial/create-queries-that-ensure-selectivity/#std-label-index-selectivity)

  Selectivity is the ability of a query to narrow results using the index. Selectivity allows MongoDB to use the index for a larger portion of the work associated with fulfilling the query.

ESR in one example: the query `{ tenant_id: "t1", status: "open" }` sorted by `created_at` and filtered by `total: { $gt: 100 }` wants the index `{ tenant_id: 1, status: 1, created_at: -1, total: 1 }` - equality fields first in any order, then the sort field in its sort direction, then the range field.

```text
// Which indexes exist, and are they actually used?
db.orders.getIndexes()
db.orders.aggregate([{ $indexStats: {} }], { comment: "find unused indexes" })
// Look at "accesses.ops" == 0 to find candidates for dropping
```

[Table of Contents](#MongoDB)

## How does MongoDB ensure data consistency and reliability?

MongoDB ensures data consistency and reliability through several mechanisms:

- Write Concern: Allows you to specify the level of acknowledgment required from MongoDB for write operations.
- Replica Sets: Provides data redundancy and high availability.
- Journaling: Ensures data durability by writing operations to a journal before applying them to the data files.
- Data Validation: Allows you to enforce document structure.

The combination to reason about is write concern plus read concern plus read preference:

```text
// Durable, majority-acknowledged, journaled write
db.orders.insertOne(
  { _id: "order_1003", total: NumberDecimal("99.00") },
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
)

// Read only data that a majority has acknowledged, from the primary
db.orders.find({ _id: "order_1003" }).readConcern("majority").readPref("primary")
```

`w: 1` acknowledges from the primary only and is fast but can be rolled back after failover. `w: "majority"` survives failover. `readConcern: "majority"` returns data that will not be rolled back; `"snapshot"` gives a consistent point-in-time view and is what transactions use. `readPreference: "secondaryPreferred"` scales reads but can serve stale data (eventual consistency).

[Table of Contents](#MongoDB)

## What are MongoDB's backup and restore options?

MongoDB offers several backup and restore options:

- mongodump and mongorestore: Command-line tools for creating binary exports of database contents and restoring them.
- Filesystem snapshots: For creating point-in-time snapshots of data (only consistent if taken with the journal, or on a stopped/fsync-locked node).
- MongoDB Atlas Backup: Continuous backups and point-in-time recovery for cloud-hosted databases.
- MongoDB Ops Manager: For on-premises deployments, offering backup automation and point-in-time recovery.

```bash
# Logical backup of one database
mongodump --uri="mongodb://localhost:27017" --db=shop --out=/backup/2026-10-04

# Point-in-time-consistent backup of a replica set (captures oplog for replay)
mongodump --uri="mongodb://localhost:27017/?replicaSet=rs0" --oplog --out=/backup/rs-2026-10-04

# Restore into a different database name
mongorestore --uri="mongodb://localhost:27017" --nsFrom="shop.*" --nsTo="shop_restore.*" /backup/2026-10-04
```

mongodump is logical and slows down on multi-terabyte clusters; for large clusters prefer snapshots or Atlas continuous backup plus oplog replay, and always test a restore. For a single collection, `mongoexport`/`mongoimport` produce JSON/CSV but lose BSON types such as `Decimal128`.

[Table of Contents](#MongoDB)

## How does MongoDB handle concurrency?

MongoDB handles concurrency through:

- Document-level locking: Allows multiple clients to read and write different documents simultaneously.
- WiredTiger storage engine: Provides document-level concurrency control and compression.
- Multi-version Concurrency Control (MVCC): Allows readers to see a consistent view of data without blocking writers.

Two keys on the application side:

```text
// Optimistic concurrency: version field guards against lost updates
const res = db.documents.updateOne(
  { _id: "doc1", version: 42 },
  { $set: { body: "new" }, $inc: { version: 1 } }
)
if (res.matchedCount === 0) {
  throw new Error("conflict: document changed since it was read")
}

// Atomic compare-and-set on a queue
db.jobs.findOneAndUpdate(
  { status: "queued" },
  { $set: { status: "running", worker: "w1", started_at: new Date() } },
  { sort: { priority: -1 }, returnDocument: "after" }
)
```

An unindexed update that matches many documents still takes a collection-level intent and can cause write conflicts (`WriteConflict` errors) under high concurrency; keeping documents small and updates targeted by `_id` avoids most of it.

[Table of Contents](#MongoDB)

## What security features does MongoDB offer?

Once again we have many options for security as well, like:

- Authentication: Supports various authentication mechanisms (SCRAM, x.509 certificates, LDAP, Kerberos).
- Authorization: Role-Based Access Control (RBAC) for fine-grained access control.
- Encryption: Supports encryption at rest and in transit (TLS/SSL).
- Auditing: Allows tracking of system and user activities.
- Network isolation: Supports IP whitelisting and VPC peering.

```text
// Least-privilege application user with a custom role
db.createRole({
  role: "ordersApp",
  privileges: [
    { resource: { db: "shop", collection: "orders" }, actions: ["find", "insert", "update"] }
  ],
  roles: []
})
db.createUser({
  user: "orders-svc",
  pwd: passwordPrompt(),
  roles: [{ role: "ordersApp", db: "shop" }]
})

// Never leave the server open: bind to the private interface and require auth
db.adminCommand({ getCmdLineOpts: 1 })
```

Also name Client-Side Field Level Encryption (CSFLE) for sensitive fields such as PII or card numbers, and note that encrypting fields makes them unqueryable by equality unless you use deterministic encryption.

[Table of Contents](#MongoDB)

## How does MongoDB manage schema design and changes?

MongoDB uses a flexible, document-based model for schema design:

- Schemaless: Collections don't enforce document structure by default.
- Dynamic Schema: Documents in a collection can have different fields.
- Schema Validation: Optional rules can be set to enforce document structure.
- Indexing: Supports various index types to optimize query performance.

For schema changes:

- Adding fields: Simply update documents with new fields.
- Removing fields: Delete fields from documents or use $unset in updates.
- Changing field types: Update documents with new data types.
- Large-scale changes: Can be done programmatically or using tools like Mongoose for Node.js.

```text
// JSON Schema validation: enforce shape, types, and required fields
db.createCollection("customers", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "tier", "created_at"],
      additionalProperties: false,
      properties: {
        email: { bsonType: "string", pattern: "^.+@.+$" },
        tier: { enum: ["free", "pro", "enterprise"] },
        created_at: { bsonType: "date" },
        schema_version: { bsonType: "int", minimum: 1 }
      }
    }
  },
  validationLevel: "moderate",     // existing invalid docs are allowed
  validationAction: "error"        // or "warn"
})

// Apply validation to an existing collection, or relax it during a migration
db.runCommand({ collMod: "customers", validationLevel: "off" })
```

Two patterns make changes safe. First, version documents (`schema_version`) so readers handle both shapes during a rollout. Second, expand-migrate-contract: add the new nullable field, dual-write, backfill with a batched update, then remove the old field. `validationLevel: "off"` or `"moderate"` avoids blocking writes mid-migration.

[Table of Contents](#MongoDB)

## What are the limitations or disadvantages of MongoDB?

Some limitations and disadvantages of MongoDB include:

- Limited JOIN functionality compared to relational databases (`$lookup` exists but is not a cost-based join optimizer).
- Document size limit of 16MB.
- Lack of built-in data integrity constraints (like foreign key constraints) - you enforce them with `$jsonSchema`, unique indexes, and transactions.
- Higher storage space requirements due to data duplication in denormalized models.
- Steeper learning curve for those accustomed to relational databases.
- Less mature ecosystem compared to some traditional RDBMSs, especially for BI, star-schema modeling, and ad-hoc analysts.
- Unbounded document growth: `$push` into an ever-growing array degrades updates and eventually hits 16 MB.
- No cross-collection unique constraint: a unique index is per collection, so global uniqueness needs an extra collection or a sharded check.
- Analytics: aggregations can be slow on huge collections without pre-aggregation, and there is no equivalent of a columnar warehouse.

[Table of Contents](#MongoDB)

## How do you perform migrations from RDBMS to MongoDB?

Migrating from RDBMS to MongoDB typically involves these steps:

1. Analyze the relational schema and design a document model based on the top access patterns, not on the table diagram.
2. Map relational tables to MongoDB collections, deciding what to embed and what to reference.
3. Convert relational data to JSON or BSON, preserving types (decimals as `Decimal128`, timestamps as `Date`).
4. Use tools like mongoimport or write custom scripts to import data, and load in dependency order or in one pass for embedded aggregates.
5. Verify data integrity after migration: counts, checksums, and referential spot checks.
6. Add indexes and validators that mirror the constraints the RDBMS enforced (unique keys, not-null, enums).
7. Update application code to work with MongoDB instead of SQL.
8. Test thoroughly to ensure functionality and performance, then run both systems in parallel before cutover.

Tools that can assist in this process include:

- MongoDB Compass for visualizing and manipulating data.
- MongoDB Relational Migrator for schema mapping and CDC-based cutover.
- Official MongoDB connectors for various programming languages.
- Third-party ETL (Extract, Transform, Load) tools.

```python
# One-shot loader: read relational rows, reshape into documents, bulk insert
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
orders_col = client.shop.orders

# rows come from a SQL query that joins orders and order_items
docs = []
for order_id, customer_id, created_at, items in rows:
    docs.append({
        "_id": order_id,
        "customer_id": customer_id,
        "created_at": created_at,
        "items": [{"sku": s, "qty": q, "price": p} for s, q, p in items],
    })

orders_col.insert_many(docs, ordered=False)
orders_col.create_index([("customer_id", 1), ("created_at", -1)])
```

The risky part is not the copy but the cutover: keep relational IDs as `_id` so references remain stable, run dual writes or CDC, and decide how to handle transactions that spanned several tables.

[Table of Contents](#MongoDB)

## What is MongoDB Atlas and what benefits does it provide?

MongoDB Atlas is the cloud-hosted database-as-a-service (DBaaS) platform for MongoDB. Benefits include:

- Automated deployment and scaling of MongoDB clusters.
- Multi-cloud and multi-region deployment options.
- Built-in security features (network isolation, encryption, access controls).
- Automated backups and point-in-time recovery.
- Performance monitoring and optimization tools, including the Performance Advisor and index suggestions.
- Easy integration with other cloud services.
- Reduced operational overhead for database management.
- Automatic updates and patches for the database software.

Atlas additions that come up in interviews: Atlas Search (Lucene-based full-text and vector search), Atlas Vector Search for RAG applications, Atlas Stream Processing, online archive to move cold data to object storage while keeping it queryable, and the Data API for HTTPS access without a driver.

[Table of Contents](#MongoDB)

## How can you monitor and optimize MongoDB performance?

Monitoring and optimizing MongoDB performance involves several strategies:

##### Monitoring:

- Use MongoDB's built-in tools like mongotop and mongostat
- Leverage MongoDB Compass for visual performance insights
- Implement MongoDB Atlas monitoring for cloud deployments
- Use third-party monitoring tools like Prometheus with MongoDB exporter

##### Optimization:

- Analyze and optimize slow queries using explain() method
- Create appropriate indexes based on query patterns
- Use proper schema design to minimize data duplication
- Configure appropriate write concern and read preferences
- Optimize server and storage configurations (WiredTiger cache, IOPS)
- Use appropriate shard keys for distributed systems

```text
// Find the slowest operations currently in flight
db.adminCommand({ currentOp: true, secs_running: { $gt: 1 } })

// Database profiler: record slow ops, then inspect them
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(5)

// Index usage and per-collection size
db.orders.aggregate([{ $indexStats: {} }])
db.stats()
```

```bash
# Server-level counters and per-collection activity
mongostat --uri="mongodb://localhost:27017" --rowcount=5
mongotop 5
```

Look at disk IOPS and the WiredTiger cache hit ratio before blaming the query: a working set that does not fit in RAM will scan on disk even with a perfect index.

[Table of Contents](#MongoDB)

## What is a replica set in MongoDB and how does it work?

A replica set in MongoDB is a group of mongod processes that maintain the same data set. It provides:

- High Availability: If the primary node fails, an election occurs to choose a new primary from the secondary nodes.
- Data Redundancy: Data is replicated across multiple nodes.
- Read Scaling: Secondary nodes can handle read operations.

How it works:

- One primary node accepts all write operations
- Multiple secondary nodes replicate data from the primary via the oplog
- Optionally, arbiter nodes can participate in elections but don't hold data
- Automatic failover occurs if the primary becomes unavailable

```text
// Inspect and manage a replica set from mongosh
rs.status()
rs.conf()
rs.add("mongo3.example.com:27017")
rs.stepDown(60)                       // hand over the primary deliberately

// Why is this node lagging?
rs.printSecondaryReplicationInfo()
rs.printReplicationInfo()
```

Elections need a majority of voting members, so use an odd number of voters (3 or 5) and never two arbiters in a 3-node set. A replica set does not split data - every member holds the full collection - so it scales reads and availability, not write capacity or dataset size; sharding does that.

[Table of Contents](#MongoDB)

## How do change streams work in MongoDB?

Change streams expose a real-time, resumable stream of data changes (insert, update, replace, delete, and DDL events) without tailing the oplog manually. They require a replica set or a sharded cluster, and every event carries a `resumeToken` so a consumer resumes exactly where it stopped after a crash.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
orders = client.shop.orders

pipeline = [
    {"$match": {"operationType": {"$in": ["insert", "update"]}}},
    {"$project": {"fullDocument": 1, "operationType": 1, "ns": 1}},
]

resume_token = None
while True:
    with orders.watch(pipeline, resume_after=resume_token, full_document="updateLookup") as stream:
        for change in stream:
            resume_token = stream.resume_token
            publish_to_kafka(change["fullDocument"])   # or write to a search index
```

Use cases: syncing to Elasticsearch or a cache, emitting events to Kafka, invalidating application caches, and audit trails. `updateLookup` fetches the current version of the changed document. Oplog/change-stream retention bounds how long a consumer may be offline; if it falls behind the retention window the token is no longer valid and it must resynchronize.

[Table of Contents](#MongoDB)

## How do you handle data integrity in MongoDB?

While MongoDB doesn't have built-in referential integrity like relational databases, you can maintain data integrity through:

- Schema Validation: Define JSON Schema to enforce document structure
- Application-Level Checks: Implement integrity checks in your application code
- Atomic Operations: Use multi-document transactions for operations that must succeed or fail as a unit
- Unique Indexes: Ensure uniqueness of certain fields
- Data Validation: Use $jsonSchema operator to define validation rules
- Consistent Data Modeling: Design schemas to minimize the need for complex integrity constraints

```text
// Uniqueness is an index, not an assumption
db.users.createIndex({ email: 1 }, { unique: true })

// The database rejects the duplicate, so the app must handle the error
try {
  db.users.insertOne({ email: "a@example.com", tier: "pro" })
} catch (e) {
  if (e.code === 11000) {
    // duplicate key: treat as an idempotent upsert
    db.users.updateOne({ email: "a@example.com" }, { $set: { tier: "pro" } })
  } else {
    throw e
  }
}
```

Referential integrity across collections is a trade-off, not a bug: you either pay for transactions on write, or you accept orphan risk and run a periodic reconciliation job. Referential cascade deletes must be implemented by the application or by a change-stream consumer.

[Table of Contents](#MongoDB)

## How does MongoDB fit into the CAP theorem?

The CAP theorem states that a distributed system can only provide two of three guarantees: Consistency, Availability, and Partition tolerance. MongoDB's position in the CAP theorem can be described as:

**Partition Tolerance**: MongoDB is designed to handle network partitions in distributed deployments.
**Consistency vs. Availability**: MongoDB allows you to tune the balance between consistency and availability:

With default settings, MongoDB leans towards **CP** (Consistency and Partition Tolerance)
By adjusting write concern and read preferences, you can shift towards **AP** (Availability and Partition Tolerance)

In practice:

- For strong consistency, use majority write concern and read preference
- For higher availability at the cost of potential inconsistency, use lower write concerns or read from secondaries

```text
// CP-leaning read after a majority write: never see rolled-back data
db.orders.insertOne({ _id: "order_1004", total: 10 }, { writeConcern: { w: "majority" } })
db.orders.find({ _id: "order_1004" }).readConcern("majority").readPref("primary")

// AP-leaning: fastest available node, possibly stale by a few milliseconds
db.orders.find({ _id: "order_1004" }).readPref("nearest", [{ dc: "dfw" }])
```

Nuance worth stating: a partition that removes the majority of voters makes a replica set unavailable for writes (no primary can be elected) even though minority nodes still answer reads. That is a CP choice. Setting `w: 1` and reading secondaries shifts the same deployment toward availability at the cost of possible rollback visibility.

[Table of Contents](#MongoDB)

## How do you handle large data volumes in MongoDB?

MongoDB offers several strategies for handling large data volumes:

- Sharding: Distribute data across multiple machines to handle large datasets and high throughput operations.
- Indexing: Create appropriate indexes to improve query performance on large collections.
- Aggregation Pipeline: Use for efficient data processing and analysis on large datasets, with `$merge` to maintain pre-aggregated rollups.
- GridFS: Store and retrieve large files (above 16 MB) by chunking them across two collections.
- Data Compression: WiredTiger storage engine provides data compression to reduce storage requirements.
- Capped Collections: Use for high-volume data that doesn't require long-term storage (legacy; time series collections are usually better).
- Time Series Collections: Optimize storage and querying for time series data.
- TTL indexes: Expire documents automatically so the hot set stays small.
- Online archive: Atlas moves cold documents to S3 while leaving them queryable.

```text
// Time series collection with automatic expiry
db.createCollection("sensor_readings", {
  timeseries: {
    timeField: "ts",
    metaField: "sensor",
    granularity: "minutes"
  },
  expireAfterSeconds: 7776000      // 90 days
})

// Bucket pattern: one document per device per hour instead of one per reading
db.readings_bucketed.updateOne(
  { sensor_id: "s-1", hour: ISODate("2026-10-04T10:00:00Z") },
  {
    $push: { samples: { $each: [{ ts: new Date(), v: 21.7 }], $slice: -3600 } },
    $inc: { count: 1 },
    $setOnInsert: { sensor_id: "s-1" }
  },
  { upsert: true }
)
```

The decision framework: reduce (TTL, rollups), then split (bucket pattern, time series collections), then distribute (sharding). Archiving to cheaper storage is often cheaper than growing the cluster.

[Table of Contents](#MongoDB)

## What are the best practices for designing a MongoDB schema?

Key best practices for MongoDB schema design include:

- Embed related data in a single document when possible for faster reads.
- Use references when data is used in multiple places or for very large datasets.
- Design schema based on application query patterns, not on entity-relationship purity.
- Avoid deeply nested documents (keep nesting to 2-3 levels for better performance).
- Use appropriate data types for fields (`Decimal128` for money, `Date` for time, `ObjectId` for IDs).
- Create indexes to support common queries and verify them with `explain`.
- Consider document growth when designing schemas; never let an array grow unboundedly.
- Use schema versioning for easier updates and migrations.
- Normalize data only when necessary (e.g., for data consistency across multiple collections).
- Use array fields for one-to-many relationships within reasonable limits.
- Enforce the invariants you cannot live without with `$jsonSchema` and unique indexes.
- Store the field names you query on; long, deeply repeated field names cost bytes on every document.

[Table of Contents](#MongoDB)

## How does MongoDB handle geographic data and geospatial queries?

MongoDB provides robust support for geographic data and geospatial queries:

- Geospatial Indexes: Support for 2d and 2dsphere indexes for efficient geospatial queries.
- GeoJSON Objects: Store location data using standard GeoJSON format.
- Geospatial Queries: Support for various types of geospatial queries:
  - Proximity: Find documents near a point.
  - Intersection: Find geometries that intersect with a specified geometry.
  - Within: Find geometries contained within a specified geometry.
- Aggregation Pipeline: Geospatial stages like $geoNear for complex geo-based analytics.
- Coordinate Systems: Support for both legacy coordinate pairs and GeoJSON objects.
- Geospatial Operators: $near, $geoWithin, $geoIntersects, etc., for flexible querying.
- Spherical Geometry: 2dsphere index supports queries on an Earth-like sphere.

```text
db.stores.createIndex({ location: "2dsphere" })

// Stores within 2 km of the customer, nearest first
db.stores.find({
  location: {
    $near: {
      $geometry: { type: "Point", coordinates: [-96.7970, 32.7767] },
      $maxDistance: 2000
    }
  }
}).limit(10)

// Aggregation form, useful for adding distance to the output
db.stores.aggregate([
  { $geoNear: {
      near: { type: "Point", coordinates: [-96.7970, 32.7767] },
      distanceField: "distance_m",
      spherical: true,
      maxDistance: 2000
  } },
  { $match: { open: true } },
  { $project: { name: 1, distance_m: 1 } }
])
```

GeoJSON coordinates are `[longitude, latitude]` - reversing them is the classic bug. A `2dsphere` index also supports `$geoWithin` (for example, stores inside a delivery polygon) and `$geoIntersects` (which zones a route crosses).

[Table of Contents](#MongoDB)

## What are the trade-offs and when should you not use MongoDB?

- Consistency vs availability: `w: "majority"` plus `readConcern: "majority"` is durable and rollback-safe, but each write waits for a majority round trip and the cluster refuses writes if it loses the majority. `w: 1` with secondary reads is faster and more available, but a failover can roll writes back and replicas can be stale.
- Write amplification: every secondary index must be updated on every write, and a multikey index is updated once per array element. A collection with 12 indexes turns one insert into 13 index writes; on write-heavy workloads, indexes are often the bottleneck, not the disk.
- Hot partitions and hot shards: a monotonically increasing shard key (timestamp, ObjectId) concentrates writes in the last chunk; a low-cardinality key (status, country) creates chunks that cannot split. Hashed sharding spreads writes but makes range queries scatter-gather.
- Document growth and the 16 MB limit: unbounded `$push` arrays cause rewrites and eventually hard failures. Cap arrays with `$slice`, or move children into their own collection.
- Memory pressure: index and working-set size must fit in RAM. Once the WiredTiger cache is exhausted, `IXSCAN` still reads from disk and latency jumps even though the plan looks correct.
- Weak analytics: no cost-based join planner, no columnar execution. If the workload is mostly arbitrary ad-hoc joins and aggregations across many entities, a warehouse or a relational database is the better home for it.
- When NOT to use MongoDB: strictly relational, constraint-heavy transactional systems (banking cores, double-entry ledgers needing foreign keys and multi-table ACID by default); heavy OLAP/BI with star-schema joins; workloads requiring cross-collection uniqueness or complex cascading deletes; teams without the operational maturity to run replica sets and sharding; and any case where a small relational database with a handful of tables would simply work.

[Table of Contents](#MongoDB)

## Real world use cases for MongoDB

### 1. E-commerce product catalog

Business context: a marketplace with 8 million SKUs, each category having different attributes (clothes have sizes and colors, electronics have voltage and warranty). Volume: ~8M products, ~25M variants, read-heavy at roughly 50:1 reads to writes, 3,000 reads/s at peak. Access patterns: fetch one product page with all variants and images, search by category and tags, update price and stock frequently.

Schema design: one document per product embedding variants and a bounded image list; references to a `categories` collection so category metadata is not duplicated 8M times. A `2dsphere` index is not needed; a compound index on `{ category_id: 1, updated_at: -1 }` serves category browsing.

```text
db.products.insertOne({
  _id: "sku-1001",
  name: "Espresso Machine",
  category_id: "cat-kitchen",
  attributes: { voltage: "110V", warranty_months: 24 },
  tags: ["coffee", "kitchen"],
  variants: [
    { sku: "sku-1001-black", color: "black", price: NumberDecimal("249.00"), stock: 12 },
    { sku: "sku-1001-steel", color: "steel", price: NumberDecimal("269.00"), stock: 3 }
  ],
  updated_at: new Date()
})

db.products.createIndex({ category_id: 1, updated_at: -1 })
db.products.createIndex({ tags: 1, "attributes.voltage": 1 })
```

Why this design: the product page is a single-document read, and `variants` is bounded (a few dozen at most), so embedding wins. The heterogeneous `attributes` object is exactly the flexible-schema case a relational catalog needs EAV tables for.

### 2. IoT time series with automatic expiry

Business context: 40,000 sensors reporting every 10 seconds (about 345M readings/day, tens of billions over the retention window). Access patterns: dashboards read one sensor for the last 24 hours, rarely query across all sensors; older than 90 days is discarded.

Schema design: a time series collection with `metaField` on the sensor and a TTL, or the bucket pattern (one document per sensor per hour) when you need sub-document updates.

```text
db.createCollection("sensor_readings", {
  timeseries: { timeField: "ts", metaField: "sensor", granularity: "seconds" },
  expireAfterSeconds: 7776000
})

// Dashboard: one sensor, last 24 hours, downsampled to 5-minute averages
db.sensor_readings.aggregate([
  { $match: {
      "sensor.id": "s-1042",
      ts: { $gte: new Date(Date.now() - 24 * 3600 * 1000) }
  } },
  { $group: {
      _id: { $dateTrunc: { date: "$ts", unit: "minute", binSize: 5 } },
      avg_v: { $avg: "$v" }, max_v: { $max: "$v" }
  } },
  { $sort: { "_id": 1 } }
])
```

Why this design: time series collections store measurements columnar-ish by bucket internally, compress well, and TTL removes expired data without a delete job. Sharding uses `{ sensor.id: "hashed" }` or a compound `{ "sensor.id": 1, ts: 1 }` so writes spread across shards while a single-sensor range query stays targeted.

### 3. User activity feed

Business context: a social app with 50M users; the timeline of a user with 5,000 followers must load in under 100 ms. Access patterns: read the newest 50 items for one user, append new items at high rate, keep only the last few hundred items.

Schema design: fan-out on write into a per-user feed document that keeps a bounded array using `$push` with `$slice`; if a user's feed can exceed a few thousand items, use a dedicated `feed_items` collection keyed by `{ user_id, created_at }`.

```text
// Bounded timeline inside one document
db.timelines.updateOne(
  { _id: "user-42" },
  {
    $push: {
      items: {
        $each: [{ actor: "user-7", verb: "liked", ts: new Date() }],
        $position: 0,
        $slice: 500
      }
    }
  },
  { upsert: true }
)

// Large feeds: one row per item + range query
db.feed_items.insertOne({ user_id: "user-42", ts: new Date(), actor: "user-7", verb: "liked" })
db.feed_items.createIndex({ user_id: 1, ts: -1 })
db.feed_items.find({ user_id: "user-42" }).sort({ ts: -1 }).limit(50)
```

Why this design: reads dominate, so precomputing the feed on write (`$push` with `$slice`) removes the read-time fan-out entirely. For celebrities whose feeds would exceed 16 MB, the separate collection with a compound index keeps documents bounded and lets a shard key of `{ user_id: 1 }` localize each feed.

### 4. Fintech ledger and idempotent payments

Business context: a payments API writing double-entry ledger entries and transferring funds between accounts. Volume: ~5M transactions/day, strict correctness, auditable history. Access patterns: look up a transaction by idempotency key, list the last 100 entries for an account, move money between two accounts atomically.

Schema design: `accounts` and `ledger_entries` collections; a unique index on the idempotency key so a retried request cannot double-post; a multi-document transaction for the transfer; `w: "majority"` everywhere.

```python
from pymongo import MongoClient, ReturnDocument

client = MongoClient("mongodb://localhost:27017/?replicaSet=rs0")
db = client.ledger
db.payments.create_index("idempotency_key", unique=True)

with client.start_session() as session:
    with session.start_transaction(
        read_concern={"level": "snapshot"},
        write_concern={"w": "majority"},
    ):
        db.payments.insert_one(
            {"idempotency_key": "req-7f3a", "status": "posted", "amount": 5000},
            session=session,
        )
        db.accounts.update_one(
            {"_id": "acct-1"}, {"$inc": {"balance": -5000}}, session=session
        )
        db.accounts.update_one(
            {"_id": "acct-2"}, {"$inc": {"balance": 5000}}, session=session
        )
        db.ledger_entries.insert_many(
            [
                {"account_id": "acct-1", "amount": -5000, "ref": "req-7f3a"},
                {"account_id": "acct-2", "amount": 5000, "ref": "req-7f3a"},
            ],
            session=session,
        )
```

Why this design: `$inc` is atomic and the unique idempotency index makes retries safe; the transaction spans collections only because the accounting invariant demands it. Replicas give durability, and change streams feed the downstream audit and reporting systems.

### 5. Multi-tenant SaaS

Business context: a B2B platform with 2,000 tenants and wildly different data volumes (one tenant is 30% of all rows). Volume: 900M documents, retention differs per tenant. Access patterns: every query is scoped to one tenant; schema varies slightly per tenant plan; older data expires after the contract ends.

Schema design: a shared collection with `tenant_id` in every document and in the leading position of every index; per-tenant `$jsonSchema` variants are avoided in favor of a superset validator plus optional fields; TTL or archival per tenant.

```text
// Every index leads with tenant_id so reads are always targeted
db.tickets.createIndex({ tenant_id: 1, status: 1, created_at: -1 })

// Shard on the tenant so one big tenant cannot hotspot a single chunk range
sh.shardCollection("saas.tickets", { tenant_id: "hashed" })

// Tenant-scoped query
db.tickets.find({ tenant_id: "t-88", status: "open" }).sort({ created_at: -1 }).limit(20)
```

Why this design: a shared collection with a tenant prefix is the cheapest multi-tenant model and makes isolation a matter of discipline plus a mandatory index prefix. Truly regulated or enormous tenants can be moved to their own database and cluster without changing the application's tenant-scoped access pattern.

[Table of Contents](#MongoDB)
