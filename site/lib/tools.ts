/**
 * The tool registry: one entry per folder under notebooks/. A notebook's folder is
 * its tool, so adding a notebook needs no registry edit, but a new folder does: the
 * build fails until the folder has a label here, and an entry with no folder fails too.
 */

/** Colour family of a tool; each maps to a `--tone-*` token in globals.css. */
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

/** The sidebar and the home page group tools under these headings, in this order. */
export const TOOL_CATEGORIES = [
  { id: "languages", label: "Languages" },
  { id: "processing", label: "Processing engines" },
  { id: "streaming", label: "Streaming and ingestion" },
  { id: "orchestration", label: "Orchestration" },
  { id: "formats", label: "File and table formats" },
  { id: "warehouses", label: "Data warehouses" },
  { id: "databases", label: "NoSQL and search" },
  { id: "cloud", label: "Cloud platforms" },
  { id: "bi", label: "BI and dashboards" },
  { id: "infrastructure", label: "Containers and infrastructure" },
  { id: "foundations", label: "Concepts" },
  { id: "interviews", label: "Interview prep" },
] as const;

export type ToolCategory = (typeof TOOL_CATEGORIES)[number]["id"];

export type Tool = {
  /** Folder under notebooks/topics/, e.g. "kafka". Also the URL segment of the tool page. */
  folder: string;
  label: string;
  description: string;
  tone: GroupTone;
  category: ToolCategory;
  /**
   * Set for technology most new pipelines no longer choose. The note says what they use instead;
   * legacy tools sort after the others in their category and carry a "Legacy" label.
   */
  legacy?: string;
};

/** Active tools first, then legacy ones; by name (without a vendor prefix) within each. */
export function compareTools(a: Tool, b: Tool): number {
  if (Boolean(a.legacy) !== Boolean(b.legacy)) return a.legacy ? 1 : -1;
  return toolSortName(a.label).localeCompare(toolSortName(b.label), "en");
}

/** Sort key that ignores a vendor prefix, so "Apache Kafka" sorts under K next to "Kubernetes". */
export function toolSortName(label: string): string {
  return label.replace(/^(Apache|Amazon) /, "").toLowerCase();
}

/** What a notebook teaches with: the tool page sorts and labels subtopics by this. */
export type NotebookCategory = "lesson" | "reference" | "drill" | "challenge" | "interview";

export const CATEGORY_LABELS: Record<NotebookCategory, string> = {
  lesson: "Lesson",
  reference: "Reference",
  drill: "Drill",
  challenge: "Coding challenge",
  interview: "Interview question",
};

/** Sort order on a tool page: lessons first, then the practice that follows them. */
const CATEGORY_ORDER: NotebookCategory[] = ["lesson", "reference", "drill", "challenge", "interview"];

/** Notebooks whose file name does not say their category. */
const CATEGORY_OVERRIDES: Record<string, NotebookCategory> = {
  "pyspark-concepts-end-to-end": "reference",
};

export function categoryOf(slug: string): NotebookCategory {
  const override = CATEGORY_OVERRIDES[slug];
  if (override) return override;
  if (/reference/.test(slug)) return "reference";
  if (/drill|practice/.test(slug)) return "drill";
  if (/challenge|coding-problems/.test(slug)) return "challenge";
  if (/interview/.test(slug)) return "interview";
  return "lesson";
}

/** Sort rank: category first, then the file name with numbers compared as numbers (so a 00 overview leads). */
export function compareSubtopics(a: { slug: string }, b: { slug: string }): number {
  const rank = CATEGORY_ORDER.indexOf(categoryOf(a.slug)) - CATEGORY_ORDER.indexOf(categoryOf(b.slug));
  return rank || a.slug.localeCompare(b.slug, "en", { numeric: true });
}

