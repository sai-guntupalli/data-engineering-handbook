/**
 * The learning path on the home page: stages in reading order, each made of steps.
 * A step is a track of notebooks (all nine Python lessons, say), so its progress
 * means something, and the path can say which notebook to read next.
 * The build fails if a step names a notebook the registry does not list.
 */
import type { NotebookStatus } from "./progress";

export type PathStep = {
  id: string;
  label: string;
  /** Tool page for the step, site-relative. */
  toolHref: string;
  /** Notebooks in reading order. */
  slugs: string[];
};

export type PathStage = {
  title: string;
  /** One line on why this stage matters. */
  purpose: string;
  steps: PathStep[];
};

const series = (prefix: string, names: string[]) => names.map((name) => `${prefix}${name}`);

export const LEARNING_PATH: PathStage[] = [
  {
    title: "Foundations",
    purpose: "The two languages every pipeline is written in, and the DataFrame tools you use them with on one machine.",
    steps: [
      {
        id: "python",
        label: "Python",
        toolHref: "/tools/python/",
        slugs: [
          "python-00-start-here",
          "python-reference-01-values-and-numbers", "python-practice-01-values-and-numbers",
          "python-reference-02-strings-and-regex", "python-practice-02-strings-and-regex",
          "python-reference-03-lists-dicts-sets", "python-practice-03-lists-dicts-sets",
          "python-reference-04-collections-heapq-bisect", "python-practice-04-collections-heapq-bisect",
          "python-reference-05-functions-and-typing", "python-practice-05-functions-and-typing",
          "python-reference-06-iterators-and-itertools", "python-practice-06-iterators-and-itertools",
          "python-reference-07-classes-and-dataclasses", "python-practice-07-classes-and-dataclasses",
          "python-reference-08-files-paths-and-formats", "python-practice-08-files-paths-and-formats",
          "python-reference-09-dates-times-and-time-zones", "python-practice-09-dates-times-and-time-zones",
          "python-reference-10-errors-logging-and-testing", "python-practice-10-errors-logging-and-testing",
          "python-reference-11-concurrency-and-async", "python-practice-11-concurrency-and-async",
          "python-reference-12-data-engineering-patterns", "python-practice-12-data-engineering-patterns",
        ],
      },
      {
        id: "sql",
        label: "SQL",
        toolHref: "/tools/sql/",
        slugs: series("sql-", [
          "00-start-here",
          "01-basics",
          "02-joins",
          "03-null-handling",
          "04-case-expressions",
          "05-aggregations-and-ctes",
          "06-set-operations",
          "07-types-functions-and-json",
          "08-window-functions",
          "09-deduplication",
          "10-time-series",
          "11-modeling-and-optimization",
          "12-views-and-changing-data",
        ]),
      },
      {
        id: "dataframes",
        label: "Local DataFrames",
        toolHref: "/tools/dataframes/",
        slugs: series("dataframes-", ["01-pandas", "02-polars", "03-arrow", "04-choosing-an-engine"]),
      },
    ],
  },
  {
    title: "Store",
    purpose: "Where data lives, and how it gets there: the databases pipelines read, the files and tables they write, and the ingestion that loads them.",
    steps: [
      { id: "databases", label: "Databases", toolHref: "/tools/postgres/", slugs: ["postgres", "duckdb"] },
      { id: "parquet", label: "Parquet", toolHref: "/tools/parquet/", slugs: ["parquet"] },
      {
        id: "table-formats",
        label: "Table formats",
        toolHref: "/tools/delta/",
        slugs: ["open-table-formats", "delta", "iceberg", "lakehouse-catalogs"],
      },
      {
        id: "ingestion",
        label: "Data ingestion",
        toolHref: "/tools/ingestion/",
        slugs: series("ingestion-", ["01-batch-patterns", "02-apis", "03-object-storage", "04-dlt"]),
      },
    ],
  },
  {
    title: "Process at scale",
    purpose: "Run the same logic on data that does not fit on one machine.",
    steps: [
      {
        id: "pyspark",
        label: "PySpark",
        toolHref: "/tools/pyspark/",
        slugs: [
          "pyspark-00-start-here",
          "pyspark-reference-01-execution-model", "pyspark-practice-01-execution-model",
          "pyspark-reference-02-dataframe-api", "pyspark-practice-02-dataframe-api",
          "pyspark-reference-03-types-casting-and-nulls", "pyspark-practice-03-types-casting-and-nulls",
          "pyspark-reference-04-functions-strings-and-math", "pyspark-practice-04-functions-strings-and-math",
          "pyspark-reference-05-dates-and-times", "pyspark-practice-05-dates-and-times",
          "pyspark-reference-06-complex-types-and-json", "pyspark-practice-06-complex-types-and-json",
          "pyspark-reference-07-aggregations", "pyspark-practice-07-aggregations",
          "pyspark-reference-08-window-functions", "pyspark-practice-08-window-functions",
          "pyspark-reference-09-joins", "pyspark-practice-09-joins",
          "pyspark-reference-10-reading-and-writing", "pyspark-practice-10-reading-and-writing",
          "pyspark-reference-11-spark-sql-and-catalog", "pyspark-practice-11-spark-sql-and-catalog",
          "pyspark-reference-12-python-udfs-and-pandas", "pyspark-practice-12-python-udfs-and-pandas",
          "pyspark-reference-13-performance", "pyspark-practice-13-performance",
          "pyspark-reference-14-structured-streaming", "pyspark-practice-14-structured-streaming",
          "pyspark-reference-15-production-patterns", "pyspark-practice-15-production-patterns",
        ],
      },
      { id: "capstone", label: "Pipeline capstone", toolHref: "/tools/pyspark/", slugs: ["pyspark-concepts-end-to-end", "batch-lakehouse-capstone", "streaming-orders-capstone", "cdc-to-scd2-capstone"] },
    ],
  },
  {
    title: "Model and test",
    purpose: "Shape tables people can trust, and prove it with tests.",
    steps: [
      {
        id: "modeling",
        label: "Data modeling",
        toolHref: "/tools/data-modeling/",
        slugs: [
          ...series("data-modeling-", [
            "00-start-here",
            "01-grain-facts-and-dimensions",
            "02-star-schema-design",
            "03-slowly-changing-dimensions",
            "04-relationships-and-double-counting",
            "05-normalized-and-operational-models",
            "06-warehouse-architectures",
            "07-loading-and-late-data",
          ]),
          "data-modeling-drills",
          ...series("data-modeling-", ["08-physical-design-and-performance", "09-testing-metrics-and-change", "10-interview-case-studies"]),
        ],
      },
      { id: "dbt", label: "dbt", toolHref: "/tools/dbt/", slugs: ["dbt", "dbt-01-models-and-ref", "dbt-02-tests-and-contracts", "dbt-03-incremental-models", "dbt-04-snapshots", "dbt-05-microbatch", "semantic-layer"] },
      { id: "quality", label: "Data quality", toolHref: "/tools/concepts/", slugs: ["data-quality", "pandera-data-quality", "data-observability"] },
    ],
  },
  {
    title: "Orchestrate and stream",
    purpose: "Run pipelines on a schedule, then on events as they arrive.",
    steps: [
      { id: "orchestration", label: "Orchestration", toolHref: "/tools/airflow/", slugs: ["orchestration-patterns", "airflow", "airflow-01-test-a-dag", "airflow-02-assets", "airflow-03-backfill"] },
      { id: "batch-capstone", label: "Batch pipeline capstone", toolHref: "/tools/concepts/", slugs: ["end-to-end-pipeline-capstone"] },
      { id: "cdc", label: "Change data capture", toolHref: "/tools/concepts/", slugs: ["change-data-capture"] },
      { id: "kafka", label: "Kafka", toolHref: "/tools/kafka/", slugs: ["kafka", "kafka-01-log-and-partitions", "kafka-02-producers", "kafka-03-consumers-and-groups", "kafka-04-delivery-and-transactions", "kafka-05-connect-and-schemas", "stream-processing"] },
      { id: "flink", label: "Flink", toolHref: "/tools/flink/", slugs: ["flink"] },
    ],
  },
  {
    title: "Run in production",
    purpose: "Ship changes safely, control access, and keep cost and design in check.",
    steps: [
      { id: "delivery", label: "CI/CD and security", toolHref: "/tools/concepts/", slugs: ["cicd-and-iac", "security-and-iam", "data-governance"] },
      { id: "design", label: "Cost and design", toolHref: "/tools/concepts/", slugs: ["cost-optimization", "system-design"] },
    ],
  },
  {
    title: "Interview practice",
    purpose: "Check what you learned under interview conditions.",
    steps: [
      {
        id: "python-challenges",
        label: "Python challenges",
        toolHref: "/tools/python/",
        slugs: [
          ...series("python-challenges-", [
            "01-arrays-and-hashing",
            "02-two-pointers-and-sliding-window",
            "03-stacks-and-monotonic-stacks",
            "04-binary-search",
            "05-linked-lists",
            "06-binary-trees",
            "07-graphs-and-grids",
            "08-dynamic-programming",
            "09-backtracking-heaps-intervals-design",
          ]),
          "python-coding-problems",
        ],
      },
      { id: "sql-drills", label: "SQL interview drills", toolHref: "/tools/sql/", slugs: ["sql-13-interview-drills", "sql-14-interview-concepts"] },
      { id: "pyspark-interview", label: "PySpark interview", toolHref: "/tools/pyspark/", slugs: ["pyspark-15-interview-concepts", "pyspark-coding-challenges"] },
      { id: "question-bank", label: "Question bank", toolHref: "/tools/interview-questions/", slugs: ["interview-question-bank"] },
    ],
  },
];

