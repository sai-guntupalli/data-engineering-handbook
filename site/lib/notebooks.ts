/**
 * Build-time data: reads the notebooks from the repository and shapes them for
 * the pages. Parsing rules live in notebook-parse.ts; this module adds the file
 * system, the registry checks and the links.
 */
import fs from "node:fs";
import path from "node:path";
import { LEARNING_PATH, validatePath } from "./learning-map";
import { monogram, parseNotebook, type ParsedCell, type RawNotebook, type Section } from "./notebook-parse";
import type { SearchEntry } from "./search";
import { branch, repository } from "./site";
import {
  CATEGORY_LABELS,
  TOOL_CATEGORIES,
  TOOLS,
  TOOLS_BY_FOLDER,
  categoryOf,
  compareSubtopics,
  toolSortName,
  type GroupTone,
  type NotebookCategory,
  type Tool,
} from "./tools";

export type NotebookSummary = {
  /** Repository-relative path, e.g. notebooks/kafka/kafka.ipynb */
  repoPath: string;
  /** File name without the extension, e.g. kafka; also the reader URL segment. */
  slug: string;
  title: string;
  description: string;
  /** The tool this notebook belongs to (its folder). */
  toolFolder: string;
  toolLabel: string;
  /** Folder inside the tool folder, e.g. "learning" for python/learning; empty when the notebook sits at the top. */
  subfolder: string;
  tone: GroupTone;
  category: NotebookCategory;
  categoryLabel: string;
  monogram: string;
  sectionCount: number;
  checks: number;
  minutes: number;
  /** Reader page, site-relative. */
  href: string;
  githubHref: string;
  /** Opens this notebook in Google Colab (repository must stay public). */
  colabHref: string;
  /** The .ipynb file served by this site (base path included), for downloading. */
  downloadHref: string;
};

/** One tool and its subtopics, in the order the tool page lists them. */
export type ToolView = Tool & {
  /** Site-relative tool page. */
  href: string;
  notebooks: NotebookSummary[];
};

export type NotebookNeighbour = Pick<NotebookSummary, "title" | "href">;

export type NotebookDetail = NotebookSummary & {
  /** Opening paragraph in full, lifted out of the first cell for the page lead. */
  intro: string;
  sections: Section[];
  cells: ParsedCell[];
  previous: NotebookNeighbour | null;
  next: NotebookNeighbour | null;
};

export type PathNotebook = { slug: string; repoPath: string; href: string; title: string };
export type PathStepView = { id: string; label: string; toolHref: string; notebooks: PathNotebook[] };
export type LearningPathView = { stages: { title: string; purpose: string; steps: PathStepView[] }[] };

const GITHUB_BLOB = `https://github.com/${repository}/blob/${branch}`;
// Plain <a> links (downloads) are not rewritten by Next, so they carry the base path themselves.
const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const COLAB_HREF = "https://colab.research.google.com/github";

// The app lives in site/; the notebooks are the repository's top-level content.
const repoRoot = path.resolve(process.cwd(), "..");
/** Tools are folders under this one; a tool folder may nest subfolders such as python/learning. */
const TOPICS_DIR = path.join(repoRoot, "notebooks", "topics");

type LoadedNotebook = { summary: NotebookSummary; intro: string; sections: Section[]; cells: ParsedCell[] };

type NotebookFile = {
  /** The tool folder, e.g. "python". */
  folder: string;
  /** Repository-relative path, e.g. notebooks/topics/python/learning/python-01-values-and-types.ipynb. */
  repoPath: string;
  slug: string;
};

