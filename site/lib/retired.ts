/**
 * Notebooks merged into others. Their old reader URLs still resolve: the build
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