export type StepSummary = { done: number; total: number; status: NotebookStatus };

/** A step is done when every notebook is done, started when any notebook is touched. */
export function summarizeStep(statuses: NotebookStatus[]): StepSummary {
  const done = statuses.filter((status) => status === "done").length;
  const touched = statuses.some((status) => status !== "not-started");
  const status: NotebookStatus = done === statuses.length ? "done" : touched ? "in-progress" : "not-started";
  return { done, total: statuses.length, status };
}

export type NextUp = { stageIndex: number; stepIndex: number; slug: string };

/** The first unfinished notebook along the path, or null when the whole path is done. */
export function nextUp(stages: PathStage[], statusOf: (slug: string) => NotebookStatus): NextUp | null {
  for (const [stageIndex, stage] of stages.entries()) {
    for (const [stepIndex, step] of stage.steps.entries()) {
      const slug = step.slugs.find((candidate) => statusOf(candidate) !== "done");
      if (slug) return { stageIndex, stepIndex, slug };
    }
  }
  return null;
}

/** Problems that would draw a broken path; empty when the path is valid. */
export function validatePath(stages: PathStage[], knownSlugs: Set<string>): string[] {
  const problems: string[] = [];
  const seen = new Set<string>();
  const ids = new Set<string>();
  for (const stage of stages) {
    if (stage.steps.length === 0) problems.push(`stage "${stage.title}" has no steps`);
    for (const step of stage.steps) {
      if (ids.has(step.id)) problems.push(`step id "${step.id}" is used twice`);
      ids.add(step.id);
      if (step.slugs.length === 0) problems.push(`step "${step.id}" has no notebooks`);
      for (const slug of step.slugs) {
        if (!knownSlugs.has(slug)) problems.push(`${slug} is not a registered notebook`);
        if (seen.has(slug)) problems.push(`${slug} appears more than once`);
        seen.add(slug);
      }
    }
  }
  return problems;
}
