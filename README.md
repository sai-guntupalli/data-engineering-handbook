# Data Engineering Interview Notebooks

Runnable Jupyter notebooks for data engineering interview preparation. There is no separate prose documentation:
every topic is a notebook, so the explanation and the code that proves it live in the same place.

- **Practice notebooks** (`notebooks/01..05`) are hands-on: run them top to bottom and the `assert`s check your answers.
- **Topic notebooks** (`notebooks/topics/*.ipynb`) cover one subject each, from Python basics to Snowflake, Kafka and LLMs.

## Browse them

| Where | How |
|---|---|
| Gallery app | `npm install` then `make serve` → <http://localhost:3000> |
| Google Colab | `https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master/notebooks/topics/<topic>.ipynb` |
| Jupyter locally | `make setup-notebooks` then `jupyter lab notebooks/` |
| GitHub | open any file under [`notebooks/`](notebooks) — outputs are committed, so they read like a book |

## What is inside

| Group | Notebooks |
|---|---|
| Hands-on practice | `01_python_basics`, `02_python_coding_problems`, `03_sql_interview_questions`, `04_pyspark_concepts`, `05_interview_questions` |
| Core pipeline skills | Python, Python basics, Python coding problems, SQL, Scala, Spark, Spark tuning, Airflow, dbt, Data quality, Observability |
| Lakehouse and formats | Parquet, Delta Lake, Apache Iceberg, Apache Hudi, Avro, Change data capture, Data modeling |
| Cloud and platforms | AWS, Azure, GCP, BigQuery, Redshift, Snowflake, Databricks, Trino and Presto, ClickHouse, DynamoDB, Bigtable |
| Streaming and distributed systems | Kafka, Flink, Redis, Hadoop, Hive, HBase, Cassandra, Kubernetes |
| Warehousing, BI and governance | Data warehousing, System design, Statistics, Data governance, Cost optimization, Tableau, Looker, Superset |
| AI and LLM foundations | LLM and AI terminology |
| Additional tools | MongoDB, Apache NiFi, Flume, Greenplum, Impala, Elasticsearch, Docker, Data structures |

## Layout

```text
notebooks/
  01_python_basics.ipynb ... 05_interview_questions.ipynb   practice notebooks
  topics/<topic>.ipynb                                       54 topic notebooks
app/                    Next.js gallery: grouped cards with Colab + GitHub links
lib/notebooks.ts        reads the notebooks and builds the gallery data
lib/notebook-groups.ts  which notebook belongs to which group
scripts/                audit_notebooks.py, run_notebooks.py
```

## Checks

```bash
make check            # notebook structure audit
make notebooks-check  # execute the practice notebooks (no writes)
make validate         # audit + execution + gallery build
make stats            # notebook counts
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: edit or add a notebook, add its slug to
`lib/notebook-groups.ts`, then run `make validate`.
