## [Main title](../README.md)
### [Interview questions](full.md)

# BigQuery

**Notebook:** [`notebooks/topics/bigquery.ipynb`](../notebooks/topics/bigquery.ipynb) - runnable version of this topic with self-checking exercises.

+ [What is BigQuery, and how does it fit into the data engineering ecosystem?](#What-is-BigQuery-and-how-does-it-fit-into-the-data-engineering-ecosystem)
+ [How do partitioning and clustering improve BigQuery performance?](#How-do-partitioning-and-clustering-improve-BigQuery-performance)
+ [How do you control cost in BigQuery?](#How-do-you-control-cost-in-BigQuery)
+ [How does BigQuery handle data storage and processing?](#How-does-BigQuery-handle-data-storage-and-processing)
+ [What are the key advantages of using BigQuery?](#What-are-the-key-advantages-of-using-BigQuery)
+ [What is the difference between BigQuery and traditional relational databases?](#What-is-the-difference-between-BigQuery-and-traditional-relational-databases)
+ [Explain the concept of partitioning in BigQuery.](#Explain-the-concept-of-partitioning-in-BigQuery)
+ [What is clustering, and how does it optimize query performance?](#What-is-clustering-and-how-does-it-optimize-query-performance)
+ [How do you load data into BigQuery?](#How-do-you-load-data-into-BigQuery)
+ [What are the different data export options in BigQuery?](#What-are-the-different-data-export-options-in-BigQuery)
+ [Explain the concept of federated queries in BigQuery.](#Explain-the-concept-of-federated-queries-in-BigQuery)
+ [What are the best practices for optimizing query performance in BigQuery?](#What-are-the-best-practices-for-optimizing-query-performance-in-BigQuery)
+ [How does BigQuery handle data security?](#How-does-BigQuery-handle-data-security)
+ [What is the difference between a table and a view in BigQuery?](#What-is-the-difference-between-a-table-and-a-view-in-BigQuery)
+ [Explain the concept of nested and repeated fields in BigQuery.](#Explain-the-concept-of-nested-and-repeated-fields-in-BigQuery)
+ [How can you schedule and automate jobs in BigQuery?](#How-can-you-schedule-and-automate-jobs-in-BigQuery)
+ [What is the role of BigQuery Data Transfer Service?](#What-is-the-role-of-BigQuery-Data-Transfer-Service)
+ [How does BigQuery handle data ingestion from streaming sources?](#How-does-BigQuery-handle-data-ingestion-from-streaming-sources)
+ [What are the limitations or constraints of using BigQuery?](#What-are-the-limitations-or-constraints-of-using-BigQuery)
+ [How can you monitor and optimize BigQuery costs?](#How-can-you-monitor-and-optimize-BigQuery-costs)
+ [Explain the difference between BigQuery slots and slots reservation.](#Explain-the-difference-between-BigQuery-slots-and-slots-reservation)
+ [Can you share your experience with implementing data pipelines in BigQuery?](#Can-you-share-your-experience-with-implementing-data-pipelines-in-BigQuery)
+ [What is the difference between a view and a materialized view in BigQuery?](#What-is-the-difference-between-a-view-and-a-materialized-view-in-BigQuery)
+ [How does BigQuery handle data partitioning and clustering?](#How-does-BigQuery-handle-data-partitioning-and-clustering)
+ [Can you explain the concept of data sharding in BigQuery?](#Can-you-explain-the-concept-of-data-sharding-in-BigQuery)
+ [How does BigQuery handle schema changes for large tables?](#How-does-BigQuery-handle-schema-changes-for-large-tables)
+ [What are the benefits of using partitioned tables in BigQuery?](#What-are-the-benefits-of-using-partitioned-tables-in-BigQuery)
+ [How can you control access and permissions in BigQuery?](#How-can-you-control-access-and-permissions-in-BigQuery)
+ [What is the role of service accounts in BigQuery?](#What-is-the-role-of-service-accounts-in-BigQuery)
+ [Can you explain the concept of slots in BigQuery?](#Can-you-explain-the-concept-of-slots-in-BigQuery)
+ [What is the purpose of BigQuery reservations?](#What-is-the-purpose-of-BigQuery-reservations)
+ [How can you optimize query performance in BigQuery?](#How-can-you-optimize-query-performance-in-BigQuery)
+ [How does BigQuery handle data encryption?](#How-does-BigQuery-handle-data-encryption)
+ [Can you explain the concept of query caching in BigQuery?](#Can-you-explain-the-concept-of-query-caching-in-BigQuery)
+ [How can you export BigQuery query results to a file?](#How-can-you-export-BigQuery-query-results-to-a-file)
+ [What is the purpose of the BigQuery Data Transfer Service?](#What-is-the-purpose-of-the-BigQuery-Data-Transfer-Service)
+ [Can you explain the concept of streaming inserts in BigQuery?](#Can-you-explain-the-concept-of-streaming-inserts-in-BigQuery)
+ [What is the difference between a table decorator and a snapshot decorator in BigQuery?](#What-is-the-difference-between-a-table-decorator-and-a-snapshot-decorator-in-BigQuery)
+ [How does BigQuery handle data deduplication?](#How-does-BigQuery-handle-data-deduplication)
+ [Can you explain the concept of streaming buffer in BigQuery?](#Can-you-explain-the-concept-of-streaming-buffer-in-BigQuery)
+ [What are the limitations of using BigQuery streaming inserts?](#What-are-the-limitations-of-using-BigQuery-streaming-inserts)
+ [How does BigQuery handle nested and repeated fields in JSON data?](#How-does-BigQuery-handle-nested-and-repeated-fields-in-JSON-data)
+ [Can you explain the concept of the BigQuery Data Catalog?](#Can-you-explain-the-concept-of-the-BigQuery-Data-Catalog)
+ [How can you optimize data storage costs in BigQuery?](#How-can-you-optimize-data-storage-costs-in-BigQuery)
+ [What is the purpose of the INFORMATION_SCHEMA in BigQuery?](#What-is-the-purpose-of-the-INFORMATION_SCHEMA-in-BigQuery)
+ [Can you explain the concept of data lineage in BigQuery?](#Can-you-explain-the-concept-of-data-lineage-in-BigQuery)
+ [How does BigQuery handle nested data types like arrays and structs?](#How-does-BigQuery-handle-nested-data-types-like-arrays-and-structs)
+ [What is the purpose of the BigQuery ML service?](#What-is-the-purpose-of-the-BigQuery-ML-service)
+ [How can you monitor and troubleshoot query performance in BigQuery?](#How-can-you-monitor-and-troubleshoot-query-performance-in-BigQuery)
+ [Can you explain the concept of table clustering and its benefits?](#Can-you-explain-the-concept-of-table-clustering-and-its-benefits)
+ [How does BigQuery handle query optimization and query execution?](#How-does-BigQuery-handle-query-optimization-and-query-execution)
+ [What is the purpose of BigQuery BI Engine?](#What-is-the-purpose-of-BigQuery-BI-Engine)
+ [Can you explain the concept of wildcard tables in BigQuery?](#Can-you-explain-the-concept-of-wildcard-tables-in-BigQuery)
+ [What are the different data ingestion options in BigQuery?](#What-are-the-different-data-ingestion-options-in-BigQuery)
+ [How does BigQuery handle data deduplication during batch loading?](#How-does-BigQuery-handle-data-deduplication-during-batch-loading)
+ [Can you explain the concept of clustering keys in BigQuery?](#Can-you-explain-the-concept-of-clustering-keys-in-BigQuery)
+ [What are the best practices for data modeling in BigQuery?](#What-are-the-best-practices-for-data-modeling-in-BigQuery)
+ [How does BigQuery handle data backup and recovery?](#How-does-BigQuery-handle-data-backup-and-recovery)
+ [Can you explain the concept of materialized views in BigQuery?](#Can-you-explain-the-concept-of-materialized-views-in-BigQuery)
+ [How does BigQuery handle data export to external services?](#How-does-BigQuery-handle-data-export-to-external-services)
+ [What is the purpose of BigQuery ML's CREATE MODEL statement?](#What-is-the-purpose-of-BigQuery-MLs-CREATE-MODEL-statement)
+ [Can you explain the concept of geographic data types in BigQuery?](#Can-you-explain-the-concept-of-geographic-data-types-in-BigQuery)
+ [How does BigQuery handle data privacy and security?](#How-does-BigQuery-handle-data-privacy-and-security)
+ [Can you explain the concept of slot reservations in BigQuery?](#Can-you-explain-the-concept-of-slot-reservations-in-BigQuery)
+ [What are the different types of pricing models available for BigQuery?](#What-are-the-different-types-of-pricing-models-available-for-BigQuery)
+ [How can you automate BigQuery tasks using Cloud Composer?](#How-can-you-automate-BigQuery-tasks-using-Cloud-Composer)
+ [Can you explain the concept of BigQuery Omni?](#Can-you-explain-the-concept-of-BigQuery-Omni)
+ [What is the purpose of the BigQuery Storage API?](#What-is-the-purpose-of-the-BigQuery-Storage-API)
+ [How can you handle schema evolution in BigQuery?](#How-can-you-handle-schema-evolution-in-BigQuery)
+ [Can you explain the concept of time travel in BigQuery?](#Can-you-explain-the-concept-of-time-travel-in-BigQuery)
+ [What is the purpose of the BigQuery ML TRANSFORM statement?](#What-is-the-purpose-of-the-BigQuery-ML-TRANSFORM-statement)
+ [How does BigQuery handle data consistency in distributed queries?](#How-does-BigQuery-handle-data-consistency-in-distributed-queries)
+ [Can you explain the concept of BigQuery's query cache?](#Can-you-explain-the-concept-of-BigQuerys-query-cache)
+ [What is the purpose of the BigQuery Data Transfer Service for SaaS?](#What-is-the-purpose-of-the-BigQuery-Data-Transfer-Service-for-SaaS)
+ [How can you monitor and troubleshoot streaming data pipelines in BigQuery?](#How-can-you-monitor-and-troubleshoot-streaming-data-pipelines-in-BigQuery)
+ [Can you explain the concept of BigQuery federated queries?](#Can-you-explain-the-concept-of-BigQuery-federated-queries)
+ [What is the purpose of the BigQuery Data QnA service?](#What-is-the-purpose-of-the-BigQuery-Data-QnA-service)
+ [Can you explain the concept of BigQuery's workload management?](#Can-you-explain-the-concept-of-BigQuerys-workload-management)
+ [How does BigQuery handle data skew and hotspots in queries?](#How-does-BigQuery-handle-data-skew-and-hotspots-in-queries)
+ [What is the purpose of the BigQuery ML EVALUATE statement?](#What-is-the-purpose-of-the-BigQuery-ML-EVALUATE-statement)
+ [Can you explain the concept of BigQuery's billing export?](#Can-you-explain-the-concept-of-BigQuerys-billing-export)
+ [How can you automate BigQuery tasks using Cloud Functions?](#How-can-you-automate-BigQuery-tasks-using-Cloud-Functions)
+ [Real world use cases for BigQuery](#Real-world-use-cases-for-BigQuery)

## What is BigQuery, and how does it fit into the data engineering ecosystem?

BigQuery is Google Cloud's fully managed, serverless, columnar analytics warehouse. It separates storage (Colossus) from compute (Dremel slots), so you do not size clusters: you size slots, or let on-demand autoscaling handle burst. In a modern GCP platform it is usually the curated/serving layer, with Pub/Sub, Datastream, or Data Transfer Service for ingestion, Cloud Storage plus Iceberg or Parquet external tables for the lake, and dbt, Dataform, or Airflow for transformation.

```text
Sources            Ingestion                 Warehouse (BigQuery)              Consumption
-------            ---------                 ------------------                -----------
apps / OLTP  -->   Datastream / Pub/Sub  --> raw (landing, partitioned)   --> Looker / BI
SaaS         -->   Data Transfer Service --> staging (typed, deduped)      --> BigQuery ML
files        -->   bq load / LOAD DATA   --> marts (star schema, clustered) --> export to GCS
```

```bash
# The same curated table from the command line
bq query --use_legacy_sql=false '
select count(*) as orders, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
where order_date = current_date() - 1'
```

[Table of Contents](#BigQuery)

## How do partitioning and clustering improve BigQuery performance?

Partitioning splits a table into physical segments (usually by date), so a query with a partition filter scans only matching segments. Clustering sorts data within each partition by up to four columns, so block-level min/max metadata prunes more. Together they reduce bytes scanned, which reduces both latency and on-demand cost.

```sql
create table `acme-prod.analytics.fact_orders`
(
  order_id    string not null,
  customer_id string,
  order_ts    timestamp,
  order_date  date,
  status      string,
  amount      numeric(12,2)
)
partition by order_date
cluster by customer_id, status
as
select order_id, customer_id, order_ts, order_date, status, amount
from `acme-prod.staging.orders`;
```

The filter below prunes partitions on `order_date` and blocks inside each partition on `customer_id`:

```sql
select customer_id, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
where order_date between date '2026-09-01' and date '2026-09-30'
  and customer_id = 'c-1042'
group by customer_id;
```

Trade-off: partition on the column people actually filter by (usually a date). Over-partitioning by a high-cardinality key creates millions of tiny partitions and hurts more than it helps. Cluster columns are ordered - the first is the most effective.

[Table of Contents](#BigQuery)

## How do you control cost in BigQuery?

On-demand cost is driven by bytes scanned; capacity cost is driven by slots; storage has its own price. Control it by filtering partitions, selecting only needed columns, materializing repeated aggregations, and watching the biggest queries in `INFORMATION_SCHEMA.JOBS`.

```sql
-- The 20 most expensive queries in the last 7 days
select
  user_email,
  job_id,
  round(total_bytes_billed / pow(1024, 4), 2) as tib_billed,
  round(total_bytes_billed / pow(1024, 4) * 6.25, 2) as est_usd
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 7 day)
  and job_type = 'QUERY'
order by total_bytes_billed desc
limit 20;
```

```bash
# Dry-run first: shows bytes processed without running or billing the query
bq query --use_legacy_sql=false --dry_run '
select * from `acme-prod.analytics.fact_events` where event_date = current_date()'
```

Practical levers: avoid `select *` on wide tables, use `partition by` on the date column, cluster on the next filter columns, prefer `materialized view` for repeated rollups, set custom quotas per project, and set budgets plus alerts. Exact on-demand rates and free tiers change, so verify current pricing before quoting a number in an interview.

[Table of Contents](#BigQuery)

## How does BigQuery handle data storage and processing?

BigQuery uses a disaggregated architecture. Storage lives in Colossus, Google's distributed file system, replicated and encrypted. Compute is Dremel: a tree of mixers and leaf nodes that read columnar Capacitor-encoded data, shuffle over the Jupiter network, and return results. Because storage and compute scale independently, a slow query is a slot/shuffle problem, not a "the disk is full" problem.

```bash
# Inspect the table and its partitioning/clustering without querying data
bq show --format=prettyjson acme-prod:analytics.fact_orders | head -60

# Schema only
bq show --schema --format=prettyjson acme-prod:analytics.fact_orders
```

Interview framing: BigQuery has no indexes, no user-managed nodes, and no manual statistics. The optimizers of Dremel plus the metadata layer do the work, and the levers you own are partitioning, clustering, materialized views, and slots.

[Table of Contents](#BigQuery)

## What are the key advantages of using BigQuery?

+ Serverless and fully managed: no clusters, no vacuuming, no version upgrades.
+ Separate storage and compute: petabyte-scale storage with independent slot scaling.
+ Fast columnar scans and a mature SQL optimizer, including automatic materialized-view rewrite.
+ Native nested and repeated types, which reduces the need to flatten events.
+ Built-in ML, GIS, governance, and streaming without extra products.
+ Pay-per-use on-demand or predictable capacity pricing.

```sql
-- Nested event data and a geographic filter in the same engine, no extra tooling
select
  customer_id,
  count(*) as purchases,
  st_distance(
    st_geogpoint(-87.6298, 41.8781),
    pickup_location
  ) as meters_from_downtown
from `acme-prod.analytics.fact_deliveries`
where delivery_date = current_date() - 1
group by customer_id, meters_from_downtown
order by purchases desc
limit 10;
```

[Table of Contents](#BigQuery)

## What is the difference between BigQuery and traditional relational databases?

| Aspect | Traditional RDBMS | BigQuery |
|---|---|---|
| Storage layout | Row-oriented, pages | Columnar, Capacitor |
| Scale | Vertical, fixed hardware | Horizontal, managed |
| Schema | Strict, migration-driven | Strongly typed but supports cheap ADD COLUMN |
| Indexes | B-tree, secondary indexes | None; sort via clustering |
| Transactions | Row-level ACID, high TPS | Snapshot isolation, analytic DML, no high-TPS OLTP |
| Concurrency model | Connection/threads | Slots and reservations |
| Cost model | License/hardware | Bytes scanned or slots + storage |

```sql
-- Analytical pattern BigQuery is built for
select date_trunc(order_date, month) as month, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
group by month
order by month;
```

[Table of Contents](#BigQuery)

## Explain the concept of partitioning in BigQuery.

Partitioning splits a table into segments identified by a partition column. BigQuery supports time-unit partitioning on `date`/`timestamp`/`datetime`, ingestion-time partitioning on `_PARTITIONTIME`, integer range partitioning, and (preview) categorical partitioning on a string column. Every partition has its own metadata, so filters and `delete`/`truncate` operations can target one segment.

```sql
create table `acme-prod.analytics.events`
(
  event_id   string,
  user_id    string,
  event_ts   timestamp,
  event_type string
)
partition by date(event_ts)
cluster by user_id
options (
  partition_expiration_days = 730,
  require_partition_filter = true
);
```

`require_partition_filter = true` is a strong cost guardrail: a query that forgets the partition filter fails instead of scanning everything. Inspect partitions with:

```sql
select partition_id, total_rows, total_logical_bytes
from `acme-prod.analytics.information_schema.partitions`
where table_name = 'events'
order by partition_id desc
limit 10;
```

[Table of Contents](#BigQuery)

## What is clustering, and how does it optimize query performance?

Clustering physically sorts data within each partition by up to four columns. BigQuery stores block-level min/max metadata for clustered columns, so a filter on a clustered column lets the engine skip blocks instead of reading the whole partition. Clustering also improves aggregation performance on the clustered columns because matching rows are adjacent.

```sql
select order_id, amount
from `acme-prod.analytics.fact_orders`
where order_date = date '2026-10-01'   -- partition pruning
  and status = 'refunded'              -- block pruning via clustering
  and customer_id = 'c-9001';          -- leading cluster column
```

Notes that matter in interviews: order of `cluster by` matters (most selective/filtered first), clustering is automatic after load (BigQuery re-clusters in the background for new data), and clustering does not replace partitioning - it works on top of it.

[Table of Contents](#BigQuery)

## How do you load data into BigQuery?

The main paths are batch load from Cloud Storage, `LOAD DATA` SQL, streaming via the Storage Write API or legacy `insertAll`, and managed connectors through the Data Transfer Service.

```bash
# Batch load Parquet from GCS with an explicit schema (fastest and cheapest)
bq load \
  --source_format=PARQUET \
  --replace \
  acme-prod:analytics.fact_orders \
  'gs://acme-landing/orders/dt=2026-10-04/*.parquet'

# CSV with autodetect and a bad-row tolerance
bq load --source_format=CSV --autodetect --skip_leading_rows=1 \
  --max_bad_records=100 \
  acme-prod:staging.orders_raw 'gs://acme-landing/orders/2026-10-04.csv'
```

```sql
-- Server-side load from GCS into an existing table
load data into `acme-prod.analytics.fact_orders`
from files (
  format = 'PARQUET',
  uris = ['gs://acme-landing/orders/dt=2026-10-04/*.parquet']
);
```

Batch loads are free (you pay only storage); streaming inserts are billed per byte. Prefer Parquet or Avro over CSV, and split into multiple files for parallel load.

[Table of Contents](#BigQuery)

## What are the different data export options in BigQuery?

| Option | Shape | Notes |
|---|---|---|
| `EXPORT DATA` | SQL, server-side | Best for scheduled/partitioned exports |
| `bq extract` | CLI/API | Single table or a query result |
| BigQuery Storage Read API | Programmatic | Fast row reads into Spark/Dataflow |
| Connected Sheets / BI tools | UI | Analysis, not bulk export |
| BigQuery Data Transfer / partner tools | Managed | Fivetran, Datastream reverse ETL |

```sql
-- Server-side export, one file per partition, Parquet
export data options (
  uri = 'gs://acme-export/orders/dt=2026-10-04/*.parquet',
  format = 'PARQUET',
  compression = 'SNAPPY',
  overwrite = true
)
as
select * from `acme-prod.analytics.fact_orders`
where order_date = date '2026-10-04';
```

```bash
# Client-side extract of a table to CSV shards
bq extract --destination_format=CSV --compression=GZIP \
  acme-prod:analytics.fact_orders \
  'gs://acme-export/orders-*.csv.gz'
```

[Table of Contents](#BigQuery)

## Explain the concept of federated queries in BigQuery.

Federated queries let BigQuery read data that lives outside it - Cloud SQL, AlloyDB, Spanner, Bigtable, Cloud Storage (Parquet/ORC/Avro/JSON/CSV/Iceberg), and Google Sheets - without copying it in. `EXTERNAL_QUERY` pushes SQL to an external connection; external tables are metadata over files; Bigtable and Spanner expose external tables directly.

```sql
-- Join a BigQuery warehouse table to live Cloud SQL data via a connection
select o.order_id, o.amount, c.email, c.segment
from `acme-prod.analytics.fact_orders` o
join external_query(
  'projects/acme-prod/locations/us/connections/cloudsql-crm',
  'select customer_id, email, segment from crm.customers'
) c
on o.customer_id = c.customer_id
where o.order_date = date '2026-10-04';
```

```sql
-- External table over Parquet in Cloud Storage
create external table `acme-prod.raw.orders_ext`
options (
  format = 'PARQUET',
  uris = ['gs://acme-landing/orders/dt=2026-10-04/*.parquet']
);
```

Trade-off: federation avoids copy pipelines but pushes load onto the source and is usually slower than a native table. Use it for small dimension lookups or exploration, not for the fact table driving a dashboard.

[Table of Contents](#BigQuery)

## What are the best practices for optimizing query performance in BigQuery?

+ Filter on the partition column and keep `require_partition_filter` on hot tables.
+ Select only needed columns; wide `select *` is the most common cost bug.
+ Cluster on the first two or three columns that appear in `where` and `group by`.
+ Filter early, aggregate before joining large fact tables, and avoid `cross join` blowups.
+ Use `approximate_count_distinct` or `approx_quantiles` when exactness is not required.
+ Materialize repeated rollups as materialized views or scheduled aggregate tables.
+ Watch the query plan: high shuffle or a single hot stage usually means a skew or join-order problem.

```sql
-- Aggregating before the join keeps the shuffle small
with daily as (
  select customer_id, sum(amount) as revenue
  from `acme-prod.analytics.fact_orders`
  where order_date = date '2026-10-04'
  group by customer_id
)
select c.segment, sum(d.revenue) as revenue
from daily d
join `acme-prod.analytics.dim_customer` c using (customer_id)
group by c.segment;
```

[Table of Contents](#BigQuery)

## How does BigQuery handle data security?

BigQuery layers IAM, dataset/table/column/row-level controls, encryption, network controls, and audit logging.

+ IAM roles at project, dataset, table, view, and column level (fine-grained reader/writer).
+ Policy tags for column-level security and dynamic data masking.
+ Row access policies for row filtering without exposing the predicate.
+ CMEK via Cloud KMS, plus default Google-managed encryption at rest and TLS in transit.
+ VPC Service Controls and Private Google Access for network isolation.
+ Cloud Audit Logs for admin activity, data access, and system events.

```sql
-- Row-level security: each regional manager sees only their region
create row access policy acme_region_policy on `acme-prod.analytics.fact_orders`
grant to ('group:emea-managers@acme.com')
filter using (region = 'EMEA');

-- Column-level security uses policy tags on the schema
alter table `acme-prod.analytics.fact_orders`
alter column customer_email set options (
  policy_tags = 'projects/acme-prod/locations/us/taxonomies/123/policyTags/456'
);
```

[Table of Contents](#BigQuery)

## What is the difference between a table and a view in BigQuery?

A table stores data and is billed for storage; a view is a saved query that stores no data and is billed only when queried (the underlying tables are scanned). Materialized views sit between the two: they store precomputed results. Use views for logical models, PII masking, and decoupling consumers from physical schemas.

```sql
create view `acme-prod.analytics.v_orders_safe` as
select
  order_id,
  customer_id,
  order_date,
  status,
  amount
from `acme-prod.analytics.fact_orders`
where order_date >= date '2024-01-01';

-- Authorized view: share a subset without granting the base table
-- (run as the view owner against a private dataset)
create view `acme-prod.shared.v_orders_emea` as
select * from `acme-prod.private.fact_orders` where region = 'EMEA';
```

Note that a view's SQL is re-executed on every read; a view over a huge unpartitioned table is a cost trap. Push filters down and keep views thin.

[Table of Contents](#BigQuery)

## Explain the concept of nested and repeated fields in BigQuery.

`STRUCT` gives you a nested record (a row within a row); `ARRAY` gives you a repeated field (many values per row). BigQuery stores both natively in a columnar layout, so you can model one order with many line items without a join and without duplicating the order header. Query them with dot notation and `unnest`.

```sql
create table `acme-prod.analytics.orders_nested`
(
  order_id  string,
  order_ts  timestamp,
  customer  struct<customer_id string, segment string>,
  items     array<struct<sku string, qty int64, price numeric(12,2)>>
)
partition by date(order_ts);
```

```sql
select
  order_id,
  customer.segment,
  item.sku,
  item.qty * item.price as line_amount
from `acme-prod.analytics.orders_nested`,
unnest(items) as item
where date(order_ts) = date '2026-10-04'
  and customer.segment = 'enterprise';
```

Trade-off: nesting reduces storage and joins, but a query that always explodes every array pays the cost anyway. Model the grain of your most common query: if analysts almost always want line-item grain, a flat fact table is often simpler.

[Table of Contents](#BigQuery)

## How can you schedule and automate jobs in BigQuery?

BigQuery scheduled queries are transfer configs that run SQL on a schedule. For multi-step pipelines, use Cloud Composer (Airflow), Workflows, or dbt/Dataform with a scheduler. Cloud Scheduler can also trigger a Cloud Run job or function.

```bash
# Create a scheduled query (daily rollup at 02:00)
bq mk --transfer_config \
  --project_id=acme-prod \
  --data_source=scheduled_query \
  --target_dataset=analytics \
  --display_name='nightly revenue rollup' \
  --schedule='every day 02:00' \
  --params='{"query":"insert into `acme-prod.analytics.revenue_daily` select order_date, sum(amount) as revenue from `acme-prod.analytics.fact_orders` where order_date = current_date() - 1 group by order_date"}'
```

```bash
# Trigger on demand
bq mk --transfer_run \
  --run_time='2026-10-05T02:00:00Z' \
  projects/acme-prod/locations/us/transferConfigs/1234-abcd
```

Operational advice: make scheduled queries idempotent (delete/insert for a date, or `merge`), alert on transfer failures in Cloud Logging, and keep the schedule and the data timezone explicit.

[Table of Contents](#BigQuery)

## What is the role of BigQuery Data Transfer Service?

The Data Transfer Service (DTS) is the managed connector framework for loading data into BigQuery on a schedule. It covers Google Marketing Platform (Ads, Campaign Manager, Search Ads 360), Google Ads, YouTube, Cloud Storage transfers, Amazon S3, Teradata, and many SaaS connectors, plus scheduled queries.

```bash
# Google Ads transfer into a dataset
bq mk --transfer_config \
  --project_id=acme-prod \
  --data_source=google_ads \
  --target_dataset=marketing_raw \
  --display_name='google ads daily' \
  --schedule='every day 06:00' \
  --params='{"customer_id":"1234567890","refresh_window_days":"7","report_configs":[{"table_id":"ads_campaign","start_date":"2026-01-01"}]}'
```

```bash
# Check transfer run history
bq ls --transfer_log --transfer_config \
  projects/acme-prod/locations/us/transferConfigs/1234-abcd
```

Backfills and lookback windows are the important detail: most connectors re-pull a rolling window, so the load must be idempotent (partition overwrite or merge), not a blind append.

[Table of Contents](#BigQuery)

## How does BigQuery handle data ingestion from streaming sources?

Three patterns dominate. Pub/Sub to BigQuery via a subscription (simplest, at-least-once), Dataflow to BigQuery with deduplication, and the Storage Write API from your own app for exactly-once semantics. Pub/Sub subscriptions write to a table using an existing table's schema, and the `insertId` mechanism gives best-effort deduplication.

```python
# Storage Write API: committed data is immediately queryable, no streaming buffer limits
from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import types, writer

client = bigquery_storage_v1.BigQueryWriteClient()
stream = types.WriteStream(type_=types.WriteStream.Type.COMMITTED)
stream = client.create_write_stream(
    parent="projects/acme-prod/datasets/analytics/tables/events",
    write_stream=stream,
)
with client.append_rows(stream_name=stream.name) as append:
    append.append(proto_rows)  # repeated AppendRowsRequest
client.finalize_write_stream(name=stream.name)
```

Trade-off: streaming is billed per byte and has quota limits; if a few minutes of latency is acceptable, batch micro-batches into GCS and `LOAD` instead - it is far cheaper.

[Table of Contents](#BigQuery)

## What are the limitations or constraints of using BigQuery?

Some limits worth knowing (verify current quotas in the docs before relying on a number):

+ Not an OLTP database: no foreign keys, no enforced primary keys, no high-throughput single-row transactions.
+ DML is supported but rate-limited per table; a mutation-heavy workload belongs somewhere else.
+ Streaming inserts cost more than batch loads and historically carried streaming-buffer restrictions.
+ No user-managed indexes; performance work is partitioning, clustering, and materialization.
+ Query results are limited by shuffle and slot capacity, not by disk.
+ Some operations (for example certain schema changes, or `alter column type` widening) rewrite data or are restricted.
+ Cross-region and cross-cloud reads need careful placement; BigQuery Omni has no cross-region SQL.
+ `select *` on wide tables and unpartitioned scans are expensive by design.

```sql
-- DML is real and transactional, just not OLTP-scale
begin transaction;
update `acme-prod.analytics.dim_customer`
set segment = 'enterprise'
where customer_id = 'c-1042';
commit transaction;
```

[Table of Contents](#BigQuery)

## How can you monitor and optimize BigQuery costs?

Monitor with the Cloud Billing export to BigQuery, `INFORMATION_SCHEMA.JOBS`, reservation utilization, and budgets. Optimize by cutting bytes scanned, moving steady workloads to capacity pricing, and expiring cold data.

```sql
-- Daily scanned bytes and estimated on-demand cost over the last 30 days
select
  date(creation_time) as job_date,
  round(sum(total_bytes_billed) / pow(1024, 4), 2) as tib_billed,
  round(sum(total_bytes_billed) / pow(1024, 4) * 6.25, 2) as est_usd
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 30 day)
  and job_type = 'QUERY'
group by job_date
order by job_date desc;
```

```sql
-- Steady workloads: check slot utilization per one-minute period
select
  period_start,
  round(sum(period_slot_ms) / 60000, 1) as avg_slots,
  sum(period_slot_ms) / 1000 / 3600 as slot_hours
from `region-us`.information_schema.jobs_timeline_by_project
where period_start >= timestamp_sub(current_timestamp(), interval 1 day)
group by period_start
order by slot_hours desc;
```

Levers: table partitioning plus `partition_expiration_days`, dataset-level default expiration for raw zones, materialized views for dashboard backends, cheaper cold storage, and alerts when a project exceeds a spend threshold.

[Table of Contents](#BigQuery)

## Explain the difference between BigQuery slots and slots reservation.

A slot is a unit of computational capacity - roughly a virtual CPU plus memory used by Dremel workers. Slots are the billing and concurrency unit for capacity pricing. A reservation is a named pool of slots in a location; you assign projects (or folders/orgs) to it. Assignments can be `PIPELINE` or `ML`, and idle slots can be shared or not.

```sql
-- Create a reservation and assign a project to it
create reservation analytics_team
options (
  reservation_id = 'analytics_team',
  edition = 'ENTERPRISE',
  slot_capacity = 500,
  location = 'us'
);

create assignment analytics_team_assignment
options (
  reservation_id = 'analytics_team',
  assignee = 'projects/acme-prod',
  job_type = 'QUERY'
);
```

With on-demand pricing you get a large shared pool and pay per byte scanned. With capacity pricing you commit to slots and pay per slot-hour (with committed-use discounts), which gives predictable cost and predictable concurrency for dashboards.

[Table of Contents](#BigQuery)

## Can you share your experience with implementing data pipelines in BigQuery?

A strong answer is a concrete story with a shape: sources, ingestion, transformation, orchestration, data quality, monitoring, and the one incident that taught you something. For example: "We ran a retail ELT where Datastream replicated Postgres orders into a raw dataset, dbt built staging and marts, Airflow orchestrated incremental models, and Looker served dashboards. The hard parts were idempotent incremental loads and controlling scan cost."

```python
# Airflow: an idempotent daily incremental model run as a BigQuery job
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

SQL = """
merge `acme-prod.analytics.fact_orders` t
using (
  select * from `acme-prod.staging.orders_inc`
  where date(ingested_at) = @run_date
  qualify row_number() over (partition by order_id order by ingested_at desc) = 1
) s
on t.order_id = s.order_id
when matched then update set amount = s.amount, status = s.status
when not matched then insert (order_id, customer_id, order_date, status, amount)
values (s.order_id, s.customer_id, s.order_date, s.status, s.amount)
"""

with DAG(
    "orders_incremental",
    schedule="0 3 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=10)},
) as dag:
    BigQueryInsertJobOperator(
        task_id="merge_orders",
        configuration={
            "query": {
                "query": SQL,
                "useLegacySql": False,
                "queryParameters": [
                    {
                        "name": "run_date",
                        "parameterType": {"type": "DATE"},
                        "parameterValue": {"value": "{{ ds }}"},
                    }
                ],
            }
        },
    )
```

The follow-up questions are usually about idempotency, backfills, schema evolution, and how you detect a silent data gap (row-count and freshness tests in dbt, plus an audit table).

[Table of Contents](#BigQuery)

## What is the difference between a view and a materialized view in BigQuery?

A view is a saved query evaluated at read time. A materialized view stores the precomputed result and refreshes incrementally as base tables change. BigQuery can transparently rewrite a query to use a matching materialized view, so the speedup can apply even to legacy consumers.

```sql
create materialized view `acme-prod.analytics.mv_revenue_daily`
partition by order_date
cluster by segment
as
select
  order_date,
  segment,
  count(*) as orders,
  sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
group by order_date, segment;

-- Manual refresh (automatic refresh is the default for eligible views)
refresh materialized view `acme-prod.analytics.mv_revenue_daily`;
```

Materialized views have SQL limitations (no analytic functions, limited joins, no UDFs, no outer joins in the definition). Check the current list before designing around one, and inspect freshness with:

```sql
select table_name, last_refresh_time, refresh_watermark
from `acme-prod.analytics.information_schema.materialized_views`;
```

[Table of Contents](#BigQuery)

## How does BigQuery handle data partitioning and clustering?

Partitioning and clustering are the two physical design levers BigQuery exposes. Partitioning creates independently addressable segments; clustering sorts within a partition. Both feed the same cost/latency goal: read fewer bytes. A table can be partitioned by one column and clustered by up to four.

```sql
create table `acme-prod.analytics.fact_events`
(
  event_id   string,
  event_date date,
  event_ts   timestamp,
  user_id    string,
  country    string,
  event_type string
)
partition by event_date
cluster by country, event_type
options (require_partition_filter = true);
```

```sql
-- Verify that filters are pruning
select partition_id, total_rows
from `acme-prod.analytics.information_schema.partitions`
where table_name = 'fact_events'
order by partition_id desc
limit 5;
```

Guidance: partition on date, cluster on the two columns you filter or aggregate by most. Do not cluster on a column with millions of distinct values - it gives little block-level pruning.

[Table of Contents](#BigQuery)

## Can you explain the concept of data sharding in BigQuery?

Historically, BigQuery teams created one table per day (`events_20261004`) and queried them with wildcard tables and `_TABLE_SUFFIX`. That is sharding. It works, but it multiplies metadata, breaks schema consistency, and makes `information_schema` queries painful. Native partitioning replaced it for almost every case.

```sql
-- Legacy sharded read; the suffix is a string, so convert before comparing dates
select count(*)
from `acme-prod.events.events_*`
where _TABLE_SUFFIX between '20261001' and '20261004'
  and event_type = 'purchase';

-- Preferred: one partitioned table, normal predicate
select count(*)
from `acme-prod.events.events`
where event_date between date '2026-10-01' and date '2026-10-04'
  and event_type = 'purchase';
```

Sharding is still reasonable when retention rules require dropping whole tables (for example regulatory deletion), or when different shards have different schemas by design.

[Table of Contents](#BigQuery)

## How does BigQuery handle schema changes for large tables?

BigQuery handles most schema changes as metadata operations, not full rewrites. You can add, drop, and rename columns, and widen compatible types (for example `int64` to `numeric`, or `numeric` to `bignumeric`). Some type changes and clustering/partitioning changes require recreating the table.

```sql
-- Metadata-only and cheap on huge tables
alter table `acme-prod.analytics.fact_orders` add column if not exists channel string;
alter table `acme-prod.analytics.fact_orders` rename column amount to gross_amount;
alter table `acme-prod.analytics.fact_orders` drop column if exists legacy_flag;

-- Type widening is supported in a documented direction; an int64 -> string rewrite is not
alter table `acme-prod.analytics.fact_orders`
alter column gross_amount set data type numeric(18,2);

-- Changing partitioning/clustering requires a new table
create table `acme-prod.analytics.fact_orders_v2`
partition by order_date
cluster by customer_id
as select * from `acme-prod.analytics.fact_orders`;
drop table `acme-prod.analytics.fact_orders`;
alter table `acme-prod.analytics.fact_orders_v2` rename to fact_orders;
```

Interview point: the old claim that BigQuery must rewrite the entire table for every schema change is outdated. Say which changes are free and which are migrations.

[Table of Contents](#BigQuery)

## What are the benefits of using partitioned tables in BigQuery?

+ Lower cost: partition pruning means you pay for the partitions you query.
+ Better performance: less data scanned and less shuffle.
+ Cheap lifecycle management: `partition_expiration_days` drops old partitions automatically.
+ Targeted DML: `delete`/`truncate` on one partition is fast and safe.
+ Better observability: `information_schema.partitions` shows exactly where storage sits.
+ Idempotent loads: you can overwrite one partition without touching the rest.

```sql
-- Targeted backfill: replace exactly one day without a full-table rewrite
create or replace table `acme-prod.analytics.fact_orders`
partition by order_date
cluster by customer_id
as
select * from `acme-prod.analytics.fact_orders`
where order_date <> date '2026-10-04'
union all
select * from `acme-prod.staging.orders_repaired`
where order_date = date '2026-10-04';
```

[Table of Contents](#BigQuery)

## How can you control access and permissions in BigQuery?

BigQuery uses IAM plus dataset and table-level ACLs, column-level security via policy tags, row-level security via row access policies, and authorized views/datasets to expose derived data safely.

```sql
-- Dataset-level IAM
grant `roles/bigquery.dataViewer`
on dataset `acme-prod.analytics`
to 'group:analytics-readers@acme.com';

-- Authorized dataset: a view in the shared dataset can read the private one
grant `roles/bigquery.dataViewer`
on dataset `acme-prod.private`
to 'serviceAccount:view-owner@acme-prod.iam.gserviceaccount.com';
```

```bash
# Column-level security is configured with policy tags in Data Catalog/Dataplex,
# then attached to the column via the schema (see the security question above).
# Grant a fine-grained reader role at the table level:
bq add-iam-policy-binding \
  --member='user:analyst@acme.com' \
  --role='roles/bigquery.dataViewer' \
  acme-prod:analytics.fact_orders
```

Principle of least privilege: grant at the dataset or table level rather than project-level, use groups not individuals, and prefer authorized views over granting base tables to external consumers.

[Table of Contents](#BigQuery)

## What is the role of service accounts in BigQuery?

Service accounts are non-human identities for pipelines, schedulers, and applications. Grant them BigQuery roles scoped to the datasets they need, plus Cloud Storage or Pub/Sub roles as required, and prefer short-lived credentials (Workload Identity Federation or impersonation) over downloaded keys.

```bash
# Create a loader service account and scope it to one dataset
gcloud iam service-accounts create bq-loader \
  --display-name="BigQuery loader"

gcloud projects add-iam-policy-binding acme-prod \
  --member="serviceAccount:bq-loader@acme-prod.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding acme-prod \
  --member="serviceAccount:bq-loader@acme-prod.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"
```

```bash
# A job authenticates as the service account (or via impersonation)
gcloud auth activate-service-account --key-file=/secrets/bq-loader.json
bq query --use_legacy_sql=false 'select count(*) from `acme-prod.analytics.fact_orders`'
```

Note that `dataEditor` on a dataset does not allow running jobs; `jobUser` at the project level does. That split surprises people in interviews.

[Table of Contents](#BigQuery)

## Can you explain the concept of slots in BigQuery?

Slots are the compute units that execute queries. On capacity pricing you buy them; on on-demand pricing you draw from a shared pool. A query is broken into stages, each of which consumes slots while it runs. More slots help a big query go faster and help concurrency, but they do not fix a badly partitioned scan.

```sql
-- How many slots did a query actually use?
select
  job_id,
  total_slot_ms,
  round(total_slot_ms / 1000, 1) as slot_seconds,
  timestamp_diff(end_time, start_time, second) as elapsed_seconds,
  round(total_slot_ms / greatest(timestamp_diff(end_time, start_time, millisecond), 1), 1) as avg_slots
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 1 day)
order by total_slot_ms desc
limit 10;
```

`avg_slots` near the reservation size means the query was slot-bound; `avg_slots` near 1 means it was I/O or limit-bound. That distinction is the whole point of the metric.

[Table of Contents](#BigQuery)

## What is the purpose of BigQuery reservations?

A reservation allocates a fixed pool of slots in a location so a workload gets predictable throughput and cost. You attach projects, folders, or the organization to it and choose a job type (`QUERY`, `PIPELINE`, `ML`). Reservations support autoscaling, idle-slot sharing, and committed-use discounts.

```sql
-- Autoscaling reservation with a baseline and a ceiling
create reservation shared_bi
options (
  reservation_id = 'shared_bi',
  edition = 'ENTERPRISE',
  slot_capacity = 200,
  max_slots = 1000,
  location = 'us',
  autoscale_max_slots = 1000
);

-- Route only interactive BI jobs of a project to this reservation
create assignment bi_assignment
options (
  reservation_id = 'shared_bi',
  assignee = 'projects/acme-prod',
  job_type = 'QUERY'
);
```

Use reservations when: many dashboards must stay interactive, you need cost predictability, or you must isolate a team's resource usage. Do not buy capacity for spiky, small, ad-hoc workloads - on-demand is often cheaper there.

[Table of Contents](#BigQuery)

## How can you optimize query performance in BigQuery?

+ Prune: partition filter plus clustered columns.
+ Project: read only the columns the query needs.
+ Reduce shuffle: aggregate and filter before joining, avoid `select distinct` on huge tables.
+ Avoid exploding: `unnest` only when you need the grain.
+ Use `approx_*` functions and `materialized views` where exactness is optional.
+ Tune slots: capacity for steady concurrency, on-demand for spiky work.
+ Inspect the plan and the `information_schema.jobs` slot/shuffle numbers before guessing.

```sql
-- Rewriting a self-join that exploded into a window function
select
  order_id,
  customer_id,
  amount,
  row_number() over (partition by customer_id order by order_ts) as order_seq,
  lag(amount) over (partition by customer_id order by order_ts) as prev_amount
from `acme-prod.analytics.fact_orders`
where order_date >= date '2026-01-01';
```

[Table of Contents](#BigQuery)

## How does BigQuery handle data encryption?

Data is encrypted at rest with Google-managed keys by default (AES-256) and in transit with TLS. You can supply CMEK keys from Cloud KMS per dataset, and BigQuery exposes `AEAD` functions for application-level column encryption and `DETERMINISTIC_` variants for joinable ciphertext.

```sql
-- Column-level application encryption with a KMS-backed key set
select
  customer_id,
  aead.encrypt(
    keyset,
    cleartext,
    b''
  ) as encrypted_ssn
from `acme-prod.analytics.pii_customers`;

-- Deterministic encryption supports equality joins on ciphertext
select aead.deterministic_encrypt(keyset, cleartext, b'') as encrypted_email
from `acme-prod.analytics.pii_customers`;
```

Also available: CMEK key rotation, CMEK per dataset, and BigQuery Omni with cloud-specific key management. Audit key usage through Cloud KMS logs.

[Table of Contents](#BigQuery)

## Can you explain the concept of query caching in BigQuery?

BigQuery caches the result set of a query for about 24 hours, keyed by the exact SQL text, the referenced tables/views, and the time of the underlying snapshot. If the cache hits, the query returns instantly and is not billed for bytes scanned. Cache is skipped when a referenced table changed, when the query is non-deterministic (for example `current_timestamp()` or `rand()`), or when caching is disabled.

```sql
-- Second identical run within the cache window returns from cache (0 bytes billed)
select status, count(*) as orders
from `acme-prod.analytics.fact_orders`
where order_date = date '2026-10-04'
group by status;
```

```bash
# Inspect cache usage
bq query --use_legacy_sql=false --format=prettyjson '
select cache_hit, total_bytes_billed
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 1 hour)
order by creation_time desc limit 10'

# Disable cache for a benchmark run
bq query --use_legacy_sql=false --nouse_cache '
select count(*) from `acme-prod.analytics.fact_orders`'
```

Cache helps repeated dashboard refreshes. It does not help a query that scans different rows each time.

[Table of Contents](#BigQuery)

## How can you export BigQuery query results to a file?

Use `EXPORT DATA` for scheduled or server-side exports, `bq extract` for a table, and the BigQuery API `jobs.insert` with an extract configuration for programmatic control. Supported formats include CSV, JSON, Avro, and Parquet.

```sql
-- Query result to Parquet shards in GCS
export data options (
  uri = 'gs://acme-export/revenue/dt=2026-10-04/part-*.parquet',
  format = 'PARQUET',
  compression = 'SNAPPY',
  overwrite = true
)
as
select segment, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
where order_date = date '2026-10-04'
group by segment;
```

```bash
# Table to CSV, one header row, gzipped shards
bq extract --destination_format=CSV --compression=GZIP --print_header=true \
  'acme-prod:analytics.fact_orders' \
  'gs://acme-export/orders-*.csv.gz'
```

Exports have a per-file size limit, so large tables produce multiple shards; use a wildcard URI and a manifest or the shard list when consuming downstream.

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery Data Transfer Service?

The Data Transfer Service pulls data from external systems into BigQuery on a schedule without you writing an extractor. It supports Google marketing products, Cloud Storage, Amazon S3, Teradata, and SaaS connectors, and it also runs scheduled queries.

```bash
# Amazon S3 transfer using a Cloud Storage transfer and S3 credentials
bq mk --transfer_config \
  --project_id=acme-prod \
  --data_source=amazon_s3 \
  --target_dataset=raw_s3 \
  --display_name='s3 orders drop' \
  --schedule='every day 05:00' \
  --params='{"destination_table_name_template":"orders_{run_date}","data_path":"s3://acme-lake/orders/*.parquet","access_key_id":"AKIA...","secret_access_key":"...","file_format":"PARQUET"}'
```

Its value in a platform is guardrails: no custom code to maintain, built-in retries, and run history visible in Cloud Logging. Its weakness is control: for complex source-side extraction or heavy transformation, Dataflow, Datastream, or custom jobs fit better.

[Table of Contents](#BigQuery)

## Can you explain the concept of streaming inserts in BigQuery?

Streaming inserts push rows into a table continuously instead of loading files. The legacy path is the `tabledata.insertAll` API (exposed as `insert_rows_json` in client libraries); the modern path is the Storage Write API with exactly-once committed streams. Rows appear in the table almost immediately, which is why streaming is used for live dashboards and event monitoring.

```python
from google.cloud import bigquery

bq = bigquery.Client(project="acme-prod")
rows = [
    {"event_id": "e-1", "user_id": "u-1", "event_type": "purchase", "amount": 42.5},
    {"event_id": "e-2", "user_id": "u-2", "event_type": "view", "amount": None},
]
errors = bq.insert_rows_json("acme-prod.analytics.events_stream", rows)
if errors:
    raise RuntimeError(f"streaming insert failed: {errors}")
```

Trade-off: streaming is convenient but billed per byte and subject to quota; for data that can wait a few minutes, land files in Cloud Storage and `LOAD` instead, which is cheaper and has no buffer restrictions.

[Table of Contents](#BigQuery)

## What is the difference between a table decorator and a snapshot decorator in BigQuery?

A table decorator addresses a historical version of one table inside the time travel window: `table@-3600000` means one hour ago, and `table@SNAPSHOT_ID` means a specific snapshot. There is no dataset-wide "snapshot decorator" in current BigQuery. Durable point-in-time copies are separate objects created with `CREATE SNAPSHOT TABLE`, and the SQL form of time travel is `FOR SYSTEM_TIME AS OF`.

```sql
-- Relative decorator: the table as it was one hour ago
select count(*) from `acme-prod.analytics.fact_orders@-3600000`;

-- Absolute timestamp decorator
select count(*) from `acme-prod.analytics.fact_orders@1730700000000`;

-- Equivalent SQL form
select count(*) from `acme-prod.analytics.fact_orders`
for system_time as of timestamp_sub(current_timestamp(), interval 1 hour);

-- A durable snapshot is a real object with its own retention
create snapshot table `acme-prod.analytics.fact_orders_snap_20261004`
clone `acme-prod.analytics.fact_orders`
options (expiration_timestamp = timestamp '2027-10-04 00:00:00');
```

Interview precision matters here: decorators are ephemeral and bounded by the time travel window; snapshots and clones are objects you manage, share, and keep for longer.

[Table of Contents](#BigQuery)

## How does BigQuery handle data deduplication?

BigQuery has no unique constraints, so deduplication is part of your pipeline. The standard tools are `SELECT DISTINCT` for exact rows, `ROW_NUMBER()` for keeping the latest record per key, and `MERGE` for applying the deduplicated set to a target. On the ingest side, the legacy streaming API deduplicates best-effort on `insertId`, and the Storage Write API provides exactly-once through committed streams.

```sql
-- Keep one row per order, preferring the most recently ingested version
with ranked as (
  select
    *,
    row_number() over (
      partition by order_id
      order by ingested_at desc, source_lsn desc
    ) as rn
  from `acme-prod.staging.orders_load`
  where order_date = date '2026-10-04'
)
select * except (rn)
from ranked
where rn = 1;
```

```sql
-- Count duplicate keys before and after a dedup pass
select
  count(*) as rows_total,
  count(distinct order_id) as distinct_orders
from `acme-prod.staging.orders_load`
where order_date = date '2026-10-04';
```

[Table of Contents](#BigQuery)

## Can you explain the concept of streaming buffer in BigQuery?

When rows are streamed into a table, they first land in a streaming buffer - a short-lived, durable area that makes the rows immediately queryable. The buffer is flushed into the table's managed storage at intervals, at which point the rows become fully normal rows. Rows in the buffer behave differently: they cannot be targeted by `UPDATE`, `DELETE`, or `MERGE`, and `_PARTITIONTIME`/`_PARTITIONDATE` are `NULL` for buffered rows in ingestion-time partitioned tables.

```sql
-- Find rows still sitting in the buffer (ingestion-time partitioned table)
select count(*) as buffered_rows
from `acme-prod.analytics.events_ingest`
where _partitiontime is null;

-- Verify how much is in the buffer via the tables API/console metadata;
-- _partitiontime becomes non-null once the buffer flushes.
select
  date(_partitiontime) as partition_date,
  count(*) as rows_visible
from `acme-prod.analytics.events_ingest`
where _partitiontime >= timestamp_sub(current_timestamp(), interval 1 day)
group by partition_date;
```

The Storage Write API with committed streams writes into managed storage rather than the legacy buffer, so those tables avoid most buffer limitations. This difference is the main reason to prefer it for new pipelines.

[Table of Contents](#BigQuery)

## What are the limitations of using BigQuery streaming inserts?

+ Cost: streaming is billed per byte ingested, which is more expensive than batch loading.
+ Quotas: per-table and per-project request/row rate limits apply, especially on the legacy API.
+ Buffer semantics: rows in the legacy streaming buffer cannot be modified by DML, and partition pseudo-columns are null until flush.
+ Deduplication: best-effort only on `insertId` with the legacy API; exactly-once requires the Storage Write API.
+ Schema coupling: a mismatched field fails the insert at write time, so schema changes must be coordinated with producers.
+ No backpressure contract: a burst can fail rows rather than queue them unless the writer implements retries and a dead-letter path.

```python
# Exactly-once-ish write with the Storage Write API requires a committed stream
# and a writer-side dedup key; the legacy path below only dedups on insertId.
from google.cloud import bigquery

bq = bigquery.Client(project="acme-prod")
rows = [{"event_id": "e-1", "user_id": "u-1", "event_type": "purchase"}]
# The insertId is derived from a stable business key to make retries safe.
errors = bq.insert_rows_json(
    "acme-prod.analytics.events_stream",
    rows,
    row_ids=["e-1"],
)
```

If the freshness requirement is minutes rather than seconds, micro-batch `LOAD` is almost always the better engineering choice.

[Table of Contents](#BigQuery)

## How does BigQuery handle nested and repeated fields in JSON data?

Newline-delimited JSON loads into BigQuery either as a native schema (with `struct`/`array` inferred or declared) or into a single `json` column when the payload is open-ended. The `json` type preserves structure without a schema, and JSON functions let you extract, filter, and unnest fields on demand.

```sql
-- Land open-ended JSON, then query specific fields
create table `acme-prod.raw.events_json`
(
  ingest_ts timestamp,
  event_date date,
  payload   json
)
partition by event_date;

select
  json_value(payload, '$.event_id') as event_id,
  json_value(payload, '$.user.id') as user_id,
  json_query(payload, '$.items') as items,
  json_value(payload, '$.props.campaign') as campaign
from `acme-prod.raw.events_json`
where event_date = date '2026-10-04'
  and json_value(payload, '$.event_type') = 'purchase';
```

```sql
-- Unnest a JSON array into rows
select
  json_value(payload, '$.event_id') as event_id,
  json_value(item, '$.sku') as sku,
  cast(json_value(item, '$.qty') as int64) as qty
from `acme-prod.raw.events_json`,
unnest(json_extract_array(payload, '$.items')) as item
where event_date = date '2026-10-04';
```

For high-volume, frequently queried fields, promote them to typed columns and cluster on them; keep the raw `json` only for fields that genuinely change shape.

[Table of Contents](#BigQuery)

## Can you explain the concept of the BigQuery Data Catalog?

Data Catalog (now part of Dataplex Universal Catalog) is the metadata layer for BigQuery and other Google Cloud assets. It stores table and column descriptions, schema, tags, policy tags, data lineage, and business glossary entries. `INFORMATION_SCHEMA` is the SQL surface of that metadata for BigQuery's own objects.

```sql
-- Attach a description and tags that appear in search and governance tooling
alter table `acme-prod.analytics.fact_orders`
set options (description = 'Order-level fact, one row per order_id');

-- Search metadata with the Dataplex search syntax (in the console/API):
-- tag:finance, system=bigquery, projectid:acme-prod
```

Practical use: policy tags for column-level access, lineage for impact analysis before a schema change, and business descriptions so analysts can find the right table.

[Table of Contents](#BigQuery)

## How can you optimize data storage costs in BigQuery?

Storage is billed on logical bytes (active or long-term) or physical bytes. Long-term storage (a table or partition untouched for 90 days) is roughly half the active price. Practical levers: expire raw data, compress and drop unused columns, avoid tiny partitions, and choose physical billing when compression is good.

```sql
-- Where is storage actually going?
select
  table_name,
  round(total_logical_bytes / pow(1024, 3), 2) as logical_gib,
  round(active_logical_bytes / pow(1024, 3), 2) as active_gib,
  round(long_term_logical_bytes / pow(1024, 3), 2) as long_term_gib
from `acme-prod.analytics.information_schema.table_storage`
order by total_logical_bytes desc
limit 20;
```

```sql
-- Set default partition expiration so raw zones self-clean
alter table `acme-prod.raw.events`
set options (partition_expiration_days = 90);
```

Watch out: time travel and fail-safe keep deleted data for a period, so a `drop table` does not free storage immediately.

[Table of Contents](#BigQuery)

## What is the purpose of the INFORMATION_SCHEMA in BigQuery?

`INFORMATION_SCHEMA` exposes metadata as SQL views. The most used ones are `JOBS` (query history, bytes billed, slot usage), `TABLES` and `TABLE_STORAGE`, `COLUMNS`, `PARTITIONS`, `MATERIALIZED_VIEWS`, `RESERVATIONS`, and `STREAMING_TIMELINE`. Region-qualified views like `region-us.INFORMATION_SCHEMA.JOBS` cover the whole region; dataset-qualified ones cover one dataset.

```sql
-- Find the top five referenced tables and their scan cost this week
select
  referenced_table.project_id,
  referenced_table.dataset_id,
  referenced_table.table_id,
  count(*) as jobs,
  round(sum(total_bytes_billed) / pow(1024, 4), 3) as tib_billed
from `region-us`.information_schema.jobs,
unnest(referenced_tables) as referenced_table
where creation_time >= timestamp_sub(current_timestamp(), interval 7 day)
group by project_id, dataset_id, table_id
order by tib_billed desc
limit 5;
```

```sql
-- Columns and types for one table
select column_name, data_type, is_nullable
from `acme-prod.analytics.information_schema.columns`
where table_name = 'fact_orders'
order by ordinal_position;
```

[Table of Contents](#BigQuery)

## Can you explain the concept of data lineage in BigQuery?

Lineage tracks how data flows from source columns to destination columns across BigQuery jobs, Dataplex/Data Catalog, and supported external systems. It is populated automatically from query history (including dbt and scheduled queries), so you can answer "what breaks if I drop this column?" and "where did this metric come from?".

```sql
-- The lineage to a table's columns is available through Dataplex lineage,
-- and the raw inputs are visible in query history:
select
  job_id,
  referenced_table.table_id as read_table,
  destination_table.table_id as written_table
from `region-us`.information_schema.jobs,
unnest(referenced_tables) as referenced_table
where destination_table.table_id = 'fact_orders'
  and creation_time >= timestamp_sub(current_timestamp(), interval 30 day)
limit 50;
```

Use lineage for impact analysis, PII propagation review, and audit evidence. It is not a substitute for an explicit contract between producers and consumers.

[Table of Contents](#BigQuery)

## How does BigQuery handle nested data types like arrays and structs?

BigQuery's type system includes `struct<...>` for records and `array<...>` for repeated values; arrays of structs give full event nesting. Query them with dot notation, `unnest`, `array_agg`, and `array` subqueries. This is one of BigQuery's biggest modeling advantages over engines that only support flat tables.

```sql
-- Build a nested order document from flat rows
select
  order_id,
  any_value(order_ts) as order_ts,
  array_agg(
    struct(line_id, sku, qty, price)
    order by line_id
  ) as lines
from `acme-prod.staging.order_lines`
where order_date = date '2026-10-04'
group by order_id;
```

```sql
-- Aggregate back out and compute a nested total
select
  order_id,
  (select sum(l.qty * l.price) from unnest(lines) as l) as order_total
from `acme-prod.analytics.orders_nested`
where date(order_ts) = date '2026-10-04';
```

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery ML service?

BigQuery ML lets you train and run models with SQL. It supports linear/logistic regression, k-means, boosted trees (XGBoost), deep neural nets (TensorFlow), matrix factorization, ARIMA/ARIMA_PLUS time series, AutoML Tables, imported custom models, and remote calls to Vertex AI endpoints. Features: `ML.PREDICT`, `ML.EVALUATE`, `ML.TRANSFORM`, `ML.EXPLAIN_PREDICT`, and `ML.FORECAST`.

```sql
create model `acme-prod.analytics.churn_model`
options (
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['churned'],
  auto_class_weights = true
) as
select
  days_since_last_order,
  orders_90d,
  tickets_90d,
  churned
from `acme-prod.analytics.customer_features`
where feature_date < date '2026-09-01';
```

```sql
select * from ml.evaluate(
  model `acme-prod.analytics.churn_model`,
  (select * from `acme-prod.analytics.customer_features`
   where feature_date >= date '2026-09-01')
);
```

Trade-off: BigQuery ML removes the data-movement step and is great for tabular baselines; for deep learning at scale or custom training loops, Vertex AI is the better home.

[Table of Contents](#BigQuery)

## How can you monitor and troubleshoot query performance in BigQuery?

Start with the query execution plan in the console (or the job statistics), then use `INFORMATION_SCHEMA.JOBS` to compare against history. Look for: a stage that reads far more bytes than expected (partition/cluster miss), a stage with a huge shuffle (bad join or `group by`), and a single hot task (data skew).

```sql
-- Slowest queries with slot usage and shuffle in the last day
select
  job_id,
  query,
  timestamp_diff(end_time, start_time, second) as elapsed_s,
  total_slot_ms,
  round(total_slot_ms / greatest(timestamp_diff(end_time, start_time, millisecond), 1), 1) as avg_slots,
  total_bytes_billed,
  total_bytes_processed
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 1 day)
  and job_type = 'QUERY'
  and statement_type in ('SELECT', 'INSERT', 'MERGE')
order by total_slot_ms desc
limit 20;
```

BigQuery Standard SQL does not support `EXPLAIN`; use `--dry_run` for bytes, the execution plan for stages, and `information_schema.jobs` for the historical numbers.

[Table of Contents](#BigQuery)

## Can you explain the concept of table clustering and its benefits?

Clustering is the sorting of rows inside a partition by up to four columns. The benefits: block-level pruning on clustered columns, faster filter/aggregation queries, and often smaller storage because sorted data compresses better. BigQuery keeps clustering current automatically for newly written data; bulk rewrites may need a re-cluster.

```sql
create table `acme-prod.analytics.fact_clickstream`
(
  event_date date,
  user_id    string,
  country    string,
  device     string,
  event_type string
)
partition by event_date
cluster by country, device, event_type;
```

```sql
-- This touches only the blocks for one country on one day
select device, count(*) as events
from `acme-prod.analytics.fact_clickstream`
where event_date = date '2026-10-04'
  and country = 'DE'
group by device;
```

[Table of Contents](#BigQuery)

## How does BigQuery handle query optimization and query execution?

A BigQuery SQL query is parsed, validated against metadata, and converted to a Dremel plan of stages connected by shuffles. The optimizer applies predicate pushdown, join reordering, partition pruning, and materialized-view rewriting. Leaf stages read columnar data; mixers combine partial results; the root returns rows to the client. There are no user-visible indexes or statistics to maintain.

```sql
-- Inspect the plan and stage-by-stage bytes/shuffle
select
  job_id,
  total_bytes_processed,
  total_bytes_billed,
  total_slot_ms,
  -- the full plan is in the job's statistics; this is the quick summary
  statement_type,
  priority
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 6 hour)
order by creation_time desc
limit 5;
```

Interview framing: you influence the optimizer through table design (partitioning, clustering, materialized views), query shape (filters early, avoid exploding joins), and capacity (slots). You do not tune it with hints, and there is no `analyze table`.

[Table of Contents](#BigQuery)

## What is the purpose of BigQuery BI Engine?

BI Engine is an in-memory analysis cache for sub-second dashboard queries. It is configured as a per-project, per-location capacity (GB of memory) and accelerates compatible queries against tables and views, especially Tableau, Looker, and Looker Studio workloads. It does not replace partitioning or the warehouse: it caches hot data.

```sql
-- BI Engine acceleration is transparent; the reservation is created via
-- the bigqueryreservation API or the console (per project, per location).
-- Check whether BI Engine served a query:
select
  job_id,
  bi_engine_statistics.bi_engine_mode as bi_engine_mode
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 1 day)
  and bi_engine_statistics.bi_engine_mode is not null
limit 20;
```

Limits: supported query shapes are restricted (no `order by` on huge results, limited joins/aggregations), and capacity is bounded by the reservation size. Use it for a fixed dashboard working set, not for ad-hoc exploration of the whole warehouse.

[Table of Contents](#BigQuery)

## Can you explain the concept of wildcard tables in BigQuery?

A wildcard table matches a set of same-schema tables by name and unions them at query time. `_TABLE_SUFFIX` exposes the matched suffix, and filtering on it prunes which tables are read. It is the standard way to query legacy date-sharded tables.

```sql
-- Union of daily shards, with shard pruning
select
  _TABLE_SUFFIX as shard_date,
  event_type,
  count(*) as events
from `acme-prod.events.events_*`
where _TABLE_SUFFIX between '20261001' and '20261007'
group by shard_date, event_type
order by shard_date, events desc;

-- Restrict to a known set of tables with a TABLE_DATE_RANGE-style filter
select count(*)
from `acme-prod.events.events_*`
where _TABLE_SUFFIX in ('20261001', '20261002');
```

Caveats: all matched tables must share a schema (a mismatch can fail the query), the `*` cannot be combined with views, and a wildcard over thousands of shards has real metadata overhead. Prefer a partitioned table.

[Table of Contents](#BigQuery)

## What are the different data ingestion options in BigQuery?

+ Batch `LOAD` / `bq load` from Cloud Storage or local files (free, cheapest).
+ `LOAD DATA` SQL for server-side loads.
+ Storage Write API or legacy `tabledata.insertAll` for streaming.
+ Pub/Sub BigQuery subscriptions, or Dataflow for stream processing.
+ Datastream for change data capture from databases.
+ Data Transfer Service connectors for SaaS and Google products.
+ External tables and federated queries for data left in place.
+ Partner tools (Fivetran, Airbyte) writing through the same APIs.

```text
latency:   batch (minutes-hours)  <  micro-batch (minutes)  <  streaming (seconds)
cost:      batch cheapest         <  micro-batch           <  streaming most expensive
```

Choose the cheapest option that meets the freshness requirement; most "real-time" dashboards are satisfied by micro-batch loads every few minutes.

[Table of Contents](#BigQuery)

## How does BigQuery handle data deduplication during batch loading?

BigQuery does not deduplicate automatically on load; it appends what you give it. Make the load idempotent by writing to a staging table and merging, or by overwriting exactly one partition. Window functions are the standard dedup primitive.

```sql
-- Keep the newest record per business key, then merge
merge `acme-prod.analytics.dim_customer` t
using (
  select * except (rn)
  from (
    select
      *,
      row_number() over (partition by customer_id order by ingested_at desc) as rn
    from `acme-prod.staging.customer_load`
  )
  where rn = 1
) s
on t.customer_id = s.customer_id
when matched then update set
  t.email = s.email,
  t.segment = s.segment,
  t.updated_at = s.ingested_at
when not matched then insert (customer_id, email, segment, updated_at)
values (s.customer_id, s.email, s.segment, s.ingested_at);
```

```sql
-- Idempotent partition replace instead of MERGE for append-only facts
create or replace table `acme-prod.analytics.fact_orders`
partition by order_date
as
select * from `acme-prod.analytics.fact_orders`
where order_date <> date '2026-10-04'
union all
select * from `acme-prod.staging.orders_dt_20261004`;
```

[Table of Contents](#BigQuery)

## Can you explain the concept of clustering keys in BigQuery?

Clustering keys are the columns listed in `cluster by`. Up to four, ordered by effectiveness. They do not need to be unique, and each must be a top-level, non-repeated column of type `bignumeric`, `bool`, `date`, `datetime`, `geography`, `int64`, `numeric`, `range`, `string`, or `timestamp`; `array`, `struct`, `json`, and `float64` are not supported (check the current type list). BigQuery stores block min/max for them and uses that metadata to skip blocks.

```sql
-- First key is the most frequently filtered; deep columns refine it
create or replace table `acme-prod.analytics.fact_events`
partition by event_date
cluster by event_type, country, user_id
as
select event_date, event_type, country, user_id, properties
from `acme-prod.raw.events`;
```

```sql
-- Audit: which cluster columns exist?
select column_name, clustering_ordinal_position
from `acme-prod.analytics.information_schema.columns`
where table_name = 'fact_events'
  and clustering_ordinal_position is not null
order by clustering_ordinal_position;
```

[Table of Contents](#BigQuery)

## What are the best practices for data modeling in BigQuery?

+ Model for your query grain: flatten when analysts always want the detail, nest when they consume the document.
+ Partition on the time column and cluster on the next filter columns.
+ Denormalize dimensions into facts when it removes a large shuffle join and the dimension is small and slow-changing.
+ Use `numeric`/`bignumeric` for money, `date`/`timestamp` for time (store UTC), and avoid stringly-typed everything.
+ Split raw, staging, and marts into separate datasets with different retention and access.
+ Make every load idempotent and every table documented.
+ Prefer a small number of wide, well-partitioned tables over hundreds of narrow ones.

```sql
-- A defensible star schema in BigQuery
create table `acme-prod.analytics.fact_orders`
(
  order_id    string not null,
  customer_id string,
  product_id  string,
  order_date  date,
  channel     string,
  quantity    int64,
  amount      numeric(12,2)
)
partition by order_date
cluster by customer_id, product_id
options (description = 'Grain: one row per order line.');

create table `acme-prod.analytics.dim_product`
(
  product_id string not null,
  category   string,
  brand      string
);
```

[Table of Contents](#BigQuery)

## How does BigQuery handle data backup and recovery?

BigQuery gives you time travel, table snapshots, table clones, and fail-safe. Time travel reads a table as of any point in the last seven days (default; configurable up to seven days). Snapshots are lightweight, read-only copies you can keep for longer. Clones are writable copies that share storage initially. Fail-safe keeps deleted or expired data for an additional period for Google's recovery process.

```sql
-- Read the table as it was an hour ago
select count(*)
from `acme-prod.analytics.fact_orders`
for system_time as of timestamp_sub(current_timestamp(), interval 1 hour);

-- Keep a point-in-time snapshot for audit
create snapshot table `acme-prod.analytics.fact_orders_snapshot_20261004`
clone `acme-prod.analytics.fact_orders`
options (expiration_timestamp = timestamp '2027-10-04 00:00:00');

-- Restore an accidentally damaged table from a clone
create table `acme-prod.analytics.fact_orders_restored`
clone `acme-prod.analytics.fact_orders_snapshot_20261004`;
```

Practice the restore path before you need it: time travel expires, snapshots cost storage, and fail-safe recovery is a support request, not a self-service button.

[Table of Contents](#BigQuery)

## Can you explain the concept of materialized views in BigQuery?

A materialized view stores the precomputed output of a query and refreshes incrementally as base data changes. BigQuery can automatically rewrite compatible queries to use it, which accelerates dashboards without changing their SQL. Use it for expensive, repeated aggregations on large fact tables.

```sql
create materialized view `acme-prod.analytics.mv_orders_by_country_day`
partition by order_date
cluster by country
as
select
  order_date,
  country,
  count(*) as orders,
  sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
group by order_date, country;

-- Refreshes are automatic; force one after a backfill
refresh materialized view `acme-prod.analytics.mv_orders_by_country_day`;
```

Limitations to remember: the definition supports a restricted SQL subset (no `unnest` of arbitrary shapes in some cases, no analytic functions, limited joins, no UDFs), a single materialized view cannot cover every aggregation, and base-table DML can temporarily make the view stale. Check freshness with `information_schema.materialized_views`.

[Table of Contents](#BigQuery)

## How does BigQuery handle data export to external services?

BigQuery pushes data out through `EXPORT DATA` to Cloud Storage, `bq extract`, the Storage Read API for programmatic consumers, partner/Data Transfer tools, and reverse ETL into operational systems. Pub/Sub is an ingestion path into BigQuery, not an export target - do not confuse the direction.

```sql
-- Export to GCS for a Spark or Trino consumer
export data options (
  uri = 'gs://acme-export/orders/*.parquet',
  format = 'PARQUET',
  compression = 'ZSTD'
)
as select * from `acme-prod.analytics.fact_orders`
where order_date = date '2026-10-04';
```

```bash
# Extract to GCS, then load into another warehouse with its own tooling
bq extract --destination_format=NEWLINE_DELIMITED_JSON --compression=GZIP \
  'acme-prod:analytics.dim_customer' \
  'gs://acme-export/dim_customer-*.json.gz'
```

For near-real-time fan-out to applications, export a change table and use a reverse-ETL tool rather than querying BigQuery from the application's request path.

[Table of Contents](#BigQuery)

## What is the purpose of BigQuery ML's CREATE MODEL statement?

`CREATE MODEL` trains a model inside BigQuery using a SQL query as the training data. You choose `model_type`, a label column, and options; BigQuery handles the training infrastructure and stores the model as a BigQuery object that is queryable with `ML.*` functions.

```sql
create or replace model `acme-prod.analytics.sales_forecast`
options (
  model_type = 'ARIMA_PLUS',
  time_series_timestamp_col = 'order_date',
  time_series_data_col = 'revenue',
  time_series_id_col = 'region',
  horizon = 30
) as
select order_date, region, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
group by order_date, region;
```

```sql
select *
from ml.forecast(
  model `acme-prod.analytics.sales_forecast`,
  horizon => 30
)
order by forecast_timestamp;
```

Training bills for the bytes scanned plus, for some model types, dedicated training slots (`ML` reservation assignments).

[Table of Contents](#BigQuery)

## Can you explain the concept of geographic data types in BigQuery?

BigQuery has a native `GEOGRAPHY` type for points, lines, and polygons on the WGS84 sphere, with `ST_*` functions for distance, containment, intersection, buffer, and nearest-neighbor search. Spatial indexes can accelerate `ST_CONTAINS`-style filters. Use it for delivery zones, store catchments, and geofencing.

```sql
select
  d.delivery_id,
  d.driver_id,
  st_distance(
    st_geogpoint(-87.6298, 41.8781),
    d.dropoff_location
  ) as meters_from_depot
from `acme-prod.analytics.deliveries` d
where d.delivery_date = date '2026-10-04'
  and st_dwithin(
    d.dropoff_location,
    st_geogpoint(-87.6298, 41.8781),
    5000
  );
```

```sql
-- Which delivery zone does each order fall in?
select o.order_id, z.zone_name
from `acme-prod.analytics.orders_geo` o
left join `acme-prod.analytics.delivery_zones` z
  on st_contains(z.polygon, o.delivery_point);
```

[Table of Contents](#BigQuery)

## How does BigQuery handle data privacy and security?

Privacy and security are layered: IAM and fine-grained roles, policy tags for column-level security, dynamic data masking, row access policies, CMEK encryption, VPC Service Controls, Sensitive Data Protection (DLP) for discovery and de-identification, and audit logs for evidence.

```sql
-- Dynamic masking: analysts see a masked value unless they hold the privileged role
-- (masking rules are attached to policy tags in Dataplex).
create or replace table `acme-prod.analytics.customers_masked` as
select
  customer_id,
  case
    when session_user() in ('auditor@acme.com') then email
    else regexp_replace(email, r'^[^@]+', '***')
  end as email
from `acme-prod.private.customers`;

-- Row access policy for tenant isolation
create row access policy tenant_policy on `acme-prod.analytics.fact_orders`
grant to ('group:tenant-support@acme.com')
filter using (tenant_id = session_user());
```

Operational practice: classify data on write, default to masked views for broad audiences, rotate and separate KMS keys by sensitivity, and log data access for regulated datasets.

[Table of Contents](#BigQuery)

## Can you explain the concept of slot reservations in BigQuery?

A slot reservation is a pool of compute capacity in one location, shared by the projects, folders, or organization assigned to it. Reservations replace the shared on-demand pool with dedicated capacity, which makes concurrency and cost predictable. Features include autoscaling, idle-slot sharing, and commitment discounts.

```sql
-- Baseline 100 slots, autoscale to 600 during peaks -- for interactive BI
create reservation bi_pool
options (
  reservation_id = 'bi_pool',
  edition = 'ENTERPRISE',
  slot_capacity = 100,
  max_slots = 600,
  location = 'us'
);

create assignment bi_queries
options (
  reservation_id = 'bi_pool',
  assignee = 'projects/acme-bi',
  job_type = 'QUERY'
);
```

When NOT to use reservations: small ad-hoc projects, one-off migrations, or workloads whose usage is genuinely unpredictable and low - on-demand is simpler and often cheaper there. Also remember that slots are regional.

[Table of Contents](#BigQuery)

## What are the different types of pricing models available for BigQuery?

| Component | Options |
|---|---|
| Compute | On-demand (per TiB scanned) or capacity (slot reservations/commitments) |
| Editions | Standard, Enterprise, Enterprise Plus (differ in features and governance) |
| Storage | Logical active, logical long-term (after 90 days), or physical bytes |
| Streaming | Billed per byte ingested (Storage Write API / legacy streaming) |
| BI Engine | Billed per GB-hour of in-memory capacity |
| ML | Bytes scanned plus ML slot usage for some model types |

```sql
-- Capacity vs on-demand reality check: how slot-bound is the workload?
select
  date(creation_time) as job_date,
  count(*) as jobs,
  round(sum(total_bytes_billed) / pow(1024, 4), 2) as tib_billed,
  sum(total_slot_ms) / 1000 / 3600 as slot_hours
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 14 day)
  and job_type = 'QUERY'
group by job_date
order by job_date desc;
```

Interview answer: on-demand is right for spiky, low-volume usage; capacity is right when slot-hours are steady and concurrency matters. Storage choice depends on compression and access age. Rates change, so describe the model, not a hardcoded price.

[Table of Contents](#BigQuery)

## How can you automate BigQuery tasks using Cloud Composer?

Cloud Composer is managed Apache Airflow. You orchestrate BigQuery with the `airflow.providers.google.cloud` operators, passing the SQL as a job configuration, templating dates, and chaining dependencies and sensors.

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
    BigQueryCheckOperator,
)

SQL = """
insert into `acme-prod.analytics.revenue_daily`
select order_date, sum(amount) as revenue
from `acme-prod.analytics.fact_orders`
where order_date = date('{{ ds }}')
group by order_date
"""

with DAG(
    "bigquery_revenue_daily",
    schedule="0 4 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=True,
    default_args={"retries": 3, "retry_delay": timedelta(minutes=5)},
) as dag:
    insert = BigQueryInsertJobOperator(
        task_id="insert_revenue",
        configuration={"query": {"query": SQL, "useLegacySql": False}},
    )
    check = BigQueryCheckOperator(
        task_id="check_rows",
        sql="""
        select count(*) > 0
        from `acme-prod.analytics.revenue_daily`
        where order_date = date('{{ ds }}')
        """,
        use_legacy_sql=False,
    )
    insert >> check
```

Keep transformation logic in dbt/Dataform and let Airflow handle scheduling, dependencies, and sensors; that separation keeps the DAGs thin.

[Table of Contents](#BigQuery)

## Can you explain the concept of BigQuery Omni?

BigQuery Omni runs BigQuery compute in AWS or Azure regions against data in S3 or Azure Blob Storage. You create a connection, define external tables over the other cloud's storage, and query them with the same SQL. It is designed for data that must stay in another cloud for sovereignty, latency, or egress-cost reasons.

```sql
-- Query S3 data from BigQuery without copying it into GCP (conceptual)
select region, sum(amount) as revenue
from `acme-prod.aws_omni.s3_orders_ext`
where order_date = date '2026-10-04'
group by region;
```

Limitations: no joins across regions or across clouds in one query, a restricted SQL surface, limited DML, and results must be exported or joined within the same Omni region. Use it for targeted cross-cloud analytics, not as a general federation layer.

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery Storage API?

The Storage API has two directions. The Storage Read API streams table data directly to clients (Arrow or Avro) with high parallelism, which is what Spark, Trino, and Dataflow use to read BigQuery fast. The Storage Write API ingests rows with exactly-once semantics via streams and commits.

```python
# Storage Read API: read a table into Arrow for a Spark or pandas consumer
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1

bq = bigquery.Client(project="acme-prod")
bqstorage = bigquery_storage_v1.BigQueryReadClient()

table = bq.get_table("acme-prod.analytics.fact_orders")
read_session = bqstorage.create_read_session(
    parent=f"projects/acme-prod/locations/us",
    read_session=bqstorage_v1.types.ReadSession(
        table=table.path,
        data_format=bqstorage_v1.types.DataFormat.ARROW,
    ),
    max_stream_count=10,
)
arrow_table = bqstorage.read_rows(read_session.name).to_arrow(read_session)
print(arrow_table.num_rows)
```

Use it when you need high-throughput programmatic reads; for ordinary SQL consumers, a plain query is simpler.

[Table of Contents](#BigQuery)

## How can you handle schema evolution in BigQuery?

BigQuery supports adding nullable columns cheaply, dropping and renaming columns, and widening compatible types. For files or streams where the schema genuinely changes over time, use schema autodetection on load, JSON columns for unknown payloads, or `mergeSchema`-style external table evolution for Parquet/ORC.

```sql
-- Additive evolution: safe and metadata-only
alter table `acme-prod.analytics.fact_orders`
add column if not exists fulfillment_type string;

-- Store genuinely open payloads as JSON and query fields on demand
alter table `acme-prod.analytics.events`
add column if not exists properties json;

select
  event_id,
  json_value(properties, '$.campaign_id') as campaign_id,
  json_query(properties, '$.tags') as tags
from `acme-prod.analytics.events`
where event_date = date '2026-10-04';
```

Rules: never reuse a dropped column name with a new meaning, add columns as nullable, and communicate renames to downstream BI and dbt models, because BigQuery cannot rename it for them.

[Table of Contents](#BigQuery)

## Can you explain the concept of time travel in BigQuery?

Time travel lets you query a table as of any point within its retention window using `for system_time as of`. The window is seven days by default and can be configured from two to seven days at the dataset level. It is used for debugging a bad load, auditing, and comparing before/after states.

```sql
-- Did the backfill change yesterday's revenue?
select
  current.revenue as new_revenue,
  prior.revenue as old_revenue,
  current.revenue - prior.revenue as delta
from (
  select sum(amount) as revenue
  from `acme-prod.analytics.fact_orders`
  where order_date = date '2026-10-03'
) current
cross join (
  select sum(amount) as revenue
  from `acme-prod.analytics.fact_orders`
  for system_time as of timestamp '2026-10-04 12:00:00'
  where order_date = date '2026-10-03'
) prior;
```

Time travel is not a backup: it expires, it is bounded by the retention window, and it does not survive an accidental `drop table` beyond the fail-safe period. Use snapshots for anything you need to keep.

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery ML TRANSFORM statement?

`TRANSFORM` defines the feature engineering applied to the training data; BigQuery stores that transformation with the model and reapplies it automatically at prediction time, which prevents training/serving skew.

```sql
create model `acme-prod.analytics.churn_model`
transform (
  ml.standard_scaler(days_since_last_order) over () as days_scaled,
  ml.one_hot_encoder(channel) over () as channel_encoded,
  orders_90d / greatest(tenure_days, 1) as orders_per_day
)
options (
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['churned'],
  auto_class_weights = true
) as
select
  days_since_last_order,
  channel,
  orders_90d,
  tenure_days,
  churned
from `acme-prod.analytics.customer_features`;
```

At prediction time `ML.PREDICT` applies the same transforms, so the caller only supplies raw columns.

[Table of Contents](#BigQuery)

## How does BigQuery handle data consistency in distributed queries?

BigQuery gives a consistent snapshot per query: all reads see a single point-in-time view of the tables involved, even if other jobs are writing concurrently. Within a multi-statement transaction, statements see each other's writes and conflicts are detected optimistically rather than by blocking locks. The historical caveat is the streaming buffer, where recently streamed rows may be visible to `select` but not available for certain operations such as `update`/`delete` until they are flushed.

```sql
-- Transactions are supported for multi-table, atomic DML
begin transaction;
update `acme-prod.analytics.dim_account`
set balance = balance - 100
where account_id = 'a-1';
update `acme-prod.analytics.dim_account`
set balance = balance + 100
where account_id = 'a-2';
commit transaction;
```

So the interview-accurate phrasing is: snapshot-isolated reads, ACID transactions for modest DML volumes, and eventual availability for rows still in a streaming buffer.

[Table of Contents](#BigQuery)

## Can you explain the concept of BigQuery's query cache?

BigQuery keeps a per-project, roughly 24-hour cache of query results. A cache hit requires identical SQL text, unchanged referenced tables, and a deterministic query. Cached results are free. You can disable the cache per query, and you can see whether a job hit the cache in `INFORMATION_SCHEMA.JOBS`.

```sql
-- Look at cache hit rate for a dashboard query pattern
select
  cache_hit,
  count(*) as jobs,
  sum(total_bytes_billed) as bytes_billed
from `region-us`.information_schema.jobs_by_project
where creation_time >= timestamp_sub(current_timestamp(), interval 1 day)
  and statement_type = 'SELECT'
group by cache_hit;
```

```bash
# Force a cold read for benchmarking
bq query --use_legacy_sql=false --nouse_cache '
select count(*) from `acme-prod.analytics.fact_orders`'
```

Cache is a latency and cost optimization for repeated identical queries, not a data freshness mechanism.

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery Data Transfer Service for SaaS?

The SaaS connectors of DTS load data from applications like Salesforce, Marketo, HubSpot, Facebook Ads, and Amazon S3 on a schedule without custom extraction code. Each connector exposes report/object configurations and a lookback window.

```bash
# Salesforce transfer (illustrative flags; check the connector's current params)
bq mk --transfer_config \
  --project_id=acme-prod \
  --data_source=salesforce \
  --target_dataset=crm_raw \
  --display_name='salesforce accounts' \
  --schedule='every 6 hours' \
  --params='{"object":"Account","destination_table_name_template":"account_{run_time}","operation":"Upsert","key_column":"Id"}'
```

Use it for standard objects and steady schedules. For custom objects, very large volumes, or transformations during extraction, build the ingestion yourself (Fivetran, Airbyte, or a custom Cloud Run job) and land into Parquet before loading.

[Table of Contents](#BigQuery)

## How can you monitor and troubleshoot streaming data pipelines in BigQuery?

Monitor four things: arrival latency, error rates at the writer, streaming buffer health, and cost. `INFORMATION_SCHEMA.STREAMING_TIMELINE` shows ingested bytes and rows over time; the writer side (Pub/Sub subscription, Dataflow, or your app) shows failures; Cloud Logging captures quota and schema errors.

```sql
-- Streaming volume and errors over the last day, in one-minute buckets
select
  start_timestamp,
  error_code,
  sum(total_rows) as rows_ingested,
  sum(total_input_bytes) / pow(1024, 2) as mib_ingested
from `region-us`.information_schema.streaming_timeline_by_project
where start_timestamp >= timestamp_sub(current_timestamp(), interval 1 day)
group by start_timestamp, error_code
order by start_timestamp desc
limit 50;
```

Common failure modes: schema mismatch (a new field appears and the writer fails every row), quota exhaustion on legacy streaming inserts, and duplicate delivery because the writer retried without `insertId` deduplication. Prefer the Storage Write API with committed streams and a dead-letter path.

[Table of Contents](#BigQuery)

## Can you explain the concept of BigQuery federated queries?

Federated queries let BigQuery join its own tables to external systems in one SQL statement. There are three mechanisms: external tables (files and Iceberg in Cloud Storage, Bigtable, Spanner), `EXTERNAL_QUERY` (send SQL to Cloud SQL/AlloyDB and read the result), and connections that carry credentials. Nothing is copied or cached by BigQuery, so the external system does the work for `EXTERNAL_QUERY`.

```sql
-- Federation from a Bigtable external table
select
  rowkey,
  cf['amount'] as amount
from `acme-prod.raw.bigtable_events`
where rowkey between '2026-10-04#0000' and '2026-10-04#9999';
```

```sql
-- Federation to Cloud SQL, filtered on the source side
select c.email, sum(o.amount) as lifetime_value
from external_query(
  'projects/acme-prod/locations/us/connections/cloudsql-crm',
  'select customer_id, email from customers where active = true'
) c
join `acme-prod.analytics.fact_orders` o using (customer_id)
group by c.email
order by lifetime_value desc
limit 100;
```

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery Data QnA service?

Data QnA was Google's natural-language question-answering interface for BigQuery. It has been discontinued as a standalone product, so the honest interview answer is: the capability now lives in conversational analytics on top of Looker and Gemini in BigQuery, which translate natural language into SQL against governed semantic models. Do not describe Data QnA as a current product.

```sql
-- The durable pattern underneath conversational analytics is a semantic layer:
create view `acme-prod.analytics.semantic_revenue` as
select
  order_date,
  region,
  segment,
  sum(amount) as revenue,
  count(distinct order_id) as orders
from `acme-prod.analytics.fact_orders`
group by order_date, region, segment;
```

A curated semantic view is what makes any natural-language layer accurate; without it, a language model has no reliable definition of "revenue" or "active customer".

[Table of Contents](#BigQuery)

## Can you explain the concept of BigQuery's workload management?

Workload management in BigQuery means routing workloads to the right capacity and priority. You use reservations and assignments to separate interactive BI from ETL and ad-hoc, choose editions for the governance features you need, and set query priority to `INTERACTIVE` (default, counts against concurrency) or `BATCH` (queued, no concurrency slot, may take longer). Autoscaling and idle-slot sharing let pools borrow capacity.

```sql
-- Run a heavy backfill as a BATCH job so it does not compete with dashboards
create or replace table `acme-prod.analytics.fact_orders_new`
partition by order_date
as
select * from `acme-prod.staging.orders_full`;

-- In the API/CLI, set the priority for a job:
```

```bash
bq query --use_legacy_sql=false --batch '
insert into `acme-prod.analytics.revenue_daily`
select order_date, sum(amount) from `acme-prod.analytics.fact_orders` group by order_date'
```

Practical separation: a reservation for BI dashboards, a reservation for scheduled ETL, and on-demand or a shared autoscaling pool for ad-hoc analysis. Measure with `information_schema.reservation_timeline_by_project`.

[Table of Contents](#BigQuery)

## How does BigQuery handle data skew and hotspots in queries?

Skew shows up as a query plan where one task or one stage takes far longer than its siblings, usually from a join key with a dominant value (for example `country = 'US'` or `customer_id = 'unknown'`) or from `group by` on a skewed column. BigQuery does not expose a manual partitioner, so you fix it in the query: filter the hot key, pre-aggregate, or salt the key.

```sql
-- Hot key problem: one gigantic 'UNKNOWN' customer dominates the join
with cleaned as (
  select *
  from `acme-prod.analytics.fact_orders`
  where order_date = date '2026-10-04'
    and customer_id is not null
    and customer_id <> 'UNKNOWN'
)
select c.segment, sum(o.amount) as revenue
from cleaned o
join `acme-prod.analytics.dim_customer` c using (customer_id)
group by c.segment;

-- Salting a skewed group by spreads one key across N synthetic buckets
select
  bucket,
  count(*) as events
from (
  select mod(abs(farm_fingerprint(user_id)), 16) as bucket
  from `acme-prod.analytics.fact_events`
  where event_date = date '2026-10-04'
)
group by bucket;
```

Also reduce bytes read disproportionately for the hot value by clustering on the skewed column, and prefer `approx_count_distinct` for high-cardinality distinct counts.

[Table of Contents](#BigQuery)

## What is the purpose of the BigQuery ML EVALUATE statement?

`ML.EVALUATE` scores a trained model against a dataset and returns quality metrics: for classification, precision, recall, accuracy, F1, log loss, and ROC AUC; for regression, MAE, MSE, RMSE, R2; for forecasting, several error metrics. It is how you decide whether a model is good enough to ship.

```sql
-- Evaluate the churn model on a held-out period
select *
from ml.evaluate(
  model `acme-prod.analytics.churn_model`,
  (select * from `acme-prod.analytics.customer_features`
   where feature_date >= date '2026-09-01')
);
```

```sql
-- Confusion matrix by threshold for choosing an operating point
select *
from ml.confusion_matrix(
  model `acme-prod.analytics.churn_model`,
  (select * from `acme-prod.analytics.customer_features`
   where feature_date >= date '2026-09-01'),
  struct(0.6 as threshold)
);
```

Pair `ML.EVALUATE` with `ML.EXPLAIN_PREDICT` to see which features drive predictions; stakeholders usually ask "why" immediately after "how accurate".

[Table of Contents](#BigQuery)

## Can you explain the concept of BigQuery's billing export?

The Cloud Billing export writes cost and usage data into BigQuery, either as a standard usage cost table (daily, by service and SKU) or as a detailed export with resource-level and price-level data plus CUD and credit breakdowns. Once exported, you can join cost to your own job metadata and build chargeback.

```sql
-- BigQuery cost by project and dataset for the current month, joined to usage
select
  project.id as project_id,
  service.description as service,
  sku.description as sku,
  round(sum(cost), 2) as cost_usd,
  round(sum(usage.amount), 2) as usage_amount,
  usage.unit as usage_unit
from `acme-prod.billing.gcp_billing_export_v1_012345_6789AB_CDEF01`
where invoice.month = format_date('%Y%m', current_date())
  and service.description = 'BigQuery'
group by project_id, service, sku, usage_unit
order by cost_usd desc;
```

```sql
-- Join cost to query jobs for per-team chargeback
select
  j.user_email,
  round(sum(b.cost), 2) as cost_usd
from `acme-prod.billing.gcp_billing_export_resource_v1_012345_6789AB_CDEF01` b
join `region-us`.information_schema.jobs_by_project j
  on j.job_id = b.labels.value
where b.invoice.month = format_date('%Y%m', current_date())
group by j.user_email
order by cost_usd desc;
```

The export is eventually consistent (hours), so use `jobs` data for real-time investigation and billing export for month-end numbers.

[Table of Contents](#BigQuery)

## How can you automate BigQuery tasks using Cloud Functions?

Cloud Functions (or Cloud Run functions) is a good fit for event-driven, short tasks: validate an object that just landed in Cloud Storage, load it into BigQuery, publish a result, or start a scheduled query. Use Pub/Sub or Cloud Storage triggers, and keep long transformations in Dataflow or SQL rather than in the function.

```python
# Triggered by a new object in gs://acme-landing/orders/
import functions_framework
from google.cloud import bigquery

bq = bigquery.Client(project="acme-prod")


@functions_framework.cloud_event
def load_orders(cloud_event):
    data = cloud_event.data
    bucket = data["bucket"]
    name = data["name"]
    if not name.endswith(".parquet"):
        return

    load_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    uri = f"gs://{bucket}/{name}"
    job = bq.load_table_from_uri(
        uri, "acme-prod.staging.orders_raw", job_config=load_config
    )
    job.result()
    print(f"loaded {job.output_rows} rows from {uri}")
```

For anything stateful, multi-step, or longer than a few minutes, use Workflows, Cloud Composer, or Dataform instead; functions have time and memory limits and are awkward to retry safely.

[Table of Contents](#BigQuery)

## Real world use cases for BigQuery

### 1. Retail: daily sales and inventory marts

A national retailer with 1,200 stores ingests POS transactions (about 4 TB/month, 60 million rows/day) and nightly inventory snapshots. Raw events land in Cloud Storage as Parquet; a `LOAD` job appends into a partitioned fact table; dbt builds a store-day aggregate mart served by Looker.

```sql
create table `acme-prod.analytics.fact_pos_lines`
(
  line_id     string,
  receipt_id  string,
  store_id    string,
  product_id  string,
  sale_date   date,
  qty         int64,
  amount      numeric(12,2)
)
partition by sale_date
cluster by store_id, product_id
options (require_partition_filter = true);

merge `acme-prod.analytics.fact_pos_lines` t
using (
  select * except (rn)
  from (
    select *, row_number() over (partition by line_id order by ingested_at desc) as rn
    from `acme-prod.staging.pos_lines_load`
    where sale_date = date '2026-10-04'
  )
  where rn = 1
) s
on t.line_id = s.line_id
when not matched then insert (line_id, receipt_id, store_id, product_id, sale_date, qty, amount)
values (s.line_id, s.receipt_id, s.store_id, s.product_id, s.sale_date, s.qty, s.amount);
```

Why this design: `sale_date` partitioning keeps dashboard scans to one day of data, `store_id` clustering makes per-store reports prune blocks, and the merge on `line_id` makes reruns idempotent. On-demand pricing plus `require_partition_filter` keeps a 4 TB/month feed cheap.

### 2. Fintech: transaction reconciliation and regulatory reporting

A payments company must reconcile 200 million daily card transactions across a ledger and a processor file, and keep seven years of history for audit. Raw processor files land hourly; a scheduled pipeline reconciles against the internal ledger and writes exceptions to a control table.

```sql
create table `acme-prod.finance.fact_transactions`
(
  txn_id          string,
  account_id      string,
  processor_id    string,
  txn_ts          timestamp,
  txn_date        date,
  amount          numeric(18,2),
  currency        string,
  processor_amount numeric(18,2)
)
partition by txn_date
cluster by processor_id, currency
options (partition_expiration_days = 2555);

create or replace view `acme-prod.finance.v_recon_breaks` as
select txn_id, account_id, txn_date, amount, processor_amount,
       amount - processor_amount as break_amount
from `acme-prod.finance.fact_transactions`
where txn_date = current_date() - 1
  and amount <> processor_amount;
```

Why this design: `numeric` avoids floating-point money errors, date partitioning supports both daily recon and multi-year audit queries, and `partition_expiration_days = 2555` encodes the seven-year retention policy in the table itself. For the immutable regulatory copy, take a snapshot table at month end.

### 3. Marketing: multi-touch attribution across ad platforms

An e-commerce company spends across Google Ads, Meta, and TikTok and wants channel-level ROAS. Ad platform data comes in through Data Transfer Service connectors daily (about 30 GB/day); clickstream and orders are in BigQuery already. A scheduled query joins touchpoints to conversions within a 30-day lookback.

```sql
with touches as (
  select
    user_id,
    channel,
    campaign_id,
    event_ts,
    row_number() over (partition by user_id, channel order by event_ts) as touch_seq
  from `acme-prod.analytics.fact_touchpoints`
  where event_date between date_sub(current_date(), interval 30 day) and current_date()
),
conversions as (
  select user_id, order_id, order_date, amount
  from `acme-prod.analytics.fact_orders`
  where order_date >= date_sub(current_date(), interval 30 day)
)
select
  t.channel,
  count(distinct c.order_id) as attributed_orders,
  sum(c.amount / cnt.touches) as attributed_revenue
from conversions c
join touches t using (user_id)
join (
  select user_id, order_id, count(*) as touches
  from touches join conversions using (user_id)
  group by user_id, order_id
) cnt using (user_id, order_id)
group by t.channel
order by attributed_revenue desc;
```

Why this design: partitioning both tables on the event date keeps the 30-day lookback bounded, and the touchpoint table is clustered by `channel` so per-channel analysis prunes blocks. Attribution logic sits in a materialized view so dashboards stay sub-second.

### 4. SaaS: product analytics with nested events

A B2B SaaS product sends about 500 million events/day, each with a nested `properties` object that differs per event type. The pipeline lands JSON in Cloud Storage, loads into a partitioned table with a `json` column plus a few typed hot columns, and exposes a flattened view for the product team.

```sql
create table `acme-prod.product.events`
(
  event_id   string,
  user_id    string,
  account_id string,
  event_date date,
  event_name string,
  properties json
)
partition by event_date
cluster by account_id, event_name;

create or replace view `acme-prod.product.v_feature_usage` as
select
  event_date,
  account_id,
  event_name,
  json_value(properties, '$.feature') as feature,
  count(*) as events
from `acme-prod.product.events`
group by event_date, account_id, event_name, feature;
```

Why this design: a `json` column absorbs schema churn from hundreds of event types without a migration, while the typed hot columns and clustering keep the common per-account usage queries fast. The view gives analysts a stable interface even as `properties` evolves.

### 5. IoT: fleet telemetry with BI Engine dashboards

A logistics operator receives 12,000 vehicles reporting every 10 seconds (about 100 million messages/day, 2 TB/month) through Pub/Sub. A Dataflow job writes committed streams to a partitioned table; operations dashboards need sub-second refresh on the last 24 hours.

```sql
create table `acme-prod.ops.telemetry`
(
  vehicle_id  string,
  event_ts    timestamp,
  event_date  date,
  lat         float64,
  lon         float64,
  speed_kph   float64,
  fuel_pct    float64
)
partition by event_date
cluster by vehicle_id
options (partition_expiration_days = 365);

-- Hot path: last 24 hours for one fleet region, served from BI Engine
select
  vehicle_id,
  max(event_ts) as last_seen,
  avg(speed_kph) as avg_speed
from `acme-prod.ops.telemetry`
where event_date >= current_date() - 1
  and vehicle_id in (select vehicle_id from `acme-prod.ops.dim_vehicle` where region = 'north')
group by vehicle_id;
```

Why this design: the committed Storage Write API path gives exactly-once ingest without streaming-buffer restrictions, daily partitioning plus `vehicle_id` clustering bounds the 24-hour dashboard scan, and a BI Engine reservation makes the interactive query sub-second. Cold data older than a year expires automatically.

[Table of Contents](#BigQuery)
