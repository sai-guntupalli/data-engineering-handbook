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
    slug: "pyspark-01-how-spark-runs",
    repoPath: "notebooks/topics/pyspark/pyspark-01-how-spark-runs.ipynb",
    movedTo: "pyspark-reference-01-execution-model",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-01-execution-model.ipynb",
    note: "PySpark 1: how Spark runs your code is now part of PySpark reference 1: execution model.",
  },
  {
    slug: "pyspark-02-dataframe-essentials",
    repoPath: "notebooks/topics/pyspark/pyspark-02-dataframe-essentials.ipynb",
    movedTo: "pyspark-reference-02-dataframe-api",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-02-dataframe-api.ipynb",
    note: "PySpark 2: DataFrame essentials is now part of PySpark reference 2: DataFrame API.",
  },
  {
    slug: "pyspark-03-types-functions-and-nulls",
    repoPath: "notebooks/topics/pyspark/pyspark-03-types-functions-and-nulls.ipynb",
    movedTo: "pyspark-reference-03-types-casting-and-nulls",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-03-types-casting-and-nulls.ipynb",
    note: "PySpark 3: types, functions and nulls is now part of PySpark reference 3: types, casting and nulls.",
  },
  {
    slug: "pyspark-04-reading-and-writing-data",
    repoPath: "notebooks/topics/pyspark/pyspark-04-reading-and-writing-data.ipynb",
    movedTo: "pyspark-reference-10-reading-and-writing",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-10-reading-and-writing.ipynb",
    note: "PySpark 4: reading and writing data is now part of PySpark reference 10: reading and writing data.",
  },
  {
    slug: "pyspark-05-spark-sql-and-the-catalog",
    repoPath: "notebooks/topics/pyspark/pyspark-05-spark-sql-and-the-catalog.ipynb",
    movedTo: "pyspark-reference-11-spark-sql-and-catalog",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-11-spark-sql-and-catalog.ipynb",
    note: "PySpark 5: Spark SQL and the catalog is now part of PySpark reference 11: Spark SQL and the catalog.",
  },
  {
    slug: "pyspark-06-joins",
    repoPath: "notebooks/topics/pyspark/pyspark-06-joins.ipynb",
    movedTo: "pyspark-reference-09-joins",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-09-joins.ipynb",
    note: "PySpark 6: joins is now part of PySpark reference 9: joins.",
  },
  {
    slug: "pyspark-07-aggregations-and-windows",
    repoPath: "notebooks/topics/pyspark/pyspark-07-aggregations-and-windows.ipynb",
    movedTo: "pyspark-reference-07-aggregations",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-07-aggregations.ipynb",
    note: "PySpark 7: aggregations and windows is now part of PySpark reference 7: aggregations.",
  },
  {
    slug: "pyspark-08-nested-and-semi-structured-data",
    repoPath: "notebooks/topics/pyspark/pyspark-08-nested-and-semi-structured-data.ipynb",
    movedTo: "pyspark-reference-06-complex-types-and-json",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-06-complex-types-and-json.ipynb",
    note: "PySpark 8: nested and semi-structured data is now part of PySpark reference 6: complex types and JSON.",
  },
  {
    slug: "pyspark-09-python-udfs-and-pandas",
    repoPath: "notebooks/topics/pyspark/pyspark-09-python-udfs-and-pandas.ipynb",
    movedTo: "pyspark-reference-12-python-udfs-and-pandas",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-12-python-udfs-and-pandas.ipynb",
    note: "PySpark 9: Python UDFs and pandas is now part of PySpark reference 12: Python UDFs, pandas and Arrow.",
  },
  {
    slug: "pyspark-10-batch-pipelines",
    repoPath: "notebooks/topics/pyspark/pyspark-10-batch-pipelines.ipynb",
    movedTo: "pyspark-reference-15-production-patterns",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-15-production-patterns.ipynb",
    note: "PySpark 10: batch pipelines is now part of PySpark reference 15: production patterns.",
  },
  {
    slug: "pyspark-11-structured-streaming",
    repoPath: "notebooks/topics/pyspark/pyspark-11-structured-streaming.ipynb",
    movedTo: "pyspark-reference-14-structured-streaming",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-14-structured-streaming.ipynb",
    note: "PySpark 11: structured streaming is now part of PySpark reference 14: Structured Streaming.",
  },
  {
    slug: "pyspark-12-internals-and-monitoring",
    repoPath: "notebooks/topics/pyspark/pyspark-12-internals-and-monitoring.ipynb",
    movedTo: "pyspark-reference-13-performance",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-13-performance.ipynb",
    note: "PySpark 12: internals and monitoring is now part of PySpark reference 13: performance and optimization.",
  },
  {
    slug: "pyspark-13-performance-tuning",
    repoPath: "notebooks/topics/pyspark/pyspark-13-performance-tuning.ipynb",
    movedTo: "pyspark-reference-13-performance",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-13-performance.ipynb",
    note: "PySpark 13: performance tuning is now part of PySpark reference 13: performance and optimization.",
  },
  {
    slug: "pyspark-14-production-pyspark",
    repoPath: "notebooks/topics/pyspark/pyspark-14-production-pyspark.ipynb",
    movedTo: "pyspark-reference-15-production-patterns",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-15-production-patterns.ipynb",
    note: "PySpark 14: production PySpark is now part of PySpark reference 15: production patterns.",
  },
  {
    slug: "pyspark-window-functions",
    repoPath: "notebooks/topics/pyspark/pyspark-window-functions.ipynb",
    movedTo: "pyspark-reference-08-window-functions",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-08-window-functions.ipynb",
    note: "PySpark window functions is now part of PySpark reference 8: window functions.",
  },
  {
    slug: "pyspark-functions-reference",
    repoPath: "notebooks/topics/pyspark/pyspark-functions-reference.ipynb",
    movedTo: "pyspark-reference-04-functions-strings-and-math",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-04-functions-strings-and-math.ipynb",
    note: "PySpark functions reference is now part of PySpark reference 4: functions for strings, math and conditions.",
  },
  {
    slug: "pyspark-reference",
    repoPath: "notebooks/topics/pyspark/pyspark-reference.ipynb",
    movedTo: "pyspark-00-start-here",
    movedToPath: "notebooks/topics/pyspark/pyspark-00-start-here.ipynb",
    note: "PySpark reference was replaced by the PySpark cookbook; PySpark 0 lists every reference and practice notebook.",
  },
  {
    slug: "pyspark-drills-02-dataframe-essentials",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-02-dataframe-essentials.ipynb",
    movedTo: "pyspark-practice-02-dataframe-api",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-02-dataframe-api.ipynb",
    note: "PySpark drills 2: DataFrame essentials is now part of PySpark practice 2: DataFrame API.",
  },
  {
    slug: "pyspark-drills-03-types-functions-and-nulls",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-03-types-functions-and-nulls.ipynb",
    movedTo: "pyspark-practice-03-types-casting-and-nulls",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-03-types-casting-and-nulls.ipynb",
    note: "PySpark drills 3: types, functions and nulls is now part of PySpark practice 3: types, casting and nulls.",
  },
  {
    slug: "pyspark-drills-04-reading-and-writing-data",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-04-reading-and-writing-data.ipynb",
    movedTo: "pyspark-practice-10-reading-and-writing",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-10-reading-and-writing.ipynb",
    note: "PySpark drills 4: reading and writing data is now part of PySpark practice 10: reading and writing data.",
  },
  {
    slug: "pyspark-drills-05-spark-sql-and-the-catalog",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-05-spark-sql-and-the-catalog.ipynb",
    movedTo: "pyspark-practice-11-spark-sql-and-catalog",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-11-spark-sql-and-catalog.ipynb",
    note: "PySpark drills 5: Spark SQL and the catalog is now part of PySpark practice 11: Spark SQL and the catalog.",
  },
  {
    slug: "pyspark-drills-06-joins",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-06-joins.ipynb",
    movedTo: "pyspark-practice-09-joins",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-09-joins.ipynb",
    note: "PySpark drills 6: joins is now part of PySpark practice 9: joins.",
  },
  {
    slug: "pyspark-drills-07-aggregations-and-windows",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-07-aggregations-and-windows.ipynb",
    movedTo: "pyspark-practice-07-aggregations",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-07-aggregations.ipynb",
    note: "PySpark drills 7: aggregations and windows is now part of PySpark practice 7: aggregations.",
  },
  {
    slug: "pyspark-drills-08-nested-and-semi-structured-data",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-08-nested-and-semi-structured-data.ipynb",
    movedTo: "pyspark-practice-06-complex-types-and-json",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-06-complex-types-and-json.ipynb",
    note: "PySpark drills 8: nested and semi-structured data is now part of PySpark practice 6: complex types and JSON.",
  },
  {
    slug: "pyspark-drills-09-python-udfs-and-pandas",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-09-python-udfs-and-pandas.ipynb",
    movedTo: "pyspark-practice-12-python-udfs-and-pandas",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-12-python-udfs-and-pandas.ipynb",
    note: "PySpark drills 9: Python UDFs and pandas is now part of PySpark practice 12: Python UDFs, pandas and Arrow.",
  },
  {
    slug: "pyspark-drills-10-batch-pipelines",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-10-batch-pipelines.ipynb",
    movedTo: "pyspark-practice-15-production-patterns",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-15-production-patterns.ipynb",
    note: "PySpark drills 10: batch pipelines is now part of PySpark practice 15: production patterns.",
  },
  {
    slug: "pyspark-drills-11-structured-streaming",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-11-structured-streaming.ipynb",
    movedTo: "pyspark-practice-14-structured-streaming",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-14-structured-streaming.ipynb",
    note: "PySpark drills 11: structured streaming is now part of PySpark practice 14: Structured Streaming.",
  },
  {
    slug: "pyspark-drills-12-execution-and-production",
    repoPath: "notebooks/topics/pyspark/pyspark-drills-12-execution-and-production.ipynb",
    movedTo: "pyspark-practice-01-execution-model",
    movedToPath: "notebooks/topics/pyspark/pyspark-practice-01-execution-model.ipynb",
    note: "PySpark drills: execution and production is now part of PySpark practice 1: execution model.",
  },
  {
    slug: "data-warehousing",
    repoPath: "notebooks/topics/concepts/data-warehousing.ipynb",
    movedTo: "data-modeling-06-warehouse-architectures",
    movedToPath: "notebooks/topics/data-modeling/data-modeling-06-warehouse-architectures.ipynb",
    note: "Data warehousing architecture is now Data modeling 6: warehouse architectures.",
  },
  {
    slug: "data-modeling",
    repoPath: "notebooks/topics/concepts/data-modeling.ipynb",
    movedTo: "data-modeling-00-start-here",
    movedToPath: "notebooks/topics/data-modeling/data-modeling-00-start-here.ipynb",
    note: "Data modeling and warehousing is now its own section of eleven lessons, drills and a reference; start with Data modeling 0.",
  },
  {
    slug: "pyspark-tuning",
    repoPath: "notebooks/topics/pyspark/pyspark-tuning.ipynb",
    movedTo: "pyspark-reference-13-performance",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-13-performance.ipynb",
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
    movedTo: "pyspark-reference-01-execution-model",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-01-execution-model.ipynb",
    note: "PySpark foundations is now PySpark 1: how Spark runs your code.",
  },
  {
    slug: "pyspark-02-reading-sql-and-cleaning",
    repoPath: "notebooks/topics/pyspark/pyspark-02-reading-sql-and-cleaning.ipynb",
    movedTo: "pyspark-reference-10-reading-and-writing",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-10-reading-and-writing.ipynb",
    note: "Reading, SQL and cleaning was split into PySpark 3, 4 and 5; file reading is in PySpark 4.",
  },
  {
    slug: "pyspark-03-joins-and-aggregations",
    repoPath: "notebooks/topics/pyspark/pyspark-03-joins-and-aggregations.ipynb",
    movedTo: "pyspark-reference-09-joins",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-09-joins.ipynb",
    note: "Joins and aggregations was split into PySpark 6: joins and PySpark 7: aggregations and windows.",
  },
  {
    slug: "pyspark-04-windows-and-nested-data",
    repoPath: "notebooks/topics/pyspark/pyspark-04-windows-and-nested-data.ipynb",
    movedTo: "pyspark-reference-07-aggregations",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-07-aggregations.ipynb",
    note: "Windows and nested data was split into PySpark 7: aggregations and windows and PySpark 8: nested data.",
  },
  {
    slug: "pyspark-05-writing-pipelines-and-quality",
    repoPath: "notebooks/topics/pyspark/pyspark-05-writing-pipelines-and-quality.ipynb",
    movedTo: "pyspark-reference-15-production-patterns",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-15-production-patterns.ipynb",
    note: "Writing, pipelines and quality is now PySpark 10: batch pipelines; UDFs moved to PySpark 9.",
  },
  {
    slug: "pyspark-06-structured-streaming",
    repoPath: "notebooks/topics/pyspark/pyspark-06-structured-streaming.ipynb",
    movedTo: "pyspark-reference-14-structured-streaming",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-14-structured-streaming.ipynb",
    note: "Structured streaming is now PySpark 11.",
  },
  {
    slug: "pyspark-07-monitoring-and-performance",
    repoPath: "notebooks/topics/pyspark/pyspark-07-monitoring-and-performance.ipynb",
    movedTo: "pyspark-reference-13-performance",
    movedToPath: "notebooks/topics/pyspark/pyspark-reference-13-performance.ipynb",
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
