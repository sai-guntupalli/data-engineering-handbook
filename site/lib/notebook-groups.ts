/**
 * The registry: the only place that says which notebooks the gallery shows.
 * A group's `folder` is where its notebooks live; `slugs` are file names without
 * the extension. The build fails on a missing or unregistered notebook.
 */

/** Colour family of a group; each maps to a `--tone-*` token in globals.css. */
export type GroupTone =
  | "practice"
  | "python"
  | "sql"
  | "core"
  | "lake"
  | "cloud"
  | "stream"
  | "warehouse"
  | "ai"
  | "other";

export type NotebookGroup = {
  label: string;
  /** Short name for filters and the sidebar on narrow screens. */
  shortLabel: string;
  tone: GroupTone;
  folder: string;
  slugs: string[];
};

const PRACTICE_FOLDER = "notebooks";
const TOPIC_FOLDER = "notebooks/topics";

export const INTERVIEW_GROUP: NotebookGroup = {
  label: "Interview practice",
  shortLabel: "Practice",
  tone: "practice",
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

const topicGroup = (label: string, shortLabel: string, tone: GroupTone, slugs: string[]): NotebookGroup => ({
  label,
  shortLabel,
  tone,
  folder: TOPIC_FOLDER,
  slugs,
});

export const TOPIC_GROUPS: NotebookGroup[] = [
  topicGroup("Python learning path", "Python", "python", [
    "python-01-values-and-types",
    "python-02-collections",
    "python-03-control-flow-and-functions",
    "python-04-iterators-and-generators",
    "python-05-classes-and-dataclasses",
    "python-06-files-and-formats",
    "python-07-errors-logging-and-testing",
    "python-08-concurrency",
    "python-09-data-engineering",
  ]),
  topicGroup("SQL learning path", "SQL", "sql", [
    "sql-01-basics",
    "sql-02-aggregations-and-ctes",
    "sql-03-types-functions-and-json",
    "sql-04-null-handling",
    "sql-05-case-expressions",
    "sql-06-joins",
    "sql-07-set-operations",
    "sql-08-window-functions",
    "sql-09-deduplication",
    "sql-10-time-series",
    "sql-11-modeling-and-optimization",
    "sql-12-views-and-changing-data",
    "sql-13-interview-drills",
    "sql-14-interview-concepts",
  ]),
  topicGroup("Data Engineering", "Core", "core", [
    "sql",
    "scala",
    "spark",
    "spark-tuning",
    "airflow",
    "dbt",
    "data-quality",
    "observability",
  ]),
  topicGroup("Lakehouse Formats", "Lakehouse", "lake", [
    "parquet",
    "delta",
    "iceberg",
    "hudi",
    "avro",
    "cdc",
    "data-modeling",
  ]),
  topicGroup("Cloud Platforms", "Cloud", "cloud", [
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
  topicGroup("Streaming and Distributed Systems", "Streaming", "stream", [
    "kafka",
    "flink",
    "redis",
    "hadoop",
    "hive",
    "hbase",
    "cassandra",
    "kubernetes",
  ]),
  topicGroup("Warehousing and BI", "Warehousing", "warehouse", [
    "dwha",
    "system-design",
    "statistics",
    "data-governance",
    "cost-optimization",
    "tableau",
    "looker",
    "superset",
  ]),
  topicGroup("AI Foundations", "AI", "ai", ["llm"]),
  topicGroup("Other Tools", "Other", "other", [
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

export const ALL_GROUPS: NotebookGroup[] = [INTERVIEW_GROUP, ...TOPIC_GROUPS];

/** URL-safe id for a label or heading, e.g. "Data Engineering" -> "data-engineering". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
