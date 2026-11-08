/**
 * Search over notebooks and their sections. The command palette loads the
 * entries from /search-index.json; /search ranks notebooks with the same rules.
 */
import type { GroupTone } from "./notebook-groups";

export type SearchEntry = {
  kind: "notebook" | "section";
  repoPath: string;
  /** Notebook title for a notebook, heading text for a section. */
  title: string;
  notebookTitle: string;
  groupLabel: string;
  tone: GroupTone;
  monogram: string;
  snippet: string;
  /** Site-relative link, without the base path. */
  href: string;
  colabHref: string;
};

export type SearchResults = { notebooks: SearchEntry[]; sections: SearchEntry[]; total: number };

/** Fields a notebook-only search needs (the /search page). */
export type SearchableNotebook = {
  repoPath: string;
  title: string;
  description: string;
  groupLabel: string;
};

function wordsOf(query: string): string[] {
  return query.trim().toLowerCase().split(/\s+/).filter(Boolean);
}

/**
 * 0: title starts with the query, 1: title contains it, 2: every word is in the
 * title, 3: every word is somewhere in the other fields, null: no match.
 */
function rankText(title: string, others: string[], query: string, words: string[]): number | null {
  const lowerTitle = title.toLowerCase();
  const phrase = query.trim().toLowerCase();
  if (lowerTitle.startsWith(phrase)) return 0;
  if (lowerTitle.includes(phrase)) return 1;
  if (words.every((word) => lowerTitle.includes(word))) return 2;
  const haystack = `${lowerTitle} ${others.join(" ").toLowerCase()}`;
  return words.every((word) => haystack.includes(word)) ? 3 : null;
}

function ranked<T>(items: T[], rankOf: (item: T) => number | null): T[] {
  return items
    .flatMap((item, position) => {
      const rank = rankOf(item);
      return rank === null ? [] : [{ item, rank, position }];
    })
    .sort((a, b) => a.rank - b.rank || a.position - b.position)
    .map(({ item }) => item);
}

/** Notebooks matching the query, best match first. Empty for a blank query. */
export function matchNotebooks<T extends SearchableNotebook>(notebooks: T[], query: string): T[] {
  const words = wordsOf(query);
  if (words.length === 0) return [];
  return ranked(notebooks, (notebook) =>
    rankText(notebook.title, [notebook.description, notebook.groupLabel, notebook.repoPath], query, words),
  );
}

/** Palette search: best notebooks and sections, each list capped. */
export function searchEntries(
  entries: SearchEntry[],
  query: string,
  limits: { notebooks: number; sections: number },
): SearchResults {
  const words = wordsOf(query);
  if (words.length === 0) return { notebooks: [], sections: [], total: 0 };
  const matches = ranked(entries, (entry) =>
    rankText(entry.title, [entry.notebookTitle, entry.groupLabel, entry.snippet], query, words),
  );
  const notebooks = matches.filter((entry) => entry.kind === "notebook");
  const sections = matches.filter((entry) => entry.kind === "section");
  return {
    notebooks: notebooks.slice(0, limits.notebooks),
    sections: sections.slice(0, limits.sections),
    total: matches.length,
  };
}

/** Split text around case-insensitive occurrences of the query words, for <mark>. */
export function highlightParts(text: string, query: string): { text: string; match: boolean }[] {
  const words = wordsOf(query).map((word) => word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  if (words.length === 0) return [{ text, match: false }];
  const pattern = new RegExp(`(${words.join("|")})`, "gi");
  return text
    .split(pattern)
    .filter(Boolean)
    .map((part) => ({ text: part, match: words.some((word) => new RegExp(`^${word}$`, "i").test(part)) }));
}