export const TOOLS: Tool[] = [
  { folder: "duckdb", label: "DuckDB", description: "Embedded analytics, local Parquet queries and transformation tests.", tone: "sql", category: "processing" },
  { folder: "postgres", label: "PostgreSQL", description: "Transactions, constraints, upserts and pipeline integration.", tone: "sql", category: "databases" },
  { folder: "airflow", label: "Apache Airflow", description: "Scheduling, DAGs, retries and operators for pipelines.", tone: "core", category: "orchestration" },
  { folder: "avro", label: "Apache Avro", description: "Row-based schemas and compact binary data for streams.", tone: "lake", category: "formats" },
  { folder: "aws", label: "AWS", description: "Storage, compute and data services on Amazon Web Services.", tone: "cloud", category: "cloud" },
  { folder: "azure", label: "Azure", description: "Storage, analytics and pipeline services on Microsoft Azure.", tone: "cloud", category: "cloud" },
  { folder: "bigquery", label: "BigQuery", description: "Google's serverless warehouse: partitioning, costs and SQL.", tone: "cloud", category: "warehouses" },
  { folder: "bigtable", label: "Bigtable", description: "Wide-column storage for high-volume key lookups.", tone: "cloud", category: "databases" },
  { folder: "cassandra", label: "Apache Cassandra", description: "Partitioned, replicated storage with tunable consistency.", tone: "stream", category: "databases" },
  { folder: "clickhouse", label: "ClickHouse", description: "Columnar analytics database for fast aggregations.", tone: "cloud", category: "warehouses" },
  { folder: "concepts", label: "Data concepts", description: "Modeling, quality, governance, cost and design ideas that apply to any stack.", tone: "warehouse", category: "foundations" },
  { folder: "databricks", label: "Databricks", description: "Lakehouse platform: Spark, Delta tables and Unity Catalog.", tone: "cloud", category: "cloud" },
  { folder: "dbt", label: "dbt", description: "SQL transformations as tested, documented models.", tone: "core", category: "orchestration" },
  { folder: "delta", label: "Delta Lake", description: "ACID tables on object storage, with time travel and merges.", tone: "lake", category: "formats" },
  { folder: "docker", label: "Docker", description: "Images, layers and containers for reproducible jobs.", tone: "other", category: "infrastructure" },
  { folder: "dynamodb", label: "DynamoDB", description: "Key-value and document storage with single-table design.", tone: "cloud", category: "databases" },
  { folder: "elasticsearch", label: "Elasticsearch", description: "Search and log analytics on inverted indexes.", tone: "other", category: "databases" },
  { folder: "flink", label: "Apache Flink", description: "Stateful stream processing with event time and checkpoints.", tone: "stream", category: "processing" },
  { folder: "flume", label: "Apache Flume", description: "Log collection and transport into Hadoop.", tone: "stream", category: "streaming", legacy: "Retired in most stacks: new log and event ingestion uses Kafka Connect, Fluent Bit or Vector." },
  { folder: "gcp", label: "Google Cloud", description: "Storage, analytics and pipeline services on Google Cloud.", tone: "cloud", category: "cloud" },
  { folder: "greenplum", label: "Greenplum", description: "Massively parallel PostgreSQL-based warehouse.", tone: "other", category: "warehouses", legacy: "Closed-source under Broadcom since 2024; the open-source line continues as Apache Cloudberry. New warehouses usually run on Snowflake, BigQuery or Redshift." },
  { folder: "hadoop", label: "Hadoop", description: "HDFS and MapReduce, the foundation of the Hadoop ecosystem.", tone: "stream", category: "processing", legacy: "HDFS and MapReduce have largely given way to object storage and Spark; YARN and the Hive metastore still appear in older stacks." },
  { folder: "hbase", label: "Apache HBase", description: "Wide-column storage on HDFS for random reads and writes.", tone: "stream", category: "databases", legacy: "Still runs in Hadoop estates; new wide-column workloads usually use Bigtable, Cassandra or DynamoDB." },
  { folder: "hive", label: "Apache Hive", description: "SQL over files in Hadoop, with a metastore and partitions.", tone: "stream", category: "processing" },
  { folder: "hudi", label: "Apache Hudi", description: "Upserts and incremental pipelines on data lakes.", tone: "lake", category: "formats" },
  { folder: "iceberg", label: "Apache Iceberg", description: "Open table format with snapshots, schema evolution and hidden partitions.", tone: "lake", category: "formats" },
  { folder: "impala", label: "Apache Impala", description: "Low-latency SQL on Hadoop data.", tone: "other", category: "processing", legacy: "Mostly found on Cloudera clusters; new lakehouse SQL usually runs on Trino, Spark SQL or a cloud warehouse." },
  { folder: "interview-questions", label: "Interview questions", description: "Questions across Python, SQL and Spark, with model answers and runnable checks.", tone: "practice", category: "interviews" },
  { folder: "kafka", label: "Apache Kafka", description: "Topics, partitions, consumer groups and delivery guarantees.", tone: "stream", category: "streaming" },
  { folder: "kubernetes", label: "Kubernetes", description: "Running containers and scheduled jobs on a cluster.", tone: "core", category: "infrastructure" },
  { folder: "llm", label: "LLMs and AI", description: "Terminology and data-engineering ideas for language models.", tone: "ai", category: "foundations" },
  { folder: "looker", label: "Looker", description: "Semantic modeling and dashboards on top of a warehouse.", tone: "warehouse", category: "bi" },
  { folder: "mongodb", label: "MongoDB", description: "Document storage, aggregation pipelines and indexes.", tone: "other", category: "databases" },
  { folder: "nifi", label: "Apache NiFi", description: "Visual data flows for routing and transforming records.", tone: "stream", category: "streaming" },
  { folder: "parquet", label: "Parquet", description: "Columnar file format: encodings, row groups and predicate pushdown.", tone: "lake", category: "formats" },
  { folder: "python", label: "Python", description: "The language of most data pipelines: values, collections, iterators, files, concurrency and testing.", tone: "python", category: "languages" },
  { folder: "redis", label: "Redis", description: "In-memory data structures for caches, counters and queues.", tone: "stream", category: "databases" },
  { folder: "redshift", label: "Amazon Redshift", description: "AWS columnar warehouse: distribution keys, sort keys and COPY.", tone: "cloud", category: "warehouses" },
  { folder: "scala", label: "Scala", description: "The language behind Spark: basics for reading and writing Spark jobs.", tone: "core", category: "languages" },
  { folder: "snowflake", label: "Snowflake", description: "Cloud warehouse with virtual warehouses, micro-partitions and streams.", tone: "cloud", category: "warehouses" },
  { folder: "pyspark", label: "PySpark", description: "Spark from Python for batch and streaming: DataFrames, joins, pipelines and tuning.", tone: "core", category: "processing" },
  { folder: "sql", label: "SQL", description: "Querying and modeling data: from SELECT to window functions and time-series.", tone: "sql", category: "languages" },
  { folder: "superset", label: "Apache Superset", description: "Open-source dashboards and charts on SQL databases.", tone: "warehouse", category: "bi" },
  { folder: "tableau", label: "Tableau", description: "Visual analysis and dashboards for business users.", tone: "warehouse", category: "bi" },
  { folder: "trino", label: "Trino", description: "Federated SQL across many data sources.", tone: "cloud", category: "processing" },
];

export const TOOLS_BY_FOLDER = new Map(TOOLS.map((tool) => [tool.folder, tool]));

/** URL-safe id for a label or heading, e.g. "Data Engineering" -> "data-engineering". */
export function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
