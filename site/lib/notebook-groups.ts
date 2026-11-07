/**
 * The registry: the only place that says which notebooks the gallery shows.
 * A group's `folder` is where its notebooks live; `slugs` are file names without
 * the extension. The build fails on a missing or unregistered notebook.
 */
export type NotebookGroup = {
  label: string;
  folder: string;
  slugs: string[];
};

const PRACTICE_FOLDER = "notebooks";
const TOPIC_FOLDER = "notebooks/topics";

export const PRACTICE_GROUP: NotebookGroup = {
  label: "Hands-on practice",
  folder: PRACTICE_FOLDER,
  slugs: [
    "01_python_basics",
    "02_python_coding_problems",
    "03_sql_interview_questions",
    "04_pyspark_concepts",
    "05_interview_questions",
    "06_pyspark_coding_challenges",
  ],
};

const topicGroup = (label: string, slugs: string[]): NotebookGroup => ({
  label,
  folder: TOPIC_FOLDER,
  slugs,
});

export const TOPIC_GROUPS: NotebookGroup[] = [
  topicGroup("SQL learning path", [
    "sql-01-basics",
    "sql-02-aggregations-and-ctes",
    "sql-03-null-handling",
    "sql-04-case-expressions",
    "sql-05-joins",
    "sql-06-window-functions",
    "sql-07-deduplication",
    "sql-08-time-series",
    "sql-09-modeling-and-optimization",
    "sql-10-interview-drills",
  ]),
  topicGroup("Core pipeline skills", [
    "python",
    "sql",
    "scala",
    "spark",
    "spark-tuning",
    "airflow",
    "dbt",
    "data-quality",
    "observability",
  ]),
  topicGroup("Lakehouse and formats", ["parquet", "delta", "iceberg", "hudi", "avro", "cdc", "data-modeling"]),
  topicGroup("Cloud and platforms", [
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
  ]),
  topicGroup("Streaming and distributed systems", [
    "kafka",
    "flink",
    "redis",
    "hadoop",
    "hive",
    "hbase",
    "cassandra",
    "kubernetes",
  ]),
  topicGroup("Warehousing, BI and governance", [
    "dwha",
    "system-design",
    "statistics",
    "data-governance",
    "cost-optimization",
    "tableau",
    "looker",
    "superset",
  ]),
  topicGroup("AI and LLM foundations", ["llm"]),
  topicGroup("Additional tools", [
    "mongo",
    "nifi",
    "flume",
    "greenplum",
    "impala",
    "elasticsearch",
    "docker",
    "data-structure",
  ]),
];

export const ALL_GROUPS: NotebookGroup[] = [PRACTICE_GROUP, ...TOPIC_GROUPS];

/** URL anchor id for a group label, e.g. "Core pipeline skills" -> "core-pipeline-skills". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
