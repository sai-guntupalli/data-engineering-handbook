/**
 * The registry: the only place that says which notebooks the gallery shows.
 * A group's `folder` is where its notebooks live, and `folderOverrides` names the
 * few notebooks that live elsewhere. `slugs` are file names without the extension.
 * The build fails on a missing or unregistered notebook.
 *
 * Groups come in two sections. "learn" groups teach a topic in the order listed;
 * "practice" groups hold questions and drills for the topic they name. The sidebar
 * and the catalog show groups in this array order.
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
  /** Notebooks whose file is not in `folder`, keyed by slug. */
  folderOverrides?: Record<string, string>;
  slugs: string[];
};

const ROOT_FOLDER = "notebooks";
const TOPIC_FOLDER = "notebooks/topics";

/** The repository path of one registered notebook, e.g. "notebooks/topics/sql-01-basics.ipynb". */
export function repoPathFor(group: NotebookGroup, slug: string) {
  return `${group.folderOverrides?.[slug] ?? group.folder}/${slug}.ipynb`;
}

const group = (
  label: string,
  shortLabel: string,
  section: GroupSection,
  tone: GroupTone,
  folder: string,
  slugs: string[],
  folderOverrides?: Record<string, string>,
): NotebookGroup => ({ label, shortLabel, section, tone, folder, slugs, folderOverrides });

const learn = (label: string, shortLabel: string, tone: GroupTone, slugs: string[], folderOverrides?: Record<string, string>) =>
  group(label, shortLabel, "learn", tone, TOPIC_FOLDER, slugs, folderOverrides);

const practice = (
  label: string,
  shortLabel: string,
  tone: GroupTone,
  folder: string,
  slugs: string[],
  folderOverrides?: Record<string, string>,
) => group(label, shortLabel, "practice", tone, folder, slugs, folderOverrides);

/** Learning groups in reading order: languages first, then the tools built on them. */
export const LEARNING_GROUPS: NotebookGroup[] = [
  learn("Python learning path", "Python", "python", [
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
  learn(
    "SQL learning path",
    "SQL",
    "sql",
    [
      "03_sql_interview_questions",
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
    ],
    { "03_sql_interview_questions": ROOT_FOLDER },
  ),
  learn("PySpark learning path", "PySpark", "core", [
    "spark",
    "pyspark-01-foundations",
    "pyspark-02-reading-sql-and-cleaning",
    "pyspark-03-joins-and-aggregations",
    "pyspark-04-windows-and-nested-data",
    "pyspark-05-writing-pipelines-and-quality",
    "pyspark-06-structured-streaming",
    "pyspark-07-monitoring-and-performance",
    "pyspark-08-real-world-and-interviews",
  ]),
  learn("Foundations", "Foundations", "core", ["sql", "data-structure", "statistics", "system-design"]),
  learn("Modeling and governance", "Modeling", "warehouse", [
    "data-modeling",
    "dwha",
    "data-governance",
    "cost-optimization",
    "data-quality",
  ]),
  learn("Processing engines", "Processing", "core", [
    "spark-tuning",
    "scala",
    "hadoop",
    "hive",
    "impala",
    "trino",
  ]),
  learn("Orchestration and tooling", "Tooling", "core", [
    "airflow",
    "dbt",
    "observability",
    "docker",
    "kubernetes",
  ]),
  learn("Lakehouse formats", "Lakehouse", "lake", ["parquet", "avro", "delta", "iceberg", "hudi"]),
  learn("Ingestion and streaming", "Streaming", "stream", ["kafka", "flink", "cdc", "nifi", "flume"]),
  learn("Databases", "Databases", "other", [
    "mongo",
    "cassandra",
    "hbase",
    "redis",
    "dynamodb",
    "bigtable",
    "elasticsearch",
    "clickhouse",
    "greenplum",
  ]),
  learn("Cloud platforms", "Cloud", "cloud", [
    "aws",
    "azure",
    "gcp",
    "databricks",
    "snowflake",
    "bigquery",
    "redshift",
  ]),
  learn("BI and visualization", "BI", "warehouse", ["tableau", "looker", "superset"]),
  learn("AI and LLMs", "AI", "ai", ["llm"]),
];

/** Practice groups: each one trains the topic in its name. */
export const PRACTICE_GROUPS: NotebookGroup[] = [
  practice("Python drills", "Python drills", "python", TOPIC_FOLDER, [
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
  practice(
    "Python coding challenges",
    "Coding challenges",
    "python",
    TOPIC_FOLDER,
    [
      "02_python_coding_problems",
      "python-challenges-01-arrays-and-hashing",
      "python-challenges-02-two-pointers-and-sliding-window",
      "python-challenges-03-stacks-and-monotonic-stacks",
      "python-challenges-04-binary-search",
      "python-challenges-05-linked-lists",
      "python-challenges-06-binary-trees",
      "python-challenges-07-graphs-and-grids",
      "python-challenges-08-dynamic-programming",
      "python-challenges-09-backtracking-heaps-intervals-design",
    ],
    { "02_python_coding_problems": ROOT_FOLDER },
  ),
  practice("Interview questions", "Interview questions", "practice", ROOT_FOLDER, [
    "01_python_basics",
    "05_interview_questions",
  ]),
  practice("SQL interview drills", "SQL drills", "sql", TOPIC_FOLDER, ["sql-13-interview-drills", "sql-14-interview-concepts"]),
  practice("PySpark interview practice", "PySpark practice", "core", ROOT_FOLDER, [
    "04_pyspark_concepts",
    "06_pyspark_coding_challenges",
  ]),
];

/** The question bank that the home page points to for interview prep. */
export const INTERVIEW_GROUP = PRACTICE_GROUPS[2];

export const ALL_GROUPS: NotebookGroup[] = [...LEARNING_GROUPS, ...PRACTICE_GROUPS];

/** URL-safe id for a label or heading, e.g. "Data Engineering" -> "data-engineering". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
