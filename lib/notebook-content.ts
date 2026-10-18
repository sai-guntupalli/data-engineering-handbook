import fs from "node:fs";
import path from "node:path";

import { renderMarkdown } from "./markdown";
import type { NotebookSummary } from "./notebooks";

export type NotebookSectionBlock =
  | { kind: "markdown"; source: string; html: string }
  | { kind: "code"; source: string; illustrative: boolean; cellIndex: number };

/** Aliases the viewer's cell renderer can switch on without re-writing Extract. */
export type MarkdownSectionBlock = Extract<NotebookSectionBlock, { kind: "markdown" }>;
export type CodeSectionBlock = Extract<NotebookSectionBlock, { kind: "code" }>;

export type NotebookSection = { id: string; heading: string; blocks: NotebookSectionBlock[] };

export type NotebookPage = {
  slug: string;
  repoPath: string;
  title: string;
  sections: NotebookSection[];
};

type RawCell = { cell_type?: string; source?: string | string[] };
type RawNotebook = { cells?: RawCell[] };

/** "## " lines start a viewer section; everything else (including "# " h1s) is
 *  ordinary markdown inside whatever section it falls in. The heading line
 *  becomes the section heading, so it is not duplicated into the blocks. */
const SECTION_HEADING = /^##\s+(.+)$/;

/** Same cell-source convention as lib/notebooks.ts: lists join, absent is "". */
function sourceToString(source: string | string[] | undefined): string {
  if (Array.isArray(source)) return source.join("");
  return source ?? "";
}

/** Lowercase heading, non-alphanumerics collapsed to one dash, trimmed. */
function slugify(heading: string): string {
  const base = heading
    .toLowerCase()
    .replaceAll(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return base || "section";
}

/**
 * Split a markdown cell's source at its "## " heading lines. Segments between
 * headings keep their raw source; heading lines surface as `heading` and own a
 * new viewer section instead of rendering twice. A "## " line inside a fenced
 * code block is fence content, not a heading — otherwise the fence would be
 * torn into two unterminated segments and a bogus section created.
 */
function splitAtHeadings(
  source: string,
): Array<{ heading: string | null; source: string }> {
  const segments: Array<{ heading: string | null; source: string }> = [];
  let lines: string[] = [];
  let heading: string | null = null;
  let inFence = false;

  for (const line of source.split("\n")) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    const match = inFence ? undefined : line.match(SECTION_HEADING);
    if (match?.[1]) {
      segments.push({ heading, source: lines.join("\n") });
      heading = match[1].trim();
      lines = [];
      continue;
    }
    lines.push(line);
  }
  segments.push({ heading, source: lines.join("\n") });

  return segments;
}

/** Rendered in the client too (the viewer's Elaborate gate); client-safe
 *  module without node:fs, re-exported here as the single section API. */
export { isElaboratable } from "./section-elaborate";

/**
 * Parse the notebook at summary.repoPath into viewer sections. `## ` headings
 * start a section (slugified id; repeated headings get -2/-3 suffixes); content
 * before the first one forms the "intro" section, headed by the notebook title.
 * Code blocks carry their RAW index in the notebook's cells array (markdown
 * included) — that is the backend /execute convention, and lib/notebooks.ts
 * never reorders cells, so the backend's load_cell_source agrees with it.
 * A cell with a missing/absent source parses as an empty block, never a crash.
 */
export function readNotebookPage(summary: NotebookSummary): NotebookPage {
  const file = path.isAbsolute(summary.repoPath)
    ? summary.repoPath
    : path.join(process.cwd(), summary.repoPath);
  let notebook: RawNotebook;
  try {
    notebook = JSON.parse(fs.readFileSync(file, "utf8")) as RawNotebook;
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(`Could not parse notebook ${summary.repoPath}: ${reason}`);
  }

  const sections: NotebookSection[] = [];
  // ids already handed out, including suffixed forms — candidates are checked
  // against this set so ["Notes", "Notes 2", "Notes"] cannot yield two
  // "notes-2" sections (anchors would collide).
  const usedIds = new Set<string>();

  const usedSectionId = (heading: string): string => {
    const base = slugify(heading);
    let candidate = base;
    let suffix = 1;
    while (usedIds.has(candidate)) {
      suffix += 1;
      candidate = `${base}-${suffix}`;
    }
    usedIds.add(candidate);
    return candidate;
  };

  const startSection = (id: string, heading: string): NotebookSection => {
    const created = { id, heading, blocks: [] };
    sections.push(created);
    return created;
  };
  usedIds.add("intro"); // a "## Intro" heading must not duplicate the intro anchor
  let section = startSection("intro", summary.title);

  for (const [cellIndex, cell] of (notebook.cells ?? []).entries()) {
    const type = cell.cell_type ?? "markdown";
    if (type === "code") {
      const source = sourceToString(cell.source);
      section.blocks.push({
        kind: "code",
        source,
        illustrative: source.includes("# ILLUSTRATIVE"),
        cellIndex,
      });
      continue;
    }
    if (type !== "markdown") continue; // raw cells stay out of the reader view

    const segments = splitAtHeadings(sourceToString(cell.source));
    // A heading-less cell is stored verbatim, even when empty; segments that
    // merely surround a heading (the blank line after it) are not content.
    const wholeCell = segments.length === 1 && segments[0].heading === null;
    for (const segment of segments) {
      if (segment.heading !== null) {
        section = startSection(usedSectionId(segment.heading), segment.heading);
      }
      const source = segment.source.replace(/^\n+/, "");
      if (source === "" && !wholeCell) continue;
      section.blocks.push({
        kind: "markdown",
        source,
        html: source.trim() === "" ? "" : renderMarkdown(source),
      });
    }
  }

  return { slug: summary.slug, repoPath: summary.repoPath, title: summary.title, sections };
}
