/**
 * The registry: the only place that says which notebooks the gallery shows.
 * A group's `folder` is where its notebooks live; `slugs` are file names without
 * the extension. The build fails on a missing or unregistered notebook.
 *
 * Groups come in two sections. "learn" groups teach a topic in order; "practice"
 * groups hold questions and drills. The sidebar and the catalog list them in
 * this order, so the array order below is the order the reader sees.
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

/** Whether a group teaches a topic or holds questions to test it. */
export type GroupSection = "learn" | "practice";

export type NotebookGroup = {
  label: string;
  /** Short name for filters and the sidebar on narrow screens. */
  shortLabel: string;
  section: GroupSection;
  tone: GroupTone;
  folder: string;
  slugs: string[];
};

const PRACTICE_FOLDER = "notebooks";
const TOPIC_FOLDER = "notebooks/topics";

const group = (
  label: string,
  shortLabel: string,
  section: GroupSection,
  tone: GroupTone,
  folder: string,
  slugs: string[],
): NotebookGroup => ({ label, shortLabel, section, tone, folder, slugs });

export const INTERVIEW_GROUP = group(
  "Interview questions",
  "Questions",
  "practice",
  "practice",
  PRACTICE_FOLDER,
  [
    "01_python_basics",
    "02_python_coding_problems",
    "03_sql_interview_questions",
    "04_pyspark_concepts",
    "05_interview_questions",
    "06_pyspark_coding_challenges",
  ],
);

const topic = (label: string, shortLabel: string, tone: GroupTone, slugs: string[]) =>
  group(label, shortLabel, "learn", tone, TOPIC_FOLDER, slugs);

export const LEARNING_GROUPS: NotebookGroup[] = [
  topic("Python learning path", "Python", "python", [
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
  topic("SQL learning path", "SQL", "sql", [
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
  topic("Data Engineering", "Core", "core", [
    "sql",
    "scala",
    "spark",
    "spark-tuning",
    "airflow",
    "dbt",
    "data-quality",
    "observability",
  ]),
  topic("Lakehouse Formats", "Lakehouse", "lake", [
    "parquet",
    "delta",
    "iceberg",
    "hudi",
    "avro",
    "cdc",
    "data-modeling",
  ]),
  topic("Cloud Platforms", "Cloud", "cloud", [
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
  topic("Streaming and Distributed Systems", "Streaming", "stream", [
    "kafka",
    "flink",
    "redis",
    "hadoop",
    "hive",
    "hbase",
    "cassandra",
    "kubernetes",
  ]),
  topic("Warehousing and BI", "Warehousing", "warehouse", [
    "dwha",
    "system-design",
    "statistics",
    "data-governance",
    "cost-optimization",
    "tableau",
    "looker",
    "superset",
  ]),
  topic("AI Foundations", "AI", "ai", ["llm"]),
  topic("Other Tools", "Other", "other", [
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

export const PRACTICE_GROUPS: NotebookGroup[] = [
  INTERVIEW_GROUP,
  group("Python practice", "Python drills", "practice", "practice", TOPIC_FOLDER, [
    "python-01-practice-values-and-types",
    "python-02-practice-collections",
    "python-03-practice-control-flow-and-functions",
    "python-04-practice-iterators-and-generators",
    "python-05-practice-classes-and-dataclasses",
    "python-06-practice-files-and-formats",
    "python-07-practice-errors-logging-and-testing",
    "python-08-practice-concurrency",
    "python-09-practice-data-engineering",
  ]),
  group("Coding interviews", "LeetCode", "practice", "practice", TOPIC_FOLDER, [
    "leetcode-01-arrays-and-hashing",
    "leetcode-02-two-pointers-and-sliding-window",
    "leetcode-03-stacks-and-monotonic-stacks",
    "leetcode-04-binary-search",
    "leetcode-05-linked-lists",
    "leetcode-06-binary-trees",
    "leetcode-07-graphs-and-grids",
    "leetcode-08-dynamic-programming",
    "leetcode-09-backtracking-heaps-intervals-design",
  ]),
];

export const ALL_GROUPS: NotebookGroup[] = [...LEARNING_GROUPS, ...PRACTICE_GROUPS];

/** URL-safe id for a label or heading, e.g. "Data Engineering" -> "data-engineering". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
