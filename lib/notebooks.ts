import fs from "node:fs";
import path from "node:path";
import { PRACTICE_GROUP, TOPIC_GROUPS, type NotebookGroup } from "./notebook-groups";

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
  githubHref: string;
};

export type NotebookGroupView = {
  label: string;
  notebooks: NotebookSummary[];
};

const REPO = "sai-guntupalli/data-engineering-handbook";
const BRANCH = "master";
const GITHUB_BLOB = `https://github.com/${REPO}/blob/${BRANCH}`;
// Note: Google Colab can only open notebooks in public repositories, so this
// gallery links to the private repository's files instead.

const notebooksRoot = path.join(process.cwd(), "notebooks");

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
    githubHref: `${GITHUB_BLOB}/${repoPath}`,
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
  return {
    notebooks: summaries.length,
    codeCells: summaries.reduce((total, notebook) => total + notebook.codeCells, 0),
    checks: summaries.reduce((total, notebook) => total + notebook.assertCount, 0),
  };
}

export const repositoryHref = `https://github.com/${REPO}`;
