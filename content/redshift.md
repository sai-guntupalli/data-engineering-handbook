## [Main title](../README.md)
### [Interview questions](full.md)

# Redshift

**Notebook:** [`notebooks/topics/redshift.ipynb`](../notebooks/topics/redshift.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is Amazon Redshift?](#What-is-Amazon-Redshift)
+ [How do distribution styles and sort keys affect Redshift performance?](#How-do-distribution-styles-and-sort-keys-affect-Redshift-performance)
+ [How do you load data efficiently into Redshift?](#How-do-you-load-data-efficiently-into-Redshift)
+ [What are the key benefits of using Amazon Redshift?](#What-are-the-key-benefits-of-using-Amazon-Redshift)
+ [How does Amazon Redshift achieve scalability?](#How-does-Amazon-Redshift-achieve-scalability)
+ [What is columnar storage, and why is it important in Redshift?](#What-is-columnar-storage-and-why-is-it-important-in-Redshift)
+ [How is data distributed in Amazon Redshift?](#How-is-data-distributed-in-Amazon-Redshift)
+ [What is a Redshift cluster?](#What-is-a-Redshift-cluster)
+ [How can you optimize query performance in Amazon Redshift?](#How-can-you-optimize-query-performance-in-Amazon-Redshift)
+ [What is a sort key in Amazon Redshift?](#What-is-a-sort-key-in-Amazon-Redshift)
+ [What is a distribution key in Amazon Redshift?](#What-is-a-distribution-key-in-Amazon-Redshift)
+ [Can you change the sort key or distribution key of an existing table in Redshift?](#Can-you-change-the-sort-key-or-distribution-key-of-an-existing-table-in-Redshift)
+ [What is a Redshift Spectrum?](#What-is-a-Redshift-Spectrum)
+ [How does Redshift Spectrum work?](#How-does-Redshift-Spectrum-work)
+ [Can you join tables from Redshift and Redshift Spectrum in a single query?](#Can-you-join-tables-from-Redshift-and-Redshift-Spectrum-in-a-single-query)
+ [How can you load data into Amazon Redshift?](#How-can-you-load-data-into-Amazon-Redshift)
+ [What is the recommended way to load large amounts of data into Redshift?](#What-is-the-recommended-way-to-load-large-amounts-of-data-into-Redshift)
+ [Can you load data into Redshift from multiple files in parallel?](#Can-you-load-data-into-Redshift-from-multiple-files-in-parallel)
+ [How can you monitor the performance of Amazon Redshift?](#How-can-you-monitor-the-performance-of-Amazon-Redshift)
+ [What is the purpose of the VACUUM command in Amazon Redshift?](#What-is-the-purpose-of-the-VACUUM-command-in-Amazon-Redshift)
+ [What is the difference between VACUUM and ANALYZE commands in Redshift?](#What-is-the-difference-between-VACUUM-and-ANALYZE-commands-in-Redshift)
+ [How can you secure data in Amazon Redshift?](#How-can-you-secure-data-in-Amazon-Redshift)
+ [Can you encrypt data in Amazon Redshift?](#Can-you-encrypt-data-in-Amazon-Redshift)
+ [What is the maximum size of a single Amazon Redshift cluster?](#What-is-the-maximum-size-of-a-single-Amazon-Redshift-cluster)
+ [How can you take backups of Amazon Redshift clusters?](#How-can-you-take-backups-of-Amazon-Redshift-clusters)
+ [What is the difference between a Redshift snapshot and a Redshift cluster backup?](#What-is-the-difference-between-a-Redshift-snapshot-and-a-Redshift-cluster-backup)
+ [Can you restore a Redshift snapshot to a different AWS region?](#Can-you-restore-a-Redshift-snapshot-to-a-different-AWS-region)
+ [How can you resize a Redshift cluster?](#How-can-you-resize-a-Redshift-cluster)
+ [What is the difference between dense compute and dense storage node types in Redshift?](#What-is-the-difference-between-dense-compute-and-dense-storage-node-types-in-Redshift)
+ [What is the maximum number of tables you can create in an Amazon Redshift database?](#What-is-the-maximum-number-of-tables-you-can-create-in-an-Amazon-Redshift-database)
+ [How can you optimize storage in Amazon Redshift?](#How-can-you-optimize-storage-in-Amazon-Redshift)
+ [What is the maximum size of a single table in Amazon Redshift?](#What-is-the-maximum-size-of-a-single-table-in-Amazon-Redshift)
+ [What is the purpose of the UNLOAD command in Redshift?](#What-is-the-purpose-of-the-UNLOAD-command-in-Redshift)
+ [How can you manage Redshift query concurrency?](#How-can-you-manage-Redshift-query-concurrency)
+ [What is the purpose of the ANALYZE command in Redshift?](#What-is-the-purpose-of-the-ANALYZE-command-in-Redshift)
+ [Can you perform cross-database queries in Amazon Redshift?](#Can-you-perform-cross-database-queries-in-Amazon-Redshift)
+ [What is the difference between a leader node and a compute node in Amazon Redshift?](#What-is-the-difference-between-a-leader-node-and-a-compute-node-in-Amazon-Redshift)
+ [How can you improve query performance for small tables in Amazon Redshift?](#How-can-you-improve-query-performance-for-small-tables-in-Amazon-Redshift)
+ [Can you create indexes on tables in Amazon Redshift?](#Can-you-create-indexes-on-tables-in-Amazon-Redshift)
+ [What is the maximum number of columns you can have in a table in Amazon Redshift?](#What-is-the-maximum-number-of-columns-you-can-have-in-a-table-in-Amazon-Redshift)
+ [What happens when a compute node fails in Amazon Redshift?](#What-happens-when-a-compute-node-fails-in-Amazon-Redshift)
+ [How can you automate data loading into Amazon Redshift?](#How-can-you-automate-data-loading-into-Amazon-Redshift)
+ [How does Redshift handle data compression?](#How-does-Redshift-handle-data-compression)
+ [Can you resize a Redshift cluster while it is running?](#Can-you-resize-a-Redshift-cluster-while-it-is-running)
+ [How does Redshift handle data distribution in a cluster?](#How-does-Redshift-handle-data-distribution-in-a-cluster)
+ [What is the purpose of the COPY command in Amazon Redshift?](#What-is-the-purpose-of-the-COPY-command-in-Amazon-Redshift)
+ [Can you use Redshift as an OLTP (Online Transaction Processing) database?](#Can-you-use-Redshift-as-an-OLTP-Online-Transaction-Processing-database)
+ [How does Redshift handle data backup and durability?](#How-does-Redshift-handle-data-backup-and-durability)
+ [What is the purpose of the Redshift Query Optimizer?](#What-is-the-purpose-of-the-Redshift-Query-Optimizer)
+ [Can you run Redshift queries from third-party BI tools?](#Can-you-run-Redshift-queries-from-third-party-BI-tools)
+ [Can you create temporary tables in Amazon Redshift?](#Can-you-create-temporary-tables-in-Amazon-Redshift)
+ [How can you monitor query performance in Amazon Redshift?](#How-can-you-monitor-query-performance-in-Amazon-Redshift)
+ [Can you perform updates and deletes on tables in Amazon Redshift?](#Can-you-perform-updates-and-deletes-on-tables-in-Amazon-Redshift)
+ [What is the purpose of the Redshift COPY command's IGNOREHEADER option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-IGNOREHEADER-option)
+ [What is the purpose of the Redshift COPY command's MAXERROR option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-MAXERROR-option)
+ [Can you create materialized views in Amazon Redshift?](#Can-you-create-materialized-views-in-Amazon-Redshift)
+ [What is the purpose of the Redshift UNLOAD command's MANIFEST option?](#What-is-the-purpose-of-the-Redshift-UNLOAD-commands-MANIFEST-option)
+ [Can you enable automatic compression encoding for columns in Amazon Redshift?](#Can-you-enable-automatic-compression-encoding-for-columns-in-Amazon-Redshift)
+ [What is the purpose of the Redshift ANALYZE command's VERBOSE option?](#What-is-the-purpose-of-the-Redshift-ANALYZE-commands-VERBOSE-option)
+ [Can you use Redshift Federated Query to query data in other AWS data sources?](#Can-you-use-Redshift-Federated-Query-to-query-data-in-other-AWS-data-sources)
+ [How can you export data from Amazon Redshift to Amazon S3?](#How-can-you-export-data-from-Amazon-Redshift-to-Amazon-S3)
+ [What is the purpose of the Redshift REINDEX command?](#What-is-the-purpose-of-the-Redshift-REINDEX-command)
+ [Can you restore a Redshift cluster to a specific point in time?](#Can-you-restore-a-Redshift-cluster-to-a-specific-point-in-time)
+ [What is the purpose of the Redshift EXPLAIN command?](#What-is-the-purpose-of-the-Redshift-EXPLAIN-command)
+ [Can you create user-defined functions (UDFs) in Amazon Redshift?](#Can-you-create-user-defined-functions-UDFs-in-Amazon-Redshift)
+ [How does Redshift handle query optimization for star schema data models?](#How-does-Redshift-handle-query-optimization-for-star-schema-data-models)
+ [Can you schedule query executions in Amazon Redshift?](#Can-you-schedule-query-executions-in-Amazon-Redshift)
+ [What is the purpose of the Redshift WLM (Workload Management) configuration?](#What-is-the-purpose-of-the-Redshift-WLM-Workload-Management-configuration)
+ [Can you create Redshift tables from existing Amazon S3 data?](#Can-you-create-Redshift-tables-from-existing-Amazon-S3-data)
+ [What is the purpose of the Redshift COPY command's TRUNCATECOLUMNS option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-TRUNCATECOLUMNS-option)
+ [Can you use Redshift with AWS PrivateLink for private network access?](#Can-you-use-Redshift-with-AWS-PrivateLink-for-private-network-access)
+ [How does Redshift handle query optimization for time-series data?](#How-does-Redshift-handle-query-optimization-for-time-series-data)
+ [Can you use Redshift to query and analyze semi-structured data formats like JSON or Avro?](#Can-you-use-Redshift-to-query-and-analyze-semi-structured-data-formats-like-JSON-or-Avro)
+ [What is the purpose of the Redshift COPY command's COMPUPDATE option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-COMPUPDATE-option)
+ [Can you use Redshift cross-region replication for disaster recovery?](#Can-you-use-Redshift-cross-region-replication-for-disaster-recovery)
+ [How does Redshift handle data distribution when a new node is added to the cluster?](#How-does-Redshift-handle-data-distribution-when-a-new-node-is-added-to-the-cluster)
+ [Can you use Redshift with AWS Identity and Access Management (IAM) for access control?](#Can-you-use-Redshift-with-AWS-Identity-and-Access-Management-IAM-for-access-control)
+ [What is the purpose of the Redshift ANALYZE command's DELETE option?](#What-is-the-purpose-of-the-Redshift-ANALYZE-commands-DELETE-option)
+ [Can you use Redshift with AWS Glue for data cataloging and ETL?](#Can-you-use-Redshift-with-AWS-Glue-for-data-cataloging-and-ETL)
+ [How does Redshift handle query optimization for dimensionally modeled data warehouses?](#How-does-Redshift-handle-query-optimization-for-dimensionally-modeled-data-warehouses)
+ [Can you restore a Redshift cluster to a different cluster?](#Can-you-restore-a-Redshift-cluster-to-a-different-cluster)
+ [What is the purpose of the Redshift VACUUM command's REINDEX option?](#What-is-the-purpose-of-the-Redshift-VACUUM-commands-REINDEX-option)
+ [Can you enable audit logging in Amazon Redshift?](#Can-you-enable-audit-logging-in-Amazon-Redshift)
+ [How does Redshift handle query optimization for complex join operations?](#How-does-Redshift-handle-query-optimization-for-complex-join-operations)
+ [Can you use Redshift with AWS Key Management Service (KMS) for encryption key management?](#Can-you-use-Redshift-with-AWS-Key-Management-Service-KMS-for-encryption-key-management)
+ [What is the purpose of the Redshift COPY command's ACCEPTINVCHARS option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-ACCEPTINVCHARS-option)
+ [Can you use Redshift with AWS CloudTrail for audit trail and compliance?](#Can-you-use-Redshift-with-AWS-CloudTrail-for-audit-trail-and-compliance)
+ [How does Redshift handle query optimization for complex aggregations and window functions?](#How-does-Redshift-handle-query-optimization-for-complex-aggregations-and-window-functions)
+ [Can you use Redshift with Amazon QuickSight for data visualization and analytics?](#Can-you-use-Redshift-with-Amazon-QuickSight-for-data-visualization-and-analytics)
+ [What is the purpose of the Redshift VACUUM command's DELETE option?](#What-is-the-purpose-of-the-Redshift-VACUUM-commands-DELETE-option)
+ [Can you use Redshift with AWS Lambda for serverless data processing?](#Can-you-use-Redshift-with-AWS-Lambda-for-serverless-data-processing)
+ [How does Redshift handle query optimization for large-scale joins and aggregations?](#How-does-Redshift-handle-query-optimization-for-large-scale-joins-and-aggregations)
+ [Can you use Redshift with Amazon Athena for ad-hoc SQL queries on S3 data?](#Can-you-use-Redshift-with-Amazon-Athena-for-ad-hoc-SQL-queries-on-S3-data)
+ [What is the purpose of the Redshift COPY command's ENCRYPTED option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-ENCRYPTED-option)
+ [Can you use Redshift with AWS Step Functions for serverless workflow orchestration?](#Can-you-use-Redshift-with-AWS-Step-Functions-for-serverless-workflow-orchestration)
+ [How does Redshift handle query optimization for data filtering and predicate pushdown?](#How-does-Redshift-handle-query-optimization-for-data-filtering-and-predicate-pushdown)
+ [Can you use Redshift with Amazon Kinesis Data Firehose for real-time data ingestion?](#Can-you-use-Redshift-with-Amazon-Kinesis-Data-Firehose-for-real-time-data-ingestion)
+ [What is the purpose of the Redshift VACUUM command's SORTONLY option?](#What-is-the-purpose-of-the-Redshift-VACUUM-commands-SORTONLY-option)
+ [Can you use Redshift with AWS Glue DataBrew for data preparation and cleansing?](#Can-you-use-Redshift-with-AWS-Glue-DataBrew-for-data-preparation-and-cleansing)
+ [How does Redshift handle query optimization for subqueries and correlated subqueries?](#How-does-Redshift-handle-query-optimization-for-subqueries-and-correlated-subqueries)
+ [Can you use Redshift with AWS Lake Formation for data lake management and access control?](#Can-you-use-Redshift-with-AWS-Lake-Formation-for-data-lake-management-and-access-control)
+ [What is the purpose of the Redshift COPY command's GZIP option?](#What-is-the-purpose-of-the-Redshift-COPY-commands-GZIP-option)
+ [Real world use cases for Redshift](#Real-world-use-cases-for-Redshift)

## What is Amazon Redshift?

Amazon Redshift is a fully managed, massively parallel, columnar data warehouse on AWS. A cluster has a leader node that plans and coordinates queries plus compute nodes divided into slices that store data and run query fragments. RA3 nodes separate compute from Redshift Managed Storage, so you can scale compute without moving data, and Redshift Serverless provides the same engine without cluster management.

```sql
-- The shape of a typical Redshift warehouse query
select
  d.calendar_month,
  p.category,
  sum(f.net_amount) as revenue
from analytics.fact_sales f
join analytics.dim_date d on f.date_key = d.date_key
join analytics.dim_product p on f.product_key = p.product_key
where d.calendar_year = 2026
group by d.calendar_month, p.category
order by d.calendar_month, revenue desc;
```

[Table of Contents](#Redshift)

## How do distribution styles and sort keys affect Redshift performance?

Distribution style decides which slice owns each row, which determines whether a join needs a network redistribution. Sort key decides physical order on each slice, which drives zone-map pruning and merge-join efficiency.

+ `DISTSTYLE KEY` colocates matching keys, removing redistribution for that join.
+ `DISTSTYLE ALL` copies a small table to every slice, turning a join into a local lookup.
+ `DISTSTYLE EVEN` round-robins rows; good for tables with no dominant join key.
+ `DISTSTYLE AUTO` lets Redshift choose and change as the workload evolves.
+ `SORTKEY` compound is ordered by priority; `INTERLEAVED` gives equal weight to several columns at the cost of expensive vacuum.

```sql
create table analytics.fact_sales (
  sale_id      bigint       encode az64,
  date_key     integer      encode az64,
  product_key  integer      encode az64,
  store_key    integer      encode az64,
  net_amount   numeric(12,2) encode az64,
  quantity     integer      encode az64
)
diststyle key
distkey (product_key)
sortkey (date_key, store_key);

create table analytics.dim_product (
  product_key integer not null,
  category    varchar(64),
  brand       varchar(64)
)
diststyle all
sortkey (product_key);
```

The fact table colocates on `product_key` with the small dimension copied everywhere, so the common star-schema join has no data movement.

[Table of Contents](#Redshift)

## How do you load data efficiently into Redshift?

Bulk load with `COPY` from Amazon S3 using an IAM role, compressed columnar files, and many files so every slice works in parallel. Avoid single-row `INSERT` for volume, and run `ANALYZE` (and `VACUUM` when needed) after large changes.

```sql
copy analytics.fact_sales
from 's3://acme-lake/manifests/fact_sales.manifest'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
manifest
region 'us-east-1'
statupdate on
compupdate on;
```

```bash
# How many objects are waiting to load, and how big are they?
aws s3 ls s3://acme-lake/curated/fact_sales/ --recursive --human-readable --summarize
```

Rules that matter: use one file per slice (or a manifest with many files), load Parquet or ORC over CSV, never load through the leader node with a single huge file, and keep the S3 bucket in the same region as the cluster.

[Table of Contents](#Redshift)

## What are the key benefits of using Amazon Redshift?

+ Fully managed MPP warehouse with columnar storage and compression.
+ RA3 separates compute from managed storage, so storage grows without resizing.
+ Redshift Spectrum queries S3 data lake files without loading them.
+ Concurrency scaling absorbs burst concurrency; short query acceleration speeds dashboards.
+ Mature SQL surface: window functions, stored procedures, materialized views, UDFs, cross-database queries.
+ Deep AWS integration: IAM, Glue, Lake Formation, KMS, CloudWatch, Kinesis, Lambda.
+ Data sharing and zero-ETL integrations with operational databases.

```sql
-- A workload only a columnar MPP warehouse handles comfortably
select
  customer_id,
  sum(net_amount) as lifetime_value,
  rank() over (order by sum(net_amount) desc) as value_rank
from analytics.fact_sales
where date_key >= 20240101
group by customer_id
qualify value_rank <= 100;
```

[Table of Contents](#Redshift)

## How does Amazon Redshift achieve scalability?

Redshift scales in three dimensions: node count and type (elastic or classic resize, or Serverless base capacity), storage (RA3 Redshift Managed Storage grows independently), and concurrency (concurrency scaling adds transient clusters for read bursts). AQUA accelerates scans on RA3 by pushing work to a hardware cache.

```bash
# Serverless: raise base capacity (RPUs) for a heavy month-end window
aws redshift-serverless update-workgroup \
  --workgroup-name analytics-wg \
  --base-capacity 256

# Provisioned: elastic resize an RA3 cluster
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --node-type ra3.4xlarge \
  --number-of-nodes 12
```

[Table of Contents](#Redshift)

## What is columnar storage, and why is it important in Redshift?

Columnar storage keeps each column's values together on disk instead of storing whole rows. Analytical queries touch a few columns but many rows, so columnar layout reads far less data, compresses better because values in a column share a type and range, and lets zone maps skip whole blocks. Redshift combines this with per-column encodings.

```sql
-- Reads only four of the wide table's columns and compresses to those blocks
select date_key, store_key, sum(net_amount) as revenue, sum(quantity) as units
from analytics.fact_sales
where date_key between 20261001 and 20261031
group by date_key, store_key;
```

[Table of Contents](#Redshift)

## How is data distributed in Amazon Redshift?

The leader node parses and plans; compute nodes are partitioned into slices, and each slice owns a subset of every table's rows. Distribution style controls the mapping. During a join, if the joining rows are not colocated, Redshift either redistributes one side, broadcasts the smaller side, or uses a merge join on a common sort key. Minimizing that movement is the core of physical design.

```text
leader node  -> parse, plan, coordinate
   |
   +-- compute node 1 [slice 0][slice 1]
   +-- compute node 2 [slice 0][slice 1]
   +-- compute node N [slice 0][slice 1]
```

[Table of Contents](#Redshift)

## What is a Redshift cluster?

A Redshift cluster is the provisioned unit of the warehouse: a leader node, one or more compute nodes of a chosen type, parameter and security groups, and a database. Modern deployments often use RA3 nodes or Redshift Serverless, which removes node management while keeping the same SQL engine.

```bash
aws redshift describe-clusters \
  --cluster-identifier analytics-cluster \
  --query 'Clusters[0].{Status:ClusterStatus,Nodes:NumberOfNodes,Type:NodeType,DB:DBName}'
```

[Table of Contents](#Redshift)

## How can you optimize query performance in Amazon Redshift?

+ Distribute and sort for the dominant joins and filters (or trust `AUTO`).
+ Keep statistics fresh with `ANALYZE`; stale stats cause bad join order and scan choices.
+ Run `VACUUM` after heavy delete/update churn so space is reclaimed and rows are sorted.
+ Use columnar compressed files for `COPY`, and load in parallel.
+ Materialize expensive repeated aggregations as materialized views.
+ Use `EXPLAIN` to confirm there is no unexpected `DS_DIST_BOTH` or full-table scan.
+ Watch WLM queue wait and use concurrency scaling or short query acceleration for dashboards.

```sql
analyze analytics.fact_sales;
vacuum sort only analytics.fact_sales to 75 percent;

explain
select p.category, sum(f.net_amount)
from analytics.fact_sales f
join analytics.dim_product p on f.product_key = p.product_key
where f.date_key between 20261001 and 20261031
group by p.category;
```

[Table of Contents](#Redshift)

## What is a sort key in Amazon Redshift?

A sort key stores rows on each slice in a defined order. Range-restricted predicates on the leading sort column let zone maps skip blocks, and sorted data makes merge joins cheap. Compound sort keys prioritize columns left to right; interleaved sort keys weight up to eight columns equally for multi-dimensional filters, but they require `VACUUM REINDEX` and cost more to maintain.

```sql
-- Time-series fact: date_key first makes range scans prune aggressively
create table analytics.fact_events (
  event_ts   timestamp encode az64,
  event_date date      encode az64,
  user_id    bigint    encode az64,
  event_type varchar(32) encode zstd,
  payload    varchar(4096) encode zstd
)
diststyle even
compound sortkey (event_date, user_id);
```

[Table of Contents](#Redshift)

## What is a distribution key in Amazon Redshift?

A distribution key is the column (or the `ALL`/`EVEN` strategy) that determines which slice stores each row. Choosing the join key of the largest fact-to-fact join colocates matching rows and removes network redistribution, which is usually the single biggest performance decision in a Redshift model.

```sql
-- Two facts that are frequently joined on customer_key share that distkey
create table analytics.fact_orders (
  order_id     bigint,
  customer_key integer,
  order_date   date,
  amount       numeric(12,2)
)
diststyle key distkey (customer_key)
sortkey (order_date);

create table analytics.fact_returns (
  return_id    bigint,
  customer_key integer,
  return_date  date,
  amount       numeric(12,2)
)
diststyle key distkey (customer_key)
sortkey (return_date);
```

[Table of Contents](#Redshift)

## Can you change the sort key or distribution key of an existing table in Redshift?

Yes in many cases. `ALTER TABLE ... ALTER SORTKEY` changes a compound sort key, and `ALTER TABLE ... ALTER DISTSTYLE` changes the distribution style; interleaved sort keys are the main exception, and the operation can be expensive because it reorganizes data. The zero-risk pattern is still to build a new table with the target design, copy the data, and rename.

```sql
-- In-place, supported for many conversions but potentially long-running
alter table analytics.fact_sales alter sortkey (date_key, store_key);
alter table analytics.fact_sales alter diststyle key distkey (product_key);

-- Rebuild pattern, which you can schedule and roll back
create table analytics.fact_sales_new (
  sale_id      bigint,
  date_key     integer,
  product_key  integer,
  store_key    integer,
  net_amount   numeric(12,2),
  quantity     integer
)
diststyle key distkey (product_key)
sortkey (date_key, store_key);

insert into analytics.fact_sales_new
select * from analytics.fact_sales;

analyze analytics.fact_sales_new;

alter table analytics.fact_sales rename to fact_sales_old;
alter table analytics.fact_sales_new rename to fact_sales;
```

[Table of Contents](#Redshift)

## What is a Redshift Spectrum?

Redshift Spectrum is the Redshift feature that queries data directly in Amazon S3 - Parquet, ORC, JSON, CSV, Avro, and Iceberg - using external tables in the AWS Glue Data Catalog. You pay per terabyte scanned and per Spectrum compute, and you avoid loading or transforming the data first.

[Table of Contents](#Redshift)

## How does Redshift Spectrum work?

The leader node compiles the query, then Spectrum compute nodes - a separate, elastically scaled fleet - read and filter the S3 objects. Predicate and partition projection is pushed down so only the needed columns, row groups, and partitions are read. The result is returned to the cluster, where it can be joined with local tables.

```sql
create external schema spectrum_lake
from data catalog
database 'acme_lake'
iam_role 'arn:aws:iam::123456789012:role/redshift-spectrum-role'
create external database if not exists;

create external table spectrum_lake.orders (
  order_id    varchar(64),
  customer_id varchar(64),
  order_date  date,
  amount      decimal(12,2)
)
partitioned by (dt varchar(10))
stored as parquet
location 's3://acme-lake/orders/';

alter table spectrum_lake.orders
add partition (dt = '2026-10-04')
location 's3://acme-lake/orders/dt=2026-10-04/';

select customer_id, sum(amount) as revenue
from spectrum_lake.orders
where dt = '2026-10-04'
group by customer_id;
```

[Table of Contents](#Redshift)

## Can you join tables from Redshift and Redshift Spectrum in a single query?

Yes. The optimizer decides what to push to Spectrum and what to run locally, and can broadcast a local dimension to the Spectrum scan or redistribute the S3 result. This is the standard pattern for a lakehouse with hot data in Redshift and cold history in S3.

```sql
-- Local dimension joined to an S3 fact table
select
  p.category,
  sum(s.amount) as revenue
from spectrum_lake.orders s
join analytics.dim_product p on s.product_id = p.product_id
where s.dt between '2026-09-01' and '2026-09-30'
group by p.category
order by revenue desc;
```

The performance lever is external table design: partition on the filter column, store Parquet, keep partitions reasonably large, and run `MSCK REPAIR` or add partitions when new data lands.

[Table of Contents](#Redshift)

## How can you load data into Amazon Redshift?

The main paths are `COPY` from S3 (or DynamoDB, EMR, or a remote host over SSH), `INSERT`/`INSERT ... SELECT` for small volumes, `CREATE TABLE AS` from an external table, streaming through Kinesis Data Firehose, zero-ETL integrations from Aurora/RDS, and Redshift Data API or JDBC/ODBC from an application.

```sql
-- COPY from a manifest of columnar files
copy analytics.fact_sales
from 's3://acme-lake/manifests/fact_sales.manifest'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
manifest;

-- ELT from the lake: transform while loading from Spectrum
create table analytics.fact_sales_2026 as
select order_id, customer_id, order_date, amount
from spectrum_lake.orders
where dt between '2026-01-01' and '2026-12-31';
```

[Table of Contents](#Redshift)

## What is the recommended way to load large amounts of data into Redshift?

Stage compressed, columnar files in S3, split into many files, and run a single parallel `COPY` with an IAM role, a manifest, `COMPUPDATE` and `STATUPDATE` on, and `MAXERROR` tuned to your tolerance. Then `ANALYZE` the table and `VACUUM` if the load caused churn.

```bash
# Example: convert CSV to Parquet and upload many files, then COPY in parallel
aws s3 cp ./curated/fact_sales/ s3://acme-lake/curated/fact_sales/ --recursive --exclude "*" --include "*.parquet"
```

```sql
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on
statupdate on
maxerror 0;

analyze analytics.fact_sales;
```

Beware the anti-patterns: one giant file, CSV with a single uncompressible stream, row-by-row inserts, and loading into a table whose sort key forces a full resort on every batch.

[Table of Contents](#Redshift)

## Can you load data into Redshift from multiple files in parallel?

Yes, and that is the point of the design: each file can be loaded by a slice, so throughput scales with the number of files up to the slice count. Use a prefix in `COPY`, or a manifest file for explicit control, and keep files roughly the same size so no slice finishes long before the others.

```sql
-- Prefix load: every object under the prefix is read in parallel
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet;

-- Manifest load: explicit list, which avoids picking up stray objects
copy analytics.fact_sales
from 's3://acme-lake/manifests/fact_sales.manifest'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
manifest
format as parquet;
```

If the file count is much larger than the slice count, Redshift still parallelizes well, but thousands of tiny files add S3 request overhead; target files of a few hundred MB.

[Table of Contents](#Redshift)

## How can you monitor the performance of Amazon Redshift?

Use CloudWatch metrics for cluster-level health (CPU, disk space, queue length, commit latency), the Redshift console performance tab for query-level views, and the system tables for the details: `STL_QUERY`, `STL_QUERYTEXT`, `SVL_QUERY_SUMMARY`, `SVL_QUERY_REPORT`, `STL_WLM_QUERY`, and `SVV_TABLE_INFO` for table design. Redshift Advisor and `SVV_ALTER_TABLE_RECOMMENDATIONS` suggest design changes.

```sql
-- Longest-running queries in the last day
select
  q.query,
  trim(t.text) as sql_text,
  q.starttime,
  datediff(second, q.starttime, q.endtime) as elapsed_s,
  q.aborted
from stl_query q
join stl_querytext t
  on q.query = t.query and t.sequence = 0
where q.starttime >= dateadd(day, -1, getdate())
order by elapsed_s desc
limit 20;
```

```sql
-- Tables that need attention: high skew, stale stats, or high unsorted percentage
select
  schema, "table", diststyle, sortkey1,
  nvl(unsorted, 0) as unsorted_pct,
  nvl(stats_off, 0) as stats_off_pct,
  nvl(skew_rows, 0) as skew_rows,
  tbl_rows
from svv_table_info
where nvl(unsorted, 0) > 20 or nvl(stats_off, 0) > 10
order by unsorted_pct desc;
```

[Table of Contents](#Redshift)

## What is the purpose of the VACUUM command in Amazon Redshift?

`VACUUM` reclaims space left by deletes and re-sorts rows that became unsorted after loads, which restores zone-map effectiveness and merge-join order. It has variants: `VACUUM FULL` (sort and reclaim), `VACUUM SORT ONLY`, `VACUUM DELETE ONLY`, `VACUUM REINDEX` (interleaved sort keys), and `VACUUM ... TO threshold PERCENT`.

```sql
-- Reclaim space and resort the whole table
vacuum full analytics.fact_sales;

-- Only resort, and stop when the table is 95 percent sorted
vacuum sort only analytics.fact_sales to 95 percent;

-- Rebuild interleaved sort keys (only needed for INTERLEAVED tables)
vacuum reindex analytics.fact_events;
```

VACUUM is I/O heavy and takes an exclusive-ish lock during the merge; run it in a maintenance window, target only tables that need it, and prefer `VACUUM SORT ONLY` when space is not the problem.

[Table of Contents](#Redshift)

## What is the difference between VACUUM and ANALYZE commands in Redshift?

| Aspect | VACUUM | ANALYZE |
|---|---|---|
| Purpose | Reclaim space, re-sort rows, rebuild interleaved keys | Refresh table and column statistics |
| Affects | Physical layout and zone maps | Optimizer cardinality estimates |
| Cost | High, I/O heavy, can block | Moderate, samples rows |
| Frequency | After heavy delete/update or out-of-order loads | After significant data changes |
| Risk if skipped | Bloated storage, poor pruning, slow merges | Bad join order and plan choices |

```sql
vacuum sort only analytics.fact_sales to 95 percent;
analyze analytics.fact_sales;
```

They solve different problems: a table can be perfectly sorted and still get a terrible plan from stale statistics, and a table with fresh statistics can still scan bloated, unsorted blocks.

[Table of Contents](#Redshift)

## How can you secure data in Amazon Redshift?

+ IAM controls who can call the Redshift APIs; database users/roles control query access.
+ Encryption at rest with KMS or CloudHSM; TLS for data in transit.
+ VPC, security groups, private subnets, and PrivateLink for network isolation.
+ Column-level access control and row-level security for least privilege.
+ IAM authentication and Secrets Manager for credential handling.
+ Audit logging (connection, user activity, user) and CloudTrail for API history.
+ Lake Formation and Spectrum permissions for the S3 side.

```sql
-- Row-level security scoped to the current user's region
create role emea_analyst;
grant usage on schema analytics to role emea_analyst;
grant select on analytics.fact_sales to role emea_analyst;

create rls policy emea_only
  with (region varchar(32))
  using (region = current_setting('app.region'));

attach rls policy emea_only
  on analytics.fact_sales to role emea_analyst;

-- Column-level grants keep PII out of reach
grant select (order_id, order_date, amount) on analytics.fact_orders to role emea_analyst;
```

[Table of Contents](#Redshift)

## Can you encrypt data in Amazon Redshift?

Yes. Redshift encrypts data at rest with AES-256 using either AWS KMS keys or CloudHSM keys (with automatic key rotation), and supports encryption in transit with SSL/TLS. You can also encrypt the S3 side of a `COPY`/`UNLOAD` with SSE-S3, SSE-KMS, or client-side keys, and use `COPY ... ENCRYPTED` for client-side encrypted load files.

```bash
# Enable KMS encryption on an existing cluster (requires a reboot)
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --encrypted \
  --kms-key-id alias/redshift-prod
```

```sql
-- Client-side encrypted load: the file is encrypted before it reaches S3
copy analytics.fact_orders
from 's3://acme-secure/orders/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
master_symmetric_key '${MASTER_KEY}'
encrypted;
```

[Table of Contents](#Redshift)

## What is the maximum size of a single Amazon Redshift cluster?

Provisioned RA3 clusters support up to 128 compute nodes per cluster as documented at the time of writing, and Redshift Managed Storage scales far beyond the local disk of older DS2/DC2 nodes. Redshift Serverless removes the node-count question entirely and scales capacity in RPUs. AWS raises these limits periodically, so quote the architecture ("RA3 separates storage, so capacity is not tied to node count") rather than a hardcoded ceiling.

```bash
# Current limits for a workgroup/cluster in your account
aws redshift describe-clusters --cluster-identifier analytics-cluster \
  --query 'Clusters[0].[NumberOfNodes,NodeType,ClusterStatus]'
```

[Table of Contents](#Redshift)

## How can you take backups of Amazon Redshift clusters?

Redshift takes automated snapshots on a retention schedule (1 to 35 days, default 1) and supports manual snapshots you keep until deleted. RA3 and Serverless snapshots can be shared across accounts, copied to another region, and restored into a new cluster or namespace.

```bash
# Automated snapshot retention
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --automated-snapshot-retention-period 14

# On-demand snapshot before a risky migration
aws redshift create-cluster-snapshot \
  --cluster-identifier analytics-cluster \
  --snapshot-identifier analytics-pre-migration
```

[Table of Contents](#Redshift)

## What is the difference between a Redshift snapshot and a Redshift cluster backup?

In Redshift a "backup" is delivered as snapshots: a point-in-time, cluster-level copy stored in S3, including data and cluster metadata (users, schemas, configuration). The distinction people usually mean is automated snapshots versus manual snapshots, or cluster snapshots versus a cross-region copy or a data-share. There is no separate continuous-backup product to configure.

```bash
aws redshift describe-cluster-snapshots \
  --cluster-identifier analytics-cluster \
  --query 'Snapshots[].[SnapshotIdentifier,SnapshotType,SnapshotCreateTime,Status]'
```

[Table of Contents](#Redshift)

## Can you restore a Redshift snapshot to a different AWS region?

Yes. Redshift supports cross-region snapshot copy: enable it on the source cluster with a destination region and retention, and Redshift copies new automated and manual snapshots (encrypted with a KMS key in the destination) so you can restore or use them there. You can also copy a single snapshot on demand.

```bash
# Enable ongoing cross-region snapshot copy
aws redshift enable-snapshot-copy \
  --cluster-identifier analytics-cluster \
  --destination-region us-west-2 \
  --retention-period 7

# Copy one snapshot now
aws redshift copy-cluster-snapshot \
  --source-snapshot-identifier analytics-pre-migration \
  --target-snapshot-identifier analytics-pre-migration-west \
  --source-region us-east-1 \
  --target-region us-west-2 \
  --target-snapshot-kms-key-id alias/redshift-dr
```

[Table of Contents](#Redshift)

## How can you resize a Redshift cluster?

Use elastic resize for a fast change to a supported target configuration (adds or removes nodes or changes some node types with a short reboot), classic resize for arbitrary changes (which migrates data and takes longer), or move to Redshift Serverless to avoid node management. RA3 also lets you scale compute and storage independently.

```bash
# Elastic resize: double the nodes
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --number-of-nodes 8 \
  --node-type ra3.4xlarge \
  --elastic-resize

# Classic resize to a different node family
aws redshift resize-cluster \
  --cluster-identifier analytics-cluster \
  --cluster-type multi-node \
  --number-of-nodes 16 \
  --node-type ra3.16xlarge
```

[Table of Contents](#Redshift)

## What is the difference between dense compute and dense storage node types in Redshift?

| Family | Storage | Best for | Notes |
|---|---|---|---|
| DC2 (dense compute) | Local SSD | High-performance, compute-heavy, smaller data | Fast local I/O, storage tied to nodes |
| DS2 (dense storage) | Local HDD | Large data at low cost, sequential scans | Legacy; being superseded by RA3 |
| RA3 | Managed storage (SSD cache + S3) | Most production warehouses | Scale compute and storage independently |

```text
RA3: compute nodes hold a local SSD cache; the authoritative data lives in
Redshift Managed Storage, so growing storage does not require adding nodes.
```

For new deployments, RA3 or Serverless is the modern default: DS2 is legacy and RA3 removes the "add nodes to get disk" trade-off.

[Table of Contents](#Redshift)

## What is the maximum number of tables you can create in an Amazon Redshift database?

The documented limit varies by node type - 9,900 tables per database on smaller nodes (for example `ra3.large`) and 200,000 on `ra3.4xlarge`/`ra3.16xlarge`, while Redshift Serverless allows 200,000. System tables are excluded, and AWS has raised these limits over time, so verify the current quota. In practice the limit is never the constraint - super-wide schemas with thousands of tiny tables are, because each adds planning and maintenance overhead.

```sql
-- How many user tables does this database actually have?
select count(*) as user_tables
from svv_tables
where table_schema not in ('pg_catalog', 'information_schema');
```

[Table of Contents](#Redshift)

## How can you optimize storage in Amazon Redshift?

+ Choose the right compression encoding per column (or let `COPY` pick with `COMPUPDATE`).
+ Set sort and distribution keys so blocks hold related rows and zone maps work.
+ Run `VACUUM` to reclaim deleted space and re-sort.
+ Drop or archive cold tables and use Spectrum for rarely queried history.
+ On RA3, managed storage grows automatically; on DS2/DC2, watch per-node disk usage.

```sql
-- Where is storage going, and how much is unsorted or skewed?
select
  schema, "table",
  diststyle, sortkey1,
  tbl_rows,
  size as size_mb,
  nvl(unsorted, 0) as unsorted_pct,
  nvl(skew_rows, 0) as skew_rows
from svv_table_info
order by size_mb desc
limit 20;
```

[Table of Contents](#Redshift)

## What is the maximum size of a single table in Amazon Redshift?

A single table is bounded by the cluster's usable storage rather than by an internal per-table cap. On RA3 the table lives in Redshift Managed Storage and can grow into petabytes across the cluster, while DS2/DC2 tables are bounded by local disk and are usually kept smaller through archival. Treat any specific number as version-dependent and verify the current service quotas.

```sql
-- Largest tables in bytes
select schema, "table", size as size_mb, tbl_rows
from svv_table_info
order by size_mb desc
limit 5;
```

[Table of Contents](#Redshift)

## What is the purpose of the UNLOAD command in Redshift?

`UNLOAD` runs a query and writes the result to Amazon S3 in parallel across slices, producing multiple files. It is the standard way to export curated data for the lake, hand data to another system, or archive a partition before dropping it. `UNLOAD` writes Parquet, ORC, or delimited text with compression and partitioning.

```sql
unload ('select * from analytics.fact_sales where date_key between 20260101 and 20260131')
to 's3://acme-export/fact_sales/2026-01/'
iam_role 'arn:aws:iam::123456789012:role/redshift-unload-role'
format as parquet
partition by (date_key)
allowoverwrite
manifest;
```

Note that `UNLOAD` is server-side: the data never flows through the client, and it parallelizes automatically. Use `PARALLEL OFF` only when a single ordered file is genuinely required.

[Table of Contents](#Redshift)

## How can you manage Redshift query concurrency?

Three tools work together: WLM queues (automatic or manual) allocate memory and slots to query classes, short query acceleration (SQA) routes short queries ahead of long ones, and concurrency scaling adds transient clusters for read-heavy bursts. Query monitoring rules (QMR) can abort, log, or hop a query that exceeds thresholds like runtime or returned rows.

```bash
# Automatic WLM with a query monitoring rule that aborts runaway queries
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --wlm-json-configuration '[{"name":"default","auto_wlm":true,"query_concurrency_scaling":"auto","rules":[{"rule_name":"abort_long","predicate":[{"metric_name":"query_execution_time","operator":">","value":3600}],"action":"abort"}]}]'
```

```sql
-- Which queue waited the longest in the last day?
select service_class, count(*) as queries, avg(total_queue_time) as avg_queue_us
from stl_wlm_query
where queue_start_time >= dateadd(day, -1, getdate())
group by service_class
order by avg_queue_us desc;
```

[Table of Contents](#Redshift)

## What is the purpose of the ANALYZE command in Redshift?

`ANALYZE` collects table and column statistics - row counts, distinct values, null fractions, and block-level range information - that the optimizer uses to estimate cardinality and choose join order, join type, and distribution method. Without fresh statistics the optimizer guesses, and a guessed plan on a large table is usually a slow one.

```sql
-- Analyze one table
analyze analytics.fact_sales;

-- Only re-analyze columns used in predicates or joins (cheaper on wide tables)
analyze analytics.fact_sales predicate columns;

-- Analyze every table in the connected database after a big load
analyze;
```

Run `ANALYZE` after loads that change a meaningful fraction of rows, after large deletes, and before benchmarking a query. `COPY ... STATUPDATE ON` updates statistics as part of the load.

[Table of Contents](#Redshift)

## Can you perform cross-database queries in Amazon Redshift?

Yes. On RG and RA3 provisioned clusters and on Redshift Serverless you can query across databases in the same cluster using three-part names (`database.schema.table`). Cross-database queries work on local databases and on databases accessed through data sharing; they do not extend to a different cluster's local databases unless those are shared.

```sql
-- Query a table in another database on the same cluster
select c.customer_id, c.email, sum(s.amount) as revenue
from sales_db.analytics.fact_sales s
join crm_db.public.customers c on s.customer_id = c.customer_id
where s.order_date >= date '2026-01-01'
group by c.customer_id, c.email
order by revenue desc
limit 100;
```

Requirements: RG or RA3 provisioned nodes (or Serverless), the databases on the same cluster, and appropriate privileges on the objects in the other database. DS2/DC2 clusters cannot do it.

[Table of Contents](#Redshift)

## What is the difference between a leader node and a compute node in Amazon Redshift?

The leader node is the query planner and coordinator: it parses SQL, optimizes the plan, distributes work, and merges results. It also stores metadata but no user data. Compute nodes store the data in slices and execute the query fragments; each node reports results back to the leader.

```text
client -> leader node (plan, coordinate) -> compute nodes/slices (scan, join, aggregate) -> leader -> client
```

You scale compute for query throughput and storage for data volume; on RA3 the two are decoupled, while on DS2/DC2 adding storage means adding nodes.

[Table of Contents](#Redshift)

## How can you improve query performance for small tables in Amazon Redshift?

Use `DISTSTYLE ALL` so the table is replicated to every slice, which turns joins against it into local lookups and avoids redistribution. Keep its sort key small and keep statistics fresh. Do not distribute a small lookup table `EVEN` or by a key that does not match the join.

```sql
create table analytics.dim_currency (
  currency_code char(3) not null,
  currency_name varchar(64),
  usd_rate      numeric(12,6)
)
diststyle all
sortkey (currency_code);

analyze analytics.dim_currency;

-- With DISTSTYLE ALL this join needs no redistribution of the fact table
select f.sale_id, f.net_amount * c.usd_rate as usd_amount
from analytics.fact_sales f
join analytics.dim_currency c on f.currency_code = c.currency_code;
```

`DISTSTYLE ALL` is wrong for anything but genuinely small, slowly changing tables: it multiplies storage by the slice count and slows every write.

[Table of Contents](#Redshift)

## Can you create indexes on tables in Amazon Redshift?

Redshift has no secondary or B-tree indexes like an OLTP database. The closest analogues are sort keys (including interleaved sort keys), zone maps, and distribution keys. If an interviewer asks about "indexes", explain those mechanisms and when to use an interleaved sort key instead.

```sql
-- Interleaved sort key: equal weight to multiple filter columns
create table analytics.fact_events (
  event_date date,
  country    varchar(2),
  event_type varchar(32),
  user_id    bigint
)
interleaved sortkey (event_date, country, event_type);

-- A query that filters on several of those columns benefits from the interleave
select country, count(*)
from analytics.fact_events
where event_date between date '2026-10-01' and date '2026-10-07'
  and event_type = 'purchase'
group by country;
```

Interleaved sort keys cost more to maintain because `VACUUM REINDEX` is required; prefer a compound sort key unless queries genuinely filter on several columns with equal weight.

[Table of Contents](#Redshift)

## What is the maximum number of columns you can have in a table in Amazon Redshift?

The documented limit is 1,600 columns per table. Wide tables are legal but expensive: every column adds block metadata, and `SELECT *` over 1,600 columns forces the engine to read them all. Model wide event data with `SUPER`/JSON or separate tables rather than hundreds of sparse columns.

```sql
-- Count the columns a table actually exposes
select count(*) as column_count
from svv_columns
where table_schema = 'analytics' and table_name = 'fact_sales';
```

[Table of Contents](#Redshift)

## What happens when a compute node fails in Amazon Redshift?

Redshift keeps replicas of data across nodes, so when a compute node fails the leader routes work for its slices to other nodes and the cluster continues, typically with reduced performance. The node is replaced automatically and Redshift re-replicates the data. RA3 with Multi-AZ deployments adds an available-zone failure story; RA3/DS2 clusters also support relocation to another AZ during recovery.

```bash
# Watch for node replacement and cluster events
aws redshift describe-events \
  --source-identifier analytics-cluster \
  --source-type cluster \
  --duration 1440
```

[Table of Contents](#Redshift)

## How can you automate data loading into Amazon Redshift?

Common patterns: AWS Glue jobs or Glue DataBrew for transformation plus `COPY`, Step Functions or Airflow to orchestrate, EventBridge Scheduler plus the Redshift Data API for scheduled SQL, Lambda for event-driven loads, and Kinesis Data Firehose for streaming. The Redshift Data API is the modern way to run SQL without managing a JDBC connection.

```python
# EventBridge/Lambda style: run a COPY through the Redshift Data API
import time

import boto3

client = boto3.client("redshift-data")
response = client.execute_statement(
    WorkgroupName="analytics-wg",
    Database="analytics",
    Sql="""
        copy analytics.fact_sales
        from 's3://acme-lake/curated/fact_sales/'
        iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
        format as parquet;
    """,
)
statement_id = response["Id"]

# There is no built-in waiter; poll until the statement finishes.
while client.describe_statement(Id=statement_id)["Status"] not in ("FINISHED", "FAILED", "ABORTED"):
    time.sleep(2)
```

Patterns that survive production: make each load idempotent (staging table plus `MERGE`, or partition swap), record every run in an audit table, and alert on `MAXERROR` breaches rather than ignoring them.

[Table of Contents](#Redshift)

## How does Redshift handle data compression?

Redshift compresses each column independently and chooses an encoding based on the data type and value distribution. Common encodings include `AZ64` (numeric and date types, good default), `ZSTD`/`LZO` (general), `BYTEDICT`/`TEXT255` (low-cardinality strings), `DELTA`/`DELTA32K` (sorted integers and dates), `RUNLENGTH` (repeated values), and `MOSTLY8`/`MOSTLY16`/`MOSTLY32` (small integers). You can let `COPY ... COMPUPDATE ON` choose, or set encodings explicitly.

```sql
-- Inspect current encodings
select "column", type, encoding
from pg_table_def
where schemaname = 'analytics' and tablename = 'fact_sales';

-- Let COPY choose encodings for new data
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on;
```

[Table of Contents](#Redshift)

## Can you resize a Redshift cluster while it is running?

Yes. An elastic resize changes the node count or moves between certain node types with a short reboot and minimal downtime; a classic resize migrates data and makes the cluster read-only during the operation. Serverless workgroups scale base capacity without any node-level resize at all.

```bash
# Elastic resize (fast, short reboot)
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --number-of-nodes 6 \
  --node-type ra3.4xlarge \
  --elastic-resize

# Classic resize (arbitrary target, longer, read-only window)
aws redshift resize-cluster \
  --cluster-identifier analytics-cluster \
  --cluster-type multi-node \
  --number-of-nodes 12 \
  --node-type ra3.4xlarge
```

[Table of Contents](#Redshift)

## How does Redshift handle data distribution in a cluster?

The leader assigns each slice a portion of every table according to the table's distribution style. `KEY` hashes the distribution column, `EVEN` round-robins, `ALL` replicates small tables, and `AUTO` lets Redshift choose and adapt. During joins the optimizer either redistributes, broadcasts, or merge-joins the inputs, so distribution design is about eliminating the most expensive movement for your dominant queries.

```sql
-- Which tables are skewed, and by how much?
select schema, "table", diststyle, skew_rows, skew_sortkey1
from svv_table_info
where skew_rows > 1.5
order by skew_rows desc;
```

[Table of Contents](#Redshift)

## What is the purpose of the COPY command in Amazon Redshift?

`COPY` is the high-throughput bulk loader. It reads from S3, DynamoDB, EMR, or a remote host and loads directly into slices in parallel, applying compression, encoding selection, statistics updates, and error handling along the way. It is dramatically faster and cheaper than row-by-row `INSERT`.

```sql
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on
statupdate on
maxerror 10;
```

[Table of Contents](#Redshift)

## Can you use Redshift as an OLTP (Online Transaction Processing) database?

No, not as a general-purpose OLTP database. Redshift is an OLAP columnar, MPP warehouse optimized for large scans and aggregations; it lacks row-level secondary indexes and is not designed for thousands of concurrent single-row transactions. It does support ACID transactions, `MERGE`, and UDFs, so modest operational-style writes are fine, but a high-TPS application belongs on Aurora, DynamoDB, or another OLTP engine.

```sql
-- Occasional operational-style upsert is fine ...
merge into analytics.dim_customer t
using analytics.stg_customer s
on t.customer_id = s.customer_id
when matched then update set t.email = s.email, t.segment = s.segment
when not matched then insert (customer_id, email, segment)
values (s.customer_id, s.email, s.segment);

-- ... but thousands of these per second is an OLTP workload, not a warehouse one.
```

[Table of Contents](#Redshift)

## How does Redshift handle data backup and durability?

Redshift replicates data within the cluster so a node failure does not lose it, and continuously backs the cluster up to S3 as automated snapshots with a configurable retention window (1 to 35 days). Manual snapshots persist until deleted, and snapshots can be copied to another region or shared across accounts. RA3 Multi-AZ deployments add synchronous standby capacity for zone failures.

```bash
aws redshift describe-clusters --cluster-identifier analytics-cluster \
  --query 'Clusters[0].[ClusterStatus,AutomatedSnapshotRetentionPeriod,Encrypted]'
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift Query Optimizer?

It is a cost-based optimizer: it rewrites the query, enumerates join orders and join types, estimates cardinality from table and column statistics, and picks the plan with the lowest estimated cost. It decides whether to redistribute or broadcast, whether to use a merge join on sort keys, and where to push predicates. Its blind spot is stale or missing statistics, which is why `ANALYZE` matters so much.

```sql
analyze analytics.fact_sales;

explain
select p.category, sum(f.net_amount)
from analytics.fact_sales f
join analytics.dim_product p on f.product_key = p.product_key
where f.date_key = 20261004
group by p.category;
```

[Table of Contents](#Redshift)

## Can you run Redshift queries from third-party BI tools?

Yes. Redshift speaks PostgreSQL-compatible SQL and exposes JDBC/ODBC drivers plus native connectors, so Tableau, Power BI, Looker, Metabase, DBeaver, and similar tools can query it. For BI workloads, plan the concurrency side: WLM queues, short query acceleration, concurrency scaling, and materialized views for repeated aggregates.

```sql
-- A materialized view keeps a common dashboard aggregate cheap
create materialized view analytics.mv_revenue_daily
auto refresh yes
as
select
  date_trunc('day', order_date) as order_day,
  region,
  sum(amount) as revenue
from analytics.fact_orders
group by order_day, region;
```

[Table of Contents](#Redshift)

## Can you create temporary tables in Amazon Redshift?

Yes. Temp tables exist for the session (default) or the transaction (`ON COMMIT DROP`/`ON COMMIT DELETE ROWS`), and they are useful for staging within an ETL step. Create them with `CREATE TEMP TABLE ... AS` so no explicit distribution design is needed for short-lived data.

```sql
create temp table stg_orders as
select order_id, customer_id, order_date, amount
from spectrum_lake.orders
where dt = '2026-10-04';

-- ... transform ...

drop table stg_orders;

-- Transaction-scoped variant
create temp table stg_load (id bigint, payload varchar(1024))
on commit drop;
```

[Table of Contents](#Redshift)

## How can you monitor query performance in Amazon Redshift?

Use the console's query monitoring and performance insights, CloudWatch for cluster metrics, and the system tables for detail. The most useful are `STL_QUERY`/`STL_QUERYTEXT`, `SVL_QUERY_SUMMARY` (step and time breakdown), `SVL_QUERY_REPORT` (slice-level skew), `STL_WLM_QUERY` (queue waits), and `STL_ALERT_EVENT_LOG` (nested loops, missing stats, and other alerts).

```sql
-- Find the slowest step of the slowest query, and check for slice skew
select
  query,
  segment,
  step,
  max(rows) as max_rows,
  avg(rows) as avg_rows,
  max(rows) - avg(rows) as skew,
  max(elapsed_time) as elapsed_us
from svl_query_report
where query = 1234567
group by query, segment, step
order by elapsed_us desc
limit 10;
```

```sql
-- Alert events in the last day: what did the optimizer complain about?
select query, event, solution
from stl_alert_event_log
where event_time >= dateadd(day, -1, getdate())
order by event_time desc
limit 20;
```

[Table of Contents](#Redshift)

## Can you perform updates and deletes on tables in Amazon Redshift?

Yes. Redshift supports `UPDATE`, `DELETE`, and `MERGE` with full ACID transactions and snapshot isolation. Internally, an update or delete marks rows for deletion and writes new versions; the old rows stay until `VACUUM` reclaims space, which is why heavy mutation churn causes bloat and unsorted data.

```sql
-- Update and delete are normal SQL
update analytics.fact_orders
set status = 'shipped'
where order_id = 'o-1042' and status = 'packed';

delete from analytics.fact_orders
where order_date < date '2020-01-01';

-- MERGE is the idiomatic upsert for batch ELT
merge into analytics.fact_orders t
using analytics.stg_orders s
on t.order_id = s.order_id
when matched then update set t.status = s.status, t.amount = s.amount
when not matched then insert (order_id, customer_id, order_date, status, amount)
values (s.order_id, s.customer_id, s.order_date, s.status, s.amount);
```

For very large rewrites, the faster pattern is `CREATE TABLE AS SELECT` (or `INSERT INTO ... SELECT`) into a new table and rename, which avoids touching rows one at a time.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's IGNOREHEADER option?

`IGNOREHEADER n` tells `COPY` to skip the first `n` lines of each input file, which is how you load CSV files that begin with a header row. Use `IGNOREHEADER 1` for a single header line; the option is per file, not per load, so every file must have the same structure.

```sql
copy analytics.stg_orders
from 's3://acme-lake/raw/orders_2026-10-04.csv'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
csv
ignoreheader 1
region 'us-east-1';
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's MAXERROR option?

`MAXERROR n` allows up to `n` rows to fail during the load before `COPY` aborts (default `MAXERROR 0`). The rejected rows are written to `STL_LOAD_ERRORS` with the reason, so a tolerant load must be paired with a review of that table. Use a small tolerance for messy external feeds and zero for internal, well-validated data.

```sql
copy analytics.stg_orders
from 's3://acme-lake/raw/orders_2026-10-04.csv'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
csv
ignoreheader 1
maxerror 100;

-- Exactly which rows were rejected, and why
select line_number, colname, raw_line, err_code, err_reason
from stl_load_errors
where filename like '%orders_2026-10-04.csv%'
order by line_number
limit 50;
```

[Table of Contents](#Redshift)

## Can you create materialized views in Amazon Redshift?

Yes. `CREATE MATERIALIZED VIEW` stores the precomputed result, and `AUTO REFRESH YES` keeps it current as base tables change. The optimizer can automatically rewrite matching queries to use the materialized view, so dashboards speed up without changing their SQL. Refresh incrementally or fully, depending on the query.

```sql
create materialized view analytics.mv_sales_by_category
diststyle even
sortkey (order_day)
auto refresh yes
as
select
  date_trunc('day', f.order_date) as order_day,
  p.category,
  sum(f.amount) as revenue
from analytics.fact_sales f
join analytics.dim_product p on f.product_key = p.product_key
group by order_day, p.category;

refresh materialized view analytics.mv_sales_by_category;

-- Freshness check
select name, state, is_stale, autorefresh
from stv_mv_info;
```

Limitations: not every query shape is supported, an auto-refresh view can lag the base tables briefly, and a materialized view costs storage. Use them for repeated, expensive aggregates rather than one-off analysis.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift UNLOAD command's MANIFEST option?

`MANIFEST` makes `UNLOAD` write a manifest file that lists the exported data files. Downstream tools read the manifest to discover exactly which files belong to the export, which avoids both "read the whole prefix" and "read a half-finished export" bugs, and it is what `COPY` expects when loading a multi-file export back in.

```sql
unload ('select * from analytics.fact_sales where date_key = 20261004')
to 's3://acme-export/fact_sales/2026-10-04/'
iam_role 'arn:aws:iam::123456789012:role/redshift-unload-role'
format as parquet
allowoverwrite
manifest;

-- The manifest is written alongside the data files:
-- s3://acme-export/fact_sales/2026-10-04/manifest-<id>
```

```sql
-- Reload exactly those files elsewhere
copy analytics.fact_sales_reload
from 's3://acme-export/fact_sales/2026-10-04/manifest-1234'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
manifest
format as parquet;
```

[Table of Contents](#Redshift)

## Can you enable automatic compression encoding for columns in Amazon Redshift?

Yes. `COPY ... COMPUPDATE ON` (or `TRUE`) analyzes incoming data and applies the best encoding per column; `COMPUPDATE PRESET` applies the default encoding without analyzing, and `OFF` disables it. You can also change an encoding explicitly on an existing column.

```sql
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on;

-- Explicit encoding change on an existing column
alter table analytics.fact_sales
alter column net_amount encode az64;
```

Changing an encoding rewrites the column, so do it in a maintenance window on large tables.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift ANALYZE command's VERBOSE option?

`ANALYZE ... VERBOSE` prints progress and detail about each table as statistics are collected, which is useful when you are analyzing a large schema and want to see where time is going. Without `VERBOSE`, the command succeeds silently.

```sql
analyze verbose analytics.fact_sales;
```

For scheduled maintenance, prefer non-verbose `ANALYZE` and inspect `SVV_TABLE_INFO.stats_off` to decide what needs re-analysis.

[Table of Contents](#Redshift)

## Can you use Redshift Federated Query to query data in other AWS data sources?

Yes. Federated Query lets Redshift read live data from Amazon RDS and Aurora (PostgreSQL and MySQL), and Amazon DocumentDB, through an external schema backed by a Secrets Manager secret. Redshift pushes filters and aggregations down to the source where possible and joins the result with local tables.

```sql
create external schema crm from postgres
  database 'crm' schema 'public'
  uri 'my-rds-instance.abc123.us-east-1.rds.amazonaws.com'
  iam_role 'arn:aws:iam::123456789012:role/redshift-federated-role'
  secret_arn 'arn:aws:secretsmanager:us-east-1:123456789012:secret:crm-creds';

select c.customer_id, c.email, sum(s.amount) as revenue
from crm.customers c
join analytics.fact_sales s on s.customer_id = c.customer_id
where s.order_date >= date '2026-01-01'
group by c.customer_id, c.email
order by revenue desc
limit 100;
```

Federated Query is for relatively small lookups and enrichment; it is not a substitute for a proper ingestion pipeline when the source is large.

[Table of Contents](#Redshift)

## How can you export data from Amazon Redshift to Amazon S3?

Use `UNLOAD` for large, parallel, server-side exports; use `CREATE EXTERNAL TABLE AS` (CETAS) when you want the exported data to be immediately queryable as a Spectrum table; and use the Redshift Data API plus an application if you need a small, custom extract.

```sql
-- Export a month of sales as Parquet, partitioned by day
unload ('select * from analytics.fact_sales where date_key between 20261001 and 20261031')
to 's3://acme-export/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-unload-role'
format as parquet
partition by (date_key)
allowoverwrite;

-- Export straight into a queryable external table
create external table spectrum_lake.fact_sales_202610
stored as parquet
location 's3://acme-export/fact_sales/2026-10/'
as
select * from analytics.fact_sales where date_key between 20261001 and 20261031;
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift REINDEX command?

There is no standalone `REINDEX` command in Redshift. The equivalent is `VACUUM REINDEX`, which rebuilds the index structure for tables that use an `INTERLEAVED` sort key. `VACUUM REINDEX` first re-analyzes the distribution of values and then rebuilds the interleaved index, which is expensive and should be scheduled.

```sql
-- Only meaningful for interleaved sort keys
vacuum reindex analytics.fact_events;

-- After the reindex, statistics should be refreshed
analyze analytics.fact_events;

-- Check whether a table uses interleaved sort keys
select schema, "table", sortkey1, sortkey_num
from svv_table_info
where sortkey1 is not null
order by schema, table;
```

For compound sort key tables, use `VACUUM SORT ONLY` instead; calling `VACUUM REINDEX` on them does not do what people expect.

[Table of Contents](#Redshift)

## Can you restore a Redshift cluster to a specific point in time?

Yes. Automated snapshots are the basis for point-in-time restore within the retention window (1 to 35 days). Point-in-time restore creates a new cluster from a snapshot as of a chosen time; it does not rewind the existing cluster in place, so the source cluster keeps running and you cut over deliberately.

```bash
# Restore to a specific time into a new cluster
aws redshift restore-from-cluster-snapshot \
  --cluster-identifier analytics-restore-20261004 \
  --snapshot-identifier <automated-snapshot-id> \
  --node-type ra3.4xlarge \
  --number-of-nodes 4 \
  --availability-zone us-east-1a

# Find the snapshot closest to the target time
aws redshift describe-cluster-snapshots \
  --cluster-identifier analytics-cluster \
  --snapshot-type automated \
  --query 'reverse(sort_by(Snapshots,&SnapshotCreateTime))[:5].[SnapshotIdentifier,SnapshotCreateTime]'
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift EXPLAIN command?

`EXPLAIN` prints the query plan the optimizer chose, with each step (scan, hash join, merge join, aggregate, distribute, broadcast) and its estimated cost and row count. It is the first tool for understanding a slow query: look for `DS_DIST_BOTH`, `DS_BCAST_INNER`, `XN_Nested_Loop`, or a full sequential scan where you expected a range-restricted scan.

```sql
explain
select p.category, sum(f.net_amount)
from analytics.fact_sales f
join analytics.dim_product p on f.product_key = p.product_key
where f.date_key between 20261001 and 20261031
group by p.category;

-- Runtime counterpart: where did the time actually go?
select query, stm, seg, step, avg(elapsed_time) as avg_us, sum(rows) as rows
from svl_query_summary
where query = pg_last_query_id()
group by query, stm, seg, step
order by avg_us desc
limit 10;
```

Redshift does not expose a single `EXPLAIN ANALYZE` statement; you pair `EXPLAIN` with execution statistics from `STL`/`SVL` system views.

[Table of Contents](#Redshift)

## Can you create user-defined functions (UDFs) in Amazon Redshift?

Yes, in three forms. SQL UDFs wrap a SQL expression and are inlined by the optimizer. Python UDFs (`LANGUAGE plpythonu`) run scalar Python for logic SQL cannot express, although AWS is phasing them out (no new Python UDFs from Patch 198, with end of support after June 30, 2026). Lambda UDFs call an AWS Lambda function from SQL. Redshift also supports stored procedures for multi-statement logic.

```sql
-- SQL scalar UDF, inlined into the query plan
create function analytics.mask_email(email varchar)
returns varchar
immutable
as $$
  select regexp_replace(email, '^[^@]+', '***')
$$ language sql;

select customer_id, analytics.mask_email(email) as masked_email
from analytics.dim_customer
limit 10;

-- Lambda UDF
create external function analytics.score_risk(features varchar)
returns float
volatile
lambda 'risk-score'
iam_role 'arn:aws:iam::123456789012:role/redshift-lambda-role';
```

Python and Lambda UDFs are slower per row, so reserve them for genuinely custom logic, not for operations SQL already does well.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for star schema data models?

The optimizer is tuned for star schemas: a large fact table surrounded by small dimension tables. If the fact is distributed on the foreign key and the dimensions are small and `DISTSTYLE ALL`, joins require no redistribution; sort keys on the fact (typically date first) allow range pruning; and the optimizer can push dimension filters into the fact scan.

```sql
-- Balanced star schema
create table analytics.fact_sales (
  sale_id bigint, date_key integer, product_key integer,
  store_key integer, net_amount numeric(12,2)
)
diststyle key distkey (product_key)
sortkey (date_key);

create table analytics.dim_product (
  product_key integer, category varchar(64), brand varchar(64)
)
diststyle all sortkey (product_key);

create table analytics.dim_store (
  store_key integer, region varchar(32), city varchar(64)
)
diststyle all sortkey (store_key);
```

[Table of Contents](#Redshift)

## Can you schedule query executions in Amazon Redshift?

Yes. Options include Redshift query editor v2 scheduled queries, EventBridge Scheduler invoking the Redshift Data API, Step Functions with the Redshift integrations, AWS Glue triggers, and Airflow with the Redshift operators. The Data API is the modern, connectionless path.

```bash
# EventBridge Scheduler calling the Redshift Data API via a Lambda target
aws scheduler create-schedule \
  --name nightly-revenue-rollup \
  --schedule-expression 'cron(0 4 * * ? *)' \
  --flexible-time-window 'Mode=OFF' \
  --target '{"Arn":"arn:aws:lambda:us-east-1:123456789012:function:run-redshift-sql","RoleArn":"arn:aws:iam::123456789012:role/scheduler-role"}'
```

```python
# Lambda target: run the SQL and poll for completion
import boto3, time

client = boto3.client("redshift-data")
statement = client.execute_statement(
    WorkgroupName="analytics-wg",
    Database="analytics",
    Sql="refresh materialized view analytics.mv_sales_by_category;",
)["Id"]

while True:
    status = client.describe_statement(Id=statement)["Status"]
    if status in ("FINISHED", "FAILED", "ABORTED"):
        break
    time.sleep(2)
print(status)
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift WLM (Workload Management) configuration?

WLM (Workload Management) divides a cluster's memory and query slots into queues, so that ETL, BI dashboards, and ad-hoc queries do not starve each other. Automatic WLM lets Redshift manage concurrency and memory per queue using query priorities and monitoring rules; manual WLM gives you explicit slot counts and memory percentages. Concurrency scaling and short query acceleration are configured alongside WLM.

```bash
# Automatic WLM with two named queues and priorities
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --wlm-json-configuration '[
    {"name":"bi","auto_wlm":true,"priority":"highest","query_group":"bi","query_concurrency_scaling":"auto"},
    {"name":"etl","auto_wlm":true,"priority":"low","query_group":"etl"},
    {"name":"default","auto_wlm":true,"priority":"normal"}
  ]'
```

```sql
-- Route a query to a queue with a query group label
set query_group to 'etl';
insert into analytics.fact_sales
select * from analytics.stg_sales;
reset query_group;
```

[Table of Contents](#Redshift)

## Can you create Redshift tables from existing Amazon S3 data?

Yes. You can create an external table over the S3 data (Spectrum) and query it in place, or create a native table populated from it with `CREATE TABLE AS` or `COPY`. The choice is about whether the data should be local (fast, costs storage) or remote (cheap, slower, no load).

```sql
-- Remote: external table over S3 Parquet
create external table spectrum_lake.orders (
  order_id varchar(64),
  order_date date,
  amount decimal(12,2)
)
partitioned by (dt varchar(10))
stored as parquet
location 's3://acme-lake/orders/';

-- Local: materialize a copy into Redshift for fast BI
create table analytics.orders_2026
diststyle key distkey (order_id)
sortkey (order_date)
as
select order_id, order_date, amount
from spectrum_lake.orders
where dt between '2026-01-01' and '2026-12-31';
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's TRUNCATECOLUMNS option?

`TRUNCATECOLUMNS` truncates string values that are longer than the target column definition instead of failing the load. It is a pragmatic option for messy source data, but it silently loses data, so use it only where the target length is a deliberate contract and the truncation is acceptable.

```sql
copy analytics.stg_orders
from 's3://acme-lake/raw/orders_2026-10-04.csv'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
csv
ignoreheader 1
truncatecolumns
maxerror 0;

-- Audit: how often did truncation actually bite?
select query, filename, line_number, colname, raw_line, err_reason
from stl_load_errors
where err_code = 1204
order by starttime desc
limit 20;
```

[Table of Contents](#Redshift)

## Can you use Redshift with AWS PrivateLink for private network access?

Yes. Redshift supports VPC endpoints powered by AWS PrivateLink, so clients reach the cluster or Serverless workgroup over a private endpoint inside their VPC instead of the public internet. This keeps traffic on the AWS network, avoids public IP allow-lists, and simplifies cross-account access when combined with endpoint policies.

```bash
# Create an interface VPC endpoint for Redshift in the client VPC
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc1234 \
  --service-name com.amazonaws.us-east-1.redshift \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-0abc1234 subnet-0def5678 \
  --security-group-ids sg-0abc1234
```

Pair PrivateLink with security groups that allow only the application subnets and TLS-required connections.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for time-series data?

Time-series queries are range queries on a timestamp or date, so the decisive design choice is the sort key: put the time column first in a compound sort key so zone maps can skip whole blocks outside the range. Partition the data by time (natively or in Spectrum external tables) and prune with predicates. Materialized views on the daily/weekly grain and Spectrum for cold history keep the hot path small.

```sql
create table analytics.fact_events (
  event_ts   timestamp encode az64,
  event_date date      encode az64,
  device_id  bigint    encode az64,
  metric     numeric(12,4)
)
diststyle even
compound sortkey (event_date, device_id);

-- Range scan prunes blocks using the leading sort key
select device_id, avg(metric) as avg_metric
from analytics.fact_events
where event_date between date '2026-10-01' and date '2026-10-07'
group by device_id;
```

[Table of Contents](#Redshift)

## Can you use Redshift to query and analyze semi-structured data formats like JSON or Avro?

Yes, in two ways. Native `SUPER` columns store semi-structured data in Redshift and are queried with PartiQL and `json_parse`, which is ideal for flexible event attributes you query often. Redshift Spectrum queries JSON, Avro, ORC, Parquet, and Iceberg files in S3 without loading them.

```sql
-- Native SUPER column with PartiQL access
create table analytics.events_super (
  event_id   varchar(64),
  event_ts   timestamp,
  properties super
)
diststyle even sortkey (event_ts);

select
  event_id,
  properties.event_type::varchar as event_type,
  properties.campaign.campaign_id::varchar as campaign_id
from analytics.events_super
where event_ts >= timestamp '2026-10-01 00:00:00';
```

```sql
-- Spectrum external table over JSON, with a serializer/deserializer
create external table spectrum_lake.events_json (
  event_id varchar(64),
  event_ts varchar(32),
  properties varchar(4096)
)
row format serde 'org.openx.data.jsonserde.JsonSerDe'
stored as textfile
location 's3://acme-lake/events-json/';
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's COMPUPDATE option?

`COMPUPDATE` controls whether `COPY` chooses compression encodings for the loaded columns: `ON`/`TRUE` analyzes and applies the best encoding, `PRESET` applies the default without the analysis pass, and `OFF` leaves encodings untouched. `ON` is the usual choice for a table's initial load, and `PRESET` is useful when the extra analysis pass would slow a frequent incremental load without meaningfully changing encodings.

```sql
-- Initial load: pick good encodings
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on;

-- Frequent small load: keep existing encodings, skip the analysis pass
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales_inc/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate preset;
```

[Table of Contents](#Redshift)

## Can you use Redshift cross-region replication for disaster recovery?

Yes. Cross-region snapshot copy replicates snapshots from the primary region to a destination region on a schedule so you can restore there after a regional failure. It is asynchronous, and the copies are encrypted with the destination KMS key. For a hot standby, restore the latest cross-region snapshot into a cluster in the target region and cut over; full active-active multi-region writes are not a native Redshift feature.

```bash
aws redshift enable-snapshot-copy \
  --cluster-identifier analytics-cluster \
  --destination-region us-west-2 \
  --retention-period 7

aws redshift describe-cluster-snapshots \
  --cluster-identifier analytics-cluster \
  --snapshot-type automated \
  --query 'Snapshots[?SnapshotCreateTime>`2026-09-01`].[SnapshotIdentifier,SnapshotCreateTime]'
```

[Table of Contents](#Redshift)

## How does Redshift handle data distribution when a new node is added to the cluster?

A resize changes the number of slices. Redshift redistributes each table according to its distribution style: `KEY` rows hash to the new slice count, `EVEN` rows rebalance round-robin, and `ALL` tables are copied to the new slices. Elastic resize streams the movement with a short reboot; classic resize copies through a temporary cluster and requires a read-only window.

```bash
# After a resize, verify distribution health
psql -h analytics-cluster.abc123.us-east-1.redshift.amazonaws.com -U admin -d analytics \
  -c "select schema, \"table\", diststyle, skew_rows from svv_table_info order by skew_rows desc limit 10;"
```

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Identity and Access Management (IAM) for access control?

Yes, and at several layers: IAM controls the Redshift APIs (create, resize, snapshot, restore); IAM roles and policies grant Spectrum/S3/Glue/Lambda access; database roles control query privileges; IAM database authentication lets users connect with short-lived credentials; and `GetClusterCredentials` issues temporary database credentials without storing passwords.

```sql
-- Database-side roles and grants
create role bi_reader;
grant usage on schema analytics to role bi_reader;
grant select on analytics.mv_sales_by_category to role bi_reader;
grant role bi_reader to user report_svc;
```

```sql
-- IAM role attached to the cluster is used by COPY/Spectrum, not by users
copy analytics.fact_sales
from 's3://acme-lake/curated/fact_sales/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet;
```

[Table of Contents](#Redshift)

## What is the purpose of the Redshift ANALYZE command's DELETE option?

`ANALYZE` has no `DELETE` option - that is a common mix-up with `VACUUM`. `ANALYZE` only collects table and column statistics; `VACUUM DELETE ONLY` is the command that reclaims the space occupied by rows marked for deletion. If statistics are stale or misleading, re-run `ANALYZE`; if storage is bloated by deletes, run `VACUUM DELETE ONLY`.

```sql
-- ANALYZE collects statistics; there is no ANALYZE ... DELETE
analyze analytics.fact_sales;

-- The DELETE option belongs to VACUUM, which reclaims deleted-row space
vacuum delete only analytics.fact_sales;
```

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Glue for data cataloging and ETL?

Yes. Glue Data Catalog can be the metastore behind Spectrum external schemas for S3 and Iceberg data, and Glue jobs (Spark) plus Glue DataBrew can transform and write the Parquet that Redshift loads. Glue crawlers keep the catalog in sync with new S3 partitions, and Redshift can also expose its own tables into Glue for Athena-style access in some configurations.

```sql
-- Spectrum external schema backed by the Glue Data Catalog
create external schema spectrum_lake
from data catalog
database 'acme_lake'
iam_role 'arn:aws:iam::123456789012:role/redshift-spectrum-role'
create external database if not exists;
```

```bash
# Run a Glue job that writes curated Parquet for Redshift COPY
aws glue start-job-run --job-name curate_orders --arguments '{"--dt":"2026-10-04"}'
```

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for dimensionally modeled data warehouses?

For a dimensional model, the optimizer exploits distribution and sort keys to avoid redistribution, uses zone maps to prune fact blocks by date, and pushes dimension filters into the fact scan. The classic advice still holds: distribute the fact on the busiest foreign key, give small dimensions `DISTSTYLE ALL`, sort the fact by the most common date filter, and keep dimensions sorted by their primary key for merge joins.

```sql
-- Common dimension-filtered fact query
select d.calendar_month, p.brand, sum(f.net_amount) as revenue
from analytics.fact_sales f
join analytics.dim_date d on f.date_key = d.date_key
join analytics.dim_product p on f.product_key = p.product_key
where d.calendar_year = 2026 and p.category = 'electronics'
group by d.calendar_month, p.brand;
```

[Table of Contents](#Redshift)

## Can you restore a Redshift cluster to a different cluster?

Yes. A snapshot is independent of the cluster that produced it, so you can restore it into a new cluster - with a different name, node type, node count, or even a different subnet/AZ configuration. This is the standard way to promote a staging snapshot to production, clone a production database for testing, or recover after a failed migration.

```bash
aws redshift restore-from-cluster-snapshot \
  --cluster-identifier analytics-test-clone \
  --snapshot-identifier analytics-prod-2026-10-04 \
  --node-type ra3.4xlarge \
  --number-of-nodes 2 \
  --no-publicly-accessible
```

The restored cluster keeps database contents, users, and cluster metadata from the snapshot; you still need to re-point applications, DNS, and IAM policies.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift VACUUM command's REINDEX option?

`VACUUM REINDEX` rebuilds the interleaved sort-key index for tables defined with `INTERLEAVED SORTKEY`. It re-analyzes the value distribution, drops the old interleaved index, and rebuilds it, which restores the multi-column pruning benefit that degrades after many loads and updates. It is expensive, so schedule it rather than running it casually.

```sql
vacuum reindex analytics.fact_events;
analyze analytics.fact_events;
```

For compound sort key tables, `VACUUM SORT ONLY` is the right tool; `VACUUM REINDEX` is specifically for interleaved keys.

[Table of Contents](#Redshift)

## Can you enable audit logging in Amazon Redshift?

Yes. Redshift writes three audit log streams: connection log (authentication and connection attempts), user log (DDL and DCL statements), and user activity log (every query before and after processing). You can deliver them to Amazon S3 and/or CloudWatch Logs, and each can be enabled independently.

```bash
aws redshift enable-logging \
  --cluster-identifier analytics-cluster \
  --bucket-name acme-redshift-audit \
  --s3-key-prefix audit/ \
  --logging-enabled true
```

```sql
-- Alternatively, the database-level audit views
select * from stl_connection_log order by record_time desc limit 20;
select * from stl_ddltext order by starttime desc limit 20;
select * from stl_userlog order by starttime desc limit 20;
```

Audit logs support compliance (PCI, HIPAA, SOC 2) and incident investigation; store them in a bucket with Object Lock or lifecycle rules that match your retention policy, and restrict who can read them.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for complex join operations?

Redshift can execute nested-loop, hash, and merge joins, and the optimizer picks based on estimated cardinality and whether inputs are already colocated or sorted. For large joins it prefers hash joins with redistribution or broadcast; for sorted inputs it can use merge joins without a sort; nested loops only make sense for tiny outer inputs. `EXPLAIN` shows the chosen method and the movement steps.

```sql
explain
select f.sale_id, c.customer_name
from analytics.fact_sales f
join analytics.dim_customer c on f.customer_id = c.customer_id
where f.date_key = 20261004;
```

Symptoms to look for: `XN_Nested_Loop` on a large table, `DS_DIST_BOTH` on both sides of a big join, or `DS_BCAST_INNER` broadcasting a large inner table. Fixes are distribution-key alignment, `DISTSTYLE ALL` for genuinely small dimensions, and filtering before the join.

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Key Management Service (KMS) for encryption key management?

Yes. Redshift cluster encryption can use AWS KMS customer managed keys (or CloudHSM), with automatic key rotation. KMS is also what encrypts cross-region snapshot copies in the destination region, and what protects `COPY`/`UNLOAD` S3 objects with SSE-KMS. IAM policies govern who may use the key, which is the real access boundary.

```bash
aws redshift modify-cluster \
  --cluster-identifier analytics-cluster \
  --encrypted \
  --kms-key-id alias/redshift-prod

aws kms describe-key --key-id alias/redshift-prod \
  --query 'KeyMetadata.[KeyId,KeyState,KeyManager]'
```

Use separate keys per environment (dev, staging, prod) and grant decrypt only to the roles that operate the cluster.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's ACCEPTINVCHARS option?

`ACCEPTINVCHARS` lets `COPY` replace invalid UTF-8 byte sequences with a replacement character instead of failing. The default replacement is a question mark; you can specify another single ASCII character with `ACCEPTINVCHARS AS '^'`. It is the counterpart to `TRUNCATECOLUMNS` for messy external data.

```sql
copy analytics.stg_orders
from 's3://acme-lake/raw/orders_2026-10-04.csv'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
csv
ignoreheader 1
acceptinvchars as '^'
maxerror 50;
```

Because it silently alters values, log and review the affected rows; if encoding quality matters, fix the producer instead.

[Table of Contents](#Redshift)

## Can you use Redshift with AWS CloudTrail for audit trail and compliance?

Yes. CloudTrail records Redshift control-plane API calls (create/modify/delete cluster, snapshot operations, IAM changes) as events, which you can deliver to S3 and query with Athena or CloudTrail Lake. It complements the database-level audit logs: CloudTrail tells you who changed the infrastructure, Redshift audit logs tell you who ran queries.

```bash
# Confirm that Redshift management events are being recorded
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=redshift.amazonaws.com \
  --max-results 20
```

The two log families together give end-to-end evidence: API changes from CloudTrail, query activity from `STL`/`STV` audit views or S3 audit logs.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for complex aggregations and window functions?

Simple aggregates use hash or stream aggregation, and window functions require the data to be partitioned and sorted by the window definition (`PARTITION BY ... ORDER BY ...`). The optimizer chooses between sorting the input or using an existing sort key; when the window's `PARTITION BY`/`ORDER BY` matches a table's distribution and sort key, Redshift can avoid a re-sort and a redistribution. `QUALIFY` filters on window results without a subquery.

```sql
select
  customer_id,
  order_date,
  sum(amount) over (
    partition by customer_id
    order by order_date
    rows between 90 preceding and current row
  ) as trailing_90d_revenue,
  row_number() over (partition by customer_id order by order_date desc) as recency_rank
from analytics.fact_orders
where order_date >= date '2026-01-01'
qualify recency_rank <= 3;
```

A window whose `PARTITION BY` matches the distribution key keeps each customer's rows on one slice, which avoids a global reshuffle.

[Table of Contents](#Redshift)

## Can you use Redshift with Amazon QuickSight for data visualization and analytics?

Yes. QuickSight connects to Redshift directly or through a VPC connection, and can query live or import into SPICE. For large datasets, the common pattern is to expose curated tables and materialized views, use SPICE for dashboards that tolerate periodic refresh, and reserve direct query for near-real-time operational views.

```sql
-- A dashboard-friendly materialized view that QuickSight can query or import
create materialized view analytics.mv_kpi_daily
auto refresh yes
as
select
  date_trunc('day', order_date) as order_day,
  region,
  channel,
  count(distinct order_id) as orders,
  sum(amount) as revenue
from analytics.fact_orders
group by order_day, region, channel;
```

QuickSight's Redshift connector also supports row-level security pass-through, which lets one dashboard serve many tenants.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift VACUUM command's DELETE option?

`VACUUM DELETE ONLY` reclaims the space occupied by rows that were deleted or superseded by updates, without re-sorting the table. Use it when storage or block efficiency is the problem but row order is already fine (for example after a large delete of an old partition).

```sql
vacuum delete only analytics.fact_orders;
analyze analytics.fact_orders;

-- Compare before and after
select "table", size as size_mb, nvl(unsorted, 0) as unsorted_pct
from svv_table_info
where "table" = 'fact_orders';
```

If rows are also out of order, use `VACUUM SORT ONLY` or full `VACUUM` instead; running both options in a single command is generally the most efficient.

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Lambda for serverless data processing?

Yes, three patterns dominate: Lambda UDFs invoked from SQL, event-driven loads where an S3 event triggers a Lambda that runs `COPY` via the Redshift Data API, and lightweight transformation/validation before the load. Lambda is for short, stateless work; heavy transformation belongs in Glue or Redshift SQL itself.

```python
# S3 event -> Lambda -> Redshift Data API COPY
import boto3, json

redshift = boto3.client("redshift-data")


def handler(event, context):
    key = event["Records"][0]["s3"]["object"]["key"]
    sql = f"""
        copy analytics.stg_orders
        from 's3://acme-lake/{key}'
        iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
        format as parquet
        compupdate preset;
    """
    return redshift.execute_statement(
        WorkgroupName="analytics-wg", Database="analytics", Sql=sql
    )
```

Combine with a dead-letter queue and an audit table so failed loads are visible, not silent.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for large-scale joins and aggregations?

At scale the cost is dominated by data movement and spilling. The optimizer tries to push filters and partial aggregations below the join, choose `KEY`-colocated joins when possible, broadcast only genuinely small inputs, and aggregate on the slice before the final combine. When it cannot, a large hash join spills to disk and the query slows sharply.

```sql
-- Pre-aggregate before the join so the shuffle carries far fewer rows
with daily as (
  select customer_id, date_key, sum(net_amount) as revenue
  from analytics.fact_sales
  where date_key between 20260101 and 20261231
  group by customer_id, date_key
)
select c.region, d.calendar_month, sum(daily.revenue) as revenue
from daily
join analytics.dim_customer c on daily.customer_id = c.customer_id
join analytics.dim_date d on daily.date_key = d.date_key
group by c.region, d.calendar_month;
```

Watch `SVL_QUERY_REPORT` for a single slice doing much more work than the others; that indicates skew, which no amount of join tuning will fix.

[Table of Contents](#Redshift)

## Can you use Redshift with Amazon Athena for ad-hoc SQL queries on S3 data?

Yes, in a complementary way. Athena queries the same Glue Data Catalog and S3 objects serverlessly, which is ideal for occasional ad-hoc exploration and one-off lake queries without touching cluster capacity. Redshift Spectrum handles the same data when it must be joined with warehouse tables. Keep one catalog and one file layout so both engines see the same partitions.

```sql
-- Athena over the same Parquet prefix that Redshift Spectrum reads
select
  dt,
  count(*) as orders,
  sum(amount) as revenue
from acme_lake.orders
where dt between '2026-10-01' and '2026-10-07'
group by dt
order by dt;
```

Practical split: Athena for sparse exploration and log forensics; Redshift/ Spectrum for governed, join-heavy, scheduled analytics.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's ENCRYPTED option?

`ENCRYPTED` tells `COPY` that the files in S3 were encrypted on the client side before upload. You supply the master symmetric key with `MASTER_SYMMETRIC_KEY`, and Redshift decrypts during load. This is different from server-side encryption (SSE-S3/SSE-KMS), where AWS decrypts the object transparently and `COPY` needs no key.

```sql
copy analytics.fact_orders
from 's3://acme-secure/orders/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as csv
master_symmetric_key '${MASTER_KEY}'
encrypted;
```

```bash
# Server-side encrypted variant: no key needed in COPY, but the role needs kms:Decrypt
aws s3 cp ./orders.parquet s3://acme-secure/orders/ \
  --sse aws:kms --sse-kms-key-id alias/acme-data
```

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Step Functions for serverless workflow orchestration?

Yes. Step Functions orchestrates multi-step pipelines with retries, branching, and error handling, and has direct integrations for Redshift (including the Data API), Glue, Lambda, and S3. The typical pipeline is: check S3 for new files, run `COPY`, run `ANALYZE`, refresh materialized views, and publish a completion event.

```json
{
  "Comment": "Daily Redshift ELT",
  "StartAt": "CopyRaw",
  "States": {
    "CopyRaw": {
      "Type": "Task",
      "Resource": "arn:aws:states:::redshift-data:executeStatement",
      "Parameters": {
        "WorkgroupName": "analytics-wg",
        "Database": "analytics",
        "Sql.$": "$.copySql"
      },
      "Retry": [
        {"ErrorEquals": ["States.TaskFailed"], "IntervalSeconds": 60, "MaxAttempts": 3, "BackoffRate": 2}
      ],
      "Next": "RefreshViews"
    },
    "RefreshViews": {
      "Type": "Task",
      "Resource": "arn:aws:states:::redshift-data:executeStatement",
      "Parameters": {
        "WorkgroupName": "analytics-wg",
        "Database": "analytics",
        "Sql": "refresh materialized view analytics.mv_kpi_daily;"
      },
      "End": true
    }
  }
}
```

Step Functions is a good fit for AWS-native shops that do not want to run Airflow; for large DAGs with backfills and data-aware scheduling, Airflow or MWAA is usually more productive.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for data filtering and predicate pushdown?

Predicates are pushed as deep as possible: into the scan so zone maps skip blocks, into Spectrum so S3 objects, row groups, and partitions are pruned, and into federated sources so the remote database filters before returning rows. The optimizer also rewrites `WHERE` clauses, folds constants, and removes redundant joins, but it cannot push a non-sargable expression such as a function on the sort-key column.

```sql
-- Sargable: predicate matches the sort key and prunes blocks
select count(*) from analytics.fact_events
where event_date between date '2026-10-01' and date '2026-10-07';

-- Non-sargable: a function on the sort-key column defeats pruning
select count(*) from analytics.fact_events
where date_part(year, event_date) = 2026;
```

Write range predicates on the bare sort-key column, filter before joining when possible, and keep the leading sort key as the column you constrain most often.

[Table of Contents](#Redshift)

## Can you use Redshift with Amazon Kinesis Data Firehose for real-time data ingestion?

Yes. Firehose buffers streaming records and delivers them to S3 (which Redshift then loads with `COPY`), or uses its Redshift destination, which stages records in S3 and issues a `COPY` for you with configurable buffering, retries, and a manifest. That makes near-real-time ingestion possible without running a consumer.

```sql
-- Firehose delivers to S3; a scheduled COPY loads new files in micro-batches
copy analytics.stg_stream_events
from 's3://acme-firehose/events/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as json 'auto'
compupdate preset
maxerror 100;
```

Firehose buffering (size and interval) is the latency/cost dial: smaller buffers mean fresher data and more, smaller S3 files. The Redshift destination further batches into `COPY`, so sub-minute latency is not its sweet spot - use it for seconds-to-minutes freshness.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift VACUUM command's SORTONLY option?

`VACUUM SORT ONLY` re-sorts rows into sort-key order without reclaiming deleted space. Use it after out-of-order loads or large updates made the table unsorted, so zone maps and merge joins work again. It is cheaper than full `VACUUM` and can run to a threshold.

```sql
vacuum sort only analytics.fact_sales to 95 percent;

analyze analytics.fact_sales;

select "table", nvl(unsorted, 0) as unsorted_pct
from svv_table_info
where "table" = 'fact_sales';
```

If the table is both unsorted and bloated, a full `VACUUM` does both in one pass and is usually the better choice.

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Glue DataBrew for data preparation and cleansing?

Yes. DataBrew provides a visual, no-code interface for profiling and transforming datasets, and it can read from and write to Redshift (and S3, which Redshift then loads). Typical uses are standardizing messy source fields, removing duplicates, and profiling data quality before a `COPY`.

```text
Raw CSV in S3 -> DataBrew recipe (trim, cast, standardize, dedupe) -> Parquet in S3 -> COPY -> Redshift
```

```sql
-- After DataBrew writes clean Parquet, load it
copy analytics.stg_customers
from 's3://acme-cleansed/customers/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate on;
```

DataBrew is a good fit for analyst-driven preparation and one-off cleanup; for repeatable, version-controlled transformation, keep the logic in SQL/dbt or Glue jobs.

[Table of Contents](#Redshift)

## How does Redshift handle query optimization for subqueries and correlated subqueries?

The optimizer decorrelates subqueries where possible, turning `IN`/`EXISTS` predicates into semi-joins and `NOT IN`/`NOT EXISTS` into anti-joins. Scalar correlated subqueries that cannot be decorrelated can be evaluated per row, which is slow on large tables. The usual fix is to rewrite them as joins or window functions.

```sql
-- Correlated scalar subquery: potentially per-row evaluation
select o.order_id,
       (select max(order_date) from analytics.fact_orders p
        where p.customer_id = o.customer_id) as last_order_date
from analytics.fact_orders o;

-- Rewritten with a window function: one pass, no per-row subquery
select
  order_id,
  max(order_date) over (partition by customer_id) as last_order_date
from analytics.fact_orders;
```

Use `EXPLAIN` to confirm the rewrite: look for `XN_HashJoin` with a semi/anti-join step rather than a nested loop over the outer table.

[Table of Contents](#Redshift)

## Can you use Redshift with AWS Lake Formation for data lake management and access control?

Yes. Lake Formation centralizes permissions on S3/Glue Catalog data, and Redshift Spectrum honors those grants, so an external table can be queried only by principals allowed by Lake Formation. Combined with IAM roles, this lets governance live in one place while the same S3 data is queried by Redshift, Athena, and Spark.

```sql
-- Spectrum external schema over a Lake Formation-governed database
create external schema spectrum_governed
from data catalog
database 'governed_lake'
iam_role 'arn:aws:iam::123456789012:role/redshift-spectrum-lf-role'
create external database if not exists;

select count(*) from spectrum_governed.orders where dt = '2026-10-04';
```

The role must be registered with Lake Formation and granted on the relevant tables; if a grant is missing, the query fails with an access error even though the S3 path is reachable.

[Table of Contents](#Redshift)

## What is the purpose of the Redshift COPY command's GZIP option?

`GZIP` tells `COPY` that the input files are gzip-compressed, so Redshift decompresses them on read (and can still parallelize across multiple files). It is the classic way to reduce S3 transfer volume for delimited text. For Parquet and ORC, compression is internal to the format, so you do not use `GZIP` there.

```sql
copy analytics.stg_orders
from 's3://acme-lake/raw/orders_2026-10-04/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
csv
gzip
ignoreheader 1
region 'us-east-1';
```

```bash
# Splitting into many gzip files keeps the load parallel
aws s3 cp ./raw/ s3://acme-lake/raw/orders_2026-10-04/ --recursive --exclude "*" --include "*.csv.gz"
```

A single large gzip file loads on one slice and wastes the cluster; many modest gzip files are the right shape.

[Table of Contents](#Redshift)

## Real world use cases for Redshift

### 1. Retail: store-level sales reporting on RA3

A grocery chain with 800 stores loads 6 TB/month of POS line items and nightly inventory snapshots. The fact table is distributed on `product_key` and sorted by `date_key`; small dimensions use `DISTSTYLE ALL`; cold history older than 24 months lives as Parquet in S3 and is queried through Spectrum.

```sql
create table analytics.fact_pos_lines (
  line_id     bigint,
  date_key    integer,
  store_key   integer,
  product_key integer,
  quantity    integer,
  net_amount  numeric(12,2)
)
diststyle key distkey (product_key)
compound sortkey (date_key, store_key);

-- Store/day rollup served to BI
create materialized view analytics.mv_store_daily
auto refresh yes
as
select date_key, store_key, sum(net_amount) as revenue, sum(quantity) as units
from analytics.fact_pos_lines
group by date_key, store_key;

-- Cold history joined with hot data, no load required
select p.category, sum(s.net_amount) as revenue
from spectrum_lake.pos_history s
join analytics.dim_product p on s.product_key = p.product_key
where s.dt between '2024-01-01' and '2024-12-31'
group by p.category;
```

Why this design: the `product_key` distribution colocates the fact with a `DISTSTYLE ALL` product dimension, so the dominant join has no redistribution; the date-first sort key gives zone-map pruning for the "last N days by store" dashboard; the materialized view keeps the interactive query off the raw fact; and Spectrum keeps the 24-month storage bill on S3 instead of RA3 managed storage.

### 2. Fintech: daily reconciliation with strict freshness and auditability

A payments processor ingests 120 million card transactions per day and must reconcile them against processor settlement files by 06:00, with seven years of queryable history for audits. The load is a single parallel `COPY` from encrypted Parquet, followed by a `MERGE`-based exception step and an `ANALYZE`.

```sql
copy analytics.stg_transactions
from 's3://acme-secure/txn/2026-10-04/'
iam_role 'arn:aws:iam::123456789012:role/redshift-copy-role'
format as parquet
compupdate preset
maxerror 0;

merge into analytics.fact_transactions t
using (
  select txn_id, account_id, txn_ts, amount, processor_amount, ingested_at,
         row_number() over (partition by txn_id order by ingested_at desc) as rn
  from analytics.stg_transactions
) s
on t.txn_id = s.txn_id and s.rn = 1
when matched then update set t.processor_amount = s.processor_amount
when not matched then insert (txn_id, account_id, txn_ts, amount, processor_amount, ingested_at)
values (s.txn_id, s.account_id, s.txn_ts, s.amount, s.processor_amount, s.ingested_at);

analyze analytics.fact_transactions;

select count(*) as breaks
from analytics.fact_transactions
where amount <> processor_amount and txn_date = current_date - 1;
```

Why this design: `MAXERROR 0` makes a bad settlement file fail the run instead of loading partially; the dedup window plus `MERGE` makes reruns idempotent; the sorting is on the transaction timestamp so audit range queries prune; and audit logging plus cross-region snapshot copy satisfy the retention and DR requirements.

### 3. Marketing: multi-channel attribution and spend reporting

An e-commerce company spends across Google, Meta, and TikTok and loads about 40 GB/day of click and impression data plus 2 GB/day of ad spend. Ad platform files land in S3 as Parquet; attribution runs nightly in Redshift against order data; dashboards query a materialized view.

```sql
create table analytics.fact_touchpoints (
  touch_id    bigint,
  user_id     bigint,
  channel     varchar(32),
  campaign_id varchar(64),
  event_ts    timestamp,
  event_date  date
)
diststyle key distkey (user_id)
compound sortkey (event_date, channel);

create table analytics.fact_spend (
  spend_date  date,
  channel     varchar(32),
  campaign_id varchar(64),
  spend       numeric(12,2)
)
diststyle even sortkey (spend_date, channel);

create materialized view analytics.mv_roas_daily
auto refresh yes
as
select
  t.event_date,
  t.channel,
  count(distinct t.user_id) as reach,
  sum(s.spend) as spend
from analytics.fact_touchpoints t
left join analytics.fact_spend s
  on s.channel = t.channel and s.spend_date = t.event_date
group by t.event_date, t.channel;
```

Why this design: distributing both facts on the channel/date grain keeps the nightly attribution join local; sorting on `event_date` keeps the 30-day lookback scans bounded; and the materialized view gives the marketing team sub-second ROAS without re-running attribution.

### 4. SaaS: product and revenue analytics with governed self-service

A B2B SaaS company stores 3 TB of event and subscription data in Redshift and exposes it to analysts and to embedded customer dashboards. Row-level security isolates tenants, column-level grants hide PII, and WLM separates BI from ETL.

```sql
-- Tenant isolation and column-level least privilege
create role tenant_reader;
grant usage on schema product to role tenant_reader;
grant select (event_date, account_id, event_name, event_count) on product.fact_usage to role tenant_reader;

create rls policy tenant_isolation
  with (account_id varchar(64))
  using (account_id = current_setting('app.account_id'));

attach rls policy tenant_isolation
  on product.fact_usage to role tenant_reader;

-- WLM separation: dashboards get priority, ETL gets a low-priority queue
-- (configured on the cluster; see the WLM question)
```

Why this design: row-level security lets one physical table serve every tenant without duplicating data; WLM priority ensures an ETL backfill cannot degrade customer-facing dashboards; and concurrency scaling absorbs the morning dashboard spike without permanently adding nodes.

### 5. Logistics: fleet telemetry and SLA monitoring

A logistics operator tracks 9,000 vehicles reporting every 15 seconds, about 50 GB/day compressed. Events land in S3 via Firehose, load into a date-sorted fact table, and a nightly job computes on-time delivery SLA by lane. Data older than 90 days is archived with `UNLOAD` to Parquet and dropped from the cluster.

```sql
create table analytics.fact_telemetry (
  vehicle_id  bigint,
  event_ts    timestamp,
  event_date  date,
  lat         numeric(9,6),
  lon         numeric(9,6),
  speed_kph   numeric(6,2),
  fuel_pct    numeric(5,2)
)
diststyle even
compound sortkey (event_date, vehicle_id);

-- Archive before dropping the hot copy
unload ('select * from analytics.fact_telemetry where event_date < current_date - 90')
to 's3://acme-archive/telemetry/'
iam_role 'arn:aws:iam::123456789012:role/redshift-unload-role'
format as parquet
partition by (event_date)
manifest
allowoverwrite;

delete from analytics.fact_telemetry where event_date < current_date - 90;
vacuum delete only analytics.fact_telemetry;
analyze analytics.fact_telemetry;
```

Why this design: a date-first compound sort key makes the "last 24 hours for a lane" range query prune hard; `UNLOAD` to Parquet keeps archive costs on S3 while remaining queryable through Spectrum; and a weekly `VACUUM DELETE ONLY` reclaims the space from the archive delete without a full resort.

[Table of Contents](#Redshift)
