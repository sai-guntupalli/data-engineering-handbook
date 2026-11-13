/**
 * Notebooks merged into others, or renumbered. Their old reader URLs still resolve: the build
 * writes a small page at /notebooks/<old slug>/ that redirects to the notebook
 * that now holds the content. Saved progress and stars move to the new notebook.
 */
export type RetiredNotebook = {
  /** Old reader URL segment. */
  slug: string;
  /** Old repository path, the key progress and stars were saved under. */
  repoPath: string;
  /** Slug of the notebook that now holds the content. */
  movedTo: string;
  /** Repository path of that notebook. */
  movedToPath: string;
  /** One line on what happened, shown on the redirect page. */
  note: string;
};

export const RETIRED_NOTEBOOKS: RetiredNotebook[] = [
  {
    slug: "data-warehousing",
    repoPath: "notebooks/topics/concepts/data-warehousing.ipynb",
    movedTo: "data-modeling",
    movedToPath: "notebooks/topics/concepts/data-modeling.ipynb",
    note: "Data warehousing architecture is now part of Data modeling and warehousing.",
  },
  {
    slug: "pyspark-tuning",
    repoPath: "notebooks/topics/pyspark/pyspark-tuning.ipynb",
    movedTo: "pyspark-13-performance-tuning",
    movedToPath: "notebooks/topics/pyspark/pyspark-13-performance-tuning.ipynb",
    note: "Spark tuning is now PySpark 13: performance tuning.",
  },
  {
    slug: "pyspark-00-overview",
    repoPath: "notebooks/topics/pyspark/pyspark-00-overview.ipynb",
    movedTo: "pyspark-00-start-here",
    movedToPath: "notebooks/topics/pyspark/pyspark-00-start-here.ipynb",
    note: "The PySpark overview is now PySpark 0: start here.",
  },
  {
    slug: "pyspark-01-foundations",
    repoPath: "notebooks/topics/pyspark/pyspark-01-foundations.ipynb",
    movedTo: "pyspark-01-how-spark-runs",
    movedToPath: "notebooks/topics/pyspark/pyspark-01-how-spark-runs.ipynb",
    note: "PySpark foundations is now PySpark 1: how Spark runs your code.",
  },
  {
    slug: "pyspark-02-reading-sql-and-cleaning",
    repoPath: "notebooks/topics/pyspark/pyspark-02-reading-sql-and-cleaning.ipynb",
    movedTo: "pyspark-04-reading-and-writing-data",
    movedToPath: "notebooks/topics/pyspark/pyspark-04-reading-and-writing-data.ipynb",
    note: "Reading, SQL and cleaning was split into PySpark 3, 4 and 5; file reading is in PySpark 4.",
  },
  {
    slug: "pyspark-03-joins-and-aggregations",
    repoPath: "notebooks/topics/pyspark/pyspark-03-joins-and-aggregations.ipynb",
    movedTo: "pyspark-06-joins",
    movedToPath: "notebooks/topics/pyspark/pyspark-06-joins.ipynb",
    note: "Joins and aggregations was split into PySpark 6: joins and PySpark 7: aggregations and windows.",
  },
  {
    slug: "pyspark-04-windows-and-nested-data",
    repoPath: "notebooks/topics/pyspark/pyspark-04-windows-and-nested-data.ipynb",
    movedTo: "pyspark-07-aggregations-and-windows",
    movedToPath: "notebooks/topics/pyspark/pyspark-07-aggregations-and-windows.ipynb",
    note: "Windows and nested data was split into PySpark 7: aggregations and windows and PySpark 8: nested data.",
  },
  {
    slug: "pyspark-05-writing-pipelines-and-quality",
    repoPath: "notebooks/topics/pyspark/pyspark-05-writing-pipelines-and-quality.ipynb",
    movedTo: "pyspark-10-batch-pipelines",
    movedToPath: "notebooks/topics/pyspark/pyspark-10-batch-pipelines.ipynb",
    note: "Writing, pipelines and quality is now PySpark 10: batch pipelines; UDFs moved to PySpark 9.",
  },
  {
    slug: "pyspark-06-structured-streaming",
    repoPath: "notebooks/topics/pyspark/pyspark-06-structured-streaming.ipynb",
    movedTo: "pyspark-11-structured-streaming",
    movedToPath: "notebooks/topics/pyspark/pyspark-11-structured-streaming.ipynb",
    note: "Structured streaming is now PySpark 11.",
  },
  {
    slug: "pyspark-07-monitoring-and-performance",
    repoPath: "notebooks/topics/pyspark/pyspark-07-monitoring-and-performance.ipynb",
    movedTo: "pyspark-13-performance-tuning",
    movedToPath: "notebooks/topics/pyspark/pyspark-13-performance-tuning.ipynb",
    note: "Monitoring and performance was split into PySpark 12: internals and monitoring and PySpark 13: performance tuning.",
  },
  {
    slug: "pyspark-08-real-world-and-interviews",
    repoPath: "notebooks/topics/pyspark/pyspark-08-real-world-and-interviews.ipynb",
    movedTo: "pyspark-15-interview-concepts",
    movedToPath: "notebooks/topics/pyspark/pyspark-15-interview-concepts.ipynb",
    note: "Real-world use cases moved to PySpark 14: production PySpark; interview questions are in PySpark 15.",
  },
  {
    slug: "python-interview-basics",
    repoPath: "notebooks/topics/python/practice/python-interview-basics.ipynb",
    movedTo: "python-01-values-and-types",
    movedToPath: "notebooks/topics/python/learning/python-01-values-and-types.ipynb",
    note: "Python interview basics was folded into the Python lessons; its interview questions are in Python coding problems.",
  },
  {
    slug: "sql-06-joins",
    repoPath: "notebooks/topics/sql/sql-06-joins.ipynb",
    movedTo: "sql-02-joins",
    movedToPath: "notebooks/topics/sql/sql-02-joins.ipynb",
    note: "SQL 6: joins is now SQL 2: joins. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
  {
    slug: "sql-04-null-handling",
    repoPath: "notebooks/topics/sql/sql-04-null-handling.ipynb",
    movedTo: "sql-03-null-handling",
    movedToPath: "notebooks/topics/sql/sql-03-null-handling.ipynb",
    note: "SQL 4: NULL handling is now SQL 3: NULL handling. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
  {
    slug: "sql-05-case-expressions",
    repoPath: "notebooks/topics/sql/sql-05-case-expressions.ipynb",
    movedTo: "sql-04-case-expressions",
    movedToPath: "notebooks/topics/sql/sql-04-case-expressions.ipynb",
    note: "SQL 5: CASE expressions is now SQL 4: CASE expressions. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
  {
    slug: "sql-02-aggregations-and-ctes",
    repoPath: "notebooks/topics/sql/sql-02-aggregations-and-ctes.ipynb",
    movedTo: "sql-05-aggregations-and-ctes",
    movedToPath: "notebooks/topics/sql/sql-05-aggregations-and-ctes.ipynb",
    note: "SQL 2: aggregations and CTEs is now SQL 5: aggregations and CTEs. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
  {
    slug: "sql-07-set-operations",
    repoPath: "notebooks/topics/sql/sql-07-set-operations.ipynb",
    movedTo: "sql-06-set-operations",
    movedToPath: "notebooks/topics/sql/sql-06-set-operations.ipynb",
    note: "SQL 7: set operations is now SQL 6: set operations. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
  {
    slug: "sql-03-types-functions-and-json",
    repoPath: "notebooks/topics/sql/sql-03-types-functions-and-json.ipynb",
    movedTo: "sql-07-types-functions-and-json",
    movedToPath: "notebooks/topics/sql/sql-07-types-functions-and-json.ipynb",
    note: "SQL 3: types, functions and JSON is now SQL 7: types, functions and JSON. The SQL chapters were renumbered so joins come before the chapters that use them.",
  },
];

export const RETIRED_BY_SLUG = new Map(RETIRED_NOTEBOOKS.map((retired) => [retired.slug, retired]));

/** Old repository path -> new one, for migrating progress and stars saved before a merge. */
export const RETIRED_PATHS: ReadonlyMap<string, string> = new Map(
  RETIRED_NOTEBOOKS.map((retired) => [retired.repoPath, retired.movedToPath]),
);

/** Stars saved under an old path count for the notebook that replaced it. */
export function migrateStarred(paths: Iterable<string>, renames: ReadonlyMap<string, string> = RETIRED_PATHS): Set<string> {
  return new Set([...paths].map((repoPath) => renames.get(repoPath) ?? repoPath));
}