function readNotebook(tool: Tool, { repoPath, slug }: NotebookFile): LoadedNotebook {
  const file = path.join(repoRoot, repoPath);
  let raw: RawNotebook;
  try {
    raw = JSON.parse(fs.readFileSync(file, "utf8")) as RawNotebook;
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Could not parse notebook ${repoPath}: ${reason}`);
  }
  const parsed = parseNotebook(raw, slug);
  const category = categoryOf(slug);
  return {
    summary: {
      repoPath,
      slug,
      title: parsed.title,
      description: parsed.description,
      toolFolder: tool.folder,
      toolLabel: tool.label,
      subfolder: path.dirname(path.relative(path.join("notebooks", "topics", tool.folder), repoPath)).replace(/^\.$/, ""),
      tone: tool.tone,
      category,
      categoryLabel: CATEGORY_LABELS[category],
      monogram: monogram(parsed.title),
      sectionCount: parsed.sections.length,
      checks: parsed.checks,
      minutes: parsed.minutes,
      href: `/notebooks/${slug}/`,
      githubHref: `${GITHUB_BLOB}/${repoPath}`,
      colabHref: `${COLAB_HREF}/${repository}/blob/${branch}/${repoPath}`,
      downloadHref: `${BASE_PATH}/files/${slug}.ipynb`,
    },
    intro: parsed.intro,
    sections: parsed.sections,
    cells: parsed.cells,
  };
}

/** Every notebook under notebooks/topics/, with the tool it belongs to (the first folder below topics). */
function listNotebookFiles(dir = TOPICS_DIR): NotebookFile[] {
  const toolFolders = fs.readdirSync(dir, { withFileTypes: true }).filter((entry) => entry.isDirectory());
  const walk = (current: string): string[] =>
    fs.readdirSync(current, { withFileTypes: true }).flatMap((entry) => {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) return walk(full);
      return entry.name.endsWith(".ipynb") ? [full] : [];
    });
  return toolFolders.flatMap((tool) =>
    walk(path.join(dir, tool.name)).map((file) => ({
      folder: tool.name,
      repoPath: path.relative(repoRoot, file).split(path.sep).join("/"),
      slug: path.basename(file, ".ipynb"),
    })),
  );
}

/**
 * Fail the build when the tool registry and the folders disagree: a folder with no
 * entry, an entry with no folder, a notebook outside a tool folder, or two
 * notebooks sharing a reader URL.
 */
function assertRegistryMatchesFolders(files: NotebookFile[]): void {
  const problems: string[] = [];
  const slugs = new Set<string>();
  for (const file of files) {
    if (!TOOLS_BY_FOLDER.has(file.folder)) problems.push(`notebooks/topics/${file.folder}/ has no entry in lib/tools.ts`);
    if (slugs.has(file.slug)) problems.push(`two notebooks share the slug "${file.slug}"`);
    slugs.add(file.slug);
  }
  const folders = new Set(files.map((file) => file.folder));
  for (const tool of TOOLS) {
    if (!folders.has(tool.folder)) problems.push(`lib/tools.ts lists "${tool.folder}", but notebooks/topics/${tool.folder}/ is missing or empty`);
  }
  if (problems.length > 0) {
    throw new Error(`lib/tools.ts and notebooks/topics/ disagree:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
}

let cache: { tools: ToolView[]; details: Map<string, LoadedNotebook> } | undefined;

/** Parsed once per build; the notebooks tree is static repository content. */
function load() {
  if (cache) return cache;
  const files = listNotebookFiles();
  assertRegistryMatchesFolders(files);
  const details = new Map<string, LoadedNotebook>();
  const tools: ToolView[] = [...TOOLS]
    .sort((a, b) => toolSortName(a.label).localeCompare(toolSortName(b.label), "en"))
    .map((tool) => {
      const notebooks = files
        .filter((file) => file.folder === tool.folder)
        .sort((a, b) => compareSubtopics(a, b))
        .map((file) => {
          const loaded = readNotebook(tool, file);
          details.set(file.slug, loaded);
          return loaded.summary;
        });
      return { ...tool, href: `/tools/${tool.folder}/`, notebooks };
    });
  cache = { tools, details };
  return cache;
}

/** Every tool, alphabetical (ignoring "Apache" and "Amazon"), each with its subtopics in reading order. */
export function getTools(): ToolView[] {
  return load().tools;
}

export type ToolCategoryView = { id: string; label: string; tools: ToolView[] };

/** Tools under their category headings, in the order of TOOL_CATEGORIES. */
export function getToolCategories(): ToolCategoryView[] {
  const tools = getTools();
  return TOOL_CATEGORIES.map((category) => ({
    id: category.id,
    label: category.label,
    tools: tools.filter((tool) => tool.category === category.id),
  })).filter((category) => category.tools.length > 0);
}

export function getTool(folder: string): ToolView | null {
  return getTools().find((tool) => tool.folder === folder) ?? null;
}

/** Every notebook, grouped by tool. */
export function getNotebookList(): NotebookSummary[] {
  return getTools().flatMap((tool) => tool.notebooks);
}

export function getNotebookSlugs(): string[] {
  return getNotebookList().map((notebook) => notebook.slug);
}

/** One notebook with its cells, plus the notebooks before and after it in its tool. */
export function getNotebook(slug: string): NotebookDetail | null {
  const { details } = load();
  const loaded = details.get(slug);
  if (!loaded) return null;
  const siblings = getTool(loaded.summary.toolFolder)?.notebooks ?? [];
  const at = siblings.findIndex((notebook) => notebook.slug === slug);
  const neighbour = (notebook: NotebookSummary | undefined): NotebookNeighbour | null =>
    notebook ? { title: notebook.title, href: notebook.href } : null;
  return {
    ...loaded.summary,
    intro: loaded.intro,
    sections: loaded.sections,
    cells: loaded.cells,
    previous: neighbour(siblings[at - 1]),
    next: neighbour(siblings[at + 1]),
  };
}

/** Notebooks and their sections, for the command palette. */
export function getSearchEntries(): SearchEntry[] {
  const { details } = load();
  return getNotebookList().flatMap((notebook) => {
    const shared = {
      repoPath: notebook.repoPath,
      notebookTitle: notebook.title,
      toolLabel: notebook.toolLabel,
      tone: notebook.tone,
      monogram: notebook.monogram,
      colabHref: notebook.colabHref,
    };
    const sections = details.get(notebook.slug)?.sections ?? [];
    return [
      { ...shared, kind: "notebook" as const, title: notebook.title, snippet: notebook.description, href: notebook.href },
      ...sections.map((section) => ({
        ...shared,
        kind: "section" as const,
        title: section.title,
        snippet: section.snippet,
        href: `${notebook.href}#${section.id}`,
      })),
    ];
  });
}

/** The home page learning path, with each step's notebooks resolved to links and titles. */
export function getLearningPath(): LearningPathView {
  const { details } = load();
  const problems = validatePath(LEARNING_PATH, new Set(details.keys()));
  if (problems.length > 0) {
    throw new Error(`lib/learning-map.ts issues:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
  return {
    stages: LEARNING_PATH.map((stage) => ({
      title: stage.title,
      purpose: stage.purpose,
      steps: stage.steps.map((step) => ({
        id: step.id,
        label: step.label,
        toolHref: step.toolHref,
        notebooks: step.slugs.map((slug) => {
          const { summary } = details.get(slug)!;
          return { slug, repoPath: summary.repoPath, href: summary.href, title: summary.title };
        }),
      })),
    })),
  };
}
