import fs from "node:fs";
import path from "node:path";
import { ALL_GROUPS, type NotebookGroup } from "./notebook-groups";
import type { SearchableNotebook } from "./search";
import { branch, repository } from "./site";

export type NotebookSummary = {
  /** Repository-relative path, e.g. notebooks/topics/spark.ipynb */
  repoPath: string;
  /** File name without the extension, e.g. spark */
  slug: string;
  title: string;
  description: string;
  githubHref: string;
  /** Opens this notebook in Google Colab (repository must stay public). */
  colabHref: string;
};

export type NotebookListItem = NotebookSummary & { groupLabel: string };

export type NotebookGroupView = {
  label: string;
  notebooks: NotebookListItem[];
};

const GITHUB_BLOB = `https://github.com/${repository}/blob/${branch}`;
// Google Colab can only open notebooks from public repositories. The handbook
// is public, so every card gets a Colab permalink next to the GitHub link.
const COLAB_HREF = "https://colab.research.google.com/github";

// The app lives in site/; the notebooks are the repository's top-level content.
const repoRoot = path.resolve(process.cwd(), "..");
const notebooksRoot = path.join(repoRoot, "notebooks");

function sourceToString(source: string | string[] | undefined): string {
  if (Array.isArray(source)) return source.join("");
  return source ?? "";
}

function titleFromMarkdown(markdown: string, fallback: string): string {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  if (match?.[1]) return match[1].trim();
  return fallback.replace(/^\d+_/, "").replaceAll("_", " ").replaceAll("-", " ");
}

/** Turn inline markdown (code spans, links, images, emphasis) into plain text. */
function inlineToText(line: string): string {
  return line
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .trim();
}

const MAX_DESCRIPTION_LENGTH = 160;

/** Cut at the last whole word that fits, then mark the cut with an ellipsis. */
function truncateAtWord(text: string, limit: number): string {
  if (text.length <= limit) return text;
  const cut = text.slice(0, limit);
  const lastSpace = cut.lastIndexOf(" ");
  return `${cut.slice(0, lastSpace > 0 ? lastSpace : limit).trimEnd()}…`;
}

/** First real paragraph after the title, used as a card description. */
function descriptionFromMarkdown(markdown: string): string {
  let seenTitle = false;
  for (const raw of markdown.split("\n")) {
    const line = raw.trim();
    if (line.startsWith("#")) {
      seenTitle = true;
      continue;
    }
    if (!seenTitle || !line) continue;
    // Skip badges, links, images, lists, quotes, tables, fenced code and HTML.
    if (/^[+\-*[>|`<]/.test(line)) continue;
    const plain = inlineToText(line);
    if (plain.length < 25) continue;
    return truncateAtWord(plain, MAX_DESCRIPTION_LENGTH);
  }
  return "";
}

function listNotebookFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .flatMap((entry) => {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) return listNotebookFiles(full);
      return entry.name.endsWith(".ipynb") ? [full] : [];
    })
    .sort();
}

type RawCell = { cell_type?: string; source?: string | string[] };
type RawNotebook = { cells?: RawCell[] };

function readSummary(file: string): NotebookSummary {
  let notebook: RawNotebook;
  try {
    notebook = JSON.parse(fs.readFileSync(file, "utf8")) as RawNotebook;
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Could not parse notebook ${path.relative(repoRoot, file)}: ${reason}`);
  }
  const markdown = (notebook.cells ?? [])
    .filter((cell) => (cell.cell_type ?? "markdown") === "markdown")
    .map((cell) => sourceToString(cell.source))
    .join("\n\n");
  const repoPath = path.relative(repoRoot, file).split(path.sep).join("/");
  const filename = path.basename(file, ".ipynb");

  return {
    repoPath,
    slug: filename,
    title: titleFromMarkdown(markdown, filename),
    description: descriptionFromMarkdown(markdown),
    githubHref: `${GITHUB_BLOB}/${repoPath}`,
    colabHref: `${COLAB_HREF}/${repository}/blob/${branch}/${repoPath}`,
  };
}

let cachedSummaries: NotebookSummary[] | undefined;

/** Parsed once per build; the notebooks tree is static repository content. */
function allSummaries(): NotebookSummary[] {
  cachedSummaries ??= listNotebookFiles(notebooksRoot).map(readSummary);
  return cachedSummaries;
}

/**
 * Fail the build when the registry (lib/notebook-groups.ts) and the notebook files
 * disagree: a registered slug with no file (a typo would hide its card), a file no
 * group lists, or a slug listed twice.
 */
function assertRegistryMatchesFiles(summaries: NotebookSummary[]): void {
  const onDisk = new Set(summaries.map((notebook) => notebook.repoPath));
  const registered = new Set<string>();
  const problems: string[] = [];
  for (const group of ALL_GROUPS) {
    for (const slug of group.slugs) {
      const repoPath = `${group.folder}/${slug}.ipynb`;
      if (registered.has(repoPath)) problems.push(`${repoPath} is registered more than once`);
      registered.add(repoPath);
      if (!onDisk.has(repoPath)) problems.push(`${repoPath} is missing (group "${group.label}")`);
    }
  }
  for (const repoPath of onDisk) {
    if (!registered.has(repoPath)) problems.push(`${repoPath} is not listed in lib/notebook-groups.ts`);
  }
  if (problems.length > 0) {
    throw new Error(`lib/notebook-groups.ts issues:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
}

function notebooksOf(summaries: NotebookSummary[], group: NotebookGroup): NotebookListItem[] {
  const byPath = new Map(summaries.map((notebook) => [notebook.repoPath, notebook]));
  return group.slugs.flatMap((slug) => {
    const notebook = byPath.get(`${group.folder}/${slug}.ipynb`);
    return notebook ? [{ ...notebook, groupLabel: group.label }] : [];
  });
}

export function getNotebookGroups(): NotebookGroupView[] {
  const summaries = allSummaries();
  assertRegistryMatchesFiles(summaries);
  return ALL_GROUPS.map((group) => ({ label: group.label, notebooks: notebooksOf(summaries, group) })).filter(
    (group) => group.notebooks.length > 0,
  );
}

/** Every notebook in group order, each carrying the label of its group. */
export function getNotebookList(): NotebookListItem[] {
  return getNotebookGroups().flatMap((group) => group.notebooks);
}

/** Slim header-search index for the suggestions panel. The ?q= query itself is
 *  client state (components/search-context.tsx); this is the build-time data. */
export function getSearchIndex(): SearchableNotebook[] {
  return getNotebookList().map(({ repoPath, slug, title, description, groupLabel, githubHref }) => ({
    repoPath,
    slug,
    title,
    description,
    groupLabel,
    githubHref,
  }));
}
