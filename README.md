<h1 align="center">More than 2000+ questions for preparing a Data Engineer interview.</h1>
<h2 align="center"><a href="./content/full.md">Full list of questions</a></h2>
<p align="center">Pick a topic below or use the full list to practice end-to-end.</p>

## How to use this repo

Use this repository as a practical interview workbook, not just a memorization list. A strong data engineering interview answer usually has four parts:

1. Define the concept clearly.
2. Explain when you would use it in a real system.
3. Name the trade-offs and failure modes.
4. Show a small example in SQL, Python, Spark, or cloud architecture.

Suggested study paths:

+ **Core pipeline path:** [Python](./content/python.md) -> [SQL](./content/sql.md) -> [PySpark](./content/spark.md) -> [Spark Tuning](./content/spark-tuning.md) -> [Airflow](./content/airflow.md) -> [Data Quality](./content/data-quality.md)
+ **Lakehouse path:** [Parquet](./content/parquet.md) -> [Delta](./content/delta.md) / [Iceberg](./content/iceberg.md) / [Hudi](./content/hudi.md) -> [CDC](./content/cdc.md) -> [Data Modeling](./content/data-modeling.md)
+ **Streaming path:** [Kafka](./content/kafka.md) -> [Flink](./content/flink.md) -> [CDC](./content/cdc.md) -> [Observability](./content/observability.md)
+ **Cloud path:** [AWS](./content/aws.md) / [GCP](./content/gcp.md) / [Azure](./content/azure.md) -> [Cost Optimization](./content/cost-optimization.md) -> [Data Governance](./content/data-governance.md)
+ **Analytics path:** [Data Warehousing](./content/dwha.md) -> [dbt](./content/dbt.md) -> [BigQuery](./content/bigquery.md) / [Redshift](./content/redshift.md) -> [Tableau](./content/tableau.md) / [Looker](./content/looker.md) / [Superset](./content/superset.md)

## Practice notebooks

Prefer learning by running code? The [`notebooks/`](./notebooks/README.md) directory contains runnable Jupyter notebooks that test the same concepts with self-checking assertions and an interview question bank at the end of each one.

| Notebook | What it drills | Dependencies | Run in Colab |
|---|---|---|---|
| [Python basics](./notebooks/01_python_basics.ipynb) | Classes and methods, dunder methods, properties, dataclasses, exceptions, context managers, generators, decorators, typing, concurrency | Standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/01_python_basics.ipynb) |
| [Python coding problems](./notebooks/02_python_coding_problems.ipynb) | Interview coding problems with tests: dedupe, top-K, sliding windows, hash joins, sessionization, LRU cache, retry | Standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/02_python_coding_problems.ipynb) |
| [SQL interview questions](./notebooks/03_sql_interview_questions.ipynb) | Window functions, top-N per group, running totals, gaps and islands, cohorts, dedupe against an in-memory SQLite database | Standard library (`sqlite3`) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/03_sql_interview_questions.ipynb) |
| [PySpark concepts](./notebooks/04_pyspark_concepts.ipynb) | Lazy evaluation, joins and shuffles, window functions, UDFs, partitioning, caching, AQE, streaming | PySpark + Java 17+ (skips gracefully) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/04_pyspark_concepts.ipynb) |
| [Interview question bank](./notebooks/05_interview_questions.ipynb) | Mixed questions across Python, SQL, Spark, modelling, lakehouse, orchestration, streaming, cloud and behavioural | Standard library | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/05_interview_questions.ipynb) |

```bash
make setup-notebooks   # uv sync --extra notebooks
make notebooks         # run every notebook and save outputs
jupyter lab notebooks/ # or open them interactively
```

Prefer zero setup? Click an **Open in Colab** badge to run a notebook in the browser straight from this repository.
The Python and SQL notebooks need nothing installed. The PySpark notebook needs one extra step in Colab: run
`!pip install pyspark` in a new cell, then pick **Runtime -> Restart session** and run all cells.

PySpark locally needs `uv sync --extra notebooks --extra notebooks-spark` plus a Java 17+ runtime; without them, notebook 04 prints setup instructions and skips the Spark cells instead of failing.

## Documentation website

This repo can be served as a MkDocs Material website. The Markdown files under `content/` stay as the source of truth, and `scripts/build_docs_source.py` generates a MkDocs-friendly `.docs_src/` directory.

