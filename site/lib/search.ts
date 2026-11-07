/** What the search matches on. Both the header suggestions and /search use this module. */
export type SearchableNotebook = {
  repoPath: string;
  slug: string;
  title: string;
  description: string;
  groupLabel: string;
  githubHref: string;
};

/** 0: title starts with the query, 1: title contains it, 2: another field contains it, null: no match. */
function rankOf(notebook: SearchableNotebook, needle: string): number | null {
  const title = notebook.title.toLowerCase();
  if (title.startsWith(needle)) return 0;
  if (title.includes(needle)) return 1;
  const others = [notebook.description, notebook.slug, notebook.repoPath, notebook.groupLabel];
  return others.some((field) => field.toLowerCase().includes(needle)) ? 2 : null;
}

/** Notebooks matching the query, best match first. Empty for a blank query. */
export function matchNotebooks<T extends SearchableNotebook>(notebooks: T[], query: string): T[] {
  const needle = query.trim().toLowerCase();
  if (!needle) return [];
  return notebooks
    .flatMap((notebook, position) => {
      const rank = rankOf(notebook, needle);
      return rank === null ? [] : [{ notebook, rank, position }];
    })
    .sort((a, b) => a.rank - b.rank || a.position - b.position)
    .map(({ notebook }) => notebook);
}
