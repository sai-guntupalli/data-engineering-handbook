import fs from "node:fs";
import path from "node:path";
import { PRACTICE_GROUP, TOPIC_GROUPS, type NotebookGroup } from "./notebook-groups";
import { repository } from "./site";

export type NotebookSummary = {
  /** Repository-relative path, e.g. notebooks/topics/spark.ipynb */
  repoPath: string;
  /** File name without the extension, e.g. spark */
  slug: string;
  title: string;
  description: string;
  markdownCells: number;
  codeCells: number;
  assertCount: number;
  /** "### Try it" exercise blocks in the markdown. */
  tryItBlocks: number;
  /** Code cells marked `# ILLUSTRATIVE` (need a platform; will not run locally). */
  illustrativeCells: number;
  /** Coarse reading time: markdown words / 200wpm plus 8s per runnable cell. */
  readingMinutes: number;
  /** Code cells and asserts that are verbatim copies of a practice notebook
   *  (merged self-contained regions). Zero except for python/spark/sql topics. */
  mergedCodeCells: number;
  mergedAsserts: number;
  githubHref: string;
  /** Opens this notebook in Google Colab (repository must stay public). */
  colabHref: string;
};

export type NotebookGroupView = {
  label: string;
  notebooks: NotebookSummary[];
};

const BRANCH = "master";
const GITHUB_BLOB = `https://github.com/${repository}/blob/${BRANCH}`;
// Google Colab can only open notebooks from public repositories. The handbook
// is public, so every carry gets a Colab permalink next to the GitHub link.
const COLAB_HREF = "https://colab.research.google.com/github";

const notebooksRoot = path.join(process.cwd(), "notebooks");

/**
 * Marker of a merged self-contained copy of a practice notebook. Must stay in
 * step with MERGE_NOTE in scripts/sync_merged_copies.py, which owns the
 * convention.
 */
const MERGE_NOTE = "merged here so this notebook is self-contained";

/**
 * Count code cells (and their asserts) that sit inside a merged-copy region,
 * i.e. verbatim copies of a practice notebook. A region starts at the markdown
 * merge-note cell and runs to the next merge note or the end of the notebook.
 * These are subtracted from repository-level stats so the hero does not report
 * every practice notebook twice (it is executed once directly and once merged).
 *
 * Region rules are owned by scripts/sync_merged_copies.py: its --check fails
 * when a merge-note notebook is missing from its CONFIG, or when unmerged code
 * cells trail a region without committed outputs, so these two implementations
 * cannot silently disagree about which cells count as merged.
 */
function mergedCopyCells(cells: RawCell[]): { codeCells: number; asserts: number } {
  const regions: Array<[number, number]> = [];
  let start = -1;
  for (let index = 0; index < cells.length; index++) {
    const cell = cells[index];
    if (cell.cell_type === "markdown" && sourceToString(cell.source).includes(MERGE_NOTE)) {
      if (start >= 0) regions.push([start, index]);
      start = index;
    }
  }
  if (start >= 0) regions.push([start, cells.length]);

  let codeCount = 0;
  let assertCount = 0;
  for (const [from, to] of regions) {
    for (const cell of cells.slice(from + 1, to)) {
      if (cell.cell_type !== "code") continue;
      codeCount++;
      assertCount += sourceToString(cell.source).match(/\bassert\b/g)?.length ?? 0;
    }
  }
  return { codeCells: codeCount, asserts: assertCount };
}

function sourceToString(source: string | string[] | undefined): string {
  if (Array.isArray(source)) return source.join("");
  return source ?? "";
}

function titleFromMarkdown(markdown: string, fallback: string): string {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  if (match?.[1]) return match[1].trim();
  return fallback.replace(/^\d+_/, "").replaceAll("_", " ").replaceAll("-", " ");
}