```bash
uv sync
uv run docs-prepare
uv run mkdocs serve
```

For CI or local validation:

```bash
uv run docs-prepare
uv run mkdocs build --strict
python3 scripts/repo_checks.py
```

To add a new topic later, create a new `content/<topic>.md` file with a top-level `# Topic Name` heading. Then add the topic slug to `TOPIC_GROUPS` in `scripts/build_docs_source.py` so it appears in the right study path on the website.

## Real-world interview examples

### Build a daily orders pipeline

Scenario: an e-commerce company needs a daily revenue table by customer and order date. The source lands JSON files in object storage. The target is a governed Unity Catalog table used by BI dashboards.

```python
from pyspark.sql import functions as F

orders = spark.read.json("s3://company-raw/orders/ds=2026-10-04/")

daily_revenue = (
    orders
    .filter(F.col("status").isin("paid", "shipped"))
    .withColumn("order_date", F.to_date("order_ts"))
    .groupBy("order_date", "customer_id")
    .agg(F.sum("amount").alias("revenue"))
)

spark.sql("create schema if not exists main.gold")

(
    daily_revenue
    .write
    .mode("overwrite")
    .saveAsTable("main.gold.daily_revenue")
)
```

What to discuss in an interview: explicit schemas, corrupt-record handling, idempotent writes, Unity Catalog permissions, small-file compaction, data quality checks, and dashboard freshness SLAs.

### Deduplicate CDC records before a merge

Scenario: a CDC connector can replay records after a retry. You need to keep only the newest change for each primary key before merging into a current-state table.

```sql
with ranked as (
  select
    *,
    row_number() over (
      partition by order_id
      order by source_lsn desc, ingested_at desc
    ) as rn
  from bronze.orders_cdc
)
select *
from ranked
where rn = 1;
```

What to discuss in an interview: ordering by source metadata instead of ingestion time, delete/tombstone handling, idempotent merges, replay safety, and storing raw CDC events for audit.

### Model orders for analytics

Scenario: finance wants revenue by product, customer segment, and day. The clean model is usually a fact table with conformed dimensions.

```text
fact_order_line
main.gold.fact_order_line
  order_id
  order_line_id
  customer_sk
  product_sk
  order_date
  quantity
  gross_amount
  discount_amount

main.gold.dim_customer
  customer_sk
  customer_id
  customer_segment
  effective_start_at
  effective_end_at
  is_current
```

What to discuss in an interview: table grain, SCD Type 2 dimensions, surrogate keys, avoiding double counting, and reconciling warehouse totals to source systems.

### Orchestrate the pipeline safely

Scenario: the pipeline must run every day, retry transient failures, and avoid duplicate writes during backfills.

```python
with DAG(
    dag_id="daily_orders_pipeline",
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
) as dag:
    extract = PythonOperator(task_id="extract_orders", python_callable=extract_orders)
    validate = PythonOperator(task_id="validate_orders", python_callable=validate_orders)
    publish = PythonOperator(task_id="publish_orders", python_callable=publish_orders)

    extract >> validate >> publish
```

What to discuss in an interview: logical dates, backfills, retries, task idempotency, alerting, dependency management, and publishing only after validation.

