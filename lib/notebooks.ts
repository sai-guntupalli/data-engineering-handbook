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
  colabHref: string;
  githubHref: string;
};

export type NotebookGroupView = {
  label: string;
  notebooks: NotebookSummary[];
};

const REPO = "sai-guntupalli/data-engineering-interview-questions";
const BRANCH = "master";
const GITHUB_BLOB = `https://github.com/${REPO}/blob/${BRANCH}`;
const COLAB = `https://colab.research.google.com/github/${REPO}/blob/${BRANCH}`;

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
    if (line.startsWith("+") || line.startsWith("-") || line.startsWith("*")) continue;
    if (line.startsWith("**Notebook:**") || line.startsWith("*Generated") || line.startsWith("*Converted")) continue;
    const plain = line.replace(/\*\*/g, "").replace(/`/g, "");
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

function readSummary(file: string): NotebookSummary {
  const notebook = JSON.parse(fs.readFileSync(file, "utf8"));
  const cells: { type: string; source: string }[] = (notebook.cells ?? []).map(
    (cell: { cell_type?: string; source?: string | string[] }) => ({
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
    colabHref: `${COLAB}/${repoPath}`,
    githubHref: `${GITHUB_BLOB}/${repoPath}`,
  };
}

function allSummaries(): NotebookSummary[] {
  return listNotebookFiles(notebooksRoot).map(readSummary);
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

/** Grouped notebooks, in the order the groups are declared. */
export function getNotebookGroups(): NotebookGroupView[] {
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
