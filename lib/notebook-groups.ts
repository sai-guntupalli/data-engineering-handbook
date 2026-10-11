export type NotebookGroup = {
  label: string;
  slugs: string[];
};

/** Hands-on notebooks that live at notebooks/<slug>.ipynb. */
export const PRACTICE_GROUP: NotebookGroup = {
  label: "Hands-on practice",
  slugs: [
    "01_python_basics",
    "02_python_coding_problems",
    "03_sql_interview_questions",
    "04_pyspark_concepts",
    "05_interview_questions",
  ],
};

/** Topic notebooks that live at notebooks/topics/<slug>.ipynb. */
export const TOPIC_GROUPS: NotebookGroup[] = [
  {
    label: "Core pipeline skills",
    slugs: [
      "python",
      "python-basics",
      "python-coding",
      "sql",
      "scala",
      "spark",
      "spark-tuning",
      "airflow",
      "dbt",
      "data-quality",
      "observability",
    ],
  },
  {
    label: "Lakehouse and formats",
    slugs: ["parquet", "delta", "iceberg", "hudi", "avro", "cdc", "data-modeling"],
  },
  {
    label: "Cloud and platforms",
    slugs: [
      "aws",
      "azure",
      "gcp",
      "bigquery",
      "redshift",
      "snowflake",
      "databricks",
      "trino",
      "clickhouse",
      "dynamodb",
      "bigtable",
    ],
  },
  {
    label: "Streaming and distributed systems",
    slugs: ["kafka", "flink", "redis", "hadoop", "hive", "hbase", "cassandra", "kubernetes"],
  },
  {
    label: "Warehousing, BI and governance",
    slugs: [
      "dwha",
      "system-design",
      "statistics",
      "data-governance",
      "cost-optimization",
      "tableau",
      "looker",
      "superset",
    ],
  },
  {
    label: "AI and LLM foundations",
    slugs: ["llm"],
  },
  {
    label: "Additional tools",
    slugs: [
      "mongo",
      "nifi",
      "flume",
      "greenplum",
      "impala",
      "elasticsearch",
      "docker",
      "data-structure",
    ],
  },
];

/** URL anchor id for a group label, e.g. "Core pipeline skills" -> "core-pipeline-skills". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