<h1 align="center">Interview questions for Data Engineer</h1>
<div>
<table>
  <tr>
    <th colspan="5">Databases and Data Warehouses</th>
  </tr>
    <tr>
    <th>GitHub Repo</th>
    <th>Official page</th>
    <th>Questions</th>
    <th>Description</th>
    <th>Useful links</th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/cassandra"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Cassandra"></a></th>
    <th><a href="https://cassandra.apache.org/_/index.html"><img  style="vertical-align:middle" src="img/icon/cassandra.ico" alt="Cassandra"></a></th>
    <th><a href="./content/cassandra.md">Apache Cassandra</a></th>
    <th>Cassandra is a distributed, wide-column store, NoSQL database management system.</th>
    <th><a href="https://github.com/Anant/awesome-cassandra">Awesome Cassandra</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/greenplum-db/gpdb"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Greenplum"></a></th>
    <th><a href="https://greenplum.org/"><img style="vertical-align:middle" src="img/icon/greenplum.ico" alt="Greenplum"></a></th>
    <th><a href="./content/greenplum.md">Greenplum</a></th>
    <th>Greenplum is a big data technology based on MPP architecture and the Postgres open source database technology.</th>
    <th><a href="https://github.com/kongyew/awesome-greenplum">Awesome Greenplum</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/mongodb/mongo"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="MongoDB"></a></th>
    <th><a href="https://www.mongodb.com/"><img style="vertical-align:middle" src="img/icon/mongo.ico" alt="MongoDB"></a></th>
    <th><a href="./content/mongo.md">MongoDB</a></th>
    <th>MongoDB is a document-oriented database.</th>
    <th><a href="https://github.com/ramnes/awesome-mongodb">Awesome MongoDB</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/hbase"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Hbase"></a></th>
    <th><a href="https://hbase.apache.org/"><img style="vertical-align:middle" src="img/icon/hbase.ico" alt="Hbase"></a></th>
    <th><a href="./content/hbase.md">Apache Hbase</a></th>
    <th>HBase is an open-source non-relational distributed database.</th>
    <th><a href="https://github.com/rayokota/awesome-hbase">Awesome HBase</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/hive"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Hive"></a></th>
    <th><a href="https://hive.apache.org/"><img style="vertical-align:middle" src="img/icon/hive.ico" alt="Hive"></a></th>
    <th><a href="./content/hive.md">Apache Hive</a></th>
    <th>Apache Hive is a data warehouse software project built on top of Apache Hadoop for providing data query and analysis.</th>
    <th><a href="https://github.com/dharmeshkakadia/awesome-hive">Awesome Hive</a></th>
  </tr>
  <tr>
    <th colspan="2"><a href="https://aws.amazon.com/dynamodb/"><img style="vertical-align:middle" src="img/icon/dynamodb.ico" alt="Amazon DynamoDB"></a></th>
    <th><a href="./content/dynamodb.md">Amazon DynamoDB</a></th>
    <th>Amazon DynamoDB is a fully managed proprietary NoSQL database service.</th>
    <th><a href="https://github.com/alexdebrie/awesome-dynamodb">Awesome DynamoDB</a>
        <a href="https://github.com/donnemartin/awesome-aws">Awesome AWS</a></th>
  </tr>
  <tr>
    <th colspan="2"><a href="https://aws.amazon.com/redshift"><img style="vertical-align:middle" src="img/icon/redshift.ico" alt="Amazon Redshift"></a></th>
    <th><a href="./content/redshift.md">Amazon Redshift</a></th>
    <th>Amazon Redshift is a data warehouse product.</th>
    <th><a href="https://github.com/awslabs/amazon-redshift-utils">Amazon Redshift Utilities</a>
        <a href="https://github.com/donnemartin/awesome-aws">Awesome AWS</a></th>
  </tr>
  <tr>
    <th colspan="2"><a href="https://cloud.google.com/bigquery"><img style="vertical-align:middle" src="img/icon/bigquery.ico" alt="BigQuery"></a></th>
    <th><a href="./content/bigquery.md">BigQuery GCP</a></th>
    <th>BigQuery is a fully-managed, serverless data warehouse.</th>
    <th><a href="https://github.com/coty/awesome-bigquery">Awesome BigQuery</a></th>
  </tr>
  <tr>
    <th colspan="2"><a href="https://cloud.google.com/bigtable"><img style="vertical-align:middle" src="img/icon/bigtable.ico" alt="Bigtable"></a></th>
    <th><a href="./content/bigtable.md">Bigtable GCP</a></th>
    <th>Bigtable is a fully managed wide-column and key-value NoSQL database service.</th>
    <th><a href="https://github.com/zrosenbauer/awesome-bigtable">Awesome Bigtable</a></th>
  </tr>
  <th colspan="5"><a></a></th>
  <tr>
    <th colspan="5">Data Formats</th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/avro"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Avro"></a></th>
    <th><a href="https://avro.apache.org/"><img style="vertical-align:middle" src="img/icon/avro.ico" alt="Avro"></a></th>
    <th><a href="./content/avro.md">Apache Avro</a></th>
    <th>Avro is a row-oriented remote procedure call and data serialization framework.</th>
    <th><a href="https://github.com/m0nhawk/awesome-avro">Awesome Avro</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/parquet"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Parquet"></a></th>
    <th><a href="https://parquet.apache.org/"><img style="vertical-align:middle" src="img/icon/parquet.ico" alt="Parquet"></a></th>
    <th><a href="./content/parquet.md">Apache Parquet</a></th>
    <th>Apache Parquet is a column-oriented data file format designed for efficient data storage and retrieval.</th>
    <th><a href="https://github.com/apache/parquet-format">Parquet format</a> · <a href="https://parquet.apache.org/docs/">Docs</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/delta-io"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Delta"></a></th>
    <th><a href="https://delta.io/"><img style="vertical-align:middle" src="img/icon/deltalake.ico" alt="Delta"></a></th>
    <th><a href="./content/delta.md">Delta</a></th>
    <th>Delta Lake is a storage framework that enables building a Lakehouse architecture with compute engines</th>
    <th><a href="https://github.com/MrPowers/delta-examples">Delta examples</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/iceberg"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Iceberg"></a></th>
    <th><a href="https://iceberg.apache.org/"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Iceberg"></a></th>
    <th><a href="./content/iceberg.md">Apache Iceberg</a></th>
    <th>Apache Iceberg is an open table format for huge analytic datasets.</th>
    <th><a href="https://iceberg.apache.org/docs/latest/">Iceberg docs</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/hudi"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Hudi"></a></th>
    <th><a href="https://hudi.apache.org/"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Hudi"></a></th>
    <th><a href="./content/hudi.md">Apache Hudi</a></th>
    <th>Apache Hudi brings upserts, deletes, and incremental processing to data lakes.</th>
    <th><a href="https://hudi.apache.org/docs/overview/">Hudi docs</a></th>
  </tr>
 <th colspan="5"><a></a></th>
  <tr>
    <th colspan="5">Big Data Frameworks</th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/airflow"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Airflow"></a></th>
    <th><a href="https://airflow.apache.org/"><img style="vertical-align:middle" src="img/icon/airflow.ico" alt="Airflow"></a></th>
    <th><a href="./content/airflow.md">Apache Airflow</a></th>
    <th>Apache Airflow is a workflow management platform for data engineering pipelines.</th>
    <th><a href="https://github.com/jghoman/awesome-apache-airflow">Awesome Airflow</a></th>
  </tr>

  <tr>
    <th><a href="https://github.com/apache/flume"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Flume"></a></th>
    <th><a href="https://flume.apache.org/"><img style="vertical-align:middle" src="img/icon/flume.ico" alt="Flume"></a></th>
    <th><a href="./content/flume.md">Apache Flume</a></th>
    <th>Apache Flume is a distributed, reliable, and available software for efficiently collecting, aggregating, and moving large amounts of log data.</th>
    <th><a href="https://flume.apache.org/FlumeUserGuide.html">Flume User Guide</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/hadoop"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Hadoop"></a></th>
    <th><a href="https://hadoop.apache.org/"><img style="vertical-align:middle" src="img/icon/hadoop.ico" alt="Hadoop"></a></th>
    <th><a href="./content/hadoop.md">Apache Hadoop</a></th>
    <th>Apache Hadoop is a collection of software utilities that facilitates using a network of many computers to solve problems involving massive amounts of data and computation.</th>
    <th><a href="https://github.com/youngwookim/awesome-hadoop">Awesome Hadoop</a></th>
  </tr>

  <tr>
    <th><a href="https://github.com/apache/impala"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Impala"></a></th>
    <th><a href="https://impala.apache.org/"><img style="vertical-align:middle" src="img/icon/impala.ico" alt="Impala"></a></th>
    <th><a href="./content/impala.md">Apache Impala</a></th>
    <th>Apache Impala is a parallel processing SQL query engine for data stored in a computer cluster running Apache Hadoop.</th>
    <th><a href="https://impala.apache.org/docs/build/html/">Impala docs</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/kafka"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Kafka"></a></th>
    <th><a href="https://kafka.apache.org/"><img style="vertical-align:middle" src="img/icon/kafka.ico" alt="Kafka"></a></th>
    <th><a href="./content/kafka.md">Apache Kafka</a></th>
    <th>Apache Kafka is a distributed event store and stream-processing platform.</th>
    <th><a href="https://github.com/semantalytics/awesome-kafka">Awesome Kafka</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/apache/nifi"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="NiFi"></a></th>
    <th><a href="https://nifi.apache.org/"><img style="vertical-align:middle" src="img/icon/nifi.ico" alt="NiFi"></a></th>
    <th><a href="./content/nifi.md">Apache NiFi</a></th>
    <th>Apache NiFi is a software project designed to automate the flow of data between software systems.</th>
    <th><a href="https://github.com/jfrazee/awesome-nifi">Awesome NiFi</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/apache/spark"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Spark"></a></th>
    <th><a href="https://spark.apache.org/"><img style="vertical-align:middle" src="img/icon/spark.ico" alt="Spark"></a></th>
    <th><a href="./content/spark.md">PySpark</a></th>
    <th>PySpark is the Python API for Apache Spark, used for distributed batch, streaming, and lakehouse data processing.</th>
    <th><a href="https://github.com/awesome-spark/awesome-spark">Awesome Spark</a></th>
  </tr>
  <tr>
    <th><a href="https://github.com/apache/spark"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Spark Tuning"></a></th>
    <th><a href="https://spark.apache.org/docs/latest/tuning.html"><img style="vertical-align:middle" src="img/icon/spark.ico" alt="Spark Tuning"></a></th>
    <th><a href="./content/spark-tuning.md">Spark Tuning</a></th>
    <th>Practical Spark performance tuning methods: repartitioning, salting, joins, AQE, caching, file sizing, and streaming tuning.</th>
    <th><a href="https://spark.apache.org/docs/latest/tuning.html">Spark tuning guide</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/apache/flink"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Flink"></a></th>
    <th><a href="https://flink.apache.org/"><img style="vertical-align:middle" src="img/icon/flink.ico" alt="Flink"></a></th>
    <th><a href="./content/flink.md">Apache Flink</a></th>
    <th>Apache Flink is unified stream-processing and batch-processing framework.</th>
    <th><a href="https://github.com/wuchong/awesome-flink">Awesome Flink</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/kubernetes/kubernetes"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Kubernetes"></a></th>
    <th><a href="https://kubernetes.io/"><img style="vertical-align:middle" src="img/icon/kuber.ico" alt="Kubernetes"></a></th>
    <th><a href="./content/kubernetes.md">Kubernetes</a></th>
    <th>  Kubernetes is a system for managing containerized applications across multiple hosts.</th>
    <th><a href="https://github.com/ramitsurana/awesome-kubernetes">Awesome Kubernetes</a></th>
  </tr>
