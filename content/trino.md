## [Main title](../README.md)
### [Interview questions](full.md)

# Trino and Presto

**Notebook:** [`notebooks/topics/trino.ipynb`](../notebooks/topics/trino.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is Trino and how is it architected?](#What-is-Trino-and-how-is-it-architected)
+ [How do catalogs and connectors work in Trino?](#How-do-catalogs-and-connectors-work-in-Trino)
+ [How do you configure the lakehouse connectors?](#How-do-you-configure-the-lakehouse-connectors)
+ [How do you query operational databases and warehouses?](#How-do-you-query-operational-databases-and-warehouses)
+ [How do you query Kafka from Trino?](#How-do-you-query-Kafka-from-Trino)
+ [How do you run federated queries across catalogs?](#How-do-you-run-federated-queries-across-catalogs)
+ [How does query planning work and how do you read EXPLAIN?](#How-does-query-planning-work-and-how-do-you-read-EXPLAIN)
+ [How do predicate and projection pushdown work?](#How-do-predicate-and-projection-pushdown-work)
+ [How do broadcast partitioned and dynamic-filter joins work?](#How-do-broadcast-partitioned-and-dynamic-filter-joins-work)
+ [How does the cost-based optimizer use statistics and ANALYZE?](#How-does-the-cost-based-optimizer-use-statistics-and-ANALYZE)
+ [How does spill to disk work?](#How-does-spill-to-disk-work)
+ [How do you manage memory and resource groups?](#How-do-you-manage-memory-and-resource-groups)
+ [How does Trino handle fault tolerance and retries?](#How-does-Trino-handle-fault-tolerance-and-retries)
+ [Which session properties are most useful for tuning?](#Which-session-properties-are-most-useful-for-tuning)
+ [How do you secure Trino with authentication access control and masking?](#How-do-you-secure-Trino-with-authentication-access-control-and-masking)
+ [How do you write data with CTAS and INSERT?](#How-do-you-write-data-with-CTAS-and-INSERT)
+ [What connector-specific write limits should you know?](#What-connector-specific-write-limits-should-you-know)
+ [How does Trino compare with Presto Spark SQL and Hive?](#How-does-Trino-compare-with-Presto-Spark-SQL-and-Hive)
+ [Real world use cases for Trino and Presto](#Real-world-use-cases-for-Trino-and-Presto)

## What is Trino and how is it architected?
Trino is a distributed MPP SQL engine for interactive analytics, forked from PrestoSQL, which came out of the Facebook Presto project. Trino stores no data of its own: it reads from connectors, plans a distributed query, and streams results back.

+ **Coordinator** - parses SQL, resolves names against catalogs, builds and optimizes the plan, splits work into stages, schedules tasks, and tracks query state. Exactly one per cluster.
+ **Workers** - execute tasks, read splits from connectors, exchange intermediate rows, and return results. Scale horizontally.
+ **Discovery service** - workers register their HTTP URLs so the coordinator can schedule onto them. Embedded in the coordinator by default.
+ **Connectors** - per-catalog plugins that expose metadata and read/write APIs over underlying systems.

```text
config.properties (coordinator)
coordinator=true
node-scheduler.include-coordinator=false
http-server.http.port=8080
discovery.uri=http://trino-coordinator:8080
query.max-memory=100GB
query.max-memory-per-node=16GB
```

```text
config.properties (worker)
coordinator=false
http-server.http.port=8080
discovery.uri=http://trino-coordinator:8080
```

A query flows as client -> coordinator (plan) -> stages -> tasks -> splits -> workers -> exchange -> client. Trino pipelines data in memory and streams results, which is why first rows return quickly on interactive queries.

[Table of Contents](#Trino-and-Presto)

## How do catalogs and connectors work in Trino?
A catalog is a named connection to a data source, backed by exactly one connector. Queries use three-part names: `catalog.schema.table`. Catalogs are files in `etc/catalog/`, and the file name becomes the catalog name.

```text
etc/catalog/iceberg.properties   ->  iceberg.analytics.orders
etc/catalog/postgres.properties  ->  postgres.public.customers
etc/catalog/kafka.properties     ->  kafka.acme.events
```

```sql
SHOW CATALOGS;
SHOW SCHEMAS FROM iceberg;
SHOW TABLES FROM iceberg.analytics;
DESCRIBE iceberg.analytics.orders;

SELECT * FROM system.metadata.catalogs;
```

Practical rules: use one catalog per physical source rather than one per team; assume a connector may be read-only (Kafka) or fully writable (Iceberg); and remember that connectors differ in pushdown capability, so the same SQL can cost very different amounts per catalog.

[Table of Contents](#Trino-and-Presto)

## How do you configure the lakehouse connectors?
The Iceberg, Delta Lake, and Hive connectors cover most lakehouse data. All three use `.properties` files, and the same catalog can be described declaratively in a Helm values file.

```text
etc/catalog/iceberg.properties
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=https://catalog.acme.internal
iceberg.rest-catalog.warehouse=s3://acme-warehouse/
fs.native-s3.enabled=true
s3.region=us-east-1
```

```text
etc/catalog/delta.properties
connector.name=delta_lake
hive.metastore.uri=thrift://hive-metastore:9083
fs.native-s3.enabled=true
s3.region=us-east-1
```

```text
etc/catalog/hive.properties
connector.name=hive
hive.metastore.uri=thrift://hive-metastore:9083
hive.parquet.use-column-names=true
hive.orc.use-column-names=true
hive.max-split-size=128MB
```

```yaml
# values.yaml for the Trino Helm chart: catalogs declared as YAML
additionalCatalogs:
  iceberg: |
    connector.name=iceberg
    iceberg.catalog.type=hive_metastore
    hive.metastore.uri=thrift://hive-metastore:9083
    fs.native-s3.enabled=true
```

```sql
CREATE TABLE iceberg.analytics.orders (
  order_id     bigint,
  customer_id  bigint,
  order_ts     timestamp(6),
  status       varchar,
  amount       decimal(18, 2)
)
WITH (
  format = 'PARQUET',
  partitioning = ARRAY['day(order_ts)', 'bucket(customer_id, 16)']
);

-- Register an existing Delta table without moving data
CALL delta.system.register_table(schema_name => 'lake', table_name => 'orders_events',
     table_location => 's3://acme-lake/delta/orders_events/');
```

`hive.parquet.use-column-names=true` maps columns by name rather than position, which matters when upstream writers append columns. Prefer `iceberg.catalog.type=rest` for multi-engine interoperability, and keep credentials out of properties files by using environment substitution or an instance role.

[Table of Contents](#Trino-and-Presto)

## How do you query operational databases and warehouses?
The PostgreSQL and BigQuery connectors are the standard federation path for joining lake data with live sources.

```text
etc/catalog/postgres.properties
connector.name=postgresql
connection-url=jdbc:postgresql://pg-primary.acme.internal:5432/app
connection-user=trino_reader
connection-password=${ENV:PG_TRINO_PASSWORD}
```

```text
etc/catalog/bigquery.properties
connector.name=bigquery
bigquery.project-id=acme-prod
bigquery.credentials-file=/etc/trino/gcp-credentials.json
bigquery.max-parallelism=8
```

```sql
SELECT o.order_id, c.tier, b.lifetime_value
FROM iceberg.analytics.orders o
JOIN postgres.public.customers c ON o.customer_id = c.customer_id
LEFT JOIN bigquery.crm.customer_value b ON b.customer_id = c.customer_id
WHERE o.order_date = DATE '2026-10-04'
  AND c.live = true;
```

Keep the JDBC-side filter selective: Trino pushes predicates into the generated SQL, but a scan of a 500 million row Postgres table through a handful of splits is still slow. The BigQuery connector reads through the BigQuery API, so bytes billed still accrue on the BigQuery side; use it for occasional federation, not as the primary compute for a petabyte warehouse.

[Table of Contents](#Trino-and-Presto)

## How do you query Kafka from Trino?
The Kafka connector exposes a topic as a table for ad-hoc inspection. It is read-only.

```text
etc/catalog/kafka.properties
connector.name=kafka
kafka.nodes=kafka-1:9092,kafka-2:9092
kafka.table-names=acme.orders
kafka.table-description-dir=/etc/trino/kafka
```

```json
{
  "tableName": "acme.orders",
  "schemaName": "acme",
  "topicName": "orders",
  "message": {
    "dataFormat": "json",
    "fields": [
      { "name": "order_id", "type": "BIGINT", "mapping": "order_id" },
      { "name": "customer_id", "type": "BIGINT", "mapping": "customer_id" },
      { "name": "amount", "type": "DOUBLE", "mapping": "amount" }
    ]
  }
}
```

```sql
SELECT _partition_id, _partition_offset, order_id, amount
FROM kafka.acme."orders"
WHERE _timestamp > now() - INTERVAL '15' MINUTE
LIMIT 100;
```

Internal columns (`_partition_id`, `_partition_offset`, `_message`, `_timestamp`) make this useful for debugging a producer. It is not a streaming engine: each query re-reads the log from the configured offset, so use Flink, Spark Structured Streaming, or ClickHouse for continuous processing.

[Table of Contents](#Trino-and-Presto)

## How do you run federated queries across catalogs?
Federation is the headline Trino feature: one SQL statement joins sources in different systems. The coordinator plans one query, but data must physically move to where the join happens.

```sql
SELECT p.region, count(*) AS orders, sum(p.amount) AS revenue
FROM postgres.public.payments p
JOIN iceberg.analytics.orders o ON p.order_id = o.order_id
WHERE o.order_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-04'
GROUP BY p.region;
```

```sql
SELECT 'iceberg' AS src, count(*) FROM iceberg.analytics.orders
UNION ALL
SELECT 'delta', count(*) FROM delta.lake.orders
UNION ALL
SELECT 'hive', count(*) FROM hive.warehouse.orders;
```

Rules that keep federation fast:

+ Push selective predicates into each source; the connector sees only the filters it supports.
+ Broadcast small dimension tables instead of shuffling the fact side.
+ Materialize a repeatedly joined external table into the lake when it is large.
+ Remember that a cross-catalog join cannot use one catalog's native acceleration for the whole plan.

[Table of Contents](#Trino-and-Presto)

## How does query planning work and how do you read EXPLAIN?
Trino turns SQL into a logical plan, optimizes it, then creates an executable distributed plan of fragments and stages. `EXPLAIN` exposes each layer.

```sql
EXPLAIN (TYPE LOGICAL)
SELECT customer_id, sum(amount) FROM iceberg.analytics.orders GROUP BY customer_id;

EXPLAIN (TYPE DISTRIBUTED)
SELECT customer_id, sum(amount) FROM iceberg.analytics.orders GROUP BY customer_id;

EXPLAIN (TYPE IO)
SELECT customer_id, sum(amount) FROM iceberg.analytics.orders
WHERE order_date = DATE '2026-10-04' GROUP BY customer_id;

EXPLAIN ANALYZE
SELECT customer_id, sum(amount) FROM iceberg.analytics.orders GROUP BY customer_id;
```

What to look for:

+ `TableScan`: `constraint`, `layout`, and `dynamicFilters` show what was pushed down.
+ `Exchange` with `type = REPARTITION`: data is being shuffled between stages.
+ `type = GATHER`: results stream to the coordinator. Fine for final output, dangerous mid-plan.
+ `Join`: `distribution = PARTITIONED` or `BROADCAST`, and which side is the build side.
+ `EXPLAIN ANALYZE` gives per-operator row counts and wall time, so an estimate that is orders of magnitude off tells you statistics are missing.

[Table of Contents](#Trino-and-Presto)

## How do predicate and projection pushdown work?
Projection pushdown means only referenced columns are read. Predicate pushdown means filters are evaluated in the source, so fewer rows cross the network.

```sql
EXPLAIN (TYPE IO)
SELECT order_id, amount
FROM iceberg.analytics.orders
WHERE order_date = DATE '2026-10-04'
  AND status = 'shipped'
  AND customer_id IN (101, 102, 103);
```

The IO plan reports a `domain` per column; an unbounded domain means the connector cannot help and Trino filters after reading.

```text
TableScan[table = iceberg:analytics.orders]
    Layout: [order_id, amount]
    Constraint: order_date IN [2026-10-04], customer_id IN [101, 102, 103], status IN [shipped]
```

Practical levers:

+ Filter on partition columns so file pruning happens before any split is created.
+ Avoid wrapping filter columns in functions. `date_trunc('day', ts) = ...` blocks pruning; use a range instead.
+ Cast literals to the column type so the connector can compare them directly.
+ Check the connector docs for the functions and predicate shapes it can push down.

[Table of Contents](#Trino-and-Presto)

## How do broadcast partitioned and dynamic-filter joins work?
Trino builds a hash table from one side of a join and probes it with the other. Choosing the distribution decides how much data moves.

+ **Broadcast**: the build side is copied to every worker. Cheap when small, fatal when not.
+ **Partitioned**: both sides are repartitioned by join key so each worker sees matching keys. Needed for large-to-large joins.
+ **AUTOMATIC** (default): the optimizer decides from statistics and falls back to broadcast when the build side looks small.
+ **Dynamic filtering**: at runtime Trino collects min/max, distinct values, and bloom filters from the build side and applies them to the probe-side scan before splits are scheduled.

```sql
SET SESSION join_distribution_type = 'BROADCAST';
SET SESSION join_max_broadcast_table_size = '64MB';
SET SESSION enable_dynamic_filtering = true;
SET SESSION dynamic_filtering_wait_timeout = '20s';

EXPLAIN (TYPE DISTRIBUTED)
SELECT f.order_id, d.region
FROM iceberg.analytics.fact_orders f
JOIN iceberg.analytics.dim_order d ON f.order_id = d.order_id
WHERE d.region = 'EMEA';
```

```text
TableScan[table = iceberg:analytics.fact_orders]
    Dynamic filters: order_id BETWEEN 1000000 AND 1002000
```

Warning signs: a broadcast node after an inexplicably large aggregation, or raising `join_max_broadcast_table_size` globally to hide a bad estimate. The right fix is usually correct statistics, not a bigger broadcast limit. The dynamic-filtering wait timeout is the trade-off: a longer wait lets the filter arrive before scheduling and saves IO, but adds latency when the build side is slow.

[Table of Contents](#Trino-and-Presto)

## How does the cost-based optimizer use statistics and ANALYZE?
The CBO estimates cardinality and cost from table and column statistics: row count, distinct values, null fraction, and data size. Those estimates drive join ordering, join distribution, and aggregation strategy.

```sql
SET SESSION optimizer.join_reordering_strategy = 'AUTOMATIC';

SHOW STATS FOR iceberg.analytics.orders;

ANALYZE iceberg.analytics.orders;
ANALYZE iceberg.analytics.orders WITH (columns = ARRAY['order_date', 'status']);
```

```text
column_name | data_size | distinct_values_count | nulls_fraction | row_count | low_value | high_value
------------+-----------+-----------------------+----------------+-----------+-----------+-----------
order_id    | 4.0E8     | 5.0E7                 | 0.0            | 5.0E7     | 1         | 50000000
status      | 1.5E8     | 8.0                   | 0.0            | NULL      | NULL      | NULL
```

If `row_count` is missing, Trino falls back to heuristics and may broadcast something enormous. Statistics are per-connector: Iceberg reads them from manifests, Hive from the metastore, and JDBC connectors estimate from the source catalog. Re-run `ANALYZE` after bulk loads or major compactions, not on every small append, and prefer connectors with native statistics collection over JDBC sources where `ANALYZE` triggers an expensive scan.

[Table of Contents](#Trino-and-Presto)

## How does spill to disk work?
Trino normally keeps intermediate state in memory. Spilling lets memory-intensive operators write to local disk instead of failing the query. It is a safety valve, not a performance feature.

```text
etc/config.properties
spill-enabled=true
spiller-spill-path=/mnt/trino-spill
max-spill-per-node=400GB
query-max-spill-per-node=100GB
spill-compression-codec=ZSTD
```

```sql
SET SESSION spill_enabled = true;   -- covers joins, aggregations, ORDER BY, and window functions

SELECT customer_id, count(*) AS orders
FROM iceberg.analytics.orders
GROUP BY customer_id
ORDER BY orders DESC;
```

Supported operators include hash joins, aggregations, sorts, and window functions. Size the spill path for local NVMe, never network storage, and monitor `spill_used_bytes` so spilling does not silently become the normal path.

[Table of Contents](#Trino-and-Presto)

## How do you manage memory and resource groups?
Two layers control memory: per-query node limits in `config.properties`, and admission control through resource groups.

```text
etc/config.properties
query.max-memory=100GB
query.max-memory-per-node=8GB
query.max-total-memory-per-node=12GB
memory.heap-headroom-per-node=25%
```

```text
etc/resource-groups.properties
resource-groups.configuration-manager=file
resource-groups.config-file=etc/resource-groups.json
```

```json
{
  "rootGroups": [
    {
      "name": "global",
      "softMemoryLimit": "80%",
      "hardConcurrencyLimit": 100,
      "maxQueued": 1000,
      "subGroups": [
        { "name": "etl", "softMemoryLimit": "60%", "hardConcurrencyLimit": 20, "maxQueued": 200, "schedulingPolicy": "fair" },
        { "name": "adhoc", "softMemoryLimit": "30%", "hardConcurrencyLimit": 60, "maxQueued": 800, "schedulingPolicy": "fair" }
      ]
    }
  ],
  "selectors": [
    { "source": ".*airflow.*", "group": "global.etl" },
    { "user": "bi_service", "group": "global.adhoc" },
    { "group": "global.adhoc" }
  ]
}
```

The pattern that works in production: give ETL a large memory share but modest concurrency, give ad-hoc large concurrency but a smaller memory share, and cap queued queries so clients fail fast instead of timing out invisibly.

[Table of Contents](#Trino-and-Presto)

## How does Trino handle fault tolerance and retries?
Trino fails a query by default when a worker dies mid-query. Two mechanisms improve resilience: task-level retries and fault-tolerant execution with a durable exchange.

```text
etc/config.properties
retry-policy=TASK
query.max-run-time=6h
query.max-execution-time=5h
```

```text
etc/exchange-manager.properties
exchange-manager.name=filesystem
exchange.base-directories=s3://acme-trino-exchange/
exchange.s3.region=us-east-1
```

How the policies differ:

+ `NONE` - no automatic retry; any worker failure fails the query.
+ `TASK` - failed tasks retry on another worker. Works with the default in-memory exchange for transient errors.
+ `QUERY` - the whole query restarts, which is simpler but more expensive.
+ Fault-tolerant execution (`retry-policy=TASK` plus an exchange manager) persists intermediate data so long ETL queries survive worker restarts.

Set `query.max-run-time` deliberately: without it, a runaway query can occupy a resource group slot for hours.

[Table of Contents](#Trino-and-Presto)

## Which session properties are most useful for tuning?
Session properties override coordinator defaults per query and per session. They are the first lever before touching cluster config.

```sql
SET SESSION join_distribution_type = 'PARTITIONED';
SET SESSION join_max_broadcast_table_size = '64MB';
SET SESSION enable_dynamic_filtering = true;
SET SESSION task_concurrency = 16;
SET SESSION task_max_writer_count = 8;
SET SESSION max_hash_partition_count = 256;
SET SESSION distinct_aggregations_strategy = 'MARK_DISTINCT';

SHOW SESSION;
RESET SESSION join_distribution_type;
```

| Property | Effect | When to change it |
|---|---|---|
| `join_distribution_type` | broadcast vs partitioned joins | large-to-large joins misplanned |
| `join_max_broadcast_table_size` | build-side size cutoff | broadcast OOM or spill |
| `enable_dynamic_filtering` | runtime probe-side pruning | selective joins on huge fact tables |
| `task_concurrency` | concurrent splits per task | small splits or high-latency storage |
| `task_max_writer_count` | writer parallelism per task | too many small output files |
| `max_hash_partition_count` | shuffle partitions for hash operations | skew or tiny partitions |
| `distinct_aggregations_strategy` | strategy for `DISTINCT` aggregations | grouped distinct queries |
| `query_max_run_time` | per-query timeout | protect shared clusters |

Apply them where they are reproducible: in the CLI or BI connection for interactive work, and in the client session for scheduled jobs. Do not rely on one engineer's shell history.

[Table of Contents](#Trino-and-Presto)

## How do you secure Trino with authentication access control and masking?
Security has three independent layers: transport, authentication, and authorization.

```text
etc/config.properties
http-server.https.enabled=true
http-server.https.port=8443
http-server.https.keystore.path=/etc/trino/keystore.jks
http-server.authentication.type=PASSWORD
```

```text
etc/password-authenticator.properties
password-authenticator.name=ldap
ldap.url=ldaps://ldap.acme.internal:636
ldap.user-bind-pattern=uid=${USER},ou=people,dc=acme,dc=internal
```

OAuth2 and JWT are alternatives (`http-server.authentication.type=oauth2` with `http-server.authentication.oauth2.issuer`), and `sql-standard` access control lets Trino enforce `GRANT` and `REVOKE` when catalogs already have a permission model. File-based rules are the most common custom policy.

```text
etc/access-control.properties
access-control.name=file
security.config-file=etc/rules.json
```

```json
{
  "catalogs": [
    { "user": "etl_user", "catalog": "iceberg", "allow": "all" },
    { "user": "analyst", "catalog": "iceberg", "allow": "read-only" }
  ],
  "tables": [
    {
      "user": "analyst",
      "catalog": "iceberg",
      "schema": "analytics",
      "table": "customers",
      "privileges": ["SELECT"],
      "columns": [
        { "name": "email", "mask": "regexp_replace(email, '(^.)[^@]*', '$1***')" },
        { "name": "national_id", "mask": "'REDACTED'" }
      ]
    }
  ]
}
```

```sql
-- The analyst still gets rows, but never the raw values
SELECT customer_id, email, national_id FROM iceberg.analytics.customers LIMIT 5;
```

A table rule can also carry a row filter (`"filter": "region = 'EMEA'"`), which removes rows rather than masking values. Design notes: masks are evaluated per row, so keep expressions simple; masking is presentation control, not encryption, so combine it with storage encryption and least-privilege grants; and test rules with a real non-admin account before rollout, because a wrong rule silently exposes data instead of failing loudly. Rules are read top to bottom and the first match wins, so ordering is part of the policy.

[Table of Contents](#Trino-and-Presto)

## How do you write data with CTAS and INSERT?
Trino writes through connectors that implement the write SPI. `CREATE TABLE AS SELECT` and `INSERT` are the two primary tools.

```sql
CREATE TABLE iceberg.analytics.orders_daily
WITH (format = 'PARQUET', partitioning = ARRAY['order_date'])
AS
SELECT order_date, customer_id, count(*) AS orders, sum(amount) AS revenue
FROM iceberg.analytics.orders
GROUP BY order_date, customer_id;

INSERT INTO iceberg.analytics.orders_daily
SELECT order_date, customer_id, count(*), sum(amount)
FROM iceberg.analytics.orders
WHERE order_date = DATE '2026-10-04'
GROUP BY order_date, customer_id;
```

For tables that support it, row-level operations are available:

```sql
DELETE FROM iceberg.analytics.orders WHERE status = 'cancelled';

MERGE INTO iceberg.analytics.customers AS t
USING postgres.public.customers AS s ON t.customer_id = s.customer_id
WHEN MATCHED THEN UPDATE SET t.tier = s.tier, t.updated_at = s.updated_at
WHEN NOT MATCHED THEN INSERT (customer_id, tier, updated_at) VALUES (s.customer_id, s.tier, s.updated_at);
```

Control output file count with `task_max_writer_count`, `writer_scaling_min_data_processed`, and `scale_writers`. A CTAS that produces thousands of tiny files is the most common Trino write complaint, and compaction afterwards is the standard remedy.

[Table of Contents](#Trino-and-Presto)

## What connector-specific write limits should you know?
Not every connector is writable, and writable connectors differ in what they accept.

| Connector | Read | Insert | CTAS | Update/Delete/Merge | Notes |
|---|---|---|---|---|---|
| Iceberg | yes | yes | yes | yes | full table-format writes, partitioning in `WITH` |
| Delta Lake | yes | yes | yes | limited | let Spark or Databricks own heavy maintenance |
| Hive | yes | yes | yes | no | append-oriented; transactional tables need care |
| PostgreSQL | yes | yes | yes | yes | writes go to the source database |
| BigQuery | yes | yes | yes | yes | some versions reject `INSERT ... VALUES`; cost accrues on BigQuery |
| Kafka | yes | no | no | no | read-only, for inspection |
| Cassandra | yes | yes | yes | yes | the write path must respect the data model |

Other practical limits: some connectors reject `INSERT INTO ... VALUES` and require `INSERT INTO ... SELECT`, because a distributed engine has no efficient single-row path; type mapping differs per connector, especially for `varchar` and `timestamp with time zone`; and DDL such as `DROP COLUMN` may be unsupported or restricted when it would invalidate the underlying format.

[Table of Contents](#Trino-and-Presto)

## How does Trino compare with Presto Spark SQL and Hive?
Trino and Presto share an ancestor but diverged. Getting the history and workload fit right is a common interview question.

| Engine | Model | Strength | Weakness |
|---|---|---|---|
| Trino | MPP, in-memory, no storage | interactive federated SQL, ANSI SQL, many connectors | not built for multi-TB shuffles without spilling |
| PrestoDB | MPP | compatible lineage, Meta-backed community | connector ecosystem and release cadence differ from Trino |
| Spark SQL | distributed batch and streaming | heavy ETL, ML, complex transformations, fault tolerance | higher latency to first result, JVM tuning overhead |
| Hive | batch on MapReduce or Tez | mature metastore, huge legacy install base | outdated execution model, poor interactive latency |

```text
Choosing in one line:
interactive and federated SQL across many sources -> Trino
large ETL transforms and ML feature builds       -> Spark SQL
legacy batch on an existing metastore             -> Hive, or migrate to Trino or Spark
```

Trino is not a scheduler and not a storage format. It reads Iceberg, Delta, Hive, Kafka, and databases; orchestration belongs to Airflow or Dagster, table semantics belong to Iceberg or Delta, and stream processing belongs to Flink. It is a poor fit for petabyte nightly shuffles, high-frequency single-row OLTP, or a tiny dataset with one source.

[Table of Contents](#Trino-and-Presto)

## Real world use cases for Trino and Presto

### 1. Federated analytics across the lake and operational databases

A retail analytics team keeps orders in Iceberg on S3, customers in PostgreSQL, and marketing data in BigQuery. Analysts run one statement instead of exporting three extracts nightly.

```sql
SELECT c.tier,
       date_trunc('month', o.order_ts) AS month,
       sum(o.amount) AS revenue
FROM iceberg.analytics.orders o
JOIN postgres.public.customers c ON o.customer_id = c.customer_id
JOIN bigquery.marketing.campaigns m ON m.customer_id = c.customer_id
WHERE o.order_ts >= TIMESTAMP '2026-01-01 00:00:00'
GROUP BY 1, 2
ORDER BY 2, 1;
```

Why Trino: connectors replace nightly exports and the join happens in the engine. Selective predicates keep each source's scan small, and the warehouse never has to hold a copy of operational data.

### 2. Lakehouse SQL while Spark owns the writes

Spark and dbt write Iceberg tables; Trino serves the interactive layer over the same files and snapshots.

```python
from trino.dbapi import connect

cur = connect(
    host="trino.acme.internal", port=8080, user="bi_service",
    catalog="iceberg", schema="analytics",
).cursor()
cur.execute(
    "SELECT order_date, sum(amount) AS revenue FROM orders "
    "WHERE order_date BETWEEN DATE '2026-10-01' AND DATE '2026-10-04' "
    "GROUP BY order_date ORDER BY order_date"
)
for order_date, revenue in cur.fetchall():
    print(order_date, revenue)
```

Why Trino: fast planning over Iceberg metadata with no data duplication. Spark keeps its strengths for large transformations while Trino answers questions.

### 3. Migrating off a monolithic warehouse with a federation bridge

A company moves from a legacy warehouse to a lakehouse over several quarters. During the transition, Trino joins tables that still live in the old system with tables already migrated.

```sql
SELECT l.customer_id, l.lifetime_value, w.last_invoice_date
FROM iceberg.analytics.customer_value l
LEFT JOIN postgres_legacy.dw.invoices w ON l.customer_id = w.customer_id
WHERE l.snapshot_date = DATE '2026-10-04';
```

Why Trino: a federation bridge removes the need for a big-bang cutover. Each migrated table is one less dependency on the legacy system, and the SQL above never changes.

### 4. Ad-hoc log and event investigation

A platform team answers incident questions across Kafka, S3 Parquet, and a metrics database without building an ETL job per question.

```sql
SELECT src, count(*) AS errors
FROM (
  SELECT 'kafka' AS src FROM kafka.acme."app-logs"
  WHERE level = 'ERROR' AND _timestamp > now() - INTERVAL '30' MINUTE
  UNION ALL
  SELECT 'archive' FROM hive.warehouse.app_logs
  WHERE level = 'ERROR' AND log_date = current_date
) t
GROUP BY src;
```

Why Trino: the Kafka connector's timestamp and offset columns make producer debugging possible, and a UNION across file-based sources gives a complete picture in one query.

### 5. Governed self-service BI with row filters and masking

Support and finance share tables but must see different rows and masked columns. Policy is enforced in Trino rather than duplicated in every BI tool.

```json
{
  "tables": [
    { "group": "finance", "catalog": "iceberg", "schema": "analytics", "table": "orders", "privileges": ["SELECT"] },
    { "group": "support", "catalog": "iceberg", "schema": "analytics", "table": "orders",
      "privileges": ["SELECT"], "filter": "region = 'EMEA'",
      "columns": [
        { "name": "customer_email", "mask": "'***@***'" }
      ] }
  ]
}
```

```sql
SELECT order_id, region, customer_email FROM iceberg.analytics.orders LIMIT 10;
```

Why Trino: one policy layer applies to the CLI, notebooks, and BI tools alike, which is far easier to audit than per-tool row filters and duplicated masking views.

[Table of Contents](#Trino-and-Presto)
