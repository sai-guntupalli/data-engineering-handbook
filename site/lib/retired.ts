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
    movedTo: "pyspark-07-monitoring-and-performance",
    movedToPath: "notebooks/topics/pyspark/pyspark-07-monitoring-and-performance.ipynb",
    note: "Spark tuning is now part of PySpark 7: monitoring, performance and tuning.",
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
