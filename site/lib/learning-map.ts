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
    purpose: "The two languages every pipeline is written in.",
    steps: [
      {
        id: "python",
        label: "Python",
        toolHref: "/tools/python/",
        // Each lesson is followed by its drill, as the lessons' "Next" lines say.
        slugs: ["01-values-and-types", "02-collections", "03-control-flow-and-functions", "04-iterators-and-generators",
          "05-classes-and-dataclasses", "06-files-and-formats", "07-errors-logging-and-testing", "08-concurrency",
          "09-data-engineering"].flatMap((name) => [`python-${name}`, `python-drills-${name}`]),
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
    ],
  },
  {
    title: "Store",
    purpose: "Where data lives: the databases pipelines read, and the files and tables they write.",
    steps: [
      {
        id: "dataframes",
        label: "Local DataFrames",
        toolHref: "/tools/dataframes/",
        slugs: series("dataframes-", ["01-pandas", "02-polars", "03-arrow", "04-choosing-an-engine"]),
      },
      {
        id: "ingestion",
        label: "Data ingestion",
        toolHref: "/tools/ingestion/",
        slugs: series("ingestion-", ["01-batch-patterns", "02-apis", "03-object-storage", "04-dlt"]),
      },
      { id: "databases", label: "Databases", toolHref: "/tools/postgres/", slugs: ["postgres", "duckdb"] },
      { id: "parquet", label: "Parquet", toolHref: "/tools/parquet/", slugs: ["parquet"] },
      {
        id: "table-formats",
        label: "Table formats",
        toolHref: "/tools/delta/",
        slugs: ["open-table-formats", "delta", "iceberg", "lakehouse-catalogs"],
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
          "pyspark-01-how-spark-runs",
          ...["02-dataframe-essentials", "03-types-functions-and-nulls", "04-reading-and-writing-data",
            "05-spark-sql-and-the-catalog", "06-joins", "07-aggregations-and-windows",
            "08-nested-and-semi-structured-data", "09-python-udfs-and-pandas", "10-batch-pipelines",
            "11-structured-streaming"].flatMap((name) => [`pyspark-${name}`, `pyspark-drills-${name}`]),
          "pyspark-12-internals-and-monitoring",
          "pyspark-13-performance-tuning",
          "pyspark-14-production-pyspark",
          "pyspark-drills-12-execution-and-production",
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
