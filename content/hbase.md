## [Main title](../README.md)
### [Interview questions](full.md)

# Apache HBase

Apache HBase is a distributed, scalable, wide-column NoSQL store modeled on Google Bigtable and built on top of HDFS. It gives random, real-time reads and writes by row key over tables with billions of rows and millions of columns, while HDFS provides the durable storage underneath.

```text
client -> ZooKeeper (who is the master, where is hbase:meta)
       -> RegionServer -> region -> MemStore + WAL + HFiles on HDFS
```

Key ideas:

+ Rows are sorted lexicographically by row key and split into regions; a region is the unit of distribution, not a table.
+ A column family is the physical storage and tuning unit; column qualifiers inside it are fully dynamic.
+ Writes land in the write-ahead log (WAL) and the in-memory MemStore, and are flushed to immutable HFiles later.
+ Reads check the MemStore and block cache, then the HFiles; tombstones hide deletes until compaction removes them.
+ HBase is optimized for key-based access and scans, not for joins, ad-hoc SQL analytics, or multi-row transactions across tables.

+ [How do you design an HBase row key?](#How-do-you-design-an-HBase-row-key)
+ [When should you use HBase?](#When-should-you-use-HBase)
+ [How do you create and query tables in the HBase shell?](#How-do-you-create-and-query-tables-in-the-HBase-shell)
+ [How do you configure an HBase cluster with hbase-site.xml?](#How-do-you-configure-an-HBase-cluster-with-hbase-sitexml)
+ [How do you read and write data with the HBase Java client?](#How-do-you-read-and-write-data-with-the-HBase-Java-client)
+ [How do you use HBase from Python with HappyBase?](#How-do-you-use-HBase-from-Python-with-HappyBase)
+ [How do you query HBase with Apache Phoenix SQL?](#How-do-you-query-HBase-with-Apache-Phoenix-SQL)
+ [What are the differences between RDBMS and HBase data model?](#What-are-the-differences-between-RDBMS-and-HBase-data-model)
+ [Explain what is HBase?](#Explain-what-is-HBase)
+ [Explain why to use HBase?](#Explain-why-to-use-HBase)
+ [Mention what are the key components of HBase?](#Mention-what-are-the-key-components-of-HBase)
+ [Explain what does HBase consists of?](#Explain-what-does-HBase-consists-of)
+ [Mention how many operational commands in HBase?](#Mention-how-many-operational-commands-in-HBase)
+ [Explain what is WAL and HLog in HBase?](#Explain-what-is-WAL-and-HLog-in-HBase)
+ [When you should use HBase?](#When-you-should-use-HBase)
+ [In HBase what is column families?](#In-HBase-what-is-column-families)
+ [Explain what is the row key?](#Explain-what-is-the-row-key)
+ [Explain deletion in HBase? Mention what are the three types of tombstone markers in HBase?](#Explain-deletion-in-HBase-Mention-what-are-the-three-types-of-tombstone-markers-in-HBase)
+ [Explain how does HBase actually delete a row?](#Explain-how-does-HBase-actually-delete-a-row)
+ [Explain what happens if you alter the block size of a column family on an already occupied database?](#Explain-what-happens-if-you-alter-the-block-size-of-a-column-family-on-an-already-occupied-database)
+ [Mention the difference between HBase and Relational Database?](#Mention-the-difference-between-HBase-and-Relational-Database)
+ [What is HBaseFsck class?](#What-is-HBaseFsck-class)
+ [What are the main key structures of HBase?](#What-are-the-main-key-structures-of-HBase)
+ [Discuss how you can use filters in Apache HBase](#Discuss-how-you-can-use-filters-in-Apache-HBase)
+ [HBase support syntax structure like SQL yes or No?](#HBase-support-syntax-structure-like-SQL-yes-or-No)
+ [What is the meaning of compaction in HBase?](#What-is-the-meaning-of-compaction-in-HBase)
+ [How will you implement joins in HBase?](#How-will-you-implement-joins-in-HBase)
+ [Explain JMX concerning HBase](#Explain-JMX-concerning-HBase)
+ [What is the use of MasterServer?](#What-is-the-use-of-MasterServer)
+ [Define the Term Thrift.](#Define-the-Term-Thrift)
+ [Why use HColumnDescriptor class?](#Why-use-HColumnDescriptor-class)
+ [What is a cell in HBase?](#What-is-a-cell-in-HBase)
+ [What is a Bloom filter?](#What-is-a-Bloom-filter)
+ [Tell me about the types of HBase Operations?](#Tell-me-about-the-types-of-HBase-Operations)
+ [What is the use of HBase HMaster?](#What-is-the-use-of-HBase-HMaster)
+ [Which technique can you use in HBase to access HFile directly without the help of HBase?](#Which-technique-can-you-use-in-HBase-to-access-HFile-directly-without-the-help-of-HBase)
+ [Can the region server will be located on all DataNodes?](#Can-the-region-server-will-be-located-on-all-DataNodes)
+ [Name the filter which accepts the page size as the parameter in HBase?](#Name-the-filter-which-accepts-the-page-size-as-the-parameter-in-HBase)
+ [When would you use HBase?](#When-would-you-use-HBase)
+ [What is the use of get method?](#What-is-the-use-of-get-method)
+ [Define the difference between Hive and HBase?](#Define-the-difference-between-Hive-and-HBase)
+ [Explain the data model of HBase.](#Explain-the-data-model-of-HBase)
+ [Define column families?](#Define-column-families)
+ [Define standalone mode in HBase?](#Define-standalone-mode-in-HBase)
+ [What is decorating Filters?](#What-is-decorating-Filters)
+ [What is RegionServer?](#What-is-RegionServer)
+ [What are the data manipulation commands of HBase?](#What-are-the-data-manipulation-commands-of-HBase)
+ [What happens when you issue a delete command in HBase?](#What-happens-when-you-issue-a-delete-command-in-HBase)
+ [What are different tombstone markers in HBase?](#What-are-different-tombstone-markers-in-HBase)
+ [HBase blocksize is configured on which level?](#HBase-blocksize-is-configured-on-which-level)
+ [Which command is used to run HBase Shell?](#Which-command-is-used-to-run-HBase-Shell)
+ [Which command is used to show the current HBase user?](#Which-command-is-used-to-show-the-current-HBase-user)
+ [What is the full form of MSLAB?](#What-is-the-full-form-of-MSLAB)
+ [Define LZO?](#Define-LZO)
+ [What is HBase Fsck?](#What-is-HBase-Fsck)
+ [What is REST?](#What-is-REST)
+ [What is Nagios?](#What-is-Nagios)
+ [What is the use of ZooKeeper?](#What-is-the-use-of-ZooKeeper)
+ [Define catalog tables in HBase?](#Define-catalog-tables-in-HBase)
+ [Define compaction in HBase?](#Define-compaction-in-HBase)
+ [Explain what is HBase?](#Explain-what-is-HBase-1)
+ [Explain why to use HBase?](#Explain-why-to-use-HBase-1)
+ [Mention what are Key Components of HBase?](#Mention-what-are-Key-Components-of-HBase)
+ [What is the Role of Master Server in HBase?](#What-is-the-Role-of-Master-Server-in-HBase)
+ [Explain what does HBase consists of?](#Explain-what-does-HBase-consists-of-1)
+ [What is the Role of ZooKeeper in HBase?](#What-is-the-Role-of-ZooKeeper-in-HBase)
+ [Mention how many operational commands in HBase?](#Mention-how-many-operational-commands-in-HBase-1)
+ [When do we need to disable a table in HBase?](#When-do-we-need-to-disable-a-table-in-HBase)
+ [Explain what is WAL and HLog in HBase?](#Explain-what-is-WAL-and-HLog-in-HBase-1)
+ [What are the different Types of Filters used in HBase?](#What-are-the-different-Types-of-Filters-used-in-HBase)
+ [In HBase what is Column Families?](#In-HBase-what-is-Column-Families)
+ [Name three disadvantages HBase has as compared to RDBMS?](#Name-three-disadvantages-HBase-has-as-compared-to-RDBMS)
+ [Explain what is the Row Key?](#Explain-what-is-the-Row-Key)
+ [Is HBase a scale out or scale up process?](#Is-HBase-a-scale-out-or-scale-up-process)
+ [Explain deletion in HBase?](#Explain-deletion-in-HBase)
+ [What are the step in writing something into Hbase by a Client?](#What-are-the-step-in-writing-something-into-Hbase-by-a-Client)
+ [Explain how does Hbase actually delete a Row?](#Explain-how-does-Hbase-actually-delete-a-Row)
+ [What is compaction in Hbase?](#What-is-compaction-in-Hbase)
+ [Explain what happens if you alter the Block Size of a column Family on an already occupied Database?](#Explain-what-happens-if-you-alter-the-Block-Size-of-a-column-Family-on-an-already-occupied-Database)
+ [What are the different compaction types in Hbase?](#What-are-the-different-compaction-types-in-Hbase)
+ [What is a Cell in Hbase?](#What-is-a-Cell-in-Hbase)
+ [What is the Scope of a Rowkey in Hbase?](#What-is-the-Scope-of-a-Rowkey-in-Hbase)
+ [What is the Role of the Class Hcolumndescriptor in Hbase?](#What-is-the-Role-of-the-Class-Hcolumndescriptor-in-Hbase)
+ [What is a Namespace in Hbase?](#What-is-a-Namespace-in-Hbase)
+ [What is the Lower Bound of Versions in Hbase?](#What-is-the-Lower-Bound-of-Versions-in-Hbase)
+ [What is Hotspotting in Hbase?](#What-is-Hotspotting-in-Hbase)
+ [What is Ttl in Hbase?](#What-is-Ttl-in-Hbase)
+ [Why do we Pre create empty Regions?](#Why-do-we-Pre-create-empty-Regions)
+ [Does Hbase support Table Joins?](#Does-Hbase-support-Table-Joins)
+ [Which File in Hbase is designed after Sstable File of Bigtable?](#Which-File-in-Hbase-is-designed-after-Sstable-File-of-Bigtable)
+ [What is a Hbase Store?](#What-is-a-Hbase-Store)
+ [What are the Two Types of Table Design Approach in Hbase?](#What-are-the-Two-Types-of-Table-Design-Approach-in-Hbase)
+ [When do we do Manual Region Splitting?](#When-do-we-do-Manual-Region-Splitting)
+ [In which scenario should we consider creating a short and wide Hbase Table?](#In-which-scenario-should-we-consider-creating-a-short-and-wide-Hbase-Table)
+ [In Hbase what is Log Splitting?](#In-Hbase-what-is-Log-Splitting)
+ [How does Hbase support Bulk Data Loading?](#How-does-Hbase-support-Bulk-Data-Loading)
+ [Why MultiWAL is Needed?](#Why-MultiWAL-is-Needed)
+ [How does Hbase provide High Availability?](#How-does-Hbase-provide-High-Availability)
+ [How does Wal help when a Regionserver Crashes?](#How-does-Wal-help-when-a-Regionserver-Crashes)
+ [What is Hregionserver in Hbase?](#What-is-Hregionserver-in-Hbase)
+ [What are the different Block Caches in Hbase?](#What-are-the-different-Block-Caches-in-Hbase)
+ [How do you manage compactions and region splits?](#How-do-you-manage-compactions-and-region-splits)
+ [When should you not use HBase, and what should you use instead?](#When-should-you-not-use-HBase-and-what-should-you-use-instead)
+ [Real world use cases for HBase](#Real-world-use-cases-for-HBase)

## How do you design an HBase row key?
An HBase row key should support the main lookup pattern and avoid region hotspotting. Because rows are sorted by key and a region serves a contiguous key range, monotonically increasing keys (timestamps, sequential ids) overload the last region. Use salting, hashing, bucketing, or reversed timestamps to spread writes.

Common patterns:

| Access pattern | Row key design |
|---|---|
| latest events for a user | `user_id + reverse_timestamp` |
| devices by tenant | `salt + tenant_id + device_id` |
| time-range scans, spread writes | `salt + reverse_timestamp + id` |
| lookup by many secondary keys | separate index/lookup table keyed by the secondary key |
| natural unique id | hash(id) or a fixed-width, zero-padded id |

```text
raw row key:        device-0001|2026-10-04T13:20:00Z
salted row key:     07|device-0001|2026-10-04T13:20:00Z   (salt = hash(device_id) % 16)
bucketed row key:   device-0001|bkt-3|1700000000000
reversed timestamp: device-0001|9999999999999-1700000000000
```

```python
# Build a salted, reverse-timestamp row key for recent-first lookups
import hashlib

def rowkey(device_id: str, ts_ms: int, buckets: int = 16) -> str:
    salt = int(hashlib.md5(device_id.encode()).hexdigest(), 16) % buckets
    reverse_ts = 9_999_999_999_999 - ts_ms
    return f"{salt:02d}|{device_id}|{reverse_ts:013d}"
```

The trade-off: reads for one device must query every salt bucket (or you scan all prefixes) unless the salt is derivable from the query. Salting spreads writes but fans out reads; reverse timestamps give newest-first scans for a known prefix.

[Table of Contents](#Apache-HBase)

## When should you use HBase?
Use HBase for sparse, wide, high-scale tables that need random reads/writes by key over large datasets. It fits operational lookups, time-series style access, and serving stores behind an application. It is not ideal for ad-hoc SQL analytics, joins, or full table scans.

Example:

+ good: get the latest 100 events for a device id
+ poor: calculate total revenue by region across all history

Analytics usually belongs in Hive, Spark, Impala, or a warehouse, while HBase serves key-based access. A common pattern is to serve from HBase and run analytics on the same data copied to Parquet or Iceberg.

[Table of Contents](#Apache-HBase)

## How do you create and query tables in the HBase shell?
The HBase shell is a JRuby REPL that talks to the cluster for DDL and DML. Namespaces, tables, and column families are created here; `disable` is required before changing a table.

```bash
hbase shell
```

```bash
# Namespace and table DDL: TTL, versions, block size, and Bloom filter per column family
create_namespace 'app'
create 'app:impressions', {NAME => 'i', VERSIONS => 1, TTL => 7776000, BLOOMFILTER => 'ROWCOL', BLOCKSIZE => 65536}
describe 'app:impressions'

# Add a column family to an existing table
disable 'app:impressions'
alter 'app:impressions', {NAME => 'meta', VERSIONS => 3}
enable 'app:impressions'
```

```bash
# DML: put, get, scan, increment, delete, count
put 'app:impressions', 'u42|9999999999999-1700000000000|a1', 'i:campaign_id', 'cmp-99'
put 'app:impressions', 'u42|9999999999999-1700000000000|a1', 'i:amount', '42.10'
get 'app:impressions', 'u42|9999999999999-1700000000000|a1'
scan 'app:impressions', {STARTROW => 'u42|', ENDROW => 'u42|\xff', LIMIT => 5}
incr 'app:counters', 'daily|2026-10-04', 'c:impressions', 1
delete 'app:impressions', 'u42|9999999999999-1700000000000|a1', 'i:amount'
count 'app:impressions'
```

```bash
# Table maintenance and reporting
status 'detailed'
list_regions 'app:impressions'
flush 'app:impressions'
major_compact 'app:impressions'
```

[Table of Contents](#Apache-HBase)

## How do you configure an HBase cluster with hbase-site.xml?
`hbase-site.xml` holds cluster-wide settings; the most important ones control durability, write throughput, and MemStore sizing. The pattern is one `property` block per setting.

```xml
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://nn.example.com:8020/hbase</value>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>zk1.example.com,zk2.example.com,zk3.example.com</value>
  </property>
  <property>
    <name>hbase.regionserver.handler.count</name>
    <value>60</value>
  </property>
  <property>
    <name>hbase.regionserver.global.memstore.size</name>
    <value>0.4</value>
  </property>
  <property>
    <name>hbase.hregion.memstore.flush.size</name>
    <value>134217728</value>
  </property>
  <property>
    <name>hbase.hregion.max.filesize</name>
    <value>10737418240</value>
  </property>
  <property>
    <name>hbase.hstore.blockingStoreFiles</name>
    <value>16</value>
  </property>
  <property>
    <name>hbase.wal.provider</name>
    <value>filesystem</value>
  </property>
  <property>
    <name>hbase.hregion.memstore.mslab.enabled</name>
    <value>true</value>
  </property>
</configuration>
```

Tuning notes:

+ `hbase.regionserver.global.memstore.size = 0.4` caps total MemStore memory at 40% of heap; the rest serves the block cache and reads.
+ Lower `hbase.hregion.memstore.flush.size` when write bursts are spiky; larger values reduce flush frequency but increase heap pressure.
+ `hbase.hregion.max.filesize` controls when a region splits; 10 GB is a common production value.
+ `hbase.hstore.blockingStoreFiles` makes the RegionServer block writes when too many store files pile up, which pushes back on the client instead of failing.

[Table of Contents](#Apache-HBase)

## How do you read and write data with the HBase Java client?
The Java client is the canonical API. Create the `Connection` once per process and reuse it; `Table` and `Admin` are cheap to obtain from it. Batch and async paths are used for high throughput.

```java
Configuration conf = HBaseConfiguration.create();
conf.set("hbase.zookeeper.quorum", "zk1,zk2,zk3");

try (Connection conn = ConnectionFactory.createConnection(conf);
     Table table = conn.getTable(TableName.valueOf("app:impressions"))) {

    // Write a cell
    Put put = new Put(Bytes.toBytes("u42|9999999999999-1700000000000|a1"));
    put.addColumn(Bytes.toBytes("i"), Bytes.toBytes("campaign_id"), Bytes.toBytes("cmp-99"));
    put.addColumn(Bytes.toBytes("i"), Bytes.toBytes("amount"), Bytes.toBytes("42.10"));
    table.put(put);

    // Point read with an explicit column selection
    Get get = new Get(Bytes.toBytes("u42|9999999999999-1700000000000|a1"));
    get.addColumn(Bytes.toBytes("i"), Bytes.toBytes("campaign_id"));
    Result result = table.get(get);
    byte[] campaign = result.getValue(Bytes.toBytes("i"), Bytes.toBytes("campaign_id"));

    // Prefix scan limited to 100 rows
    Scan scan = new Scan()
        .withStartRow(Bytes.toBytes("u42|"))
        .withStopRow(Bytes.toBytes("u42|\uFFFF".getBytes()))
        .setLimit(100)
        .setCaching(200);
    try (ResultScanner scanner = table.getScanner(scan)) {
        for (Result row : scanner) {
            System.out.println(Bytes.toString(row.getRow()));
        }
    }
}
```

Rules that matter under load: never build a `Connection` per request, set `Scan.setCaching` (rows per RPC) and `setBatch` (cells per RPC), keep row keys short, and prefer `BufferedMutator` over many single `put` calls.

[Table of Contents](#Apache-HBase)

## How do you use HBase from Python with HappyBase?
HappyBase talks to the Thrift gateway (`hbase-daemon.sh start thrift`). It is convenient for services and scripts, but the Thrift gateway is an extra hop compared with the native Java API.

```python
import happybase

connection = happybase.Connection("hbase-thrift.example.com", port=9090)
table = connection.table("app:impressions")

# Put a row
table.put(
    b"u42|9999999999999-1700000000000|a1",
    {b"i:campaign_id": b"cmp-99", b"i:amount": b"42.10"},
)

# Point read
row = table.row(b"u42|9999999999999-1700000000000|a1")
print(row.get(b"i:campaign_id"))

# Prefix scan for the most recent impressions of a user
for key, data in table.scan(row_prefix=b"u42|", limit=10):
    print(key, data)

# Atomic counter
counters = connection.table("app:counters")
counters.counter_inc(b"daily|2026-10-04", b"c:impressions", 1)

connection.close()
```

Use `happybase.ConnectionPool` in a web service so connections are reused, and keep the Thrift server close to the RegionServers to avoid an extra network round trip per scan.

[Table of Contents](#Apache-HBase)

## How do you query HBase with Apache Phoenix SQL?
Phoenix adds a SQL layer over HBase: it compiles SQL to HBase scans, maintains secondary indexes in HBase tables, and gives JDBC access. The row key is still the primary key, and the primary key order defines the physical sort order.

```sql
-- Primary key maps to the HBase row key; the leading columns drive the scan
CREATE TABLE IF NOT EXISTS impressions (
    user_id   VARCHAR NOT NULL,
    ts        TIMESTAMP NOT NULL,
    campaign  VARCHAR,
    amount    DECIMAL(10,2),
    CONSTRAINT pk PRIMARY KEY (user_id, ts DESC)
);

UPSERT INTO impressions (user_id, ts, campaign, amount)
VALUES ('u42', CURRENT_TIME(), 'cmp-99', 42.10);

-- Secondary index for queries that do not lead with the primary key
CREATE INDEX impressions_campaign_idx ON impressions (campaign);

SELECT campaign, COUNT(*), SUM(amount)
FROM impressions
WHERE user_id = 'u42'
GROUP BY campaign;
```

Phoenix is the right answer when interviewers ask "does HBase support SQL?" - **not natively, but Phoenix provides it**. Beware that a Phoenix query that does not lead with the primary key may fall back to a full scan unless a secondary index exists.

[Table of Contents](#Apache-HBase)

## What are the differences between RDBMS and HBase data model?
Schema: RDBMS defines tables and typed columns up front. HBase defines tables and column families, but column qualifiers inside a family are dynamic and untyped (everything is bytes), so the schema is much looser.

Normalization: an RDBMS is normalized; HBase is deliberately denormalized and stores wide, sparse rows.

Partitioning: an RDBMS requires manual partitioning and sharding. HBase splits a table into regions automatically as it grows, and can be pre-split manually.

Other differences: RDBMS supports joins, multi-row transactions, and SQL; HBase supports single-row atomicity, no joins, and no server-side SQL without Phoenix. HBase tables are sparse - a row only stores the cells that exist.

[Table of Contents](#Apache-HBase)

## Explain what is HBase?
HBase is a wide-column, non-relational database management system that runs on top of HDFS. It is not a relational store and does not support SQL natively (Phoenix adds a SQL layer). A master node regulates the cluster and RegionServers store portions of the tables and serve reads and writes.

HBase is often loosely called "column-oriented", but the precise term is wide-column or column-family oriented: cells are grouped and stored by column family, unlike a true columnar format such as Parquet where each column is stored separately for analytics.

[Table of Contents](#Apache-HBase)

## Explain why to use HBase?
+ High-capacity storage system that scales to billions of rows and millions of columns.
+ Distributed design to cater to very large tables.
+ Column-family-oriented storage with dynamic qualifiers.
+ Horizontally scalable by adding RegionServers.
+ High performance and availability through region replication, WAL, and multiple masters.
+ The design goal is millions of columns, thousands of versions, and billions of rows.
+ Unlike HDFS alone, it supports random real-time CRUD operations.

[Table of Contents](#Apache-HBase)

## Mention what are the key components of HBase?
+ ZooKeeper: coordinates the cluster, holds the `hbase:meta` location and master election.
+ HBase Master (HMaster): assigns regions, balances load, and performs admin operations.
+ RegionServer: serves regions and handles reads, writes, and flushes.
+ Region: a contiguous range of a table's rows, containing a MemStore and HFiles.
+ Catalog tables: `hbase:meta` maps regions to RegionServers (the older `-ROOT-` table is gone in modern HBase).
+ HDFS: durable storage for WALs and HFiles.

[Table of Contents](#Apache-HBase)

## Explain what does HBase consists of?
HBase consists of a set of tables. Each table contains rows and columns like a traditional database, but a row is identified by a unique row key and columns are grouped into column families. Cells hold multiple versions of a value with timestamps, and a column qualifier denotes an attribute of the object stored in the row.

[Table of Contents](#Apache-HBase)

## Mention how many operational commands in HBase?
The core data operations are five: Get, Put, Delete, Scan, and Increment. Around them sit admin operations such as Create, Disable/Enable, Alter, Drop, Truncate, Split, Merge, Flush, and Compact.

```bash
# One of each core operation in the shell
put 'app:impressions', 'u42|1', 'i:campaign', 'cmp-99'
get 'app:impressions', 'u42|1'
scan 'app:impressions', {LIMIT => 10}
incr 'app:counters', 'daily|2026-10-04', 'c:impressions', 1
delete 'app:impressions', 'u42|1', 'i:campaign'
```

[Table of Contents](#Apache-HBase)

## Explain what is WAL and HLog in HBase?
The WAL (Write-Ahead Log), historically called HLog, records every mutation before it is applied to memory. It is a Hadoop sequence file of `WALKey` plus cells, and it is used to replay not-yet-flushed data after a server crash. On RegionServer failure, the master splits the WAL by region and replays each region's edits so committed writes are not lost.

```properties
# Durability settings in hbase-site.xml
hbase.wal.provider = filesystem
# ASYNC_WAL is faster but can lose recent writes on crash; SYNC_WAL is the default
```

[Table of Contents](#Apache-HBase)

## When you should use HBase?
+ When the data is huge - billions of rows and millions of columns.
+ When you need random, real-time read/write access by key, not just batch scans.
+ When moving from an RDBMS, treat it as a complete redesign rather than a port.
+ When you accept no SQL, no joins, and limited transactions (Phoenix can add SQL).
+ When you have enough cluster to make HBase worthwhile - it is not a single-node tool.

[Table of Contents](#Apache-HBase)

## In HBase what is column families?
A column family is the basic unit of physical storage and the level at which storage features such as compression, block size, Bloom filters, versions, and TTL are configured. All cells in a family for a row are stored together on the same RegionServer, so families should be defined by access pattern, not by convenience.

```bash
# One family for the hot lookup path, one for cold metadata
create 'app:impressions', {NAME => 'i', VERSIONS => 1}, {NAME => 'meta', VERSIONS => 3}
```

Keep the number of column families small (typically 1-3): each family has its own MemStore and flush behavior, and many families multiply memory pressure and flush storms.

[Table of Contents](#Apache-HBase)

## Explain what is the row key?
The row key is defined by the application. Because a cell is addressed by `(row key, column family, column qualifier, timestamp)` and rows are sorted by row key, the row key controls the physical sort order and which regions hold which rows. All cells with the same row key are co-located on the same RegionServer. Row keys must be unique, and they cannot be changed after the fact without deleting and rewriting the row.

[Table of Contents](#Apache-HBase)

## Explain deletion in HBase? Mention what are the three types of tombstone markers in HBase?
When you delete a cell, the data is not immediately removed; a tombstone marker is written that makes the deleted cells invisible, and the data is physically removed during compaction.

Three types of tombstone marker:

+ Version delete marker: marks a single version of a column.
+ Column delete marker: marks all versions of one column.
+ Family delete marker: marks all columns in a column family.

[Table of Contents](#Apache-HBase)

## Explain how does HBase actually delete a row?
Writes go from RAM to disk as immutable HFiles (except during compaction). During deletion, a major compaction removes delete markers while minor compactions generally do not. A normal delete writes a tombstone; the data it hides is removed during compaction.

If you delete data and then insert new data with an earlier timestamp than the tombstone, subsequent Gets may still be masked by the tombstone and will not see the new value until a major compaction runs. This is why clients should write timestamps that move forward.

[Table of Contents](#Apache-HBase)

## Explain what happens if you alter the block size of a column family on an already occupied database?
When you alter the block size of a column family, newly written data uses the new block size while old data stays in blocks of the old size. Existing data is still read correctly, and new files flushed after the change use the new block size. All data is transformed to the new block size only after the next major compaction.

[Table of Contents](#Apache-HBase)

## Mention the difference between HBase and Relational Database?
| HBase | Relational Database |
|---|---|
| Schema-less for column qualifiers; only family schema is fixed | Fixed schema of typed columns |
| Wide-column / column-family oriented | Row oriented |
| Stores denormalized, sparse data | Stores normalized data |
| Scales horizontally by adding RegionServers | Scales up, or shards manually |
| Automatic region splitting | Manual partitioning / sharding |
| Single-row atomicity, no joins, no SQL natively | ACID transactions, joins, SQL |
| Good for key-based random access at scale | Good for complex queries over moderate data |

[Table of Contents](#Apache-HBase)

## What is HBaseFsck class?
`HBaseFsck` implements the `hbck` tool, which offers command-line switches to check region consistency and table integrity and to repair a corrupted HBase. It runs in a read-only inconsistency-identifying mode and a multi-phase read-write repair mode.

```bash
hbase hbck
hbase hbck -details
hbase hbck -repair
```

[Table of Contents](#Apache-HBase)

## What are the main key structures of HBase?
The row key and the column key (column family plus qualifier) are the two most important key structures. Together with the timestamp they form the cell address: `(row key, column family, column qualifier, timestamp)`.

[Table of Contents](#Apache-HBase)

## Discuss how you can use filters in Apache HBase
Filters perform server-side filtering for scans, so rows and cells are discarded on the RegionServer before crossing the network. They were introduced in HBase 0.92 and can be used from the shell, the Java API, and Thrift. Because filtering happens after the scan reads the row from the store, filters reduce network and client work but do not eliminate the underlying I/O - a well-designed row key is still better than a filter.

```bash
# Shell examples: prefix, single-column value, and a filter list
scan 'app:impressions', {FILTER => "PrefixFilter('u42|')", LIMIT => 10}
scan 'app:impressions', {FILTER => "SingleColumnValueFilter('i', 'campaign_id', =, 'binary:cmp-99')"}
scan 'app:impressions', {FILTER => "RowFilter(>=, 'binary:u42|') AND ColumnPrefixFilter('camp')"}
scan 'app:impressions', {FILTER => "PageFilter(100)"}
```

```python
# HappyBase: a filter string is passed through to the RegionServer
for key, data in table.scan(
    row_prefix=b"u42|",
    filter=b"SingleColumnValueFilter('i', 'campaign_id', =, 'binary:cmp-99')",
    limit=50,
):
    print(key, data)
```

[Table of Contents](#Apache-HBase)

## HBase support syntax structure like SQL yes or No?
No, HBase does not support SQL natively. However, Apache Phoenix provides a SQL layer over HBase, translating SQL into HBase scans and supporting secondary indexes and JDBC. Other options are Hive or Spark reading HBase through a connector, and the REST/Thrift gateways for non-Java clients.

[Table of Contents](#Apache-HBase)

## What is the meaning of compaction in HBase?
Under heavy writes it is impractical to keep one file per store, because every read would seek across many files. Compaction merges HFiles to reduce the number of disk seeks per read and to drop deleted or expired cells. Choosing when and how aggressively to compact is a central HBase tuning topic.

[Table of Contents](#Apache-HBase)

## How will you implement joins in HBase?
HBase does not support joins directly. Use a MapReduce or Spark job that scans the relevant tables and joins them, or denormalize at write time so that the data needed together is stored in one row (the preferred approach for a serving path).

```python
# Spark can read HBase through the HBase-Spark connector and join to curated tables
impressions = (
    spark.read.format("org.apache.hadoop.hbase.spark")
    .option("hbase.table", "app:impressions")
    .option("hbase.columns.mapping", "rowkey STRING :key, campaign STRING i:campaign_id, ts STRING i:ts")
    .load()
)
campaigns = spark.table("curated.campaigns")
joined = impressions.join(campaigns, impressions.campaign == campaigns.campaign_id)
```

The interview point: a join in a serving path means the schema is wrong. Reshape the row key and duplicate the small side into the row instead.

[Table of Contents](#Apache-HBase)

## Explain JMX concerning HBase
Java Management Extensions (JMX) is the standard mechanism for exporting the status and metrics of Java applications. HBase exposes RegionServer and Master MBeans through JMX, which monitoring tools scrape for metrics such as requests per second, MemStore size, and compaction queue depth.

```bash
# Enable the JMX remote agent on a RegionServer
export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS \
  -Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=10102 \
  -Dcom.sun.management.jmxremote.authenticate=false"
```

[Table of Contents](#Apache-HBase)

## What is the use of MasterServer?
The Master server assigns regions to RegionServers and handles load balancing across the cluster. It also performs admin operations such as create, alter, and drop table, and coordinates region splits, merges, and recovery. It is not on the read/write data path: clients talk to RegionServers directly, so a brief master outage does not stop serving.

[Table of Contents](#Apache-HBase)

## Define the Term Thrift.
Apache Thrift is a cross-language RPC framework with a compiler written in C++. It provides schema compilers and runtime libraries for C++, Java, Python, Ruby, PHP, and others. HBase ships a Thrift gateway so non-Java clients (for example Python via HappyBase) can talk to the cluster.

[Table of Contents](#Apache-HBase)

## Why use HColumnDescriptor class?
`HColumnDescriptor` describes a column family: compression settings, number of versions, TTL, block size, Bloom filter type, and other per-family attributes. It is used as input when creating a table or adding a column family. Modern code sometimes uses the builder `ColumnFamilyDescriptorBuilder` instead.

```java
ColumnFamilyDescriptor cf = ColumnFamilyDescriptorBuilder
    .newBuilder(Bytes.toBytes("i"))
    .setMaxVersions(1)
    .setTimeToLive(7_776_000)
    .setCompressionType(Compression.Algorithm.SNAPPY)
    .setBloomFilterType(BloomType.ROWCOL)
    .build();
```

[Table of Contents](#Apache-HBase)

## What is a cell in HBase?
A cell is the smallest unit of an HBase table. It holds a piece of data as a tuple of `{row, column, version}`, where column is `family:qualifier` and version is the timestamp of the value.

[Table of Contents](#Apache-HBase)

## What is a Bloom filter?
A Bloom filter is a space-efficient structure used to test whether an HFile contains a certain row or row-column cell, which avoids reading HFiles that cannot contain the requested key. HBase supports `ROW` (test row key only) and `ROWCOL` (test row key plus column) Bloom filters per column family, which improves read throughput for random point reads.

```bash
# Add a Bloom filter to a family, or tune it at create time
alter 'app:impressions', {NAME => 'i', BLOOMFILTER => 'ROWCOL'}
```

Bloom filters help point reads and hurt nothing on writes except a little memory and file size; they do not help scans of many rows.

[Table of Contents](#Apache-HBase)

## Tell me about the types of HBase Operations?
Two broad types: read operations (Get, Scan, and the read half of filters) and write operations (Put, Delete, Increment, and Append). Admin operations such as create, alter, split, merge, flush, and compact form a third practical category.

[Table of Contents](#Apache-HBase)

## What is the use of HBase HMaster?
The main responsibilities of the master are coordinating RegionServers and performing admin functions (table DDL, region assignment, load balancing, and recovery coordination). HBase supports backup masters, so the master is not a permanent single point of failure.

[Table of Contents](#Apache-HBase)

## Which technique can you use in HBase to access HFile directly without the help of HBase?
You can use the `HFile.main()` method (the `hbase org.apache.hadoop.hbase.io.hfile.HFile` tool) to inspect an HFile without a running HBase cluster.

```bash
hbase org.apache.hadoop.hbase.io.hfile.HFile -p -f /hbase/data/default/app_impressions/region/hfile
```

[Table of Contents](#Apache-HBase)

## Can the region server will be located on all DataNodes?
Yes. In a normal deployment RegionServers run on the same hosts as DataNodes so that HDFS data locality lets a RegionServer read its regions from local disks.

[Table of Contents](#Apache-HBase)

## Name the filter which accepts the page size as the parameter in HBase?
`PageFilter` accepts the page size as a parameter and limits the number of rows returned in one page.

```bash
scan 'app:impressions', {FILTER => "PageFilter(100)"}
```

[Table of Contents](#Apache-HBase)

## When would you use HBase?
HBase is used when you need random read and write operations at high throughput on large datasets. It gives strong consistency per row, can handle tables with billions of rows and millions of columns on commodity hardware, and scales horizontally. It is the wrong tool when the workload is analytical SQL over the whole table.

[Table of Contents](#Apache-HBase)

## What is the use of get method?
`get()` reads a single row (or a specific set of cells within a row) by its row key. It is the point-read path: the client uses `hbase:meta` to find the region, contacts the RegionServer, and checks the MemStore and block cache before the HFiles.

```python
row = table.row(b"u42|9999999999999-1700000000000|a1", columns=[b"i:campaign_id", b"i:amount"])
```

[Table of Contents](#Apache-HBase)

## Define the difference between Hive and HBase?
Apache Hive is a data warehousing layer on top of Hadoop. It queries data in HDFS with HiveQL (a SQL-like language) that is translated into MapReduce, Tez, or Spark jobs, and it performs batch processing.

Apache HBase is a NoSQL wide-column key/value store on top of HDFS. Unlike Hive, HBase operations run in real time against its own database rather than as batch jobs. HBase splits tables into regions and groups columns into column families.

Hive and HBase are complementary: Hive is good for analytical scans and joins, HBase for real-time key-based access. Data can be read and written between them, for example by storing HBase tables in Hive or writing Hive results into HBase.

[Table of Contents](#Apache-HBase)

## Explain the data model of HBase.
HBase comprises a set of tables. Each table has rows and column families, and the row key acts as the primary key used for every access. A cell is addressed by row key, column family, qualifier, and timestamp, and each cell can hold multiple versions. Column qualifiers are dynamic per row, so a table can be extremely sparse and wide.

```text
table
  row key (sorted) -> column family -> qualifier -> [version, value]
```

[Table of Contents](#Apache-HBase)

## Define column families?
A column family is a collection of columns that are stored together and tuned together. A row is composed of cells across one or more column families, and each family has its own MemStore, HFiles, and storage settings.

[Table of Contents](#Apache-HBase)

## Define standalone mode in HBase?
Standalone mode is the default for a fresh install. HBase does not use HDFS; it uses the local filesystem, and it runs all HBase daemons plus a local ZooKeeper in the same JVM. It is intended for development and testing, not production.

[Table of Contents](#Apache-HBase)

## What is decorating Filters?
A decorating filter wraps another filter to modify or extend its behavior. The two built-ins are `SkipFilter`, which skips the whole row when any cell fails the wrapped filter, and `WhileMatchFilter`, which stops the scan as soon as the wrapped filter stops matching.

```bash
# Stop the scan at the first row where campaign_id != cmp-99
scan 'app:impressions', {FILTER => "WhileMatchFilter(SingleColumnValueFilter('i','campaign_id',=,'binary:cmp-99'))"}
```

[Table of Contents](#Apache-HBase)

## What is RegionServer?
A table is divided into regions, and a RegionServer serves a set of regions to clients. It handles reads and writes, keeps the MemStore, appends to the WAL, flushes to HFiles, and runs compactions and splits. In a distributed cluster a RegionServer runs on a DataNode.

[Table of Contents](#Apache-HBase)

## What are the data manipulation commands of HBase?
+ `put` - writes a cell value at a specified row and column.
+ `get` - fetches a row or a specific cell.
+ `delete` - deletes a cell value.
+ `deleteall` - deletes all cells in a row.
+ `scan` - scans and returns table data.
+ `count` - counts the rows in a table.
+ `truncate` - disables, drops, and recreates a table.
+ `incr` - atomically increments a counter cell.
+ `append` - appends bytes to an existing cell value.

```bash
# Truncate keeps the table definition but removes all data
truncate 'app:impressions'
```

[Table of Contents](#Apache-HBase)

## What happens when you issue a delete command in HBase?
A delete is not applied instantly. A tombstone marker is inserted and stored alongside the data, and it hides the deleted cells from reads. The actual data is removed during a major compaction, which merges the HFiles of a region, groups column families together, and drops deleted and expired cells. Scans and gets filter the deleted cells out in the meantime.

[Table of Contents](#Apache-HBase)

## What are different tombstone markers in HBase?
+ Version marker: marks one version of a column for deletion.
+ Column marker: marks the whole column (all versions) for deletion.
+ Family marker: marks the whole column family (all columns) for deletion.

[Table of Contents](#Apache-HBase)

## HBase blocksize is configured on which level?
The HFile block size is configured per column family and defaults to 64 KB. A larger block size favors sequential scans; a smaller block size favors random point reads by reducing read amplification.

```bash
create 'app:impressions', {NAME => 'i', BLOCKSIZE => 16384}
```

[Table of Contents](#Apache-HBase)

## Which command is used to run HBase Shell?
`./bin/hbase shell` from the HBase directory starts the shell. In a packaged install, `hbase shell` is usually already on the PATH.

[Table of Contents](#Apache-HBase)

## Which command is used to show the current HBase user?
The `whoami` command shows the current HBase user in the shell.

[Table of Contents](#Apache-HBase)

## What is the full form of MSLAB?
MSLAB stands for MemStore-Local Allocation Buffer. When a request thread inserts data into a MemStore it does not allocate space from the heap at large; it allocates from a memory arena dedicated to the target region, which reduces heap fragmentation and full-GC pauses caused by many long-lived MemStore cells.

[Table of Contents](#Apache-HBase)

## Define LZO?
Lempel-Ziv-Oberhumer (LZO) is a lossless compression algorithm that focuses on decompression speed. HBase supports several codecs per column family (Snappy, LZ4, Zstd, GZIP), and Zstd or Snappy are the common modern choices.

[Table of Contents](#Apache-HBase)

## What is HBase Fsck?
HBase ships with `hbck`, implemented by the `HBaseFsck` class. It checks region consistency and table integrity and can repair a corrupted HBase. It has a read-only inconsistency-identifying mode and a multi-phase read-write repair mode.

[Table of Contents](#Apache-HBase)

## What is REST?
REST (Representational State Transfer) defines semantics so that HTTP can be used generically to address remote resources. The HBase REST server exposes tables and rows over HTTP with support for different message formats (JSON, XML, protobuf), giving non-Java clients an alternative to Thrift.

```bash
# Start the REST gateway and read a row
hbase-daemon.sh start rest -p 8080
curl -H "Accept: application/json" http://localhost:8080/app:impressions/u42%7C1/i:campaign_id
```

[Table of Contents](#Apache-HBase)

## What is Nagios?
Nagios is a widely used monitoring tool for cluster health. It polls current metrics on a schedule and compares them with configured thresholds, alerting when a check fails. HBase metrics can be scraped through JMX or the metrics endpoints that Nagios checks consume.

[Table of Contents](#Apache-HBase)

## What is the use of ZooKeeper?
ZooKeeper maintains cluster configuration and the communication path between RegionServers and clients. It also provides distributed synchronization and holds cluster state through sessions. Every RegionServer and the HMaster send heartbeats to ZooKeeper, which detects failures and provides server-failure notifications so recovery can start. Clients also use ZooKeeper to find `hbase:meta`.

[Table of Contents](#Apache-HBase)

## Define catalog tables in HBase?
Catalog tables maintain metadata about the cluster. `hbase:meta` maps each region to its RegionServer and start row key. In modern HBase the old `-ROOT-` table no longer exists; the location of `hbase:meta` is stored in ZooKeeper, and clients cache region locations locally.

[Table of Contents](#Apache-HBase)

## Define compaction in HBase?
HBase combines HFiles to reduce storage and the number of disk seeks needed for a read. Compaction chooses HFiles from a region and merges them, dropping expired and deleted cells. There are two types: minor and major.

[Table of Contents](#Apache-HBase)

## Explain what is HBase?
HBase is a wide-column, non-relational database management system that runs on top of HDFS. It is not a relational data store and does not support SQL natively. A master node regulates the cluster while RegionServers store portions of the tables and serve the data.

[Table of Contents](#Apache-HBase)

## Explain why to use HBase?
+ High-capacity storage that scales to billions of rows and millions of columns.
+ Distributed design for very large tables.
+ Wide-column / column-family-oriented storage.
+ Horizontally scalable.
+ High performance and availability through replication.
+ Unlike HDFS, it supports random real-time CRUD operations.

[Table of Contents](#Apache-HBase)

## Mention what are Key Components of HBase?
+ ZooKeeper: coordination between clients, the master, and RegionServers.
+ HBase Master: monitors RegionServers and performs admin work.
+ RegionServer: monitors and serves regions.
+ Region: contains an in-memory MemStore and HFiles.
+ Catalog tables: `hbase:meta` (the older `-ROOT-` table is obsolete).

[Table of Contents](#Apache-HBase)

## What is the Role of Master Server in HBase?
The master assigns regions to RegionServers, handles load balancing, and performs admin operations such as table creation and schema changes. It also coordinates region assignment and recovery after a RegionServer fails.

[Table of Contents](#Apache-HBase)

## Explain what does HBase consists of?
HBase consists of a set of tables. Each table contains rows and columns like a traditional database, and each table has a primary key (the row key). An HBase column denotes an attribute of an object, and columns are grouped into column families.

[Table of Contents](#Apache-HBase)

## What is the Role of ZooKeeper in HBase?
ZooKeeper maintains configuration information, provides distributed synchronization, and keeps the communication path between clients and RegionServers. It stores the location of `hbase:meta`, elects the active master, and tracks RegionServer liveness through heartbeats.

[Table of Contents](#Apache-HBase)

## Mention how many operational commands in HBase?
The core data operations are about five: Get, Put, Delete, Scan, and Increment. Append, count, and admin commands extend that set.

+ Get
+ Put
+ Delete
+ Scan
+ Increment

[Table of Contents](#Apache-HBase)

## When do we need to disable a table in HBase?
A table must be disabled before certain schema changes, such as altering or dropping a column family. A disabled table cannot be scanned or written, and it is re-enabled with `enable`.

```bash
disable 'app:impressions'
alter 'app:impressions', {NAME => 'meta', TTL => 2592000}
enable 'app:impressions'
```

[Table of Contents](#Apache-HBase)

## Explain what is WAL and HLog in HBase?
The WAL (Write Ahead Log), formerly HLog, records all changes to data before they are applied. It is a Hadoop sequence file storing WAL keys with sequential numbers plus the actual cells, and it is used to replay not-yet-persisted data after a server crash. On failure it acts as the lifeline that recovers committed writes.

[Table of Contents](#Apache-HBase)

## What are the different Types of Filters used in HBase?
Filters are used to return specific data from an HBase table rather than every record. Main categories:

+ Row key filters: `RowFilter`, `PrefixFilter`, `RowPrefixFilter`, `KeyOnlyFilter`.
+ Column and qualifier filters: `ColumnPrefixFilter`, `FamilyFilter`, `QualifierFilter`.
+ Value filters: `SingleColumnValueFilter`, `ValueFilter`.
+ Structural filters: `PageFilter`, `FirstKeyOnlyFilter`, `TimestampsFilter`.
+ Decorating filters: `SkipFilter`, `WhileMatchFilter`.
+ Composite filters: `FilterList` with `MUST_PASS_ALL` or `MUST_PASS_ONE`.

[Table of Contents](#Apache-HBase)

## In HBase what is Column Families?
A column family is the basic unit of physical storage and the level at which storage features such as compression, block size, and Bloom filters are applied. Cells in the same family for a row are stored together in the same HFiles and served by the same RegionServer.

[Table of Contents](#Apache-HBase)

## Name three disadvantages HBase has as compared to RDBMS?
+ No joins and no multi-table transactions; a read-modify-write across rows is application logic.
+ No native SQL or strict typing; almost everything is a byte array, and secondary access requires an index table or Phoenix.
+ Operational complexity: ZooKeeper, HDFS, RegionServer tuning, compactions, and region splits all need care.

Some traditional criticisms are outdated: modern HBase supports cell-level ACLs and Kerberos authentication, and backup masters remove the master as a hard single point of failure. Indexing is still limited to the row key unless you build index tables or use Phoenix secondary indexes.

[Table of Contents](#Apache-HBase)

## Explain what is the Row Key?
The row key is defined by the application and is the primary key of a row. Because the combined cell key is prefixed by the row key, the application controls the sort order and can group related cells together. All cells with the same row key are co-located on the same server, which is why row key design determines read and write distribution.

[Table of Contents](#Apache-HBase)

## Is HBase a scale out or scale up process?
HBase is scale-out. It runs on top of Hadoop, which is distributed, and capacity and throughput grow by adding more machines and RegionServers. Vertical scaling helps a single node, but the architecture is designed to add nodes.

[Table of Contents](#Apache-HBase)

## Explain deletion in HBase?
When you delete a cell, the data is not actually deleted; a tombstone marker is set that makes the deleted cells invisible. The data is physically removed during compaction.

Three types of tombstone marker:

+ Version delete marker: marks a single version of a column.
+ Column delete marker: marks all versions of a column.
+ Family delete marker: marks all columns in a column family.

[Table of Contents](#Apache-HBase)

## What are the step in writing something into Hbase by a Client?
The client does not write directly to HFiles. It first appends the mutation to the WAL, then applies it to the MemStore of the target region. The MemStore is flushed to disk as an HFile when it reaches a threshold or the region is closed, and the WAL entries for those edits can then be discarded. Region location comes from the client's cache of `hbase:meta`.

```text
put -> find region (meta cache) -> RegionServer -> WAL append -> MemStore -> (flush) HFile
```

[Table of Contents](#Apache-HBase)

## Explain how does Hbase actually delete a Row?
Data written from RAM to disk becomes immutable HFiles apart from compaction. A delete writes a tombstone rather than removing bytes. Major compaction removes delete markers and the hidden data; minor compactions generally do not. If new data is written with an earlier timestamp than the tombstone, Gets can remain masked by the tombstone until a major compaction runs.

[Table of Contents](#Apache-HBase)

## What is compaction in Hbase?
As more data is written, many HFiles are created. Compaction merges HFiles into fewer, larger files and discards the old files after the merge succeeds. It also removes deleted and expired cells, which is what keeps read latency from degrading.

[Table of Contents](#Apache-HBase)

## Explain what happens if you alter the Block Size of a column Family on an already occupied Database?
New data is written with the new block size while old data remains in blocks of the old size. New flushed files use the new block size, existing data continues to be read correctly, and all data is converted to the new block size after the next major compaction.

[Table of Contents](#Apache-HBase)

## What are the different compaction types in Hbase?
There are two types. In minor compaction, a small set of adjacent HFiles is merged into one without removing the deleted data, and the files to merge are chosen by policy. In major compaction, all HFiles of a region's column family are merged into one, deleted and expired cells are discarded, and it is often triggered manually or by a schedule.

```bash
# Trigger a major compaction on a region (shell) or a single table
major_compact 'app:impressions'
```

Major compaction rewrites a lot of data, so it should be scheduled off-peak and rate-limited with `hbase.hstore.compaction.throughput.lower.bound` and related settings.

[Table of Contents](#Apache-HBase)

## What is a Cell in Hbase?
A cell is the smallest unit of an HBase table. It holds a piece of data as a tuple of `{row, column, version}`, where the column is `family:qualifier` and the version is the value's timestamp.

[Table of Contents](#Apache-HBase)

## What is the Scope of a Rowkey in Hbase?
A row key identifies a row within a table, not within a column family. All column families in that row share the same row key; a row can exist with cells in only some (or none explicitly, if a family marker is written) of the families. Two different column families do not have separate row key spaces.

[Table of Contents](#Apache-HBase)

## What is the Role of the Class Hcolumndescriptor in Hbase?
`HColumnDescriptor` stores information about a column family such as the number of versions, TTL, compression settings, block size, and Bloom filter type. It is used as input when creating a table or adding a column family.

[Table of Contents](#Apache-HBase)

## What is a Namespace in Hbase?
A namespace is a logical grouping of tables, similar to a database or schema in a relational database. It organizes tables and controls quotas and permissions. The default namespaces are `default` and `hbase`.

```bash
create_namespace 'app'
create 'app:impressions', 'i'
```

[Table of Contents](#Apache-HBase)

## What is the Lower Bound of Versions in Hbase?
The lower bound (minimum number of versions) is the minimum number of versions to keep for a column. If it is set to 3, the three latest versions are retained when a compaction runs, and older versions are removed subject to the maximum versions and TTL settings.

[Table of Contents](#Apache-HBase)

## What is Hotspotting in Hbase?
Hotspotting is when a large amount of client traffic is directed at one node, or a few nodes, of a cluster. The traffic can be reads, writes, or other operations, and it overwhelms the machine hosting that region, causing performance degradation and potentially region unavailability. The classic cause is a monotonically increasing row key such as a timestamp or sequential id, which always writes to the last region.

Fixes, in the order an interviewer usually wants to hear them:

+ Salt the row key with a hash prefix so writes spread across regions.
+ Use a reverse timestamp so the newest row is first for a known prefix but writes are not sequential across users.
+ Pre-split the table so the key space starts balanced.
+ Use a random or hashed key when point lookups are by a secondary key.

```python
import hashlib

def salted_key(user_id: str, ts_ms: int, buckets: int = 32) -> str:
    salt = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % buckets
    return f"{salt:02d}|{user_id}|{9_999_999_999_999 - ts_ms:013d}"
```

Salting costs read fan-out: a query for one user must know the salt (derive it from the user id) rather than scanning all buckets.

[Table of Contents](#Apache-HBase)

## What is Ttl in Hbase?
TTL (time to live) is a data retention setting at the column family level. It specifies how long a cell version is kept; once a version's timestamp is older than the TTL, it is removed during compaction and is not returned by reads.

```bash
create 'app:impressions', {NAME => 'i', TTL => 7776000}   # 90 days in seconds
```

[Table of Contents](#Apache-HBase)

## Why do we Pre create empty Regions?
Tables are initially created with one region by default. During bulk import, all clients write to that single region until it grows large enough to split, which serializes the load and slows the import. Pre-creating empty regions (pre-splitting) spreads the initial write load across the cluster from the start.

```bash
create 'app:impressions', {NAME => 'i'}, SPLITS => ['10', '20', '30', '40']
```

[Table of Contents](#Apache-HBase)

## Does Hbase support Table Joins?
HBase does not support table joins. Join queries can be implemented with a MapReduce or Spark job that scans multiple HBase tables, but the serving-path answer is to denormalize so the data needed together lives in one row.

[Table of Contents](#Apache-HBase)

## Which File in Hbase is designed after Sstable File of Bigtable?
The HFile, which stores the actual data (not metadata), is designed after the SSTable file of Bigtable. HFiles are immutable once written and are merged by compaction.

[Table of Contents](#Apache-HBase)

## What is a Hbase Store?
A store hosts a MemStore and zero or more StoreFiles (HFiles). A store corresponds to one column family of one region, which is why column families are the unit of memory and flush tuning.

[Table of Contents](#Apache-HBase)

## What are the Two Types of Table Design Approach in Hbase?
They are short-and-wide and tall-and-thin.

+ Tall-and-thin: many rows, few columns per row. This is the default HBase sweet spot and scales best because rows spread across regions.
+ Short-and-wide: fewer rows, many columns per row. Useful when a natural entity is read as a whole and the number of entities is bounded, but a single row cannot be split across regions, so it limits write parallelism.

Note the common confusion: "short and wide" means few rows and many columns, not few columns and many rows.

[Table of Contents](#Apache-HBase)

## When do we do Manual Region Splitting?
Manual region splitting is done when there is an unexpected hotspot caused by many clients querying the same region, or when you know the key distribution ahead of time and want to pre-split for bulk loading. Automatic splitting handles normal growth.

```bash
# Split a table at an explicit key, and merge two adjacent regions
split 'app:impressions', '20'
merge_region 'ENCODED_REGION_A', 'ENCODED_REGION_B'
```

[Table of Contents](#Apache-HBase)

## In which scenario should we consider creating a short and wide Hbase Table?
Use a short-and-wide design when an entity is naturally read as a whole, the number of entity rows is moderate, and the attributes are numerous and sparse. The trade-off is that one row lives in one region, so write parallelism across that entity is limited. For time-series data, tall-and-thin (one row per event) is almost always the better choice.

[Table of Contents](#Apache-HBase)

## In Hbase what is Log Splitting?
When a RegionServer dies, the edits belonging to its regions must be recovered from the WAL. The edits in the WAL are grouped by region so each set can be replayed to rebuild that region's data. The process of grouping and distributing WAL edits by region is called log splitting.

[Table of Contents](#Apache-HBase)

## How does Hbase support Bulk Data Loading?
Bulk loading writes HFiles directly, bypassing the WAL and MemStore, which makes it much faster than `put` for large imports. Two steps:

1. Generate HFiles from the source data with a MapReduce or Spark job (`ImportTsv` or a custom job) in HBase's internal format.
2. Load the prepared files into a running cluster with `completebulkload` / `LoadIncrementalHFiles`, which moves each file into the correct region.

```bash
# 1) Convert a TSV on HDFS into HFiles
hbase org.apache.hadoop.hbase.mapreduce.ImportTsv \
  -Dimporttsv.columns=HBASE_ROW_KEY,i:campaign_id,i:amount \
  -Dimporttsv.bulk.output=/tmp/impressions_hfiles \
  app:impressions /data/incoming/impressions.tsv

# 2) Load the HFiles into the table (pre-split it first for balance)
hbase org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles \
  /tmp/impressions_hfiles app:impressions
```

Pre-split the table before a bulk load, because `LoadIncrementalHFiles` assigns each HFile to the region that owns its key range.

[Table of Contents](#Apache-HBase)

## Why MultiWAL is Needed?
With a single WAL per RegionServer, the RegionServer must write to the WAL serially because HDFS files must be sequential. That makes the WAL a throughput bottleneck. MultiWAL gives each RegionServer multiple WAL files so different regions can write concurrently, improving write throughput.

```xml
<property>
  <name>hbase.wal.regiongrouping.strategy</name>
  <value>identity</value>
</property>
<property>
  <name>hbase.wal.provider</name>
  <value>filesystem</value>
</property>
```

[Table of Contents](#Apache-HBase)

## How does Hbase provide High Availability?
+ Region replication: each region can have replicas served by different RegionServers, and the load balancer avoids co-hosting a replica set.
+ WAL replay: committed edits are recovered from the WAL after a RegionServer crash.
+ Multiple masters: backup H Masters are elected so the master is not a hard single point of failure.
+ HDFS replication: the underlying WALs and HFiles are stored with HDFS replication.
+ For cross-cluster DR, HBase replication ships edits from a source cluster to a peer cluster.

[Table of Contents](#Apache-HBase)

## How does Wal help when a Regionserver Crashes?
The WAL records all changes to data in file-based storage. If a RegionServer crashes or becomes unavailable before the MemStore is flushed, the WAL ensures the changes can be replayed. The master splits the WAL by region and a new RegionServer replays the edits, so acknowledged writes survive the crash.

[Table of Contents](#Apache-HBase)

## What is Hregionserver in Hbase?
`HRegionServer` is the RegionServer implementation. It is responsible for serving and managing regions: hosting MemStores, appending to the WAL, flushing HFiles, and running compactions and splits. In a distributed cluster a RegionServer runs on a DataNode.

[Table of Contents](#Apache-HBase)

## What are the different Block Caches in Hbase?
HBase provides two BlockCache implementations: the on-heap `LruBlockCache` (the default) and `BucketCache`, which is usually off-heap. A common production configuration is a combined cache: an LRU cache in front of a `BucketCache` backed by off-heap memory, SSD, or a file, to keep the JVM heap small and avoid GC pauses.

```xml
<property>
  <name>hbase.bucketcache.ioengine</name>
  <value>offheap</value>
</property>
<property>
  <name>hbase.bucketcache.size</name>
  <value>16384</value>
</property>
<property>
  <name>hfile.block.cache.size</name>
  <value>0.2</value>
</property>
```

[Table of Contents](#Apache-HBase)

## How do you manage compactions and region splits?
Compaction and splitting are the two background processes that keep a growing table healthy. Compaction controls read amplification and storage; splitting controls distribution across RegionServers. Both are usually automatic, but the commands and policies matter in interviews.

```bash
# Inspect and trigger compactions
major_compact 'app:impressions'
compact 'app:impressions'
# Split and merge regions
split 'app:impressions', '30'
merge_region 'ENCODED_REGION_A', 'ENCODED_REGION_B'
```

```xml
<property>
  <name>hbase.hregion.majorcompaction</name>
  <value>604800000</value>
</property>
<property>
  <name>hbase.hregion.majorcompaction.jitter</name>
  <value>0.5</value>
</property>
<property>
  <name>hbase.hstore.compaction.min</name>
  <value>3</value>
</property>
<property>
  <name>hbase.hstore.blockingStoreFiles</name>
  <value>16</value>
</property>
<property>
  <name>hbase.regionserver.region.split.policy</name>
  <value>org.apache.hadoop.hbase.regionserver.SteppingSplitPolicy</value>
</property>
```

Practical guidance:

+ Schedule major compactions off-peak and jitter them, because they rewrite the whole region.
+ On a write-heavy table, tune `hbase.hstore.compaction.min` and the throughput bounds rather than disabling compaction.
+ Pre-split new tables and use `SteppingSplitPolicy` to avoid split storms, where one split immediately triggers the next.
+ A region that stays hot after its split is a row key design problem, not a compaction problem.

[Table of Contents](#Apache-HBase)

## When should you not use HBase, and what should you use instead?
+ Analytical SQL over the whole dataset - use a warehouse (Snowflake, BigQuery, Redshift) or a lakehouse table (Iceberg, Delta, Hudi) on Parquet. HBase scans are not columnar and do not support joins.
+ Low-latency key-value at very high write rates with multi-region writes - consider Cassandra or Bigtable, which offer multi-datacenter replication without the RegionServer/ZooKeeper stack.
+ Ordered streaming with replay and many consumers - use Kafka as the backbone, not HBase.
+ Small or medium datasets that fit in a relational database - use PostgreSQL or MySQL; HBase only pays off at scale.
+ Mostly write-once time series analytics - use Parquet/Iceberg with time partitioning; HBase is for point access, not aggregation.
+ Strong multi-row ACID transactions - use a relational or NewSQL database, not HBase.

A useful rule: HBase serves a known key to an application. If the question is "what does this key hold right now", HBase is a candidate; if the question is "aggregate everything matching a predicate", it is not.

[Table of Contents](#Apache-HBase)

## Real world use cases for HBase

### 1. IoT device telemetry time series
A utility monitors 60,000 smart meters emitting a reading every 15 seconds. The serving API needs the latest readings for a device and a time-range view over the last day, and the raw history must be retained for 90 days.

Business context: outage detection and customer-facing usage dashboards read a single device at a time. Data volume: about 4,000 writes/second, roughly 200 GB/month after compression.

Row key design: `salt|device_id|reverse_timestamp`, where salt is a fixed hash bucket per device and the reverse timestamp makes the newest reading sort first. TTL on the column family drops data after 90 days.

```bash
# Table with a salted key, one version, 90-day TTL, and a row+column Bloom filter
create 'iot:readings', {NAME => 'd', VERSIONS => 1, TTL => 7776000, BLOOMFILTER => 'ROWCOL', COMPRESSION => 'SNAPPY'}, SPLITS => ['04', '08', '0c', '10', '14', '18', '1c', '20']
```

```python
import hashlib

def reading_key(device_id: str, ts_ms: int, buckets: int = 32) -> str:
    salt = int(hashlib.md5(device_id.encode()).hexdigest(), 16) % buckets
    return f"{salt:02d}|{device_id}|{9_999_999_999_999 - ts_ms:013d}"
```

Why this design: the salt spreads writes across all 32 buckets so no single region takes the load, the device prefix within a bucket makes the latest-reading Get a single point read, and the reverse timestamp makes `scan row_prefix=salt|device` return newest first with a `LIMIT`.

### 2. Clickstream profile store for real-time bidding
An ad-tech platform records 2 billion impressions per day and must answer "what did this user see in the last 30 minutes" in under 10 ms during an auction.

Business context: the bidder enriches a request with a user's recent behavior. Data volume: about 25,000 writes/second, 2 billion rows/day, 30-minute working set.

Row key design: `salt|user_id|reverse_timestamp` for the recent window, plus a separate compacted table `user_profile` keyed by `salt|user_id` for the latest aggregates. The recent table uses a short TTL and the serving table keeps one version per key.

```java
Table recent = conn.getTable(TableName.valueOf("rtb:user_events"));
Scan scan = new Scan()
    .withStartRow(Bytes.toBytes(saltOf(userId) + "|" + userId + "|"))
    .withStopRow(Bytes.toBytes(saltOf(userId) + "|" + userId + "|\uFFFF".getBytes()))
    .setLimit(200)
    .setCaching(200);
```

Why this design: point reads and short scans are exactly HBase's strength, the reverse timestamp gives the newest events first without sorting, and the narrow row key keeps the block cache effective. Analytics still runs on a Parquet copy, not on HBase.

### 3. Messaging and conversation history
A messaging platform stores chat history so a client can open a conversation and load the most recent messages, then page backwards.

Business context: 40 million monthly users, peak 50,000 messages/second, per-conversation ordering required. Data volume: several TB per month.

Row key design: `conversation_id|reverse_timestamp|message_id`. Because a conversation is a natural read unit, the design is tall-and-thin with one row per message; the reverse timestamp gives pagination in both directions (newest first, and older pages by advancing the start row).

```bash
# Newest 50 messages in a conversation
scan 'msg:history', {STARTROW => 'conv-88217|', ENDROW => 'conv-88217|\xff', LIMIT => 50}
```

Why this design: ordering by row key replaces an ORDER BY, pagination is a bounded scan, and atomic increments on a companion counters table provide unread counts without a transaction.

### 4. Wide sparse product catalog with per-attribute updates
A retailer stores product attributes where different categories have wildly different fields (electronics have voltages, apparel has sizes), and the pricing service updates individual attributes frequently.

Business context: the storefront reads one product at a time and updates a few attributes per event. Data volume: 50 million products, 10-40 attributes each, low-latency reads.

Row key design: `salt|sku`, with attributes as dynamic qualifiers in a single family. Sparse storage means a product only occupies the qualifiers it actually has.

```bash
put 'catalog:products', '07|sku-99321', 'p:color', 'black'
put 'catalog:products', '07|sku-99321', 'p:voltage', '220'
get 'catalog:products', '07|sku-99321'
```

Why this design: a relational schema would need dozens of sparse columns or an entity-attribute-value table with joins; HBase stores sparse rows natively and reads a whole product in one Get. Salt keeps the catalog write load balanced during bulk price updates.

### 5. Streaming feature store for fraud detection
A payments company computes features (transaction velocity, recent declines) in a stream processor and serves them to a scoring service with single-digit-millisecond latency.

Business context: the scorer runs on every authorization and cannot wait for a warehouse. Data volume: 8,000 events/second, features for 30 million cards.

Row key design: `salt|card_id` for the current feature vector, with the feature values in one family and short TTLs on the fast-moving counters. A separate `salt|card_id|reverse_timestamp` table holds the recent event trail.

```python
# Stream processor writes the latest feature vector; scorer reads it
table.put(
    (salt(card_id) + "|" + card_id).encode(),
    {
        b"f:txn_count_1h": str(count_1h).encode(),
        b"f:declines_24h": str(declines_24h).encode(),
        b"f:updated_at": str(now_ms).encode(),
    },
)
```

Why this design: HBase gives a durable, horizontally scalable, low-latency serving layer for a keyed feature vector, writes are single-row atomic so the vector is never half-updated, and the analytics side of the feature computation lives in Kafka plus Flink rather than in HBase.

[Table of Contents](#Apache-HBase)
