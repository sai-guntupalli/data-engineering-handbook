## [Main title](../README.md)
### [Interview questions](full.md)

# Apache Impala

Apache Impala is a massively parallel (MPP) SQL query engine for data stored in HDFS, object storage, and Apache Kudu. It runs as long-lived daemons (`impalad`) on every DataNode, avoids MapReduce entirely, and returns interactive results over Hive-compatible tables.

The questions below mix classic Impala interview questions with modern operational detail: DDL, partitioning, statistics, join planning, Parquet vs Kudu, resource pools, EXPLAIN plans, and real production scenarios.

+ [How do I try Impala out?](#How-do-I-try-Impala-out)
+ [Does Cloudera offer a Vm for demonstrating Impala?](#Does-Cloudera-offer-a-Vm-for-demonstrating-Impala)
+ [How much Memory is required?](#How-much-Memory-is-required)
+ [What are the main features of Impala?](#What-are-the-main-features-of-Impala)
+ [What features from relational databases or hive are not available in Impala?](#What-features-from-relational-databases-or-hive-are-not-available-in-Impala)
+ [Does Impala support Generic Jdbc?](#Does-Impala-support-Generic-Jdbc)
+ [Is Avro supported?](#Is-Avro-supported)
+ [How do I Know how many Impala Nodes are in my cluster?](#How-do-I-Know-how-many-Impala-Nodes-are-in-my-cluster)
+ [Are results returned as they become available or all at once when a query completes?](#Are-results-returned-as-they-become-available-or-all-at-once-when-a-query-completes)
+ [Why does my select statement fail?](#Why-does-my-select-statement-fail)
+ [Why does my insert statement fail?](#Why-does-my-insert-statement-fail)
+ [Does Impala performance improve as it is deployed to more hosts in a cluster in much the same way that Hadoop performance does?](#Does-Impala-performance-improve-as-it-is-deployed-to-more-hosts-in-a-cluster-in-much-the-same-way-that-Hadoop-performance-does)
+ [Is the Hdfs Block Size reduced to achieve faster query results?](#Is-the-Hdfs-Block-Size-reduced-to-achieve-faster-query-results)
+ [Does Impala use caching?](#Does-Impala-use-caching)
+ [What are the good use cases for Impala as opposed to Hive or Mapreduce?](#What-are-the-good-use-cases-for-Impala-as-opposed-to-Hive-or-Mapreduce)
+ [Is Mapreduce required for impala and will Impala continue to work as expected if Mapreduce is stopped?](#Is-Mapreduce-required-for-impala-and-will-Impala-continue-to-work-as-expected-if-Mapreduce-is-stopped)
+ [Can Impala be used for complex event processing?](#Can-Impala-be-used-for-complex-event-processing)
+ [Is Impala intended to handle Real Time Queries in Low latency Applications or is it for ad Hoc Queries for the purpose of data exploration?](#Is-Impala-intended-to-handle-Real-Time-Queries-in-Low-latency-Applications-or-is-it-for-ad-Hoc-Queries-for-the-purpose-of-data-exploration)
+ [How does Impala compare to Hive and Pig?](#How-does-Impala-compare-to-Hive-and-Pig)
+ [Can I do transforms or add New functionality?](#Can-I-do-transforms-or-add-New-functionality)
+ [Can any Impala Query also be executed in Hive?](#Can-any-Impala-Query-also-be-executed-in-Hive)
+ [Can I use Impala to Query data already loaded into Hive and Hbase?](#Can-I-use-Impala-to-Query-data-already-loaded-into-Hive-and-Hbase)
+ [Is Hive an Impala requirement?](#Is-Hive-an-Impala-requirement)
+ [Is Impala production ready?](#Is-Impala-production-ready)
+ [How do I configure Hadoop High Availability for Impala?](#How-do-I-configure-Hadoop-High-Availability-for-Impala)
+ [What happens if there is an Error in Impala?](#What-happens-if-there-is-an-Error-in-Impala)
+ [What is the Maximum number of Rows in a Table?](#What-is-the-Maximum-number-of-Rows-in-a-Table)
+ [On which hosts does Impala run?](#On-which-hosts-does-Impala-run)
+ [How are Joins performed in Impala?](#How-are-Joins-performed-in-Impala)
+ [How does Impala process Join Queries for large tables?](#How-does-Impala-process-Join-Queries-for-large-tables)
+ [What is Impala's aggregation strategy?](#What-is-Impalas-aggregation-strategy)
+ [How is Impala Metadata managed?](#How-is-Impala-Metadata-managed)
+ [What load do concurrent queries produce on the Name Node?](#What-load-do-concurrent-queries-produce-on-the-Name-Node)
+ [How does Impala achieve its performance improvements?](#How-does-Impala-achieve-its-performance-improvements)
+ [What happens when the data set exceeds available memory?](#What-happens-when-the-data-set-exceeds-available-memory)
+ [What are the most Memory intensive operations?](#What-are-the-most-Memory-intensive-operations)
+ [When does Impala hold on to or return memory?](#When-does-Impala-hold-on-to-or-return-memory)
+ [Is there an update statement?](#Is-there-an-update-statement)
+ [Can Impala do User defined functions?](#Can-Impala-do-User-defined-functions)
+ [Why do I have to use refresh and invalidate Metadata and what do they do?](#Why-do-I-have-to-use-refresh-and-invalidate-Metadata-and-what-do-they-do)
+ [Why is space not freed up when I issue drop table?](#Why-is-space-not-freed-up-when-I-issue-drop-table)
+ [Is there a dual table?](#Is-there-a-dual-table)
+ [How do I load a big Csv file into a partitioned table?](#How-do-I-load-a-big-Csv-file-into-a-partitioned-table)
+ [Can I Do Insert Select Into a partitioned table?](#Can-I-Do-Insert-Select-Into-a-partitioned-table)
+ [What kinds of Impala Queries or data are best suited for Hbase?](#What-kinds-of-Impala-Queries-or-data-are-best-suited-for-Hbase)
+ [When would you use Impala instead of Hive?](#When-would-you-use-Impala-instead-of-Hive)
+ [How do you optimize Impala queries?](#How-do-you-optimize-Impala-queries)
+ [How do you create Impala tables with DDL and choose a file format?](#How-do-you-create-Impala-tables-with-DDL-and-choose-a-file-format)
+ [How do you create partitioned tables and manage partitions in Impala?](#How-do-you-create-partitioned-tables-and-manage-partitions-in-Impala)
+ [How do COMPUTE STATS and INVALIDATE METADATA drive Impala query plans?](#How-do-COMPUTE-STATS-and-INVALIDATE-METADATA-drive-Impala-query-plans)
+ [How do you read an Impala EXPLAIN plan and tune joins and hints?](#How-do-you-read-an-Impala-EXPLAIN-plan-and-tune-joins-and-hints)
+ [How do you use Parquet and Kudu tables in Impala?](#How-do-you-use-Parquet-and-Kudu-tables-in-Impala)
+ [How do Impala resource pools and admission control work?](#How-do-Impala-resource-pools-and-admission-control-work)
+ [How do you handle small files and table maintenance in Impala?](#How-do-you-handle-small-files-and-table-maintenance-in-Impala)
+ [What are Impala's trade-offs and when should you not use it?](#What-are-Impalas-trade-offs-and-when-should-you-not-use-it)
+ [Real world use cases for Apache Impala](#Real-world-use-cases-for-Apache-Impala)

## How do I try Impala out?
To look at the core features and functionality on Impala, the easiest way to try out Impala is to download the Cloudera QuickStart VM and start the Impala service through Cloudera Manager, then use `impala-shell` in a terminal window or the Impala Query UI in the Hue web interface.

To do performance testing and try out the management features for Impala on a cluster, you need to move beyond the QuickStart VM with its virtualized single-node environment. Ideally, download the Cloudera Manager software to set up the cluster, then install the Impala software through Cloudera Manager.

```bash
# Interactive shell against a coordinator
impala-shell -i coordinator-host:21000 -d analytics

# Run a query file and exit
impala-shell -i coordinator-host:21000 -f /home/etl/load_orders.sql

# Non-interactive one-liner
impala-shell -i coordinator-host:21000 -q "select count(*) from analytics.fact_orders"
```

[Table of Contents](#Apache-Impala)

## Does Cloudera offer a Vm for demonstrating Impala?
Cloudera offers a demonstration VM called the QuickStart VM, available in VMWare, VirtualBox, and KVM formats. For more information, see the Cloudera QuickStart VM. After booting the QuickStart VM, many services are turned off by default; in the Cloudera Manager UI that appears automatically, turn on Impala and any other components that you want to try out.

Modern alternatives are the Cloudera Data Platform (CDP) trial, a container-based `impala` image, or a small cloud cluster. The single-node VM is fine for SQL learning but not for join-strategy or admission-control testing, because those behaviors appear only when data is spread over multiple `impalad` processes.

[Table of Contents](#Apache-Impala)

## How much Memory is required?
Although Impala is not an in-memory database, when dealing with large tables and large result sets, you should expect to dedicate a substantial portion of physical memory for the `impalad` daemon. Recommended physical memory for an Impala node is 128 GB or higher. If practical, devote approximately 80% of physical memory to Impala.

The amount of memory required for an Impala operation depends on several factors:

+ The file format of the table. Different file formats represent the same data in more or fewer data files. The compression and encoding for each file format might require a different amount of temporary memory to decompress the data for analysis.
+ Whether the operation is a SELECT or an INSERT. For example, Parquet tables require relatively little memory to query, because Impala reads and decompresses data in 8 MB chunks. Inserting into a Parquet table is a more memory-intensive operation because the data for each data file (potentially hundreds of megabytes, depending on the value of the `PARQUET_FILE_SIZE` query option) is stored in memory until encoded, compressed, and written to disk.
+ Whether the table is partitioned or not, and whether a query against a partitioned table can take advantage of partition pruning.
+ Whether the final result set is sorted by the ORDER BY clause. Each Impala node scans and filters a portion of the total data, and applies the LIMIT to its own portion of the result set. In Impala 1.4.0 and higher, if the sort operation requires more memory than is available on any particular host, Impala uses a temporary disk work area to perform the sort. The intermediate result sets are all sent back to the coordinator node, which does the final sorting and then applies the LIMIT clause to the final result set.

For example, if you execute the query:

```sql
select * from giant_table order by some_column limit 1000;
```

and your cluster has 50 nodes, then each of those 50 nodes will transmit a maximum of 1000 rows back to the coordinator node. The coordinator node needs enough memory to sort (LIMIT * cluster_size) rows, although in the end the final result set is at most LIMIT rows, 1000 in this case.

Likewise, if you execute the query:

```sql
select * from giant_table where test_val > 100 order by some_column;
```

then each node filters out a set of rows matching the WHERE conditions, sorts the results (with no size limit), and sends the sorted intermediate rows back to the coordinator node. The coordinator node might need substantial memory to sort the final result set, and so might use a temporary disk work area for that final phase of the query.

Whether the query contains any join clauses, GROUP BY clauses, analytic functions, or DISTINCT operators. These operations all require some in-memory work areas that vary depending on the volume and distribution of data. In Impala 2.0 and later, these kinds of operations utilize temporary disk work areas if memory usage grows too large to handle.

The size of the result set. When intermediate results are being passed around between nodes, the amount of data depends on the number of columns returned by the query. For example, it is more memory-efficient to query only the columns that are actually needed in the result set rather than always issuing `SELECT *`.

The mechanism by which work is divided for a join query. You use the COMPUTE STATS statement, and query hints in the most difficult cases, to help Impala pick the most efficient execution plan.

Operationally, memory is governed by `--mem_limit` at startup, the `MEM_LIMIT` query option (`set mem_limit = 32gb;`), and admission control through resource pools.

[Table of Contents](#Apache-Impala)

## What are the main features of Impala?
A large set of SQL statements, including SELECT and INSERT, with joins, Subqueries in Impala SELECT Statements, and Impala Analytic Functions. Highly compatible with HiveQL, and also including some vendor extensions.

+ Distributed, high-performance queries.
+ Using Cloudera Manager, you can deploy and manage your Impala services. Cloudera Manager is the best way to get started with Impala on your cluster.
+ Using Hue for queries.
+ Appending and inserting data into tables through the INSERT statement.
+ ODBC: Impala is certified to run against MicroStrategy and Tableau, with restrictions. For more information, see Configuring Impala to Work with ODBC.
+ Querying data stored in HDFS and HBase in a single query.
+ In Impala 2.2.0 and higher, querying data stored in the Amazon Simple Storage Service (S3).
+ Concurrent client requests. Each Impala daemon can handle multiple concurrent client requests. The effects on performance depend on your particular hardware and workload.
+ Kerberos authentication.
+ Partitions. With Impala SQL, you can create partitioned tables with the CREATE TABLE statement, and add and drop partitions with the ALTER TABLE statement. Impala also takes advantage of the partitioning present in Hive tables.

[Table of Contents](#Apache-Impala)

## What features from relational databases or hive are not available in Impala?
+ Querying streaming data.
+ Deleting individual rows. You delete data in bulk by overwriting an entire table or partition, or by dropping a table.
+ Indexing (not currently). LZO-compressed text files can be indexed outside of Impala, as described in Using LZO-Compressed Text Files.
+ Full text search on text fields. The Cloudera Search product is appropriate for this use case.
+ Custom Hive Serializer/Deserializer classes (SerDes). Impala supports a set of common native file formats that have built-in SerDes in CDH.
+ Checkpointing within a query. That is, Impala does not save intermediate results to disk during long-running queries. Currently, Impala cancels a running query if any host on which that query is executing fails. When one or more hosts are down, Impala reroutes future queries to only use the available hosts, and Impala detects when the hosts come back up and begins using them again. Because a query can be submitted through any Impala node, there is no single point of failure. In the future, we will consider adding additional work allocation features to Impala, so that a running query would complete even in the presence of host failures.
+ Encryption of data transmitted between Impala daemons.
+ Hive indexes.
+ Non-Hadoop data stores, such as relational databases.

Important modern correction: row-level `UPDATE` and `DELETE` do exist for Kudu-backed tables, and since Impala 4.3 also for Iceberg tables. There is still no row-level `UPDATE`/`DELETE` for plain HDFS/Parquet tables, where you change data by overwriting a partition or table; the classic "no row-level update" answer remains accurate for those.

```sql
-- Supported for Kudu tables: point update and delete
update analytics.customer_kudu set tier = 'gold' where customer_id = 1001;
delete from analytics.customer_kudu where customer_id = 1002;
```

[Table of Contents](#Apache-Impala)

## Does Impala support Generic Jdbc?
Impala supports the HiveServer2 JDBC driver. Use the Hive JDBC driver class against the Impala `hs2` port (default `21050`).

```java
// Maven: org.apache.hive:hive-jdbc (without the bundled Hive server jar)
String url = "jdbc:hive2://coordinator-host:21050/analytics;auth=noSasl";
try (Connection conn = DriverManager.getConnection(url, "impala_user", "");
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("select count(*) from fact_orders")) {
    rs.next();
    System.out.println("rows=" + rs.getLong(1));
}
```

The same HiveServer2 endpoint is reachable from Python with PyHive or `impyla` on port `21050`.

[Table of Contents](#Apache-Impala)

## Is Avro supported?
Yes, Avro is supported. Impala has always been able to query Avro tables. You can use the Impala `LOAD DATA` statement to move existing Avro data files into a table. Starting with Impala 1.4, you can create Avro tables with Impala. Impala cannot write Avro data, so there is no `INSERT` or `CREATE TABLE AS SELECT` into an Avro table: to copy data from another table, run the `INSERT` in Hive (or Spark) and then `REFRESH` the table in Impala. Avro tables also cannot contain `TIMESTAMP` columns; store time as a `STRING` or `BIGINT` instead.

```sql
create table analytics.events_avro (
  event_id string,
  event_ts string,   -- Avro tables cannot have TIMESTAMP columns
  payload string
)
stored as avro;

load data inpath '/data/events/2026-10-04' into table analytics.events_avro;
```

Avro is a row format, so it is a reasonable landing/streaming format but a poor choice for large analytical scans. Convert Avro to Parquet for curated tables with `create table ... stored as parquet as select ...`.

[Table of Contents](#Apache-Impala)

## How do I Know how many Impala Nodes are in my cluster?
The Impala statestore keeps track of how many `impalad` nodes are currently available. You can see this information through the statestore web interface. For example, at the URL `http://statestore_host:25010/metrics` you might see lines like the following:

```text
statestore.live-backends: 3
statestore.live-backends.list: [host1:22000, host1:26000, host2:22000]
```

The number of `impalad` nodes is the number of list items referring to port 22000, in this case two. (Typically, this number is one less than the number reported by the `statestore.live-backends` line.) If an `impalad` node became unavailable or came back after an outage, the information reported on this page would change appropriately.

[Table of Contents](#Apache-Impala)

## Are results returned as they become available or all at once when a query completes?
Impala streams results whenever they are available, when possible. Certain SQL operations (aggregation or ORDER BY) require all of the input to be ready before Impala can return results.

Practical consequence: a `select ... limit 10` over a large table can paint the first rows quickly, while `group by` over the same table must finish its aggregation phase before returning anything. BI tools that show partial results therefore benefit from projection and filter pushdown rather than from LIMIT tricks.

[Table of Contents](#Apache-Impala)

## Why does my select statement fail?
When a SELECT statement fails, the cause usually falls into one of the following categories:

+ A timeout because of a performance, capacity, or network issue affecting one particular node.
+ Excessive memory use for a join query, resulting in automatic cancellation of the query.
+ A low-level issue affecting how native code is generated on each node to handle particular WHERE clauses in the query. For example, a machine instruction could be generated that is not supported by the processor of a certain node. If the error message in the log suggests the cause was an illegal instruction, consider turning off native code generation temporarily, and trying the query again.
+ Malformed input data, such as a text data file with an enormously long line, or with a delimiter that does not match the character specified in the `FIELDS TERMINATED BY` clause of the CREATE TABLE statement.

Diagnose with the query profile rather than guessing:

[Table of Contents](#Apache-Impala)

## Why does my insert statement fail?
When an INSERT statement fails, it is usually the result of exceeding some limit within a Hadoop component, typically HDFS.

An INSERT into a partitioned table can be a strenuous operation due to the possibility of opening many files and associated threads simultaneously in HDFS. Impala 1.1.1 includes some improvements to distribute the work more efficiently, so that the values for each partition are written by a single node, rather than as a separate data file from each node.

Certain expressions in the SELECT part of the INSERT statement can complicate the execution planning and result in an inefficient INSERT operation. Try to make the column data types of the source and destination tables match up, for example by doing `ALTER TABLE ... REPLACE COLUMNS` on the source table if necessary. Try to avoid CASE expressions in the SELECT portion, because they make the result values harder to predict than transferring a column unchanged or passing the column through a built-in function.

Be prepared to raise some limits in the HDFS configuration settings, either temporarily during the INSERT or permanently if you frequently run such INSERT statements as part of your ETL pipeline.

The resource usage of an INSERT statement can vary depending on the file format of the destination table. Inserting into a Parquet table is memory-intensive, because the data for each partition is buffered in memory until it reaches the configured file size, at which point the data file is written to disk. Impala can distribute the work for an INSERT more efficiently when statistics are available for the source table that is queried during the INSERT statement.

```sql
-- Control Parquet writer memory and output file size, then load a single year
set PARQUET_FILE_SIZE = 256m;
set NUM_SCANNER_THREADS = 8;

insert into analytics.fact_orders partition (year)
select order_id, customer_id, amount, year
from staging.orders_raw
where year = 2026;
```

[Table of Contents](#Apache-Impala)

## Does Impala performance improve as it is deployed to more hosts in a cluster in much the same way that Hadoop performance does?
Yes. Impala scales with the number of hosts. It is important to install Impala on all the DataNodes in the cluster, because otherwise some nodes must do remote reads to retrieve data not available for local reads. Data locality is an important architectural aspect for Impala performance.

Scaling is close to linear for scan-heavy queries, but not for every query shape: a broadcast join must copy the small side to every node, so adding nodes increases fan-out. Watch the `DataStreamSender`/`Exchange` rows in `explain` before assuming more nodes will help.

[Table of Contents](#Apache-Impala)

## Is the Hdfs Block Size reduced to achieve faster query results?
No. Impala does not make any changes to the HDFS or HBase data sets.

The default Parquet block size is relatively large (256 MB in Impala 2.0 and later; 1 GB in earlier releases). You can control the block size when creating Parquet files using the `PARQUET_FILE_SIZE` query option. The underlying HDFS block size stays whatever the cluster is configured for (commonly 128 MB), and Parquet files are simply written as multi-block files.

[Table of Contents](#Apache-Impala)

## Does Impala use caching?
Impala does not cache table data. It does cache some table and file metadata. Although queries might run faster on subsequent iterations because the data set was cached in the OS buffer cache, Impala does not explicitly control this.

Impala takes advantage of the HDFS caching feature in CDH. You can designate which tables or partitions are cached through the `CACHED` and `UNCACHED` clauses of the CREATE TABLE and ALTER TABLE statements. Impala can also take advantage of data that is pinned in the HDFS cache through the `hdfscacheadmin` command.

For object storage (S3/ADLS), OS cache pinning does not apply; use the storage layer's own cache or keep hot aggregates materialized in Kudu.

[Table of Contents](#Apache-Impala)

## What are the good use cases for Impala as opposed to Hive or Mapreduce?
Impala is well-suited to executing SQL queries for interactive exploratory analytics on large data sets. Hive and MapReduce are appropriate for very long running, batch-oriented tasks such as ETL.

Rules of thumb:

+ Impala: dashboards, ad-hoc SQL, BI extracts over Parquet/Kudu, sub-second to tens of seconds.
+ Hive on Tez/Spark: heavy ETL, complex multi-stage transformations, very large joins that must spill, jobs measured in minutes to hours.
+ MapReduce: legacy, rarely the right answer for new work.

[Table of Contents](#Apache-Impala)

## Is Mapreduce required for impala and will Impala continue to work as expected if Mapreduce is stopped?
Impala does not use MapReduce at all. It runs its own distributed query fragments inside `impalad` processes, so stopping MapReduce (or never installing it) does not affect Impala. Impala does depend on the Hive metastore, the HDFS NameNode, the statestore, and `catalogd`.

[Table of Contents](#Apache-Impala)

## Can Impala be used for complex event processing?
For example, in an industrial environment, many agents may generate large amounts of data. Can Impala be used to analyze this data, checking for notable changes in the environment?

Complex Event Processing (CEP) is usually performed by dedicated stream-processing systems. Impala is not a stream-processing system, as it most closely resembles a relational database. For continuous pattern detection, use Flink, Spark Structured Streaming, or Kafka Streams, and land the results where Impala can query them.

The common hybrid architecture is: stream engine writes micro-batches to Parquet/Kudu, Impala serves interactive SQL over the result.

[Table of Contents](#Apache-Impala)

## Is Impala intended to handle Real Time Queries in Low latency Applications or is it for ad Hoc Queries for the purpose of data exploration?
Ad-hoc queries are the primary use case for Impala. We anticipate it being used in many other situations where low-latency is required. Whether Impala is appropriate for any particular use-case depends on the workload, data size and query volume.

Kudu-backed tables extend Impala toward operational analytics: single-digit-millisecond key lookups and fast scans on the same table, which fits "real-time dashboards" better than pure HDFS Parquet.

[Table of Contents](#Apache-Impala)

## How does Impala compare to Hive and Pig?
Impala is different from Hive and Pig because it uses its own daemons that are spread across the cluster for queries. Because Impala does not rely on MapReduce, it avoids the startup overhead of MapReduce jobs, allowing Impala to return results in real time.

| Aspect | Impala | Hive | Pig |
|---|---|---|---|
| Execution | MPP daemons, no MR | Tez/Spark/MR | MR |
| Latency | seconds | seconds to minutes | minutes |
| Language | SQL | HiveQL | Pig Latin |
| Updates | Kudu, modern Parquet | ACID tables (Hive 3) | no |
| Best at | interactive SQL | ETL, batch | legacy scripting |

[Table of Contents](#Apache-Impala)

## Can I do transforms or add New functionality?
Impala adds support for UDFs in Impala 1.2. You can write your own functions in C++, or reuse existing Java-based Hive UDFs. The UDF support includes scalar functions and user-defined aggregate functions (UDAs). User-defined table functions (UDTFs) are not currently supported.

Impala does not currently support an extensible serialization-deserialization framework (SerDes), and so adding extra functionality to Impala is not as straightforward as for Hive or Pig.

[Table of Contents](#Apache-Impala)

## Can any Impala Query also be executed in Hive?
Yes. There are some minor differences in how some queries are handled, but Impala queries can also be completed in Hive. Impala SQL is a subset of HiveQL, with some functional limitations such as transforms. Going the other way is not guaranteed: Hive-only features such as lateral views with custom SerDes, ACID merge syntax variants, or complex Hive types may not run in Impala.

[Table of Contents](#Apache-Impala)

## Can I use Impala to Query data already loaded into Hive and Hbase?
There are no additional steps to allow Impala to query tables managed by Hive, whether they are stored in HDFS or HBase. Make sure that Impala is configured to access the Hive metastore correctly and you should be ready to go. Keep in mind that `impalad`, by default, runs as the `impala` user, so you might need to adjust some file permissions depending on how strict your permissions are currently.

[Table of Contents](#Apache-Impala)

## Is Hive an Impala requirement?
The Hive metastore service is a requirement. Impala shares the same metastore database as Hive, allowing Impala and Hive to access the same tables transparently.

Hive itself is optional, and does not need to be installed on the same nodes as Impala. Currently, Impala supports a wider variety of read (query) operations than write (insert) operations; you use Hive to insert data into tables that use certain file formats.

In practice, most clusters run both: Hive/Spark for the write-heavy ETL path and Impala for the read-heavy serving path, against the same metastore.

[Table of Contents](#Apache-Impala)

## Is Impala production ready?
Impala has finished its beta release cycle, and the 1.0, 1.1, and 1.2 GA releases are production ready. The 1.1.x series includes additional security features for authorization, an important requirement for production use in many organizations. The 1.2.x series includes important performance features, particularly for large join queries. Some Cloudera customers are already using Impala for large workloads.

The Impala 1.3.0 and higher releases are bundled with corresponding levels of CDH 5. The number of new features grows with each release. Modern Impala (CDP 7.x and Apache Impala 4.x) supports fine-grained authorization, runtime filters, Kudu upserts, complex types, and Iceberg/Hudi reads.

[Table of Contents](#Apache-Impala)

## How do I configure Hadoop High Availability for Impala?
You can set up a proxy server to relay requests back and forth to the Impala servers, for load balancing and high availability. In modern deployments, HA has three parts:

+ HDFS HA (NameNode failover) and YARN HA, configured at the Hadoop layer.
+ Impala statestore and catalogd HA, so metadata service survives a host loss.
+ A load balancer or proxy in front of the `impalad` `hs2`/`beeswax` ports so clients do not pin to one coordinator.

For JDBC clients, use the load-balanced hostname with the standard HiveServer2 URL so a coordinator restart does not break the application.

[Table of Contents](#Apache-Impala)

## What happens if there is an Error in Impala?
There is not a single point of failure in Impala. All Impala daemons are fully able to handle incoming queries. If a machine fails however, all queries with fragments running on that machine will fail. Because queries are expected to return quickly, you can just rerun the query if there is a failure.

The longer answer: Impala must be able to connect to the Hive metastore. Impala aggressively caches metadata so the metastore host should have minimal load. Impala relies on the HDFS NameNode, and, in CDH4, you can configure HA for HDFS. Impala also has centralized services, known as the statestore and catalog services, that run on one host only. Impala continues to execute queries if the statestore host is down, but it will not get state updates. For example, if a host is added to the cluster while the statestore host is down, the existing instances of `impalad` running on the other hosts will not find out about this new host. Once the statestore process is restarted, all the information it serves is automatically reconstructed from all running Impala daemons.

If `catalogd` is down, DDL still works locally but metadata changes are not broadcast, so other coordinators may plan against stale metadata until it recovers. Monitor `catalog.ready` on the catalogd metrics endpoint.

[Table of Contents](#Apache-Impala)

## What is the Maximum number of Rows in a Table?
There is no defined maximum. Some customers have used Impala to query a table with over a trillion rows. Practical limits are metadata planning time and file count, not row count: a table with millions of tiny files becomes slow to plan regardless of how few rows each file holds.

[Table of Contents](#Apache-Impala)

## On which hosts does Impala run?
Cloudera strongly recommends running the `impalad` daemon on each DataNode for good performance. Although this topology is not a hard requirement, if there are data blocks with no Impala daemons running on any of the hosts containing replicas of those blocks, queries involving that data could be very inefficient. In that case, the data must be transmitted from one host to another for processing by "remote reads", a condition Impala normally tries to avoid.

For object storage (S3/ADLS) there is no data locality to preserve, so `impalad` placement is driven by network proximity to the storage endpoint and by CPU/memory capacity. Dedicated coordinator nodes separate client-facing planning from worker scanning.

[Table of Contents](#Apache-Impala)

## How are Joins performed in Impala?
By default, Impala automatically determines the most efficient order in which to join tables using a cost-based method, based on their overall size and number of rows. (This is a new feature in Impala 1.2.2 and higher.) The COMPUTE STATS statement gathers information about each table that is crucial for efficient join performance. Impala chooses between two techniques for join queries, known as "broadcast joins" and "partitioned joins".

+ **Broadcast join (default for a small side):** the small table is sent to every node, and each node joins it with its local slice of the large table. Fast when the small side fits comfortably in memory; disastrous when it does not.
+ **Partitioned (shuffle) join:** both sides are hash-partitioned on the join key, so matching rows land on the same node. Scales to two large tables but pays network and disk cost.

```sql
-- Force a broadcast of the small dimension (only when it is genuinely small)
select /* +BROADCAST */ ...
from analytics.fact_orders o
join analytics.dim_region r on o.region_id = r.region_id;

-- Force a shuffle/partitioned join for two large tables
select /* +SHUFFLE */ ...
from analytics.fact_orders o
join analytics.fact_returns r on o.order_id = r.order_id;

-- Let the optimizer decide, but give it good statistics
compute stats analytics.fact_orders;
compute stats analytics.dim_region;
```

Interview point: hints override the planner, so use them to fix a *known* bad plan, not as a default. Runtime filters (Impala 2.5+) let a broadcast build side filter the probe side automatically.

[Table of Contents](#Apache-Impala)

## How does Impala process Join Queries for large tables?
Impala utilizes multiple strategies to allow joins between tables and result sets of various sizes. When joining a large table with a small one, the data from the small table is transmitted to each node for intermediate processing. When joining two large tables, the data from one of the tables is divided into pieces, and each node processes only selected pieces.

The plan is visible in `explain`:

`PARTITIONED` means a shuffle; `BROADCAST` means the right-hand side was replicated. If a plan shows `BROADCAST` on a table with hundreds of millions of rows, that is the bug to fix first.

[Table of Contents](#Apache-Impala)

## What is Impala's aggregation strategy?
Impala currently only supports in-memory hash aggregation. In Impala 2.0 and higher, if the memory requirements for a join or aggregation operation exceed the memory limit for a particular host, Impala uses a temporary work area on disk to help the query complete successfully.

Two-phase aggregation reduces the size of the shuffle: partial aggregation happens where the scan runs, then final aggregation happens after the exchange.

Prefer `count(distinct ...)` on a low-cardinality column, and pre-aggregate high-cardinality GROUP BYs upstream in Spark/ETL when the grouping set is huge.

[Table of Contents](#Apache-Impala)

## How is Impala Metadata managed?
Impala uses two pieces of metadata: the catalog information from the Hive metastore and the file metadata from the NameNode. Currently, this metadata is lazily populated and cached when an `impalad` needs it to plan a query.

The `REFRESH` statement updates the metadata for a particular table after loading new data through Hive. The `INVALIDATE METADATA` statement refreshes all metadata, so that Impala recognizes new tables or other DDL and DML changes performed through Hive.

In Impala 1.2 and higher, a dedicated `catalogd` daemon broadcasts metadata changes due to Impala DDL or DML statements to all nodes, reducing or eliminating the need to use the `REFRESH` and `INVALIDATE METADATA` statements.

[Table of Contents](#Apache-Impala)

## What load do concurrent queries produce on the Name Node?
The load Impala generates is very similar to MapReduce. Impala contacts the NameNode during the planning phase to get the file metadata (this is only run on the host the query was sent to). Every `impalad` will read files as part of normal processing of the query.

With many small files, NameNode load and planning latency both rise sharply. Partition pruning reduces the directories touched, and periodic compaction keeps the file count and therefore the NameNode RPC volume manageable.

[Table of Contents](#Apache-Impala)

## How does Impala achieve its performance improvements?
These are the main factors in the performance of Impala versus that of other Hadoop components and related technologies.

Impala avoids MapReduce. While MapReduce is a great general parallel processing model with many benefits, it is not designed to execute SQL. Impala avoids the inefficiencies of MapReduce in these ways:

+ Impala does not materialize intermediate results to disk. SQL queries often map to multiple MapReduce jobs with all intermediate data sets written to disk.
+ Impala avoids MapReduce start-up time. For interactive queries, the MapReduce start-up time becomes very noticeable. Impala runs as a service and essentially has no start-up time.
+ Impala can more naturally disperse query plans instead of having to fit them into a pipeline of map and reduce jobs. This enables Impala to parallelize multiple stages of a query and avoid overheads such as sort and shuffle when unnecessary.

Impala uses a more efficient execution engine by taking advantage of modern hardware and technologies:

+ Impala generates runtime code. Impala uses LLVM to generate assembly code for the query that is being run. Individual queries do not have to pay the overhead of running on a system that needs to be able to execute arbitrary queries.
+ Impala uses available hardware instructions when possible. Impala uses the supplemental SSE3 (SSSE3) instructions which can offer tremendous speedups in some cases. (Impala 2.0 and 2.1 required the SSE4.1 instruction set; Impala 2.2 and higher relax the restriction again so only SSSE3 is required.)
+ Impala uses better I/O scheduling. Impala is aware of the disk location of blocks and is able to schedule the order to process blocks to keep all disks busy.
+ Impala is designed for performance. A lot of time has been spent in designing Impala with sound performance-oriented fundamentals, such as tight inner loops, inlined function calls, minimal branching, better use of cache, and minimal memory usage.

Modern additions on top of the classic list: runtime filters, codegen for Parquet scanning with dictionary/filter pushdown, and the columnar memory layout shared with Kudu.

[Table of Contents](#Apache-Impala)

## What happens when the data set exceeds available memory?
Currently, if the memory required to process intermediate results on a node exceeds the amount available to Impala on that node, the query is cancelled. You can adjust the memory available to Impala on each node, and you can fine-tune the join strategy to reduce the memory required for the biggest queries. We do plan on supporting external joins and sorting in the future.

Keep in mind though that the memory usage is not directly based on the input data set size. For aggregations, the memory usage is the number of rows after grouping. For joins, the memory usage is the combined size of the tables excluding the biggest table, and Impala can use join strategies that divide up large joined tables among the various nodes rather than transmitting the entire table to each node.

If a broadcast join repeatedly exceeds memory, force a shuffle join or pre-aggregate the build side.

[Table of Contents](#Apache-Impala)

## What are the most Memory intensive operations?
If a query fails with an error indicating "memory limit exceeded", you might suspect a memory leak. The problem could actually be a query that is structured in a way that causes Impala to allocate more memory than you expect, exceeded the memory allocated for Impala on a particular node. Some examples of query or table structures that are especially memory-intensive are:

+ INSERT statements using dynamic partitioning, into a table with many different partitions. (Particularly for tables using Parquet format, where the data for each partition is held in memory until it reaches the full block size in size before it is written to disk.) Consider breaking up such operations into several different INSERT statements, for example to load one year at a time rather than for all years at once.
+ GROUP BY on a unique or high-cardinality column. Impala allocates some handler structures for each different value in a GROUP BY query. Having millions of different GROUP BY values could exceed the memory limit.
+ Queries involving very wide tables, with thousands of columns, particularly with many STRING columns. Because Impala allows a STRING value to be up to 32 KB, the intermediate results during such queries could require substantial memory allocation.

[Table of Contents](#Apache-Impala)

## When does Impala hold on to or return memory?
Impala allocates memory using `tcmalloc`, a memory allocator that is optimized for high concurrency. Once Impala allocates memory, it keeps that memory reserved to use for future queries. Thus, it is normal for Impala to show high memory usage when idle. If Impala detects that it is about to exceed its memory limit (defined by the `-mem_limit` startup option or the `MEM_LIMIT` query option), it deallocates memory not needed by the current queries.

When issuing queries through the JDBC or ODBC interfaces, make sure to call the appropriate close method afterwards. Otherwise, some memory associated with the query is not freed.

[Table of Contents](#Apache-Impala)

## Is there an update statement?
Impala historically did not have an UPDATE statement, because HDFS files are optimized for bulk operations across many megabytes of data at a time, making traditional single-row UPDATE operations inefficient or impractical.

You can use the following techniques to achieve the same goals as the familiar UPDATE statement, in a way that preserves efficient file layouts for subsequent queries:

+ Replace the entire contents of a table or partition with updated data that you have already staged in a different location, either using `INSERT OVERWRITE`, `LOAD DATA`, or manual HDFS file operations followed by a `REFRESH` statement for the table. Optionally, you can use built-in functions and expressions in the INSERT statement to transform the copied data in the same way you would normally do in an UPDATE statement, for example to turn a mixed-case string into all uppercase or all lowercase.
+ To update a single row, use an HBase table, and issue an `INSERT ... VALUES` statement using the same key as the original row. Because HBase handles duplicate keys by only returning the latest row with a particular key value, the newly inserted row effectively hides the previous one.
+ To update rows at scale, use a Kudu table, which supports real `UPDATE` and `DELETE` with primary keys.

```sql
-- Bulk "update" by overwriting one partition
insert overwrite analytics.fact_orders partition (order_date = '2026-10-04')
select order_id, customer_id, upper(status) as status, amount
from staging.orders_fixed
where order_date = '2026-10-04';

-- True row-level update on a Kudu table
update analytics.customer_kudu
set tier = 'platinum', updated_at = now()
where customer_id = 1001;
```

[Table of Contents](#Apache-Impala)

## Can Impala do User defined functions?
Impala 1.2 and higher does support UDFs and UDAs. You can either write native Impala UDFs and UDAs in C++, or reuse UDFs (but not UDAs) originally written in Java for use with Hive.

Reusing Hive Java UDFs is common during migration because the jar already exists in the cluster. Keep UDFs small and side-effect free; they run in the query hot path on every node.

[Table of Contents](#Apache-Impala)

## Why do I have to use refresh and invalidate Metadata and what do they do?
In Impala 1.2 and higher, there is much less need to use the `REFRESH` and `INVALIDATE METADATA` statements:

+ The new `impala-catalog` service, represented by the `catalogd` daemon, broadcasts the results of Impala DDL statements to all Impala nodes. Thus, if you do a CREATE TABLE statement in Impala while connected to one node, you do not need to do INVALIDATE METADATA before issuing queries through a different node.
+ The catalog service only recognizes changes made through Impala, so you must still issue a `REFRESH` statement if you load data through Hive or by manipulating files in HDFS, and you must issue an `INVALIDATE METADATA` statement if you create a table, alter a table, add or drop partitions, or do other DDL statements in Hive.
+ Because the catalog service broadcasts the results of `REFRESH` and `INVALIDATE METADATA` statements to all nodes, in the cases where you do still need to issue those statements, you can do that on a single node rather than on every node, and the changes will be automatically recognized across the cluster, making it more convenient to load balance by issuing queries through arbitrary Impala nodes rather than always using the same coordinator node.

The distinction to remember: `REFRESH` re-reads data/file metadata for known tables, while `INVALIDATE METADATA` re-reads catalog structure (tables, columns, partitions). Use the narrowest one that fixes the problem.

```sql
-- External writer added files to an existing partition
refresh analytics.fact_orders partition (order_date = '2026-10-04');

-- External writer created a brand new table
invalidate metadata analytics.new_table;
```

[Table of Contents](#Apache-Impala)

## Why is space not freed up when I issue drop table?
Impala deletes data files when you issue a DROP TABLE on an internal table, but not an external one. By default, the CREATE TABLE statement creates internal tables, where the files are managed by Impala. An external table is created with a CREATE EXTERNAL TABLE statement, where the files reside in a location outside the control of Impala. Issue a `DESCRIBE FORMATTED` statement to check whether a table is internal or external. The keyword `MANAGED_TABLE` indicates an internal table, from which Impala can delete the data files. The keyword `EXTERNAL_TABLE` indicates an external table, where Impala will leave the data files untouched when you drop the table.

Even when you drop an internal table and the files are removed from their original location, you might not get the hard drive space back immediately. Deleted HDFS files normally go into a trashcan directory and are purged only after the configured `fs.trash.interval` (the trashcan is disabled by default in Apache Hadoop, value `0`; many distributions enable it and set an interval). Use `DROP TABLE ... PURGE` to skip the trashcan and delete immediately.

For external tables the safe cleanup is: drop the table, then remove the HDFS path explicitly once you are certain nothing else references it.

[Table of Contents](#Apache-Impala)

## Is there a dual table?
You might be used to running queries against a single-row table named DUAL to try out expressions, built-in functions, and UDFs. Impala does not have a DUAL table. To achieve the same result, you can issue a SELECT statement without any table name:

```sql
select 2 + 2;
select substr('hello', 2, 1);
select pow(10, 6);
```

[Table of Contents](#Apache-Impala)

## How do I load a big Csv file into a partitioned table?
To load a data file into a partitioned table, when the data file includes fields like year, month, and so on that correspond to the partition key columns, use a two-stage process. First, use the `LOAD DATA` or `CREATE EXTERNAL TABLE` statement to bring the data into an unpartitioned text table. Then use an `INSERT ... SELECT` statement to copy the data from the unpartitioned table to a partitioned one. Include a `PARTITION` clause in the INSERT statement to specify the partition key columns.

```sql
-- Stage 1: land the raw CSV as an external text table
create external table staging.orders_csv (
  order_id string,
  customer_id string,
  amount string,
  order_date string
)
row format delimited fields terminated by ','
location '/data/incoming/orders/2026-10-04/';

-- Stage 2: typed, partitioned, columnar target
create table analytics.fact_orders (
  order_id bigint,
  customer_id bigint,
  amount decimal(12,2)
)
partitioned by (order_date date)
stored as parquet;

-- Dynamic partition insert: one pass, one directory per date
set num_dynamic_partitions = 366;
insert into analytics.fact_orders partition (order_date)
select cast(order_id as bigint), cast(customer_id as bigint),
       cast(amount as decimal(12,2)), cast(order_date as date)
from staging.orders_csv;

compute stats analytics.fact_orders;
```

For very large files, load in date ranges to keep the number of open files and the memory for dynamic partitions under control.

[Table of Contents](#Apache-Impala)

## Can I Do Insert Select Into a partitioned table?
When you use the `INSERT ... SELECT *` syntax to copy data into a partitioned table, the columns corresponding to the partition key columns must appear last in the columns returned by the `SELECT *`. You can create the table with the partition key columns defined last. Or, you can use the CREATE VIEW statement to create a view that reorders the columns: put the partition key columns last, then do the `INSERT ... SELECT *` from the view.

Explicit column lists are clearer and avoid the ordering trap entirely:

```sql
insert into analytics.fact_orders (order_id, customer_id, amount, order_date)
select order_id, customer_id, amount, order_date
from staging.orders_clean;
```

[Table of Contents](#Apache-Impala)

## What kinds of Impala Queries or data are best suited for Hbase?
HBase tables are ideal for queries where normally you would use a key-value store. That is, where you retrieve a single row or a few rows, by testing a special unique key column using the `=` or `IN` operators.

HBase tables are not suitable for queries that produce large result sets with thousands of rows. HBase tables are also not suitable for queries that perform full table scans because the WHERE clause does not request specific values from the unique key column.

Use HBase tables for data that is inserted one row or a few rows at a time, such as by the `INSERT ... VALUES` syntax. Loading data piecemeal like this into an HDFS-backed table produces many tiny files, which is a very inefficient layout for HDFS data files.

If the lack of an UPDATE statement in Impala is a problem for you, you can simulate single-row updates by doing an `INSERT ... VALUES` statement using an existing value for the key column. The old row value is hidden; only the new row value is seen by queries.

HBase tables are often wide (containing many columns) and sparse (with most column values NULL). For example, you might record hundreds of different data points for each user of an online service, such as whether the user had registered for an online game or enabled particular account features. With Impala and HBase, you could look up all the information for a specific customer efficiently in a single query. For any given customer, most of these columns might be NULL, because a typical customer might not make use of most features of an online service.

For new designs, Kudu usually replaces HBase for this pattern because it offers the same key lookups with better scan performance and real UPDATE/DELETE.

[Table of Contents](#Apache-Impala)

## When would you use Impala instead of Hive?
Impala is designed for low-latency interactive SQL over data in HDFS/object storage, while classic Hive was historically more batch-oriented. Use Impala when analysts need faster ad-hoc exploration over curated Parquet tables. Use Hive/Spark for heavier ETL, complex transformations, or workloads where latency is less important.

Example:

+ Impala: dashboard query over partitioned Parquet fact table
+ Spark/Hive: daily transformation that rewrites a large derived table

Impala performance depends heavily on file format, partitions, statistics, and avoiding tiny files.

[Table of Contents](#Apache-Impala)

## How do you optimize Impala queries?
Use Parquet, collect table/column statistics, filter partition columns, avoid tiny files, and check the query profile for scan and join bottlenecks. Join order and broadcast vs partitioned joins can matter for large tables.

Example:

```sql
compute stats fact_orders;
```

Statistics help the optimizer estimate cardinality and choose better join plans.

A practical checklist:

+ Project only needed columns; Impala is columnar, so `select *` on a wide table is expensive.
+ Filter on partition columns so partitions are pruned.
+ Run `COMPUTE STATS` (or `COMPUTE INCREMENTAL STATS`) after loads.
+ Watch for `BROADCAST` joins on large tables and for exchange row counts in `explain`.
+ Compact small files and keep files in the 128-512 MB range.
+ Use `COMPUTE STATS` on both sides of a join, not just the large table.

[Table of Contents](#Apache-Impala)

## How do you create Impala tables with DDL and choose a file format?
Impala DDL is Hive-compatible; the key choices are internal vs external, file format, and partition layout.

```sql
create table if not exists analytics.fact_orders (
  order_id bigint, customer_id bigint, status string,
  amount decimal(12,2), order_ts timestamp
)
partitioned by (order_date date)
stored as parquet
tblproperties ('parquet.compression' = 'snappy');

create external table if not exists analytics.orders_ext (
  order_id bigint, customer_id bigint, amount decimal(12,2)
)
partitioned by (order_date date)
stored as parquet
location '/warehouse/analytics/orders_ext';

-- Change compression for future writes
alter table analytics.fact_orders set tblproperties ('parquet.compression' = 'zstd');
```

Format guidance: Parquet for analytical scans, ORC where the cluster is Hive-centric, Avro/Text for landing only, and Kudu for mutable key-addressable tables.

[Table of Contents](#Apache-Impala)

## How do you create partitioned tables and manage partitions in Impala?
Partitioning is the highest-leverage decision in Impala because it enables partition pruning, so a date-filtered query reads only matching directories.

```sql
create table analytics.fact_events (
  event_id bigint, user_id bigint, event_ts timestamp, payload string
)
partitioned by (event_month string, event_day string)
stored as parquet;

alter table analytics.fact_events
  add partition (event_month = '2026-10', event_day = '2026-10-04');

set num_dynamic_partitions = 400;
insert into analytics.fact_events partition (event_month, event_day)
select event_id, user_id, event_ts, payload,
       date_format(event_ts, 'yyyy-MM'), date_format(event_ts, 'yyyy-MM-dd')
from staging.events_raw;

alter table analytics.fact_events drop partition (event_month = '2025-01');
```

Keep partition count in the thousands, not millions, and never partition by a high-cardinality key such as `user_id` or a raw timestamp.

[Table of Contents](#Apache-Impala)

## How do COMPUTE STATS and INVALIDATE METADATA drive Impala query plans?
Impala's optimizer is cost-based, so it needs statistics to choose join order and strategy. Without them it guesses, which is the root cause of most "Impala picked a terrible plan" incidents.

```sql
compute stats analytics.fact_orders;
compute incremental stats analytics.fact_orders partition (order_date = '2026-10-04');
show table stats analytics.fact_orders;
show column stats analytics.fact_orders;
refresh analytics.fact_orders;
invalidate metadata analytics.fact_orders;
```

`REFRESH` re-reads data/file metadata; `INVALIDATE METADATA` re-reads catalog structure. Scope `INVALIDATE METADATA` to one table and run it off-peak, because it is expensive at the NameNode.

[Table of Contents](#Apache-Impala)

## How do you read an Impala EXPLAIN plan and tune joins and hints?
`EXPLAIN` shows the physical plan with estimates; `profile` shows what actually happened. Read them together.

```sql
explain
select c.region, count(*) as orders, sum(o.amount) as revenue
from analytics.fact_orders o
join analytics.dim_customer c on o.customer_id = c.customer_id
where o.order_date >= '2026-10-01'
group by c.region;
```

What to look for: `PARTITION RANGE` proves pruning is working; `HASH JOIN [BROADCAST]` on a large right side is the classic memory/network mistake; `EXCHANGE` rows quantify network cost; estimate-vs-actual gaps mean stale statistics.

```sql
select /* +BROADCAST */ ... from small_dim d join big_fact f on d.id = f.dim_id;
select /* +SHUFFLE */    ... from big_fact a join big_fact_b b on a.k = b.k;
select /* +STRAIGHT_JOIN */ ... from dim d join fact f on d.id = f.dim_id;
set runtime_filter_mode = global;   -- global | per_node | off
```

[Table of Contents](#Apache-Impala)

## How do you use Parquet and Kudu tables in Impala?
Parquet is the immutable, cheap-to-scan columnar format for facts; Kudu is the mutable, primary-key store for dimensions and operational lookups.

```sql
create table analytics.customer_kudu (
  customer_id bigint, name string, tier string, updated_at timestamp,
  primary key (customer_id)
)
partition by hash (customer_id) partitions 16
stored as kudu;

upsert into analytics.customer_kudu (customer_id, name, tier, updated_at)
values (1001, 'Ada Lovelace', 'gold', now());

update analytics.customer_kudu set tier = 'platinum' where customer_id = 1001;
delete from analytics.customer_kudu where customer_id = 1002;
```

Choose Kudu for upserts and millisecond key lookups, and Parquet when you need the cheapest large-scale scans.

[Table of Contents](#Apache-Impala)

## How do Impala resource pools and admission control work?
Admission control decides whether a query starts immediately, waits in a queue, or is rejected. It is configured per resource pool and enforced by `impalad`.

```text
<queue name="root">
  <queue name="bi">
    <maxResources>40000 mb</maxResources>
    <maxRunningApps>20</maxRunningApps>
  </queue>
  <queue name="etl">
    <maxResources>80000 mb</maxResources>
    <maxRunningApps>5</maxRunningApps>
  </queue>
</queue>
```

```sql
set request_pool = 'bi';
set mem_limit = 16gb;
-- Check retries/attempts in the runtime profile (impala-shell `PROFILE`, or the query profile UI)
```

Give interactive BI a shallow, small-memory pool so a huge ETL query cannot block dashboards, and use `mem_limit` as a second per-query cap.

[Table of Contents](#Apache-Impala)

## How do you handle small files and table maintenance in Impala?
Small files are the most common Impala performance problem. Each file adds planning and open cost, and thousands of tiny files per partition slow the NameNode and every scan.

```sql
set PARQUET_FILE_SIZE = 512m;
insert overwrite analytics.fact_orders partition (order_date = '2026-10-04')
select order_id, customer_id, status, amount, order_ts
from analytics.fact_orders where order_date = '2026-10-04';

refresh analytics.fact_orders partition (order_date = '2026-10-04');
compute stats analytics.fact_orders;
```

Prevention beats cleanup: land 128-512 MB files from Spark/Hive and prefer partition overwrite over many tiny appends.

[Table of Contents](#Apache-Impala)

## What are Impala's trade-offs and when should you not use it?
+ **Performance:** extremely fast for MPP scans and joins over Parquet/Kudu, but not a transactional warehouse; no multi-statement transactions, and heavy ETL belongs on Spark.
+ **Resource contention:** memory-hungry. Broadcast joins and high-cardinality aggregations can exhaust a node, so admission control and `mem_limit` are mandatory.
+ **Exactly-once / mutability:** plain Parquet cannot do single-row updates, so use `INSERT OVERWRITE` of a partition as the idempotent pattern; Kudu adds upserts but also an operational component.
+ **Concurrency:** dozens to low hundreds of concurrent queries are fine, thousands are not.

When NOT to use Impala: OLTP writes (use PostgreSQL/Kudu-backed services), long multi-stage shuffles (Spark/Hive/Tez), sub-second stateful streaming (Flink), and text search (a search engine).

[Table of Contents](#Apache-Impala)

## Real world use cases for Apache Impala

### 1. Interactive BI over a partitioned Parquet lake

A retailer's analysts query three years of orders because Hive reports take minutes. ~2 PB in HDFS, ~4 billion rows, daily partitions. Spark writes Parquet; Impala serves Hue/Tableau; `catalogd` broadcasts metadata after ETL.

```sql
compute stats analytics.fact_orders;

select order_date, sum(amount) as revenue
from analytics.fact_orders
where order_date between '2026-09-01' and '2026-09-30'
group by order_date order by order_date;
```

Why: pruning keeps a month-scoped query off 97% of the data, and statistics let the optimizer choose a sane plan without hints.

### 2. Operational dimension store on Kudu

A subscription product needs a customer table updated continuously by a service while analysts join it from SQL. ~50 million customers, ~20k upserts/minute. The service writes Kudu; Parquet facts join the Kudu dimension.

```sql
upsert into analytics.dim_customer (customer_id, email, plan, updated_at)
values (1001, 'ada@example.com', 'pro', now());

select customer_id, plan from analytics.dim_customer where customer_id = 1001;
```

Why: primary-key upserts and millisecond lookups, plus SQL access to the same mutable table without a second copy.

### 3. Ad-hoc exploration for a data science team

Data scientists slice clickstream data without waiting for Spark scheduling. ~800 TB, ~120 billion events, hourly partitions on the busiest flows, a dedicated pool, nightly compaction.

```sql
set request_pool = 'ds_ad_hoc';
set mem_limit = 32gb;

select device_type, country, count(*) as events
from analytics.fact_events
where event_date = '2026-10-04' and event_hour between '09' and '17'
group by device_type, country order by events desc limit 50;
```

Why: an isolated pool stops one exploratory query blocking BI, and hour-level pruning makes a huge table interactive.

### 4. Log analytics with HBase for sparse lookups

A support tool fetches all attributes for one user from a wide, sparse profile table. ~300 million profiles with hundreds of optional columns. HBase holds the profile; Impala serves key lookups and Parquet serves dashboards.

```sql
select customer_id, registered_at, last_login, loyalty_tier
from hbase.customer_profile
where customer_id = 'C-884422';
```

Why: HBase suits a few rows by key with a sparse schema, while full-scan analytics stays on columnar Parquet.

### 5. Migrating Hive batch reports to interactive SQL

A telco wants on-demand versions of years of Hive reports. ~500 TB of ORC/Parquet. Hive/Spark stays the ETL writer, Impala coordinators share its metastore, and metadata is refreshed after each ETL run.

```sql
refresh analytics.monthly_revenue;
compute stats analytics.monthly_revenue;
select * from analytics.monthly_revenue where month = '2026-09' order by revenue desc limit 20;
```

Why: reusing the metastore avoids duplicating data, and `REFRESH` plus `COMPUTE STATS` keeps Impala correct without a migration project.

[Table of Contents](#Apache-Impala)
