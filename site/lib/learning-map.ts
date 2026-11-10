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
        slugs: series("python-", [
          "01-values-and-types",
          "02-collections",
          "03-control-flow-and-functions",
          "04-iterators-and-generators",
          "05-classes-and-dataclasses",
          "06-files-and-formats",
          "07-errors-logging-and-testing",
          "08-concurrency",
          "09-data-engineering",
        ]),
      },
      {
        id: "sql",
        label: "SQL",
        toolHref: "/tools/sql/",
        slugs: series("sql-", [
          "00-start-here",
          "01-basics",
          "02-aggregations-and-ctes",
          "03-types-functions-and-json",
          "04-null-handling",
          "05-case-expressions",
          "06-joins",
          "07-set-operations",
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
    title: "Process at scale",
    purpose: "Run the same logic on data that does not fit on one machine.",
    steps: [
      {
        id: "pyspark",
        label: "PySpark",
        toolHref: "/tools/pyspark/",
        slugs: series("pyspark-", [
          "00-overview",
          "01-foundations",
          "02-reading-sql-and-cleaning",
          "03-joins-and-aggregations",
          "04-windows-and-nested-data",
          "05-writing-pipelines-and-quality",
          "06-structured-streaming",
          "07-monitoring-and-performance",
          "08-real-world-and-interviews",
        ]),
      },
    ],
  },
  {
    title: "Model and test",
    purpose: "Shape tables people can trust, and prove it with tests.",
    steps: [
      { id: "modeling", label: "Data modeling", toolHref: "/tools/concepts/", slugs: ["data-modeling"] },
      { id: "dbt", label: "dbt", toolHref: "/tools/dbt/", slugs: ["dbt"] },
      { id: "quality", label: "Data quality", toolHref: "/tools/concepts/", slugs: ["data-quality", "data-observability"] },
    ],
  },
  {
    title: "Store",
    purpose: "File and table formats that keep data cheap, fast and correct.",
    steps: [
      { id: "parquet", label: "Parquet", toolHref: "/tools/parquet/", slugs: ["parquet"] },
      { id: "delta", label: "Delta Lake", toolHref: "/tools/delta/", slugs: ["delta"] },
      { id: "iceberg", label: "Iceberg", toolHref: "/tools/iceberg/", slugs: ["iceberg"] },
    ],
  },
  {
    title: "Orchestrate and stream",
    purpose: "Run pipelines on a schedule, then on events as they arrive.",
    steps: [
      { id: "airflow", label: "Airflow", toolHref: "/tools/airflow/", slugs: ["airflow"] },
      { id: "kafka", label: "Kafka", toolHref: "/tools/kafka/", slugs: ["kafka"] },
      { id: "flink", label: "Flink", toolHref: "/tools/flink/", slugs: ["flink"] },
    ],
  },
  {
    title: "Interview practice",
    purpose: "Check what you learned under interview conditions.",
    steps: [
      {
        id: "python-drills",
        label: "Python drills",
        toolHref: "/tools/python/",
        slugs: series("python-drills-", [
          "01-values-and-types",
          "02-collections",
          "03-control-flow-and-functions",
          "04-iterators-and-generators",
          "05-classes-and-dataclasses",
          "06-files-and-formats",
          "07-errors-logging-and-testing",
          "08-concurrency",
          "09-data-engineering",
        ]),
      },
      { id: "sql-drills", label: "SQL interview drills", toolHref: "/tools/sql/", slugs: ["sql-13-interview-drills", "sql-14-interview-concepts"] },
      {
        id: "question-bank",
        label: "Question bank",
        toolHref: "/tools/interview-questions/",
        slugs: ["interview-question-bank", "pyspark-concepts-end-to-end"],
      },
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
