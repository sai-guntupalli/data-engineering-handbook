## [Main title](../README.md)
### [Interview questions](full.md)

# Google Cloud Platform

**Notebook:** [`notebooks/topics/gcp.ipynb`](../notebooks/topics/gcp.ipynb) - runnable version of this topic with self-checking exercises.

Google Cloud Platform is the infrastructure and data platform of Google: Cloud Storage for objects, BigQuery for serverless analytics, Dataflow/Dataproc for processing, Pub/Sub for messaging, and IAM/Cloud KMS/VPC for governance.

+ [What is Google Cloud Platform (GCP)?](#What-is-Google-Cloud-Platform-GCP)
+ [How would you design a GCP data platform?](#How-would-you-design-a-GCP-data-platform)
+ [When should you use Dataflow, Dataproc, BigQuery, or Cloud Composer?](#When-should-you-use-Dataflow-Dataproc-BigQuery-or-Cloud-Composer)
+ [What are the key components of GCP?](#What-are-the-key-components-of-GCP)
+ [What are the advantages of using GCP for data engineering?](#What-are-the-advantages-of-using-GCP-for-data-engineering)
+ [How does GCP store data?](#How-does-GCP-store-data)
+ [What is Google BigQuery?](#What-is-Google-BigQuery)
+ [How can you move data into GCP for analysis?](#How-can-you-move-data-into-GCP-for-analysis)
+ [Explain the concept of dataflow in GCP](#Explain-the-concept-of-dataflow-in-GCP)
+ [What is Cloud Dataproc?](#What-is-Cloud-Dataproc)
+ [How does GCP ensure data security?](#How-does-GCP-ensure-data-security)
+ [What is Cloud Pub/Sub?](#What-is-Cloud-PubSub)
+ [Explain the role of Cloud Storage in GCP](#Explain-the-role-of-Cloud-Storage-in-GCP)
+ [What is Cloud Composer in GCP?](#What-is-Cloud-Composer-in-GCP)
+ [How can you monitor and analyze GCP resources and services?](#How-can-you-monitor-and-analyze-GCP-resources-and-services)
+ [What is Cloud Spanner in GCP?](#What-is-Cloud-Spanner-in-GCP)
+ [How can you ensure high availability and fault tolerance in GCP?](#How-can-you-ensure-high-availability-and-fault-tolerance-in-GCP)
+ [Explain the use of Cloud Dataflow in GCP](#Explain-the-use-of-Cloud-Dataflow-in-GCP)
+ [What is Cloud SQL and how is it used in GCP?](#What-is-Cloud-SQL-and-how-is-it-used-in-GCP)
+ [Explain the use of Cloud Datastore in GCP](#Explain-the-use-of-Cloud-Datastore-in-GCP)
+ [How can you securely transfer data to and from GCP?](#How-can-you-securely-transfer-data-to-and-from-GCP)
+ [What is the purpose of Cloud Machine Learning Engine in GCP?](#What-is-the-purpose-of-Cloud-Machine-Learning-Engine-in-GCP)
+ [How does GCP handle disaster recovery?](#How-does-GCP-handle-disaster-recovery)
+ [Explain the concept of VPC (Virtual Private Cloud) in GCP](#Explain-the-concept-of-VPC-Virtual-Private-Cloud-in-GCP)
+ [What is the purpose of Cloud Identity and Access Management (IAM) in GCP?](#What-is-the-purpose-of-Cloud-Identity-and-Access-Management-IAM-in-GCP)
+ [How does GCP handle data redundancy and backup?](#How-does-GCP-handle-data-redundancy-and-backup)
+ [Explain the use of Cloud Composer in GCP](#Explain-the-use-of-Cloud-Composer-in-GCP)
+ [What is the purpose of Cloud Load Balancing in GCP?](#What-is-the-purpose-of-Cloud-Load-Balancing-in-GCP)
+ [How does GCP handle data encryption?](#How-does-GCP-handle-data-encryption)
+ [What is Memorystore in GCP?](#What-is-Memorystore-in-GCP)
+ [Explain the use of Cloud CDN (Content Delivery Network) in GCP](#Explain-the-use-of-Cloud-CDN-Content-Delivery-Network-in-GCP)
+ [How can you monitor and analyze GCP costs?](#How-can-you-monitor-and-analyze-GCP-costs)
+ [Explain the use of Cloud AutoML in GCP](#Explain-the-use-of-Cloud-AutoML-in-GCP)
+ [What is the purpose of Cloud Deployment Manager in GCP?](#What-is-the-purpose-of-Cloud-Deployment-Manager-in-GCP)
+ [How does GCP ensure compliance and data privacy?](#How-does-GCP-ensure-compliance-and-data-privacy)
+ [Explain the use of Cloud Machine Learning Engine in GCP](#Explain-the-use-of-Cloud-Machine-Learning-Engine-in-GCP)
+ [What is the purpose of Cloud Monitoring in GCP?](#What-is-the-purpose-of-Cloud-Monitoring-in-GCP)
+ [How can you optimize data ingestion in GCP?](#How-can-you-optimize-data-ingestion-in-GCP)
+ [What is Cloud Memorystore for Redis in GCP?](#What-is-Cloud-Memorystore-for-Redis-in-GCP)
+ [Explain the use of Cloud Datalab in GCP](#Explain-the-use-of-Cloud-Datalab-in-GCP)
+ [What is the purpose of Cloud DNS in GCP?](#What-is-the-purpose-of-Cloud-DNS-in-GCP)
+ [How can you ensure data integrity in GCP?](#How-can-you-ensure-data-integrity-in-GCP)
+ [Explain the use of Cloud Security Command Center in GCP](#Explain-the-use-of-Cloud-Security-Command-Center-in-GCP)
+ [What is the purpose of Cloud SQL Proxy in GCP?](#What-is-the-purpose-of-Cloud-SQL-Proxy-in-GCP)
+ [Explain the use of Cloud Run in GCP](#Explain-the-use-of-Cloud-Run-in-GCP)
+ [What is the purpose of Cloud Security Scanner in GCP?](#What-is-the-purpose-of-Cloud-Security-Scanner-in-GCP)
+ [What is the purpose of Cloud Composer in GCP?](#What-is-the-purpose-of-Cloud-Composer-in-GCP)
+ [How does GCP handle data archiving and long-term storage?](#How-does-GCP-handle-data-archiving-and-long-term-storage)
+ [How can you manage data access and permissions in GCP?](#How-can-you-manage-data-access-and-permissions-in-GCP)
+ [How can you optimize data processing in GCP?](#How-can-you-optimize-data-processing-in-GCP)
+ [What is the purpose of Cloud NAT in GCP?](#What-is-the-purpose-of-Cloud-NAT-in-GCP)
+ [Explain the use of Cloud IoT Core in GCP](#Explain-the-use-of-Cloud-IoT-Core-in-GCP)
+ [How does GCP handle data replication and synchronization?](#How-does-GCP-handle-data-replication-and-synchronization)
+ [Explain the use of Cloud VPN in GCP](#Explain-the-use-of-Cloud-VPN-in-GCP)
+ [What is the purpose of Cloud Functions in GCP?](#What-is-the-purpose-of-Cloud-Functions-in-GCP)
+ [How can you monitor and troubleshoot performance issues in GCP?](#How-can-you-monitor-and-troubleshoot-performance-issues-in-GCP)
+ [Explain the use of Cloud Key Management Service (KMS) in GCP](#Explain-the-use-of-Cloud-Key-Management-Service-KMS-in-GCP)
+ [Real world use cases for GCP](#Real-world-use-cases-for-GCP)

## What is Google Cloud Platform (GCP)?

Google Cloud Platform is a suite of cloud computing services provided by Google, offering a wide range of infrastructure and platform services for building, deploying, and managing applications and data.

For data engineering, the reference architecture is: Pub/Sub or Cloud Storage as the entry point, Dataflow or Dataproc to process, BigQuery to serve analytics, Dataplex/Data Catalog to govern, and Cloud Composer to orchestrate. The differentiator is serverless: BigQuery has no clusters and Dataflow autoscales workers, so capacity planning shifts from machines to slots and job sizing.

```bash
# The fastest way to establish project context for any gcloud interview exercise
gcloud config set project acme-data-prod
gcloud config list
gcloud services list --enabled --filter="config.name:bigquery OR config.name:dataflow"
```

[Table of Contents](#Google-Cloud-Platform)

## How would you design a GCP data platform?

A common GCP data platform uses Cloud Storage as the data lake, Dataflow or Dataproc for processing, Pub/Sub for messaging, BigQuery for analytics, Dataplex/Data Catalog for governance, and Cloud Composer for orchestration. Choose managed services when possible to reduce operational overhead.

Example:

```text
Pub/Sub -> Dataflow -> BigQuery
Cloud Storage raw files -> Dataproc/Spark -> BigQuery marts
```

Security should include IAM least privilege, service accounts, VPC Service Controls where needed, CMEK/KMS for sensitive data, and audit logging.

```hcl
# Terraform: the foundational platform resources
resource "google_storage_bucket" "raw" {
  name                        = "acme-raw-prod"
  location                    = "US"
  uniform_bucket_level_access = true
  versioning { enabled = true }
  lifecycle_rule {
    condition { age = 730 }
    action { type = "Delete" }
  }
}

resource "google_bigquery_dataset" "curated" {
  dataset_id                 = "curated"
  location                   = "US"
  default_table_expiration_ms = 0
  labels                     = { env = "prod", owner = "data-platform" }
}

resource "google_service_account" "dataflow_runner" {
  account_id   = "dataflow-runner"
  display_name = "Dataflow runner"
}
```

```text
Layer map
  landing   gs://acme-raw-prod/orders/dt=YYYY-MM-DD/        (immutable, JSON/Avro)
  curated   gs://acme-curated-prod/orders/dt=/             (Parquet/Iceberg)
  warehouse bq://acme-data-prod/curated.orders             (external or native)
  marts     bq://acme-data-prod/marts.orders_daily
  governance Dataplex zones + Data Catalog tags + audit logs
```

[Table of Contents](#Google-Cloud-Platform)

## When should you use Dataflow, Dataproc, BigQuery, or Cloud Composer?

Use Dataflow for managed Apache Beam batch/stream processing. Use Dataproc when you need Spark/Hadoop compatibility and cluster-level control. Use BigQuery for serverless analytical SQL and warehousing. Use Cloud Composer when you need Airflow-based orchestration.

Example choices:

+ streaming enrichment from Pub/Sub: Dataflow
+ existing Spark job migration: Dataproc
+ BI reporting and SQL transformations: BigQuery
+ dependency scheduling across jobs: Cloud Composer

The decision should consider latency, language/runtime, operational control, and cost.

| Need | Choose | Why | Watch out |
|---|---|---|---|
| Streaming ETL, autoscaling, Beam | Dataflow | serverless, exactly-once with BigQuery sink | worker sizing and shuffle costs |
| Existing Spark/Hadoop, custom libs | Dataproc | full cluster control, GPUs, Hive metastore | idle clusters burn money |
| SQL modeling and BI | BigQuery | serverless, slot-based pricing | partition pruning is on you |
| Cross-system scheduling | Cloud Composer | Airflow DAGs, sensors, retries | environment cost ~$300+/mo |

```python
import json
# Dataflow (Beam) is the default for new streaming work
import apache_beam as beam

with beam.Pipeline() as p:
    (
        p
        | "Read" >> beam.io.ReadFromPubSub(topic="projects/acme/topics/orders")
        | "Parse" >> beam.Map(lambda b: json.loads(b.decode("utf-8")))
        | "Write" >> beam.io.WriteToBigQuery(
            "acme:curated.orders_stream",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        )
    )
```

When NOT to use Dataflow: a small, hourly SQL transform belongs in BigQuery scheduled queries, and a one-off file conversion belongs in a Cloud Run job — a Beam pipeline you do not need is operational overhead.

[Table of Contents](#Google-Cloud-Platform)

## What are the key components of GCP?

GCP comprises various services such as compute, storage, networking, databases, big data, machine learning, and management tools.

| Category | Core services |
|---|---|
| Compute | Compute Engine, GKE, Cloud Run, Cloud Functions |
| Storage | Cloud Storage, Filestore, Persistent Disk |
| Databases | Cloud SQL, Cloud Spanner, Bigtable, Firestore |
| Analytics | BigQuery, Dataflow, Dataproc, Pub/Sub, Dataplex, Composer |
| AI/ML | Vertex AI, AutoML, Vertex Pipelines |
| Networking | VPC, Cloud DNS, Cloud NAT, Load Balancing, Cloud CDN, VPN/Interconnect |
| Security/ops | Cloud IAM, Cloud KMS, Security Command Center, Cloud Logging/Monitoring |

```bash
# Inventory the data services enabled in a project
gcloud services list --enabled \
  --filter="config.name:(bigquery.googleapis.com OR dataflow.googleapis.com OR dataproc.googleapis.com OR pubsub.googleapis.com OR composer.googleapis.com)"
```

[Table of Contents](#Google-Cloud-Platform)

## What are the advantages of using GCP for data engineering?

GCP provides scalability, flexibility, high-performance computing, data storage options, managed services, security, and integration with other Google services.

The specific data-engineering advantages: BigQuery separates storage from compute (pay for slots, not always-on clusters), Dataflow autoscales and has a strong exactly-once story with BigQuery sinks, Pub/Sub removes broker operations, and IAM/bigquery resource hierarchy gives project-level isolation. Trade-offs: BigQuery's pricing model (on-demand bytes scanned vs. flat-rate slots) can surprise teams, and multi-cloud portability is weaker than the Apache-based ecosystems on other clouds.

```sql
-- Quantify the cost model before recommending BigQuery to stakeholders
SELECT
  ROUND(SUM(total_bytes_billed) / POW(1024, 4), 2) AS tb_billed,
  ROUND(SUM(total_bytes_billed) / POW(1024, 4) * 6.25, 2) AS on_demand_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY);
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP store data?

GCP offers various storage options, including Cloud Storage for object storage, Cloud SQL for managed relational databases, Bigtable for NoSQL wide-column store, and Cloud Firestore for document-based NoSQL data.

```text
Choose by access pattern
  objects / lake files / backups        -> Cloud Storage (Standard/Nearline/Coldline/Archive)
  OLTP relational, MySQL/PG/SQL Server  -> Cloud SQL
  global strongly consistent relational -> Spanner
  wide-column, high-throughput time series -> Bigtable
  mobile/web document store             -> Firestore
  analytical warehouse                  -> BigQuery
  in-memory cache                       -> Memorystore
```

```bash
# Storage classes are a lifecycle decision, not a one-time setting
gsutil mb -l US -c STANDARD gs://acme-raw-prod
gsutil lifecycle set lifecycle.json gs://acme-raw-prod
cat lifecycle.json
{
  "rule": [
    {"action": {"type": "SetStorageClass", "storageClass": "NEARLINE"}, "condition": {"age": 30}},
    {"action": {"type": "SetStorageClass", "storageClass": "COLDLINE"}, "condition": {"age": 120}},
    {"action": {"type": "Delete"}, "condition": {"age": 1095}}
  ]
}
```

[Table of Contents](#Google-Cloud-Platform)

## What is Google BigQuery?

BigQuery is a fully-managed, serverless data warehouse provided by GCP. It enables you to analyze massive datasets using SQL queries with high speed and scalability.

```sql
-- Partitioning and clustering are the two biggest cost levers
CREATE TABLE curated.orders (
  order_id     STRING NOT NULL,
  customer_id  STRING,
  order_ts     TIMESTAMP,
  country      STRING,
  amount       NUMERIC
)
PARTITION BY DATE(order_ts)
CLUSTER BY country, customer_id
OPTIONS (partition_expiration_days = 1095,
         require_partition_filter = TRUE);
```

```bash
# Always dry-run before a large query: it reports bytes, costs nothing
bq query --dry_run --use_legacy_sql=false \
  'SELECT country, SUM(amount) FROM `acme-data-prod.curated.orders`
   WHERE DATE(order_ts) = "2026-10-04" GROUP BY country'
```

`require_partition_filter = TRUE` turns an accidental full-table scan into an error rather than a $500 surprise. Trade-off: appending to or replacing a single partition is a per-partition operation (`WRITE_APPEND` or `WRITE_TRUNCATE` against a `table$YYYYMMDD` decorator), and over-clustering on high-cardinality columns increases metadata overhead without helping pruning.

[Table of Contents](#Google-Cloud-Platform)

## How can you move data into GCP for analysis?

You can use services like Cloud Storage, Cloud Pub/Sub, Data Transfer Service, or third-party tools to import data into GCP for analysis.

```text
Batch file transfer        -> Storage Transfer Service / Transfer Appliance
SaaS and DB connectors     -> BigQuery Data Transfer Service (e.g. Google Ads, S3, Teradata)
Streaming                  -> Pub/Sub + Dataflow, or the BigQuery Storage Write API
Database CDC               -> Datastream (MySQL/PostgreSQL/Oracle -> BigQuery or GCS)
On-prem bulk               -> Transfer Appliance (physical) or Cloud Interconnect (private)
```

```bash
# Storage Transfer Service: copy on-prem S3/NFS/HDFS into a GCS bucket
gcloud transfer jobs create \
  --source-agent-pool=acme-pool \
  --source-directory=/mnt/nfs/exports \
  gs://acme-raw-prod/imports/orders/ \
  --schedule-starts=2026-10-04T02:00:00Z \
  --schedule-repeats-every=1d
```

Trade-off: BigQuery Data Transfer Service is managed but limited to supported sources and its scheduling is coarse; Datastream gives low-latency CDC but is one more streaming system to operate.

[Table of Contents](#Google-Cloud-Platform)

## Explain the concept of dataflow in GCP

Dataflow is a serverless data processing service that allows you to build, deploy, and execute data processing pipelines in GCP. It supports both batch and stream processing.

A Dataflow pipeline is a Beam pipeline run on a managed runner: you write `PTransform`s, and the runner handles work distribution, autoscaling, checkpointing, and drain/update. Batch and streaming use the same code, which is the key interview point — the difference is `--streaming` and the source/sink choices, not a second framework.

```text
Beam programming model
  PCollection (immutable, distributed)
     |  PTransform   PTransform   PTransform
  source = ReadFromPubSub / ReadFromText / ReadFromBigQuery
  sink   = WriteToBigQuery / WriteToText / WriteToPubSub
  windowing: FixedWindows / SlidingWindows / Sessions
  triggers:  AfterWatermark, AfterProcessingTime, accumulation mode
```

```python
import json
# Batch word-count skeleton: the shape of every Beam pipeline
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions(["--runner=DataflowRunner", "--region=us-central1"])

with beam.Pipeline(options=options) as p:
    (
        p
        | "Read" >> beam.io.ReadFromText("gs://acme-raw-prod/events/*.jsonl")
        | "Parse" >> beam.Map(lambda line: json.loads(line))
        | "Key" >> beam.Map(lambda e: (e["country"], e["amount"]))
        | "Sum" >> beam.CombinePerKey(sum)
        | "Format" >> beam.Map(lambda kv: {"country": kv[0], "revenue": kv[1]})
        | "Write" >> beam.io.WriteToBigQuery(
            "acme:curated.revenue_by_country",
            schema="country:STRING,revenue:FLOAT",
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
        )
    )
```

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud Dataproc?

Cloud Dataproc is a fully-managed service in GCP for running Apache Spark and Apache Hadoop clusters. It provides a scalable and cost-effective way to process big data workloads.

Dataproc is the migration path for existing Spark/Hadoop code. It supports ephemeral clusters (create, run a job, delete), autoscaling, optional components (Jupyter, Hive metastore, Druid), and Spot/preemptible workers for the shuffle tier.

```bash
# Ephemeral cluster: create, submit, delete; nothing idles overnight
gcloud dataproc clusters create etl-tmp \
  --region=us-central1 \
  --num-workers=10 \
  --worker-machine-type=n2-standard-8 \
  --num-secondary-workers=20 \
  --secondary-worker-type=spot \
  --enable-component-gateway \
  --optional-components=JUPYTER,HIVE_WAREHOUSE \
  --max-idle=30m

gcloud dataproc jobs submit pyspark gs://acme-code/orders_etl.py \
  --cluster=etl-tmp --region=us-central1 \
  --properties=spark.sql.shuffle.partitions=200
```

Trade-off: Dataproc gives full control (custom JARs, GPUs, cluster tuning) but you own cluster lifecycle and idle cost; Dataflow is less tunable but has no cluster to manage. For pure Spark SQL on GCS/BigQuery, Dataproc Serverless removes the cluster entirely.

[Table of Contents](#Google-Cloud-Platform)

## How does GCP ensure data security?

GCP employs various security measures, including encryption at rest and in transit, identity and access management, network security, and DDoS protection.

```text
Defense in depth
  Identity      IAM least privilege + service accounts + short-lived tokens (Workload Identity)
  Network       VPC firewall rules, Private Google Access, VPC Service Controls perimeters
  Data at rest  Google-managed keys by default; CMEK via Cloud KMS; CSEK for GCS
  Data in transit TLS everywhere, private interconnect for on-prem
  Detection     Security Command Center, Cloud Audit Logs, Access Transparency
```

The IAM policy below grants least privilege: read one curated dataset, run Dataflow, and no project-owner role.

```json
{
  "bindings": [
    {
      "role": "roles/bigquery.dataViewer",
      "members": ["serviceAccount:dataflow-runner@acme-data-prod.iam.gserviceaccount.com"],
      "condition": {
        "title": "curated-dataset-only",
        "expression": "resource.name.startsWith('projects/acme-data-prod/datasets/curated')"
      }
    },
    {
      "role": "roles/dataflow.worker",
      "members": ["serviceAccount:dataflow-runner@acme-data-prod.iam.gserviceaccount.com"]
    }
  ]
}
```

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud Pub/Sub?

Cloud Pub/Sub is a messaging service in GCP that enables asynchronous communication between independent applications. It allows you to build scalable event-driven architectures.

Pub/Sub is a durable, at-least-once publish/subscribe log with a 7-day default retention (up to 31 days), per-subscription acknowledgements, ordering keys for per-key ordering, and dead-letter topics.

```bash
# Topic + subscription with a dead-letter policy and retention
gcloud pubsub topics create orders-v1
gcloud pubsub topics create orders-v1-deadletter
gcloud pubsub subscriptions create orders-v1-sub \
  --topic=orders-v1 \
  --ack-deadline=60 \
  --message-retention-duration=7d \
  --dead-letter-topic=orders-v1-deadletter \
  --max-delivery-attempts=5 \
  --enable-exactly-once-delivery
```

Trade-off: Pub/Sub has no consumer groups with per-partition replay semantics like Kafka, and no long-term event log for arbitrary replay; if you need weeks of replay or a compacted topic, use Confluent/Kafka on GKE. Pub/Sub push subscriptions are also a common source of duplicate delivery, so consumers must be idempotent.

[Table of Contents](#Google-Cloud-Platform)

## Explain the role of Cloud Storage in GCP

Cloud Storage is an object storage service provided by GCP. It offers scalable, durable, and highly available storage for objects of any size. It can be used for storing files, backups, and serving static content.

```text
gs://acme-raw-prod/orders/dt=2026-10-04/part-00000.parquet
|-- bucket: globally unique, location-bound (region/multi-region/dual-region)
|-- object: immutable; "update" is a rewrite
|-- class:  Standard -> Nearline (30d) -> Coldline (90d) -> Archive (365d)
|-- consistency: strongly consistent list and read after write
```

```bash
# Parallel upload for a large directory; GCS throughput scales with parallelism
gcloud storage cp --recursive ./exports/orders/ gs://acme-raw-prod/orders/dt=2026-10-04/

# Object integrity
gcloud storage hash gs://acme-raw-prod/orders/dt=2026-10-04/part-00000.parquet
# Composite objects (parallel uploads) need crc32c, not md5.
```

Trade-off: object storage is cheapest and infinitely scalable, but object mutation is a full rewrite, so small-file compaction is essential for query performance. Use `gcloud storage` (faster, parallel) over the legacy `gsutil` for large copies.

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud Composer in GCP?

Cloud Composer is a managed workflow orchestration service based on Apache Airflow. It allows you to create, schedule, and monitor workflows composed of tasks, such as data processing or ETL pipelines.

Composer runs Airflow on GKE and gives you a GCS bucket for DAGs, a SQL database for metadata, and IAM integration. You rarely run the Airflow infrastructure, but you still own DAG quality, connections (Secret Manager), and environment sizing.

```python
# DAG: GCS -> Dataflow template -> BigQuery check
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor

with DAG(
    dag_id="orders_hourly",
    schedule="0 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:
    wait_for_file = GCSObjectExistenceSensor(
        task_id="wait_for_file",
        bucket="acme-raw-prod",
        object='orders/dt={{ ds }}/hour={{ data_interval_start.hour }}/_SUCCESS',
        timeout=3600,
        poke_interval=60,
    )
    run_dataflow = DataflowStartFlexTemplateOperator(
        task_id="run_dataflow",
        body={
            "launchParameter": {
                "jobName": "orders-hourly",
                "containerSpecGcsPath": "gs://acme-code/templates/orders.json",
                "parameters": {"input": "gs://acme-raw-prod/orders/", "output": "curated.orders"},
            }
        },
        location="us-central1",
    )
    wait_for_file >> run_dataflow
```

Trade-off: Composer is the right tool for cross-system dependencies and sensors, but it costs money even when idle and is a poor fit for per-minute latency — use Dataflow triggers or Cloud Scheduler for those.

[Table of Contents](#Google-Cloud-Platform)

## How can you monitor and analyze GCP resources and services?

GCP provides various monitoring and logging tools, such as Cloud Monitoring, Cloud Logging, and Stackdriver, which allow you to collect, analyze, and visualize metrics, logs, and traces.

```bash
# Read recent errors for a Dataflow job
gcloud logging read 'resource.type="dataflow_step" severity>=ERROR' \
  --limit=20 --format='table(timestamp, resource.labels.job_name, textPayload)'

# Create a log-based metric and alert on it
gcloud logging metrics create orders_dlq_errors \
  --description="Dead-letter records" \
  --log-filter='resource.type="dataflow_step" jsonPayload.stage="dlq"'
```

```yaml
# Alerting policy: page when a Dataflow job stops advancing
displayName: "Dataflow backlog growing"
conditions:
  - displayName: "system lag > 10 min"
    conditionThreshold:
      filter: 'resource.type="dataflow_job" AND metric.type="dataflow.googleapis.com/job/system_lag"'
      comparison: COMPARISON_GT
      thresholdValue: 600
      duration: "300s"
      aggregations:
        - alignmentPeriod: "60s"
          perSeriesAligner: ALIGN_MAX
notificationChannels: ["projects/acme-data-prod/notificationChannels/12345"]
```

Also monitor BigQuery slots, Pub/Sub oldest unacked message age, GCS request latency, and Composer task duration. The trick is to alert on user-visible symptoms (freshness, backlog age) rather than raw resource metrics.

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud Spanner in GCP?

Cloud Spanner is a horizontally scalable, globally distributed relational database service provided by GCP. It combines the benefits of relational databases with the scalability of NoSQL.

Spanner gives external consistency, ANSI SQL, and horizontal scale via interleaved tables and split points. It is expensive and its throughput is bound by the number of nodes/processing units, so it is chosen for global OLTP with strong consistency, not for analytics.

```sql
-- Interleaved tables co-locate child rows with the parent for fast joins
CREATE TABLE Customers (
  CustomerId STRING(36) NOT NULL,
  Region     STRING(16) NOT NULL,
  CreatedAt  TIMESTAMP NOT NULL OPTIONS (allow_commit_timestamp = true)
) PRIMARY KEY (CustomerId);

CREATE TABLE Orders (
  CustomerId STRING(36) NOT NULL,
  OrderId    STRING(36) NOT NULL,
  Amount     NUMERIC,
  OrderTs    TIMESTAMP
) PRIMARY KEY (CustomerId, OrderId),
  INTERLEAVE IN PARENT Customers ON DELETE CASCADE;
```

```bash
# Size the instance: start small and scale with autoscaling
gcloud spanner instances create acme-oltp --config=regional-us-central1 \
  --processing-units=1000 --description="Global orders"
```

[Table of Contents](#Google-Cloud-Platform)

## How can you ensure high availability and fault tolerance in GCP?

GCP offers regional and multi-regional options for deploying services across multiple zones and regions. Load balancing, auto-scaling, and managed instance groups help ensure high availability and fault tolerance.

```text
Service HA mapping
  GCE/GKE        regional MIG / multi-zone node pools, health checks, autoscaling
  Cloud SQL      regional HA (failover replica in a second zone) + PITR backups
  BigQuery       multi-region or dual-region datasets; storage is replicated
  Cloud Storage  regional/multi-region/dual-region; turbo replication for RPO=0
  Pub/Sub        globally replicated by design
  Spanner        regional or multi-region config with automatic failover
  Dataflow       regional workers, autoscaling, retries
```

```bash
# Cloud SQL regional HA with point-in-time recovery
gcloud sql instances create acme-pg \
  --database-version=POSTGRES_16 --region=us-central1 \
  --availability-type=REGIONAL --tier=db-custom-4-16384 \
  --backup --backup-start-time=03:00 --enable-point-in-time-recovery
```

Trade-off: multi-region raises cost, latency, and operational complexity; most analytics workloads only need regional storage plus cross-region copies of the few critical datasets.

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Dataflow in GCP

Cloud Dataflow is used for building data pipelines that transform and process data in parallel. It supports both batch and stream processing and can be integrated with other GCP services like BigQuery.

```bash
# Run a Flex Template: the production way to deploy a Beam pipeline
gcloud dataflow flex-template run orders-stream \
  --template-file-gcs-location=gs://acme-code/templates/orders.json \
  --region=us-central1 \
  --parameters=inputTopic=projects/acme-data-prod/topics/orders-v1 \
  --parameters=outputTable=acme-data-prod:curated.orders_stream \
  --parameters=windowDuration=1m \
  --max-workers=20 --num-workers=2 --worker-machine-type=n1-standard-4 \
  --enable-streaming-engine
```

```python
import json
# Streaming windowed aggregation with a watermark and late-data handling
import apache_beam as beam
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime, AccumulationMode

with beam.Pipeline() as p:
    (
        p
        | beam.io.ReadFromPubSub(topic="projects/acme/topics/orders")
        | beam.Map(lambda b: json.loads(b.decode("utf-8")))
        | beam.Map(lambda e: (e["country"], e["amount"]))
        | beam.WindowInto(
            FixedWindows(60),
            trigger=AfterWatermark(
                early=AfterProcessingTime(30),
                late=AfterProcessingTime(60),
            ),
            accumulation_mode=AccumulationMode.ACCUMULATING,
        )
        | beam.CombinePerKey(sum)
        | beam.io.WriteToBigQuery(
            "acme:curated.revenue_1m",
            schema="country:STRING,revenue:FLOAT",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        )
    )
```

Sizing rule of thumb: one worker per 1-2 vCPUs of steady load, plus headroom; use `--max-workers` to cap cost and `--num-workers` to control cold start. Streaming jobs with the Streaming Engine off will pay for shuffle on persistent disks.

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud SQL and how is it used in GCP?

Cloud SQL is a managed database service in GCP that provides MySQL, PostgreSQL, and SQL Server databases. It simplifies database management tasks, offers high availability, and scales seamlessly.

```bash
# Create a Postgres instance, database, and user for an ingest path
gcloud sql instances create acme-orders \
  --database-version=POSTGRES_16 --region=us-central1 --tier=db-custom-2-8192 \
  --storage-auto-increase --availability-type=ZONAL
gcloud sql databases create orders --instance=acme-orders
gcloud sql users create etl --instance=acme-orders --password="$PG_PASSWORD"

# Export straight to GCS as CSV for a warehouse load
gcloud sql export csv acme-orders gs://acme-raw-prod/export/orders/ \
  --database=orders \
  --query='SELECT * FROM orders WHERE updated_at >= NOW() - INTERVAL 1 DAY'
```

For analytics, do not query Cloud SQL directly from BI at scale: replicate into BigQuery with Datastream CDC or a nightly extract, and keep the OLTP instance for transactions.

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Datastore in GCP

Cloud Datastore is a NoSQL document database provided by GCP. It is schemaless, automatically scales, and is suitable for applications that require low-latency reads and writes.

Datastore is the older standalone product; the current generation is Firestore in Datastore mode (same API, better scaling and stronger consistency). It is a key-value/document store with indexes and entity groups, chosen for web/app state, not analytics.

```python
# Firestore in Datastore mode: entities and strongly consistent ancestor queries
from google.cloud import datastore

client = datastore.Client(project="acme-data-prod")

key = client.key("Order", "order-1001")
client.put(datastore.Entity(key=key, exclude_from_indexes=("payload",), order_total=42.5))
entity = client.get(key)
assert entity is not None

query = client.query(kind="Order", ancestor=client.key("Customer", "cust-7")).order("-order_total")
print([(e.key.name, e["order_total"]) for e in query.fetch(limit=5)])
```

[Table of Contents](#Google-Cloud-Platform)

## How can you securely transfer data to and from GCP?

GCP supports secure data transfer over encrypted connections using protocols like HTTPS and SSL/TLS. It also provides Cloud VPN and Dedicated Interconnect for private network connections.

```text
Connections, weakest to strongest isolation
  public internet + TLS        baseline, fine for encrypted object APIs
  Cloud VPN (HA)               IPsec over internet, ~1-3 Gbps per tunnel
  Dedicated Interconnect       private 10/100 Gbps, no internet, SLA-backed
  Partner Interconnect         private via a carrier, smaller sites
  VPC Service Controls         data-exfiltration perimeter for APIs
```

```bash
# HA VPN to on-prem with two tunnels; BGP advertises the subnets
gcloud compute vpn-gateways create acme-vpn --network=acme-vpc --region=us-central1
gcloud compute external-vpn-gateways create onprem-gw \
  --interfaces=0=203.0.113.10,1=203.0.113.11
gcloud compute vpn-tunnels create acme-tunnel-0 --peer-external-gateway=onprem-gw \
  --peer-external-gateway-interface=0 --region=us-central1 \
  --ike-version=2 --shared-secret="$IKE_PSK" \
  --router=acme-router --vpn-gateway=acme-vpn --interface=0
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Machine Learning Engine in GCP?

Cloud Machine Learning Engine is a managed service in GCP that allows you to build, train, and deploy machine learning models at scale. It supports popular frameworks like TensorFlow and scikit-learn.

The modern version is Vertex AI, which merges AI Platform (ML Engine), AutoML, and Pipelines. For data engineers the relevant piece is the integration: train from BigQuery or GCS, register the model, deploy an endpoint, and schedule retraining as part of the platform.

```python
# Train a scikit-learn model on a BigQuery extract and register it in Vertex AI
import pandas as pd
from google.cloud import bigquery
from sklearn.linear_model import LogisticRegression

client = bigquery.Client(project="acme-data-prod")
df = client.query(
    "SELECT days_since_signup, orders_30d, churned FROM `acme-data-prod.ml.churn_train`"
).to_dataframe()

model = LogisticRegression(max_iter=1000).fit(
    pd.get_dummies(df[["days_since_signup", "orders_30d"]]), df["churned"]
)
print("trained on", len(df), "rows")
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP handle disaster recovery?

GCP provides disaster recovery solutions through features like regional and multi-regional deployments, automated backups, and replication across zones and regions.

```text
RPO/RTO by tier
  Tier 1 (payments)   RPO 0,  RTO <15 min   Spanner multi-region or dual-region GCS + warm standby
  Tier 2 (reporting)  RPO 1h, RTO <4h      BigQuery multi-region, nightly snapshots, IaC rebuild
  Tier 3 (archive)    RPO 24h, RTO <24h    Coldline/Archive + documented restore runbook
```

```bash
# Cross-region backup of a critical Cloud SQL instance
gcloud sql backups create --instance=acme-pg --location=us-east1
gcloud sql instances clone acme-pg acme-pg-dr --destination-project=acme-dr-prod

# BigQuery dataset copy to a DR region
bq mk --transfer_config --project_id=acme-data-prod \
  --data_source=cross_region_copy \
  --target_dataset=curated_dr \
  --display_name='curated nightly DR copy' \
  --params='{"source_dataset_id":"curated","source_project_id":"acme-data-prod","destination_dataset_id":"curated_dr"}'
```

Trade-off: a true warm standby doubles cost. Most teams run a documented "rebuild from Terraform + rehydrate from GCS" path and accept a longer RTO for everything except the tier-1 ledger.

[Table of Contents](#Google-Cloud-Platform)

## Explain the concept of VPC (Virtual Private Cloud) in GCP

VPC allows you to create a virtual private network within GCP, providing isolation and control over network resources. It enables you to define IP ranges, subnets, firewall rules, and routing tables.

Key differences from other clouds: a GCP VPC is global (subnets are regional), firewall rules are stateful and applied at the instance/tag level, and Shared VPC lets a host project provide subnets to many service projects.

```bash
# Global VPC with a regional subnet and least-privilege firewall rules
gcloud compute networks create acme-vpc --subnet-mode=custom
gcloud compute networks subnets create acme-us-central \
  --network=acme-vpc --region=us-central1 --range=10.10.0.0/20 \
  --enable-private-ip-google-access

gcloud compute firewall-rules create allow-internal \
  --network=acme-vpc --direction=INGRESS --action=ALLOW \
  --rules=tcp:0-65535,udp:0-65535,icmp --source-ranges=10.10.0.0/20

# Deny all other ingress by default; add explicit rules for services.
gcloud compute firewall-rules create default-deny-ingress \
  --network=acme-vpc --direction=INGRESS --action=DENY --rules=all \
  --source-ranges=0.0.0.0/0 --priority=65534
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Identity and Access Management (IAM) in GCP?

IAM allows you to manage access control and permissions for GCP resources. It helps you define who has access to which resources and what actions they can perform.

IAM is a resource hierarchy (organization -> folder -> project -> resource) where policies are inherited and additive. Use predefined roles where possible, custom roles only when necessary, service accounts with Workload Identity for workloads, and conditions for fine-grained scope.

```bash
# Grant a service account BigQuery job user at project level (minimum to run jobs)
gcloud projects add-iam-policy-binding acme-data-prod \
  --member="serviceAccount:dataflow-runner@acme-data-prod.iam.gserviceaccount.com" \
  --role="roles/bigquery.jobUser"

# Grant read on one dataset instead of the whole project
bq add-iam-policy-binding \
  --member="serviceAccount:dataflow-runner@acme-data-prod.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataViewer" \
  acme-data-prod:curated
```

Trade-off: broad predefined roles (`roles/bigquery.dataEditor` at project level) are easy but give a compromised job access to every dataset; dataset-level grants and IAM conditions cost more setup but shrink the blast radius.

[Table of Contents](#Google-Cloud-Platform)

## How does GCP handle data redundancy and backup?

GCP offers redundancy and backup options such as regional and multi-regional storage, snapshot-based backups, and data replication across multiple zones and regions.

```text
Redundancy vs backup (they are not the same)
  Redundancy  GCS multi-region, Cloud SQL HA, Spanner multi-region  -> survives zone failure
  Backup      Cloud SQL automated backups + PITR, GCS object versioning, BQ snapshots -> survives deletion/corruption
  Offsite     cross-region copies, export to a separate project    -> survives account compromise
```

```bash
# BigQuery table snapshot: cheap point-in-time copy for a critical table
bq cp -n --snapshot curated.orders curated.orders_snapshot_20261004

# GCS object versioning so an overwrite does not destroy the previous file
gcloud storage buckets update gs://acme-curated-prod --versioning

# Cloud SQL point-in-time restore to a new instance
gcloud sql instances clone acme-pg acme-pg-restore \
  --point-in-time='2026-10-04T02:15:00.000Z'
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Composer in GCP

Cloud Composer is used for orchestrating workflows and managing dependencies between tasks. It allows you to create, schedule, and monitor complex data pipelines and ETL workflows.

Composer 2/3 environments expose the Airflow UI, connections via Secret Manager, and autoscaling workers. Operational practice: keep DAGs idempotent and parameterized by logical date, use sensors sparingly (deferrable operators where possible), and monitor DAG parse time and scheduler health.

```bash
# Create an environment and list it; DAGs are synced from the dags/ prefix in GCS
gcloud composer environments create acme-airflow \
  --location=us-central1 --image-version=composer-3-airflow-2 \
  --environment-size=small --node-count=3

gcloud composer environments run acme-airflow \
  --location=us-central1 dags list
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Load Balancing in GCP?

Cloud Load Balancing distributes incoming traffic across multiple instances or backend services to ensure high availability, scalability, and fault tolerance.

For data engineering, the relevant variants are global external HTTP(S) for APIs, internal TCP/UDP for services inside a VPC, and internal HTTP(S) for microservices. Global load balancing uses anycast, so a single VIP routes users to the nearest healthy region.

```bash
# Global HTTP(S) LB with a managed certificate and health check
gcloud compute health-checks create http acme-hc --port=8080 --request-path=/healthz
gcloud compute backend-services create acme-api \
  --global --protocol=HTTP --health-checks=acme-hc --port-name=http
gcloud compute backend-services add-backend acme-api --global \
  --instance-group=acme-api-mig --instance-group-region=us-central1
gcloud compute url-maps create acme-lb --default-service=acme-api
gcloud compute target-https-proxies create acme-https --url-map=acme-lb \
  --ssl-certificates=acme-cert
gcloud compute forwarding-rules create acme-fr --global \
  --target-https-proxy=acme-https --ports=443
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP handle data encryption?

GCP supports encryption at rest and in transit. It provides key management services like Cloud Key Management Service (KMS) for managing encryption keys and Cloud HSM for hardware security modules.

```text
Encryption layers
  In transit        TLS 1.2+ on every API; IPsec for VPN; ALTS inside Google infra
  At rest default   AES-256 with Google-managed keys (no action required)
  CMEK              your Cloud KMS key encrypts the data; you control rotation/revocation
  CSEK              customer-supplied keys for GCS; you own key availability
  Confidential VM   in-use memory encryption for regulated compute
```

```bash
# Create a key ring + key and use it as CMEK for a BigQuery dataset
gcloud kms keyrings create acme-bq --location=us-central1
gcloud kms keys create curated --location=us-central1 --keyring=acme-bq \
  --purpose=encryption --rotation-period=90d --next-rotation-time=2027-01-01T00:00:00Z

bq mk --dataset --default_kms_key=projects/acme-data-prod/locations/us-central1/keyRings/acme-bq/cryptoKeys/curated \
  acme-data-prod:curated_encrypted
```

Trade-off: CMEK is required by many compliance programs but adds a hard dependency — revoking the key makes the data unreadable, so key access is a production-critical permission.

[Table of Contents](#Google-Cloud-Platform)

## What is Memorystore in GCP?

Memorystore is a fully managed in-memory data store service provided by GCP. It supports Redis, offering high-performance caching for applications.

```bash
# Redis for a dashboard/API cache with HA and eviction policy
gcloud redis instances create acme-cache \
  --size=5 --region=us-central1 --redis-version=redis_7_0 \
  --tier=STANDARD_HA --enable-auth
```

Use Memorystore for caching normalized lookups, session state, and rate-limit counters. Do not use it as a system of record (no durable storage beyond replication) and do not use it as a queue for critical data unless you understand its delivery semantics.

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud CDN (Content Delivery Network) in GCP

Cloud CDN is a global content delivery network that caches and delivers content from GCP to users with low latency and high bandwidth. It improves the performance of web applications and reduces serving costs.

For data platforms, Cloud CDN is mostly relevant for serving static assets, exported reports, and public datasets from a GCS-backed backend bucket.

```bash
# GCS backend bucket behind Cloud CDN with a 1-hour default TTL
gcloud compute backend-buckets create acme-reports \
  --gcs-bucket-name=acme-reports-public --enable-cdn --cache-mode=CACHE_ALL_STATIC
gcloud compute backend-buckets update acme-reports \
  --default-ttl=3600 --client-ttl=300
```

Cost note: cache egress is cheaper than origin egress, but a low hit rate just adds a hop; set `Cache-Control` on the objects or the CDN will cache conservatively.

[Table of Contents](#Google-Cloud-Platform)

## How can you monitor and analyze GCP costs?

GCP provides tools like Cloud Billing, Cost Management, and budgets to monitor, analyze, and optimize costs associated with your GCP resources and services.

```bash
# Budget with alerts at 50/80/100% of a monthly threshold
gcloud billing budgets create --billing-account=0X0X0X-0X0X0X-0X0X0X \
  --display-name="Data platform monthly" --budget-amount=50000USD \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.8 --threshold-rule=percent=1.0
```

```sql
-- BigQuery cost by label/team from the audit logs / INFORMATION_SCHEMA
SELECT
  REGEXP_EXTRACT(job_id, r'^([^.]+)') AS team,
  ROUND(SUM(total_bytes_billed) / POW(1024, 4), 2) AS tb_billed,
  ROUND(SUM(total_bytes_billed) / POW(1024, 4) * 6.25, 2) AS usd,
  COUNT(*) AS queries
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), DAY)
GROUP BY team
ORDER BY usd DESC
LIMIT 20;
```

The biggest BigQuery levers: partition filters, clustering, `SELECT` only needed columns, materialized views for repeated aggregations, and switching stable heavy dashboards to flat-rate slots with reservations.

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud AutoML in GCP

Cloud AutoML is a suite of machine learning products in GCP that allows you to train custom machine learning models with minimal coding. It supports vision, natural language, and tabular data.

AutoML now lives inside Vertex AI (AutoML tabular, image, text, video). For data engineering, the interesting case is tabular AutoML on BigQuery data, which removes feature-engineering boilerplate for baseline models.

```python
# Vertex AI AutoML tabular training job from a BigQuery table
from google.cloud import aiplatform

aiplatform.init(project="acme-data-prod", location="us-central1")
job = aiplatform.AutoMLTabularTrainingJob(
    display_name="churn-automl",
    optimization_prediction_type="classification",
    optimization_objective="maximize-au-prc",
)
model = job.run(
    dataset=aiplatform.TabularDataset("projects/acme-data-prod/locations/us-central1/datasets/123"),
    target_column="churned",
    training_fraction_split=0.8,
    validation_fraction_split=0.1,
    test_fraction_split=0.1,
    budget_milli_node_hours=1000,
)
print(model.resource_name)
```

Trade-off: AutoML is fast to a baseline but opaque and more expensive per prediction than a simple model; use it to benchmark, then decide whether a custom model is worth the engineering.

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Deployment Manager in GCP?

Cloud Deployment Manager is an infrastructure deployment service in GCP. It allows you to define and manage resources as code, making it easier to create and maintain infrastructure configurations.

Deployment Manager was GCP's first IaC tool; today Terraform (or Pulumi) is the mainstream choice, and Deployment Manager is effectively legacy. Config Connector brings the same idea to Kubernetes.

```hcl
# The modern equivalent: Terraform manages the same resources with state and plan
resource "google_bigquery_dataset" "marts" {
  dataset_id = "marts"
  location   = "US"
  labels     = { env = "prod", owner = "analytics" }
}

resource "google_bigquery_table" "orders_daily" {
  dataset_id          = google_bigquery_dataset.marts.dataset_id
  table_id            = "orders_daily"
  deletion_protection = false
  time_partitioning { type = "DAY" }
  clustering          = ["country"]
  schema = jsonencode([
    { name = "order_date", type = "DATE", mode = "REQUIRED" },
    { name = "country", type = "STRING", mode = "REQUIRED" },
    { name = "revenue", type = "NUMERIC", mode = "NULLABLE" }
  ])
}
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP ensure compliance and data privacy?

GCP complies with various industry standards and regulations. It offers features like data location controls, access transparency, and compliance certifications to meet data privacy and compliance requirements.

```text
Controls that matter in a review
  Data residency    dataset/bucket location restrictions; Assured Workloads for regulated regions
  Access control    IAM + VPC Service Controls + Access Transparency/Approval logs
  Data protection   CMEK/CSEK, DLP API for classification and de-identification, retention policies
  Audit             Cloud Audit Logs (admin, data access), export to a locked log bucket
  Compliance        SOC 2/ISO 27001/PCI/HIPAA/GDPR certifications and BAAs
```

```bash
# DLP: find and de-identify PII before it lands in an analytics dataset
gcloud dlp jobs create --project=acme-data-prod \
  --inspect-job '{"inspect_config":{"info_types":[{"name":"EMAIL_ADDRESS"},{"name":"CREDIT_CARD_NUMBER"}]},
                  "storage_config":{"big_query_options":{"table_reference":{"project_id":"acme-data-prod","dataset_id":"raw","table_id":"customers"}}}}'
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Machine Learning Engine in GCP

Cloud Machine Learning Engine is a managed service that allows you to train, deploy, and serve machine learning models at scale. It integrates with other GCP services like BigQuery and Cloud Storage.

Concretely, ML Engine is now Vertex AI Training and Prediction. A data engineer's job is usually the plumbing: export features from BigQuery to GCS, trigger a training job on a schedule, and publish the resulting predictions back to BigQuery.

```python
# Custom training job on Vertex AI driven from a warehouse feature table
from google.cloud import aiplatform

aiplatform.init(project="acme-data-prod", location="us-central1", staging_bucket="gs://acme-ml-staging")
job = aiplatform.CustomTrainingJob(
    display_name="churn-train",
    script_path="trainer/task.py",
    container_uri="us-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-3:latest",
    requirements=["scikit-learn==1.3.0", "pandas"],
)
job.run(
    replica_count=1,
    machine_type="n1-standard-8",
    args=["--project=acme-data-prod", "--train_table=ml.churn_train", "--model_dir=gs://acme-ml/models/churn"],
)
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Monitoring in GCP?

Cloud Monitoring is a monitoring and observability service provided by GCP. It allows you to collect and analyze metrics, create dashboards, set up alerts, and visualize the health and performance of your resources.

For data platforms, the metrics that matter are pipeline freshness, Dataflow system lag, Pub/Sub oldest unacked message age, BigQuery slot utilization, Composer task failures, and GCS request latency / 5xx rate.

```bash
# Custom metric from a log filter + an alerting policy on it
gcloud logging metrics create pipeline_dq_failures \
  --log-filter='jsonPayload.event="dq_failed"'
gcloud monitoring policies create --policy-from-file=policy.json
cat policy.json
{
  "displayName": "DQ failures",
  "conditions": [{
    "displayName": "dq_failed > 0 in 15m",
    "conditionThreshold": {
      "filter": "metric.type=\"logging.googleapis.com/user/pipeline_dq_failures\"",
      "comparison": "COMPARISON_GT", "thresholdValue": 0,
      "duration": "900s",
      "aggregations": [{"alignmentPeriod": "300s", "perSeriesAligner": "ALIGN_SUM"}]
    }
  }],
  "combiner": "OR"
}
```

[Table of Contents](#Google-Cloud-Platform)

## How can you optimize data ingestion in GCP?

GCP provides services like Cloud Pub/Sub and Cloud Dataflow for efficient and scalable data ingestion. You can also optimize ingestion by using partitioning, batching, and compression techniques.

```text
Ingestion levers
  Batch size       larger Pub/Sub batches (up to 1000 msgs / 10 MB) cut per-message overhead
  File layout      target 128-512 MB Parquet/Avro files; compact small files
  Streaming API    BigQuery Storage Write API with exactly-once for high volume
  Partitioning     land into dt=/hour= paths so downstream scans prune
  Backpressure     Pub/Sub flow control + Dataflow autoscaling to protect sinks
  Dedup            idempotent keys at the sink; do not rely on transport exactly-once
```

```python
import json
# Storage Write API: high-throughput load with exactly-once semantics
import apache_beam as beam
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

with beam.Pipeline() as p:
    (
        p
        | beam.io.ReadFromPubSub(topic="projects/acme/topics/orders")
        | beam.Map(lambda b: json.loads(b.decode("utf-8")))
        | WriteToBigQuery(
            "acme:curated.orders_raw",
            schema="AUTO",
            write_disposition=BigQueryDisposition.WRITE_APPEND,
            method=WriteToBigQuery.Method.STORAGE_WRITE_API,
        )
    )
```

[Table of Contents](#Google-Cloud-Platform)

## What is Cloud Memorystore for Redis in GCP?

Cloud Memorystore for Redis is a fully-managed in-memory data store service provided by GCP. It offers high-performance, scalable Redis instances for caching and data storage.

Memorystore for Redis comes in Basic (no SLA), Standard (HA with automatic failover), and Cluster tiers. It is VPC-only and does not expose a public endpoint. Use cases in data platforms: dashboard result caches, lookup/translation tables, dedupe sets for streaming, and rate limiting.

```python
# Dedupe recent event IDs with Redis SET NX + TTL (bounded memory)
import redis

r = redis.Redis(host="10.10.0.3", port=6379, password="...", decode_responses=True)

def first_seen(event_id: str, ttl_seconds: int = 3600) -> bool:
    """True if this event has not been seen within the TTL window."""
    return bool(r.set(f"evt:{event_id}", "1", nx=True, ex=ttl_seconds))
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Datalab in GCP

Cloud Datalab is an interactive data exploration and visualization tool in GCP. It provides a Jupyter notebook interface for analyzing and visualizing data using Python, SQL, and BigQuery.

Datalab was retired in favor of Vertex AI Workbench (managed JupyterLab) and Colab Enterprise. The pattern is unchanged: a notebook instance with a service account, BigQuery and GCS client libraries preinstalled, scheduled notebooks for recurring jobs, and Git-backed notebooks for review.

```bash
# Current equivalent: a Vertex AI Workbench instance next to the data
gcloud workbench instances create acme-notebooks \
  --location=us-central1-a \
  --vm-image-project=cloud-notebooks-managed \
  --vm-image-family=workbench-instances
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud DNS in GCP?

Cloud DNS is a scalable and reliable domain name system (DNS) service provided by GCP. It allows you to manage and resolve domain names to IP addresses.

For data platforms, Cloud DNS matters for private zones (resolving Cloud SQL/Spanner/Memorystore names inside a VPC without public DNS) and for failover routing between regional endpoints.

```bash
# Private zone so services resolve internally
gcloud dns managed-zones create acme-internal \
  --dns-name=acme.internal. --visibility=private --networks=acme-vpc

gcloud dns record-sets create db.acme.internal. --zone=acme-internal \
  --type=A --ttl=300 --rrdatas=10.10.0.5
```

[Table of Contents](#Google-Cloud-Platform)

## How can you ensure data integrity in GCP?

GCP provides various mechanisms for ensuring data integrity, including checksums, encryption, redundancy, and regular backups.

```text
Integrity controls at each stage
  In transit        TLS; Pub/Sub message IDs; idempotent consumers
  At rest           GCS crc32c/md5 per object; BigQuery checksums on export
  Schema            Avro/Protobuf contracts + schema registry or BigQuery schema enforcement
  Semantic          DQ tests (uniqueness, not-null, referential, range) before publishing
  Historical        Object versioning, snapshots, time travel (BigQuery 7 days), audit logs
```

```sql
-- BigQuery: gate a gold table on DQ checks; the pipeline fails if any check returns rows
WITH checks AS (
  SELECT 'dup_order_id' AS check_name, COUNT(*) AS violations
  FROM (SELECT order_id FROM curated.orders GROUP BY order_id HAVING COUNT(*) > 1)
  UNION ALL
  SELECT 'null_customer', COUNT(*) FROM curated.orders WHERE customer_id IS NULL
  UNION ALL
  SELECT 'negative_amount', COUNT(*) FROM curated.orders WHERE amount < 0
)
SELECT * FROM checks WHERE violations > 0;
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Security Command Center in GCP

Cloud Security Command Center is a security and risk management service provided by GCP. It helps you discover, monitor, and manage security vulnerabilities and threats across your GCP resources.

SCC (now Security Command Center, with a Premium tier) aggregates findings: publicly exposed buckets, unused service-account keys, open firewall rules, and misconfigured IAM. For data platforms, wire its Pub/Sub notifications into your alerting so a newly public bucket pages someone.

```bash
# Export SCC findings to Pub/Sub, then to BigQuery for trend analysis
gcloud scc notifications create acme-scc-findings \
  --organization=123456789 --pubsub-topic=projects/acme-data-prod/topics/scc-findings \
  --filter='state="ACTIVE" AND category="PUBLIC_BUCKET_ACL"'
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud SQL Proxy in GCP?

Cloud SQL Proxy is a secure client-side proxy for connecting to Cloud SQL instances from external applications or local development environments without exposing the database to the internet.

The proxy authenticates with IAM, encrypts the connection, and connects over the Cloud SQL API. In production on GCP, prefer the built-in Cloud SQL connectors (`cloud-sql-python-connector`) over running a separate proxy process.

```bash
# Local development through the proxy (no public IP on the instance)
cloud-sql-proxy --port 5432 acme-data-prod:us-central1:acme-pg &
psql "host=127.0.0.1 port=5432 dbname=orders user=etl"

# In Cloud Run / GKE, the connector handles IAM auth without a sidecar process.
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Run in GCP

Cloud Run is a fully managed serverless execution environment in GCP. It allows you to run containers without worrying about infrastructure provisioning or scaling.

Cloud Run is the right home for small data jobs that do not justify a Beam pipeline: file-triggered transforms, API extractors, dbt runs, and webhook receivers. It scales to zero and can be triggered by Pub/Sub, Eventarc, or Cloud Scheduler.

```bash
# Deploy a containerized loader triggered by a GCS object finalize event
gcloud run deploy orders-loader \
  --image=us-docker.pkg.dev/acme-data-prod/jobs/orders-loader:1.4.0 \
  --region=us-central1 --memory=2Gi --cpu=2 --timeout=1800 \
  --no-allow-unauthenticated \
  --service-account=orders-loader@acme-data-prod.iam.gserviceaccount.com

gcloud eventarc triggers create orders-loader-trigger \
  --location=us-central1 --destination-run-service=orders-loader \
  --destination-run-region=us-central1 \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=acme-raw-prod" \
  --service-account=orders-loader@acme-data-prod.iam.gserviceaccount.com
```

Trade-off: Cloud Run is excellent for bursty, short jobs; for long-running shuffle-heavy processing use Dataflow or Dataproc Serverless instead, because Cloud Run has request timeouts and no shuffle service.

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Security Scanner in GCP?

Cloud Security Scanner is a web application vulnerability scanning service provided by GCP. It helps you identify security vulnerabilities in your web applications by crawling your website.

It is now Web Security Scanner inside Security Command Center. For data platforms it is mostly used to scan internal dashboards and API gateways exposed to users; the higher-value control is a properly scoped VPC Service Controls perimeter and least-privilege IAM.

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Composer in GCP?

Cloud Composer is a fully managed workflow orchestration service based on Apache Airflow. It allows you to create, schedule, and monitor complex data pipelines and ETL workflows.

```text
Use Composer for:                      Do not use Composer for:
  cross-system dependency graphs         per-second latency (use Dataflow/Flink)
  sensors waiting on files/partitions    single SQL transform (use a scheduled query)
  backfills with retries                 heavy in-task computation (push to a service)
  alerting on missed SLAs                high-frequency (> per-minute) triggers
```

```python
# Composer 3 / Airflow 3 style DAG using a deferrable sensor (cheap waiting)
from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

with DAG("daily_orders", schedule="0 3 * * *", start_date=datetime(2026, 1, 1),
         catchup=True, max_active_runs=1) as dag:
    wait = GCSObjectExistenceSensor(
        task_id="wait_raw", bucket="acme-raw-prod",
        object="orders/dt={{ ds }}/_SUCCESS", deferrable=True, poke_interval=60, timeout=7200)
    build = BigQueryInsertJobOperator(
        task_id="build_mart",
        configuration={"query": {"query": "{% include 'sql/orders_daily.sql' %}",
                                 "useLegacySql": False,
                                 "destinationTable": {"projectId": "acme-data-prod",
                                                      "datasetId": "marts",
                                                      "tableId": "orders_daily${{ ds_nodash }}"}}})
    wait >> build
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP handle data archiving and long-term storage?

GCP offers services like Cloud Storage Coldline and Archive for long-term data storage, providing cost-effective options for archiving data with high durability and availability.

```bash
# Lifecycle: Standard -> Nearline -> Coldline -> Archive -> delete
gcloud storage buckets update gs://acme-raw-prod --lifecycle-file=lifecycle.json
cat lifecycle.json
{
  "rule": [
    {"action": {"type": "SetStorageClass", "storageClass": "NEARLINE"}, "condition": {"age": 30, "matchesPrefix": ["orders/"]}},
    {"action": {"type": "SetStorageClass", "storageClass": "COLDLINE"}, "condition": {"age": 120, "matchesPrefix": ["orders/"]}},
    {"action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"}, "condition": {"age": 365, "matchesPrefix": ["orders/"]}},
    {"action": {"type": "Delete"}, "condition": {"age": 2555, "matchesPrefix": ["orders/"]}}
  ]
}
```

Cost context: Archive is roughly a tenth of Standard per GB per month, but retrieval has a minimum storage duration (365 days) and higher access cost, so archive only data you genuinely will not re-read. Publishing on top of Archive-class objects is a common accidental egress bill.

[Table of Contents](#Google-Cloud-Platform)

## How can you manage data access and permissions in GCP?

GCP provides Cloud Identity and Access Management (IAM) for managing access control and permissions to GCP resources. IAM allows you to define fine-grained access policies and grant access to specific users or groups.

```text
Access model
  Humans    groups from Cloud Identity / Workspace, never individual emails
  Workloads service accounts + Workload Identity Federation (no downloaded keys)
  Data      BigQuery dataset/table IAM, GCS bucket/object IAM, row-level security
  Perimeter VPC Service Controls so data cannot leave the project boundary
  Audit     data access logs (must be enabled explicitly) -> locked log bucket
```

```sql
-- BigQuery row-level security + column-level policy tags
CREATE ROW ACCESS POLICY region_filter
ON curated.orders
GRANT TO ('group:analysts-eu@acme.com')
FILTER USING (country IN ('DE', 'FR', 'ES'));

-- Column-level: PII column tagged with a policy tag that only a group can read
ALTER TABLE curated.customers
ALTER COLUMN email SET OPTIONS (policy_tags = 'projects/acme-data-prod/locations/us/taxonomies/1/policyTags/2');
```

[Table of Contents](#Google-Cloud-Platform)

## How can you optimize data processing in GCP?

GCP offers optimization techniques like data partitioning, distributed processing, caching, and using appropriate data storage and processing services to achieve efficient and scalable data processing.

```text
Optimization checklist
  Storage     columnar Parquet/Avro, 128-512 MB files, partition on filter columns, cluster on the next
  BigQuery    partition pruning, avoid SELECT *, avoid ORDER BY without LIMIT, materialized views
  Dataflow    autoscaling, Streaming Engine, right-sized workers, combiner instead of group-by-lists
  Dataproc    ephemeral clusters, spot workers for shuffle, right-size shuffle partitions
  Orchestration deferrable sensors, avoid XCom for payloads, task-level retries
  Compute     prefer SQL over Spark when the data already lives in BigQuery
```

```sql
-- Materialized view removes repeated expensive aggregation from dashboards
CREATE MATERIALIZED VIEW marts.orders_by_country_mv
PARTITION BY order_date
CLUSTER BY country
AS
SELECT DATE(order_ts) AS order_date, country, SUM(amount) AS revenue, COUNT(*) AS orders
FROM curated.orders
GROUP BY order_date, country;
```

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud NAT in GCP?

Cloud NAT is a service in GCP that allows your virtual machine instances to send outbound traffic to the internet without exposing their IP addresses. It provides network address translation capabilities.

Use it for private GKE nodes or Dataflow/Dataproc workers that need to reach external APIs (SaaS sources, package repositories) without public IPs. It is not a load balancer and not for inbound traffic.

```bash
gcloud compute routers create acme-router --network=acme-vpc --region=us-central1
gcloud compute routers nats create acme-nat \
  --router=acme-router --region=us-central1 \
  --nat-all-subnet-ip-ranges --auto-allocate-nat-external-ips \
  --min-ports-per-vm=128 --log-filter=ALL
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud IoT Core in GCP

Cloud IoT Core is a fully managed service in GCP for securely connecting, managing, and ingesting data from IoT devices at scale. It provides device management, data ingestion, and integration with other GCP services.

Cloud IoT Core was retired on 15 August 2023. The current pattern is a partner or self-managed MQTT broker (HiveMQ, EMQX, or Mosquitto on GKE) that publishes into Pub/Sub, then Dataflow processes and BigQuery stores. Mentioning the retirement and the migration path is a strong interview signal.

```text
Retired:  device -> Cloud IoT Core (MQTT/HTTP bridge) -> Pub/Sub
Today:    device -> MQTT broker (GKE/HiveMQ) -> Pub/Sub -> Dataflow -> BigQuery
          device -> Pub/Sub directly over HTTPS/gRPC (for low-rate devices)
```

[Table of Contents](#Google-Cloud-Platform)

## How does GCP handle data replication and synchronization?

GCP offers data replication and synchronization capabilities through services like Cloud Storage, Cloud Datastore, Cloud Spanner, and database-specific replication features.

```text
Replication mechanisms
  GCS              regional/multi-region/dual-region; turbo replication for fast RPO
  Cloud SQL        read replicas (async) and HA failover replica (sync, same region)
  Spanner          multi-region synchronous replication with automatic failover
  BigQuery         managed storage replication; dataset copies/transfer for DR
  Cross-cloud/DB   Datastream CDC, Database Migration Service, Storage Transfer Service
```

```bash
# Cloud SQL cross-region read replica for analytics offload
gcloud sql instances create acme-pg-replica \
  --master-instance-name=acme-pg --region=us-east1 --tier=db-custom-4-16384

# GCS dual-region bucket with turbo replication (RPO near zero)
gcloud storage buckets create gs://acme-critical-prod \
  --location=us-central1 --placement=us-east1 --rpo=ASYNC_TURBO
```

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud VPN in GCP

Cloud VPN is a service in GCP that provides a secure and encrypted connection between your on-premises network and GCP Virtual Private Cloud (VPC) network.

```text
Cloud VPN variants
  HA VPN       99.99% SLA, two interfaces, BGP; the default for production
  Classic VPN  legacy, 99.9%, static routing; migrate away
  Throughput   ~1.5-3 Gbps per tunnel, summed across tunnels; more tunnels for bandwidth
```

For sustained multi-Gbps or latency-sensitive replication, Dedicated Interconnect (10/100 Gbps, private) is the correct choice, with VPN as a backup path and BGP route preferences controlling failover.

[Table of Contents](#Google-Cloud-Platform)

## What is the purpose of Cloud Functions in GCP?

Cloud Functions is a serverless compute service in GCP that allows you to run event-driven code in response to events from various GCP services or HTTP requests.

```bash
# 2nd gen function reacting to a GCS object finalize event
gcloud functions deploy validate-orders \
  --gen2 --runtime=python312 --region=us-central1 \
  --source=./validate_orders \
  --entry-point=validate --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=acme-raw-prod" \
  --memory=512MB --timeout=300 \
  --service-account=validator@acme-data-prod.iam.gserviceaccount.com
```

```python
# validate_orders/main.py: reject a malformed file before it reaches the warehouse
import functions_framework
from google.cloud import storage

@functions_framework.cloud_event
def validate(cloud_event):
    data = cloud_event.data
    bucket, name = data["bucket"], data["name"]
    if not name.endswith(".parquet"):
        raise ValueError(f"unexpected object {name}")
    blob = storage.Client().bucket(bucket).blob(name)
    print(f"validated gs://{bucket}/{name} size={blob.size} crc32c={blob.crc32c}")
```

Trade-off: Functions have a 60-minute maximum (2nd gen) and limited CPU/memory; for multi-hour transforms use Cloud Run jobs or Dataflow.

[Table of Contents](#Google-Cloud-Platform)

## How can you monitor and troubleshoot performance issues in GCP?

GCP provides monitoring tools like Cloud Monitoring and logging tools like Cloud Logging and Stackdriver, which allow you to monitor and troubleshoot performance issues by collecting and analyzing metrics, logs, and traces.

```bash
# Triage a slumping BigQuery dashboard: find the slowest queries first
bq query --use_legacy_sql=false '
SELECT
  REGEXP_EXTRACT(query, r"(?i)FROM\s+`?([\w.-]+)") AS source_table,
  ROUND(AVG(total_slot_ms) / 1000, 1)        AS avg_slot_s,
  ROUND(SUM(total_bytes_billed)/POW(1024,3), 1) AS gb_billed,
  COUNT(*)                                   AS runs
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND job_type = "QUERY" AND state = "DONE"
GROUP BY source_table
ORDER BY avg_slot_s DESC
LIMIT 20;'
```

For Dataflow, check system lag, worker CPU, and shuffle; for Dataproc, check YARN pending memory and shuffle spill; for Composer, check scheduler heartbeat and task queue duration. Cloud Trace is the tool for end-to-end latency across an API calling BigQuery.

[Table of Contents](#Google-Cloud-Platform)

## Explain the use of Cloud Key Management Service (KMS) in GCP

Cloud KMS is a managed service in GCP for generating, using, and managing encryption keys. It helps you encrypt data and control access to sensitive information.

```text
KMS primitives
  Key ring / key     regional or global container and key material
  Rotation           automatic schedule; old versions retained for decryption
  IAM                roles/cloudkms.cryptoKeyEncrypterDecrypter is the usual service grant
  Cloud HSM          FIPS 140-2 Level 3 keys; higher cost, same API
  External key mgr   EKM keeps key material outside Google
```

```bash
# Envelope encryption of a small secret with a KMS key
gcloud kms encrypt --location=us-central1 --keyring=acme-bq --key=curated \
  --plaintext-file=secret.txt --ciphertext-file=secret.enc

# Use the same key as CMEK for a GCS bucket
gcloud storage buckets update gs://acme-curated-prod \
  --default-encryption-key=projects/acme-data-prod/locations/us-central1/keyRings/acme-bq/cryptoKeys/curated
```

Disaster-recovery note: a lost or deleted KMS key means permanent data loss, so key projects need strict IAM, soft-delete protection, and a documented recovery owner.

[Table of Contents](#Google-Cloud-Platform)

## Real world use cases for GCP

### 1. Retail demand forecasting on BigQuery and Vertex AI

Business context: a 900-store retailer forecasts SKU demand weekly across 250,000 SKU-store combinations; planners need a forecast by Monday 06:00 and the pipeline must handle Black Friday spikes. Volume: 1.2B sales rows/year, 380 GB in BigQuery, 40M rows/day during peak.

```text
POS + e-commerce -> Pub/Sub / batch to GCS -> Dataflow -> BigQuery curated
   -> dbt/BigQuery SQL features -> Vertex AI AutoML forecasting
   -> predictions back to BigQuery -> Looker/Tableau demand dashboard
```

```sql
-- Feature mart partitioned by week and clustered by store/SKU for the model export
CREATE OR REPLACE TABLE ml.demand_features
PARTITION BY week_start
CLUSTER BY store_id, sku_id AS
SELECT
  DATE_TRUNC(sale_date, WEEK) AS week_start,
  store_id, sku_id,
  SUM(units)                        AS units_7d,
  AVG(units)                        AS units_avg_28d,
  SUM(promo_flag)                   AS promo_days,
  MAX(temperature_c)                AS max_temp,
  EXTRACT(ISOWEEK FROM sale_date)   AS iso_week
FROM curated.sales
WHERE sale_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 730 DAY)
GROUP BY 1, 2, 3, 7;
```

Why this design: BigQuery holds the full history cheaply, partitioning by week keeps both training exports and planner queries to a bounded scan, and Vertex AI forecasting consumes the feature table directly, so there is one governed definition of demand instead of duplicated logic in the BI layer.

### 2. Fintech ledger with Datastream CDC and near-real-time balances

Business context: a payments company needs a near-current merchant balance and a fully auditable ledger for regulators. Volume: 25M transactions/day (~2,000/s peak), 5 KB/event, 7-year retention.

```text
Cloud SQL (Postgres) -> Datastream CDC -> GCS landing + Pub/Sub stream
   -> Dataflow: dedupe by (txn_id, lsn), window 1 min -> BigQuery ledger_current
   -> nightly reconciliation job -> BigQuery ledger_archive (7-year, partitioned)
   -> Compliance dashboard: live connection with row-level security by region
```

```sql
-- Idempotent near-real-time merge keyed on the CDC log position
MERGE curated.ledger_current AS t
USING (
  SELECT txn_id, account_id, amount, currency, txn_ts, lsn
  FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY txn_id ORDER BY lsn DESC) AS rn
    FROM staging.ledger_changes
    WHERE DATE(ingest_ts) = CURRENT_DATE()
  ) WHERE rn = 1
) AS s
ON t.txn_id = s.txn_id AND s.lsn >= t.lsn
WHEN MATCHED AND s.lsn > t.lsn THEN UPDATE SET
  t.amount = s.amount, t.lsn = s.lsn, t.txn_ts = s.txn_ts
WHEN NOT MATCHED THEN INSERT (txn_id, account_id, amount, currency, txn_ts, lsn)
VALUES (s.txn_id, s.account_id, s.amount, s.currency, s.txn_ts, s.lsn);
```

Why this design: Datastream captures deletes and updates that timestamp polling would miss, the `lsn` version makes replays safe, and separating the current-state table (small, hot) from the immutable archive (large, cold) keeps the compliance query affordable for seven years.

### 3. Streaming IoT telemetry for fleet operations

Business context: a logistics operator monitors 18,000 vehicles; operations needs alerts within 30 seconds for engine faults, and data science needs historical telemetry for predictive maintenance. Volume: 18,000 devices x 1 message/10s = 1,800 msg/s, ~4 TB/month raw.

```text
vehicle gateway -> MQTT broker on GKE -> Pub/Sub (key = vehicle_id)
   -> Dataflow streaming: 30s windows, threshold + moving-average anomaly
        -> BigQuery alerts_30s (ops dashboard, live)
        -> GCS raw Parquet (archive)
   -> hourly batch (Dataproc) -> BigQuery telemetry_1m (features + training)
```

```python
# Streaming anomaly detection with per-key state via a sliding window
import json

import apache_beam as beam
from apache_beam.transforms.window import SlidingWindows
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime
from apache_beam.transforms.combiners import MeanCombineFn

FAULT_TEMP = 105.0

with beam.Pipeline() as p:
    (
        p
        | beam.io.ReadFromPubSub(topic="projects/acme/topics/vehicle-telemetry")
        | beam.Map(lambda b: json.loads(b.decode("utf-8")))
        | beam.Map(lambda e: (e["vehicle_id"], e["engine_temp_c"]))
        | beam.WindowInto(SlidingWindows(60, 10),
                          trigger=AfterWatermark(late=AfterProcessingTime(30)),
                          accumulation_mode=AccumulationMode.DISCARDING)
        | beam.CombinePerKey(MeanCombineFn())
        | beam.Filter(lambda kv: kv[1] >= FAULT_TEMP)
        | beam.io.WriteToBigQuery("acme:gold.engine_faults",
                                  schema="vehicle_id:STRING,mean_temp:FLOAT",
                                  write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
    )
```

Why this design: a sliding 60-second window smooths sensor noise so a single spike does not page a mechanic, updating the same code with `--streaming` keeps one pipeline for cloud and on-prem testing, and the heavy feature engineering runs hourly on Parquet where scan cost is low.

### 4. Multi-tenant SaaS product analytics with VPC Service Controls

Business context: a B2B SaaS product serves 1,100 tenants; each tenant's admins see only their usage data, and the platform team needs cross-tenant health metrics. Volume: 2.5B events/month, 60 TB in the lakehouse, 400 concurrent dashboard users.

```text
tenant SDKs -> Pub/Sub -> Dataflow -> BigQuery raw.events (tenant_id in key)
   -> scheduled SQL -> curated.tenant_usage_daily
   -> Looker/embedded dashboards with row-level security on tenant_id
   -> VPC Service Controls perimeter around the project for exfiltration control
```

```sql
CREATE ROW ACCESS POLICY tenant_isolation
ON curated.tenant_usage_daily
GRANT TO ('group:tenant-admins@acme.com')
FILTER USING (tenant_id = SESSION_USER());

-- Cross-tenant health for the platform team uses a separate authorized view
CREATE OR REPLACE VIEW platform.tenant_health AS
SELECT tenant_id, usage_date, active_users, events,
       active_users / NULLIF(licensed_seats, 0) AS seat_utilization
FROM curated.tenant_usage_daily;
```

Why this design: `tenant_id` in the partition and cluster keys keeps every tenant query to its own slice, row-level security means the dashboard never has to trust the application to filter, and the VPC Service Controls perimeter makes bulk exfiltration of the tenant tables detectable and blocked.

### 5. Marketing attribution pipeline with Dataproc Serverless

Business context: a D2C brand blends six ad platforms, web clickstream, and CRM data to compute CAC and ROAS daily; the existing Spark jobs came from an on-prem Hadoop cluster. Volume: 90M impressions/day, 14M sessions/day, 220K orders/day, 12 TB/month in GCS.

```text
ad APIs -> GCS landing (Avro) ---\
web/app clickstream -> Pub/Sub -> GCS --\
CRM CDC -> Datastream -> GCS ------------> Dataproc Serverless (PySpark)
   -> BigQuery session_attribution + channel_cac_daily
   -> Tableau marketing dashboard
```

```python
# Dataproc Serverless: migrate the existing Spark logic without managing a cluster
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("attribution").getOrCreate()

spend = spark.read.format("avro").load("gs://acme-landing/ad_spend/")
sessions = spark.read.parquet("gs://acme-curated/sessions/")
conversions = spark.read.parquet("gs://acme-curated/conversions/")

attribution = (
    sessions.alias("s")
    .join(conversions.alias("c"), F.col("s.user_id") == F.col("c.user_id"))
    .where(F.col("s.session_ts").between(F.col("c.conversion_ts") - F.expr("INTERVAL 30 DAYS"),
                                         F.col("c.conversion_ts")))
    .withColumn("rn", F.row_number().over(
        F.Window.partitionBy("c.conversion_id").orderBy(F.col("s.session_ts").desc())))
    .where(F.col("rn") == 1)
    .groupBy(F.to_date("c.conversion_ts").alias("ds"), "s.channel")
    .agg(F.countDistinct("c.conversion_id").alias("conversions"), F.sum("c.revenue").alias("revenue"))
)

attribution.write.mode("overwrite").format("bigquery").save("acme-data-prod:marts.channel_attribution")
```

```bash
# Submit without a cluster; Dataproc Serverless sizes the batch automatically
gcloud dataproc batches submit pyspark gs://acme-code/attribution.py \
  --region=us-central1 --deps-bucket=gs://acme-code/deps \
  --service-account=dataproc-runner@acme-data-prod.iam.gserviceaccount.com \
  --properties=spark.executor.cores=4,spark.executor.instances=20
```

Why this design: the team keeps its Spark code and libraries (no Beam rewrite), Dataproc Serverless removes the idle-cluster cost of the old on-prem model, and BigQuery becomes the serving layer for the marketing dashboard so attribution logic lives in one place rather than in every workbook.

[Table of Contents](#Google-Cloud-Platform)