<th colspan="5"><a></a></th>
  <tr>
    <th colspan="5">Cloud providers</th>
  </tr>
    <tr>
    <th><a href="https://github.com/aws"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="AWS"></a></th>
    <th><a href="https://aws.amazon.com/"><img style="vertical-align:middle" src="img/icon/aws.ico" alt="AWS"></a></th>
    <th><a href="./content/aws.md">Amazon Web Services</a></th>
    <th>Amazon web service is an online platform that provides scalable and cost-effective cloud computing solutions.</th>
    <th><a href="https://github.com/donnemartin/awesome-aws">Awesome AWS</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/Azure"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Azure"></a></th>
    <th><a href="https://azure.microsoft.com/"><img style="vertical-align:middle" src="img/icon/azure.ico" alt="Azure"></a></th>
    <th><a href="./content/azure.md">Microsoft Azure</a></th>
    <th>Microsoft Azure is Microsoft's public cloud computing platform.</th>
    <th><a href="https://github.com/kristofferandreasen/awesome-azure">Awesome Azure</a></th>
  </tr>
    <tr>
    <th><a href="https://github.com/GoogleCloudPlatform"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="GCP"></a></th>
    <th><a href="https://cloud.google.com/"><img style="vertical-align:middle" src="img/icon/gcp.ico" alt="GCP"></a></th>
    <th><a href="./content/gcp.md">Google Cloud Platform</a></th>
    <th>Google Cloud Platform is a suite of cloud computing services.</th>
    <th><a href="https://github.com/GoogleCloudPlatform/awesome-google-cloud">Awesome GCP</a></th>
  </tr>
