import fs from "node:fs";
import path from "node:path";

export type NotebookSummary = {
  pathParts: string[];
  filename: string;
  title: string;
  downloadHref: string;
  colabHref: string;
  group: "Practice" | "Topic" | "Markdown";
  markdownCells: number;
  codeCells: number;
  assertCount: number;
};

const root = process.cwd();
const notebooksRoot = path.join(root, "notebooks");
const repoColabBase = "https://colab.research.google.com/github/sai-guntupalli/data-engineering-interview-questions/blob/master";

function sourceToString(source: string | string[] | undefined) {
  if (Array.isArray(source)) return source.join("");
  return source ?? "";
}

function titleFromCell(source: string, fallback: string) {
  const match = source.match(/^#\s+(.+?)\s*$/m);
  if (match?.[1]) return match[1].trim();
  return fallback.replace(/^\d+_/, "").replace(/\.ipynb$/, "").replaceAll("_", " ").replaceAll("-", " ");
}

function walkIpynb(dir: string): string[][] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      return walkIpynb(full);
    }
    if (!entry.name.endsWith(".ipynb")) return [];
    return [path.relative(notebooksRoot, full).split(path.sep)];
  });
}

function groupForPath(pathParts: string[]): NotebookSummary["group"] {
  if (pathParts[0] === "topics") return "Topic";
  if (pathParts[0] === "from-md") return "Markdown";
  return "Practice";
}

function readNotebookSummary(pathParts: string[]): NotebookSummary {
  const safeParts = pathParts.filter((part) => part !== ".." && !part.includes("/"));
  const file = path.join(notebooksRoot, ...safeParts);
  const notebook = JSON.parse(fs.readFileSync(file, "utf8"));
  const cells = (notebook.cells ?? []).map((cell: { cell_type?: string; source?: string | string[] }) => ({
    type: cell.cell_type ?? "markdown",
    source: sourceToString(cell.source),
  }));
  const firstMarkdown = cells.find((cell: { type: string }) => cell.type === "markdown")?.source ?? "";
  const filename = safeParts.at(-1) ?? "notebook.ipynb";
  const relative = safeParts.join("/");
  const repoRelative = `notebooks/${relative}`;

  return {
    pathParts: safeParts,
    filename,
    title: titleFromCell(firstMarkdown, filename),
    downloadHref: `/notebook-files/${relative}`,
    colabHref: `${repoColabBase}/${repoRelative}`,
    group: groupForPath(safeParts),
    markdownCells: cells.filter((cell: { type: string }) => cell.type === "markdown").length,
    codeCells: cells.filter((cell: { type: string }) => cell.type === "code").length,
    assertCount: cells.reduce((sum: number, cell: { type: string; source: string }) => sum + (cell.type === "code" ? (cell.source.match(/\bassert\b/g) ?? []).length : 0), 0),
  };
}

export function getAllNotebookSummaries() {
  return walkIpynb(notebooksRoot)
    .map(readNotebookSummary)
    .sort((a, b) => a.group.localeCompare(b.group) || a.title.localeCompare(b.title));
}

export function topicNotebookDownloadHref(slug: string) {
  return `/notebook-files/topics/${slug}.ipynb`;
}

export function topicNotebookColabHref(slug: string) {
  return `${repoColabBase}/notebooks/topics/${slug}.ipynb`;
}
