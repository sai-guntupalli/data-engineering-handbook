/**
 * Build-time data: reads the notebooks from the repository and shapes them for
 * the pages. Parsing rules live in notebook-parse.ts; this module adds the file
 * system, the registry checks and the links.
 */
import fs from "node:fs";
import path from "node:path";
import { LEARNING_MAP_COLUMNS, LEARNING_MAP_EDGES, layoutMap, validateMap, type MapLayout } from "./learning-map";
import { ALL_GROUPS, type GroupSection, type GroupTone, type NotebookGroup, repoPathFor } from "./notebook-groups";
import { monogram, parseNotebook, type ParsedCell, type RawNotebook, type Section } from "./notebook-parse";
import type { SearchEntry } from "./search";
import { branch, repository } from "./site";

export type NotebookSummary = {
  /** Repository-relative path, e.g. notebooks/topics/spark.ipynb */
  repoPath: string;
  /** File name without the extension, e.g. spark; also the reader URL segment. */
  slug: string;
  title: string;
  description: string;
  groupLabel: string;
  groupShortLabel: string;
  tone: GroupTone;
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

export type NotebookGroupView = {
  label: string;
  shortLabel: string;
  section: GroupSection;
  tone: GroupTone;
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

export type LearningMapView = MapLayout & {
  /** Slug -> reader link and repository path, for status lookups. */
  targets: Record<string, { href: string; repoPath: string; title: string }>;
};

const GITHUB_BLOB = `https://github.com/${repository}/blob/${branch}`;
// Plain <a> links (downloads) are not rewritten by Next, so they carry the base path themselves.
const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const COLAB_HREF = "https://colab.research.google.com/github";

// The app lives in site/; the notebooks are the repository's top-level content.
const repoRoot = path.resolve(process.cwd(), "..");

type LoadedNotebook = { summary: NotebookSummary; intro: string; sections: Section[]; cells: ParsedCell[] };

function readNotebook(group: NotebookGroup, slug: string): LoadedNotebook {
  const repoPath = repoPathFor(group, slug);
  const file = path.join(repoRoot, repoPath);
  if (!fs.existsSync(file)) {
    throw new Error(`lib/notebook-groups.ts lists ${repoPath} (group "${group.label}"), but the file is missing`);
  }
  let raw: RawNotebook;
  try {
    raw = JSON.parse(fs.readFileSync(file, "utf8")) as RawNotebook;
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Could not parse notebook ${repoPath}: ${reason}`);
  }
  const parsed = parseNotebook(raw, slug);
  return {
    summary: {
      repoPath,
      slug,
      title: parsed.title,
      description: parsed.description,
      groupLabel: group.label,
      groupShortLabel: group.shortLabel,
      tone: group.tone,
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

function listNotebookFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return listNotebookFiles(full);
    return entry.name.endsWith(".ipynb") ? [path.relative(repoRoot, full).split(path.sep).join("/")] : [];
  });
}

/**
 * Fail the build when the registry and the files disagree: a file no group
 * lists, a path listed twice, or two notebooks sharing a reader URL.
 */
function assertRegistryMatchesFiles(): void {
  const registered = new Set<string>();
  const slugs = new Set<string>();
  const problems: string[] = [];
  for (const group of ALL_GROUPS) {
    for (const slug of group.slugs) {
      const repoPath = repoPathFor(group, slug);
      if (registered.has(repoPath)) problems.push(`${repoPath} is registered more than once`);
      if (slugs.has(slug)) problems.push(`two notebooks share the slug "${slug}"`);
      registered.add(repoPath);
      slugs.add(slug);
    }
  }
  for (const repoPath of listNotebookFiles(path.join(repoRoot, "notebooks"))) {
    if (!registered.has(repoPath)) problems.push(`${repoPath} is not listed in lib/notebook-groups.ts`);
  }
  if (problems.length > 0) {
    throw new Error(`lib/notebook-groups.ts issues:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
}

let cache: { groups: NotebookGroupView[]; details: Map<string, LoadedNotebook> } | undefined;

/** Parsed once per build; the notebooks tree is static repository content. */
function load() {
  if (cache) return cache;
  assertRegistryMatchesFiles();
  const details = new Map<string, LoadedNotebook>();
  const groups = ALL_GROUPS.map((group) => {
    const notebooks = group.slugs.map((slug) => {
      const loaded = readNotebook(group, slug);
      details.set(slug, loaded);
      return loaded.summary;
    });
    return { label: group.label, shortLabel: group.shortLabel, section: group.section, tone: group.tone, notebooks };
  }).filter((group) => group.notebooks.length > 0);
  cache = { groups, details };
  return cache;
}

export function getNotebookGroups(): NotebookGroupView[] {
  return load().groups;
}

/** Every notebook in group order. */
export function getNotebookList(): NotebookSummary[] {
  return getNotebookGroups().flatMap((group) => group.notebooks);
}

export function getNotebookSlugs(): string[] {
  return getNotebookList().map((notebook) => notebook.slug);
}

/** One notebook with its cells, plus the notebooks before and after it in its group. */
export function getNotebook(slug: string): NotebookDetail | null {
  const { groups, details } = load();
  const loaded = details.get(slug);
  if (!loaded) return null;
  const siblings = groups.find((group) => group.label === loaded.summary.groupLabel)?.notebooks ?? [];
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
      groupLabel: notebook.groupLabel,
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

/** The home page learning map, laid out, with each node resolved to its notebook. */
export function getLearningMap(): LearningMapView {
  const { details } = load();
  const problems = validateMap(LEARNING_MAP_COLUMNS, LEARNING_MAP_EDGES, new Set(details.keys()));
  if (problems.length > 0) {
    throw new Error(`lib/learning-map.ts issues:\n${problems.map((problem) => `  - ${problem}`).join("\n")}`);
  }
  const layout = layoutMap(LEARNING_MAP_COLUMNS, LEARNING_MAP_EDGES);
  const targets = Object.fromEntries(
    layout.nodes.map((node) => {
      const summary = details.get(node.slug)!.summary;
      return [node.slug, { href: summary.href, repoPath: summary.repoPath, title: summary.title }];
    }),
  );
  return { ...layout, targets };
}