<th colspan="5"><a></a></th>
  <tr>
    <th colspan="5">Modern Data Stack</th>
  </tr>
  <tr>
    <th><a href="https://github.com/dbt-labs/dbt-core"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="dbt"></a></th>
    <th><a href="https://docs.getdbt.com/"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="dbt"></a></th>
    <th><a href="./content/dbt.md">dbt</a></th>
    <th>dbt is a transformation framework for building tested and documented SQL models.</th>
    <th><a href="https://docs.getdbt.com/docs/build/tests">dbt tests</a></th>
  </tr>
<th colspan="5"><a></a></th>
  <tr>
    <th colspan="5"><b>Theory</b></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/dwha.md"><img style="vertical-align:middle" src="img/icon/dwha.ico" alt="DWHA"></a></th>
    <th><a href="./content/dwha.md">DWH Architectures</a></th>
    <th>A data warehouse architecture is a method of defining the overall architecture of data communication processing and presentation that exist for end-clients computing within the enterprise.</th>
    <th><a href="https://github.com/numetriclabz/awesome-db">Awesome databases</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/cdc.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="CDC"></a></th>
    <th><a href="./content/cdc.md">Change Data Capture (CDC)</a></th>
    <th>CDC captures inserts/updates/deletes from source systems for low-latency ingestion.</th>
    <th><a href="https://debezium.io/documentation/">Debezium docs</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/data-modeling.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Data Modeling"></a></th>
    <th><a href="./content/data-modeling.md">Data Modeling</a></th>
    <th>Dimensional modeling concepts used to build reliable analytics datasets.</th>
    <th><a href="https://www.kimballgroup.com/">Kimball Group</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/data-quality.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Data Quality"></a></th>
    <th><a href="./content/data-quality.md">Data Quality</a></th>
    <th>Tests, monitoring, and practices to ensure datasets are trusted and correct.</th>
    <th><a href="https://greatexpectations.io/docs/">Great Expectations docs</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/observability.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Data Observability"></a></th>
    <th><a href="./content/observability.md">Data Observability</a></th>
    <th>Monitoring and incident response practices for pipeline and dataset health.</th>
    <th><a href="https://openlineage.io/">OpenLineage</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/data-governance.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Data Governance"></a></th>
    <th><a href="./content/data-governance.md">Data Governance</a></th>
    <th>Ownership, policies, privacy, and access controls for data platforms.</th>
    <th><a href="https://github.com/datahub-project/datahub">DataHub</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/cost-optimization.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Cost Optimization"></a></th>
    <th><a href="./content/cost-optimization.md">Cost Optimization</a></th>
    <th>Practical techniques to reduce compute and storage costs while meeting SLAs.</th>
    <th><a href="https://spark.apache.org/docs/latest/tuning.html">Spark tuning</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/python.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="Python"></a></th>
    <th><a href="./content/python.md">Python for Data Engineering</a></th>
    <th>Python fundamentals for reliable, scalable data pipelines and tooling.</th>
    <th><a href="https://arrow.apache.org/docs/python/">PyArrow docs</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/system-design.md"><img style="vertical-align:middle" src="img/icon/fire.ico" alt="System Design"></a></th>
    <th><a href="./content/system-design.md">Data System Design</a></th>
    <th>System design interview questions for batch/streaming data platforms.</th>
    <th><a href="https://martinfowler.com/articles/data-monolith-to-mesh.html">Data mesh overview</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/data-structure.md"><img style="vertical-align:middle" src="img/icon/datastruct.ico" alt="Airflow"></a></th>
    <th><a href="./content/data-structure.md">Data Structures</a></th>
    <th>A data structure is a specialized format for organizing, processing, retrieving and storing data. </th>
    <th><a href="https://github.com/tayllan/awesome-algorithms">Awesome Algorithms</a></th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/sql.md"><img style="vertical-align:middle" src="img/icon/sql.ico" alt="SQL"></a></th>
    <th><a href="./content/sql.md">SQL</a></th>
    <th>SQL is a domain-specific language used in programming and designed for managing data held in a relational database management system (RDBMS).</th>
    <th><a href="https://github.com/danhuss/awesome-sql">Awesome SQL</a></th>
  </tr>