/** First real paragraph after the title, used as a card description. */
function descriptionFromMarkdown(markdown: string): string {
  const lines = markdown.split("\n");
  let seenTitle = false;
  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith("#")) {
      seenTitle = true;
      continue;
    }
    if (!seenTitle || !line) continue;
    // Skip badges, links, images, lists, quotes, tables, fenced code and HTML.
    if (/^[+\-*[>|`<]/.test(line)) continue;
    if (line.startsWith("**Notebook:**") || line.startsWith("*Generated") || line.startsWith("*Converted")) continue;
    const plain = inlineToText(line);
    if (plain.length < 25) continue;
    return plain.length > 150 ? `${plain.slice(0, 147).trimEnd()}...` : plain;
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

function readSummary(file: string): NotebookSummary {
  let notebook: RawNotebook;
  try {
    notebook = JSON.parse(fs.readFileSync(file, "utf8")) as RawNotebook;
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Could not parse notebook ${path.relative(process.cwd(), file)}: ${reason}`);
  }
  const cells: { type: string; source: string }[] = (notebook.cells ?? []).map(
    (cell: RawCell) => ({
      type: cell.cell_type ?? "markdown",
      source: sourceToString(cell.source),
    }),
  );
  const markdown = cells
    .filter((cell) => cell.type === "markdown")
    .map((cell) => cell.source)
    .join("\n\n");
  const repoPath = path.relative(process.cwd(), file).split(path.sep).join("/");
  const filename = path.basename(file, ".ipynb");
  const codeCells = cells.filter((cell) => cell.type === "code");
  const illustrativeCells = codeCells.filter((cell) => cell.source.includes("# ILLUSTRATIVE")).length;
  const tryItBlocks = (markdown.match(/### Try it/g) ?? []).length;
  const markdownWords = markdown.split(/\s+/).filter(Boolean).length;
  const readingMinutes = Math.max(
    1,
    Math.round(markdownWords / 200 + ((codeCells.length - illustrativeCells) * 8) / 60),
  );
  const merged = mergedCopyCells(notebook.cells ?? []);

  return {
    repoPath,
    slug: filename,
    title: titleFromMarkdown(markdown, filename),
    description: descriptionFromMarkdown(markdown),
    markdownCells: cells.length - codeCells.length,
    codeCells: codeCells.length,
    assertCount: codeCells.reduce(
      (total, cell) => total + (cell.source.match(/\bassert\b/g)?.length ?? 0),
      0,
    ),
    tryItBlocks,
    illustrativeCells,
    readingMinutes,
    mergedCodeCells: merged.codeCells,
    mergedAsserts: merged.asserts,
    githubHref: `${GITHUB_BLOB}/${repoPath}`,
    colabHref: `${COLAB_HREF}/${repository}/blob/${BRANCH}/${repoPath}`,
  };
}

let cachedSummaries: NotebookSummary[] | undefined;

/** Parsed once per build; the notebooks tree is static repository content. */
function allSummaries(): NotebookSummary[] {
  cachedSummaries ??= listNotebookFiles(notebooksRoot).map(readSummary);
  return cachedSummaries;
}

function pick(
  summaries: NotebookSummary[],
  group: NotebookGroup,
  folder: "root" | "topics",
): NotebookSummary[] {
  const wanted = new Set(group.slugs);
  return summaries
    .filter((notebook) => {
      const inFolder =
        folder === "root"
          ? !notebook.repoPath.startsWith("notebooks/topics/")
          : notebook.repoPath.startsWith("notebooks/topics/");
      return inFolder && wanted.has(notebook.slug);
    })
    .sort((a, b) => group.slugs.indexOf(a.slug) - group.slugs.indexOf(b.slug));
}

/**
 * Fail the build when lib/notebook-groups.ts references a notebook that does not
 * exist, lives in the wrong folder, or is registered twice. Without this guard a
 * mistyped slug would make the card silently disappear from the gallery.
 */
function ensureRegisteredSlugsExist(): void {
  const bySlug = new Map<string, string[]>();
  for (const notebook of allSummaries()) {
    bySlug.set(notebook.slug, [...(bySlug.get(notebook.slug) ?? []), notebook.repoPath]);
  }

  const problems: string[] = [];
  const registered = new Set<string>();
  for (const group of [PRACTICE_GROUP, ...TOPIC_GROUPS]) {
    const folder = group === PRACTICE_GROUP ? "notebooks" : "notebooks/topics";
    for (const slug of group.slugs) {
      if (registered.has(slug)) {
        problems.push(`"${slug}" is registered in more than one group`);
        continue;
      }
      registered.add(slug);
      const hits = bySlug.get(slug) ?? [];
      if (!hits.some((repoPath) => path.dirname(repoPath) === folder)) {
        problems.push(`${folder}/${slug}.ipynb is missing (group "${group.label}")`);
      }
    }
  }
  if (problems.length > 0) {
    throw new Error(`lib/notebook-groups.ts issues:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
}

/** Grouped notebooks, in the order the groups are declared. */
export function getNotebookGroups(): NotebookGroupView[] {
  ensureRegisteredSlugsExist();
  const summaries = allSummaries();
  const groups: NotebookGroupView[] = [
    { label: PRACTICE_GROUP.label, notebooks: pick(summaries, PRACTICE_GROUP, "root") },
    ...TOPIC_GROUPS.map((group) => ({
      label: group.label,
      notebooks: pick(summaries, group, "topics"),
    })),
  ];

  const placed = new Set(groups.flatMap((group) => group.notebooks.map((notebook) => notebook.repoPath)));
  const leftovers = summaries.filter((notebook) => !placed.has(notebook.repoPath));
  if (leftovers.length > 0) {
    groups.push({ label: "Other notebooks", notebooks: leftovers });
  }

  return groups.filter((group) => group.notebooks.length > 0);
}

export function getNotebookStats() {
  const summaries = allSummaries();
  // Exclude merged copies of the practice notebooks so self-contained topics
  // (python, spark, sql) do not report the same cells and self-checks twice.
  return {
    notebooks: summaries.length,
    codeCells: summaries.reduce(
      (total, notebook) => total + notebook.codeCells - notebook.mergedCodeCells,
      0,
    ),
    checks: summaries.reduce(
      (total, notebook) => total + notebook.assertCount - notebook.mergedAsserts,
      0,
    ),
  };
}

/** Slim header-search index: one row per notebook in group order, shared by
 *  the home, /search and /license pages' SiteHeader. The ?q= query itself is
 *  client state (components/search-context.tsx); this is the build-time data. */
export function getSearchIndex() {
  return getNotebookGroups().flatMap((group) =>
    group.notebooks.map(({ slug, title, repoPath, githubHref }) => ({
      slug,
      title,
      groupLabel: group.label,
      repoPath,
      githubHref,
    })),
  );
}