<th colspan="5"><a></a></th>
  <tr>
    <th colspan="5">Data visualization tools/BI</th>
  </tr>
    <tr>
    <th colspan="2"><a href="./content/tableau.md"><img style="vertical-align:middle" src="img/icon/tableau.ico" alt="Tableau"></a></th>
    <th><a href="./content/tableau.md">Tableau</a></th>
    <th>Tableau is a powerful data visualization tool used in the Business Intelligence.</th>
    <th><a href="https://help.tableau.com/current/pro/desktop/en-us/default.htm">Tableau Desktop docs</a></th>
  </tr>
  <tr>
    <th colspan="2"><a href="./content/looker.md"><img style="vertical-align:middle" src="img/icon/looker.ico" alt="Looker"></a></th>
    <th><a href="./content/looker.md">Looker</a></th>
    <th>Looker is an enterprise platform for BI, data applications, and embedded analytics that helps you explore and share insights in real time.</th>
    <th><a href="https://cloud.google.com/looker/docs">Looker docs</a></th>
  </tr>
 <tr>
    <th><a href="https://github.com/apache/superset"><img  style="vertical-align:middle"  src="img/icon/github.ico" alt="Superset"></a></th>
    <th><a href="https://superset.apache.org/"><img style="vertical-align:middle" src="img/icon/superset.ico" alt="Apache Superset"></a></th>
    <th><a href="./content/superset.md">Apache Superset</a></th>
    <th>Superset is a modern data exploration and data visualization platform</th>
    <th><a href="https://superset.apache.org/docs/intro">Superset docs</a></th>
  </tr>


</table>
</div>
<div>

## New topics

These topics were added to cover the platforms and skills that the rest of the guide references but did not explain on their own.

| Topic | What it covers | Reference |
|---|---|---|
| [Databricks](./content/databricks.md) | Managed lakehouse on Spark and Delta: clusters, Unity Catalog, Auto Loader, Lakeflow pipelines, Workflows, Asset Bundles, Photon, cost control | [Databricks docs](https://docs.databricks.com/) |
| [Snowflake](./content/snowflake.md) | Cloud warehouse architecture, micro-partitions, streams/tasks, Snowpipe, dynamic tables, Snowpark, RBAC and cost | [Snowflake docs](https://docs.snowflake.com/) |
| [Trino and Presto](./content/trino.md) | Federated SQL engine: catalogs and connectors, pushdown, join strategies, resource groups, lakehouse queries | [Trino docs](https://trino.io/docs/current/) |
| [ClickHouse](./content/clickhouse.md) | Real-time columnar OLAP: MergeTree engines, materialized views, ReplacingMergeTree dedupe, ingestion patterns | [ClickHouse docs](https://clickhouse.com/docs) |
| [Redis](./content/redis.md) | In-memory store for caching, rate limiting, dedupe, locks, and Streams-based queues | [Redis docs](https://redis.io/docs/latest/) |
| [Elasticsearch and OpenSearch](./content/elasticsearch.md) | Search and log analytics: mappings, aggregations, pagination, ILM, ingestion pipelines, shard sizing | [Elastic docs](https://www.elastic.co/docs) |
| [Docker](./content/docker.md) | Images, Dockerfiles, Compose, volumes and networks, resource limits, local data stacks, CI image builds | [Docker docs](https://docs.docker.com/) |
| [Statistics and Experimentation](./content/statistics.md) | Percentiles, distributions, hypothesis testing, A/B testing, anomaly detection, capacity planning | [NIST statistics handbook](https://www.itl.nist.gov/div898/handbook/) |
| [Python Coding Problems](./content/python-coding.md) | Data-engineering coding exercises with runnable solutions, complexity notes, and pandas/PySpark equivalents | [Python docs](https://docs.python.org/3/) |
| [LLM and AI Terminology](./content/llm.md) | Tokens, embeddings, transformers, RAG, fine-tuning, evals, agents, guardrails, and inference cost for data engineers | [Anthropic glossary](https://docs.anthropic.com/en/docs/resources/glossary) |
| [Python Basics](./content/python-basics.md) | Language fundamentals: classes and methods, dunder methods, OOP, exceptions, context managers, generators, decorators, typing, and concurrency | [Python tutorial](https://docs.python.org/3/tutorial/) |
| [Scala Basics](./content/scala.md) | Scala for data engineers: vals/types, functions, case classes, pattern matching, traits, collections, Option/Either/Future, and Spark Scala idioms | [Scala docs](https://docs.scala-lang.org/) |

</div>
<div>
<h2 align="center"> Contribution </h2>
<h3>Please contribute to help make this repository better. New questions, code examples, doc improvements, and real-world interview scenarios are very welcome.</h3>
<p align="center">See <a href="./CONTRIBUTING.md">CONTRIBUTING.md</a> for quick checks and guidelines.</p>
</div>
