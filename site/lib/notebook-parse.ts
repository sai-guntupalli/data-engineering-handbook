/**
 * Pure notebook parsing: turns raw .ipynb JSON into what the site shows.
 * No file system access here, so every rule is unit-testable.
 */
import { marked, type Token, type Tokens } from "marked";
import { anchorFor } from "./notebook-groups";

export type RawCell = { cell_type?: string; source?: string | string[] };
export type RawNotebook = { cells?: RawCell[] };

/**
 * - `markdown`: explanation
 * - `setup`: the install cell every notebook starts with
 * - `check`: code with an `assert`, a self-check
 * - `code`: any other code
 */
export type CellKind = "markdown" | "setup" | "check" | "code";

export type ParsedCell = {
  /** Position in the original notebook, used for #cell-N anchors. */
  index: number;
  kind: CellKind;
  source: string;
};

export type Section = {
  id: string;
  title: string;
  /** First paragraph under the heading, for search previews. Empty when the section opens with code. */
  snippet: string;
};

export type ParsedNotebook = {
  title: string;
  description: string;
  /** The opening paragraph in full, shown as the reader's lead (empty when the notebook opens otherwise). */
  intro: string;
  sections: Section[];
  cells: ParsedCell[];
  checks: number;
  minutes: number;
};

const WORDS_PER_MINUTE = 220;
const CODE_LINES_PER_MINUTE = 30;
const MAX_DESCRIPTION_LENGTH = 160;
const MAX_SNIPPET_LENGTH = 180;
const MIN_SNIPPET_LENGTH = 20;
const SETUP_PREFIX = "# Setup:";

export function sourceToString(source: string | string[] | undefined): string {
  if (Array.isArray(source)) return source.join("");
  return source ?? "";
}

/** Inline markdown (code spans, links, images, emphasis) as plain text. */
export function inlineToText(line: string): string {
  return line
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .trim();
}

/** Titles read as plain prose: a leading "04 - " or "05 — " index is dropped. */
export function titleFromMarkdown(markdown: string, fallback: string): string {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  const raw = match?.[1]?.trim() ?? fallback.replace(/^\d+_/, "").replaceAll("_", " ").replaceAll("-", " ");
  return inlineToText(raw.replace(/^\d+\s*[-—–:.]\s*/, ""));
}

/** Cut at the last whole word that fits, then mark the cut with an ellipsis. */
export function truncateAtWord(text: string, limit: number): string {
  if (text.length <= limit) return text;
  const cut = text.slice(0, limit);
  const lastSpace = cut.lastIndexOf(" ");
  return `${cut.slice(0, lastSpace > 0 ? lastSpace : limit).trimEnd()}…`;
}

/** First real paragraph after the title. Notebooks hard-wrap their markdown, so the whole block is read. */
export function descriptionFromMarkdown(markdown: string, limit = MAX_DESCRIPTION_LENGTH): string {
  let seenTitle = false;
  for (const block of markdown.split(/\n\s*\n/)) {
    const text = block.trim();
    if (!text) continue;
    if (text.startsWith("#")) {
      seenTitle = true;
      continue;
    }
    // Skip badges, links, images, lists, quotes, tables, fenced code and HTML.
    if (!seenTitle || /^[+\-*[>|`<]/.test(text)) continue;
    const plain = inlineToText(text.split("\n").map((line) => line.trim()).join(" "));
    if (plain.length < 25) continue;
    return truncateAtWord(plain, limit);
  }
  return "";
}

/**
 * The first cell repeats what the page already shows: the H1 title, the author
 * credit line and the Colab badge. The reader drops those three lines.
 */
export function stripTitleBlock(markdown: string): string {
  return markdown
    .split("\n")
    .filter((line) => {
      const trimmed = line.trim();
      return !(/^#\s/.test(trimmed) || /^\*Author:.*\*$/.test(trimmed) || trimmed.startsWith("[![Open In Colab]"));
    })
    .join("\n")
    .trim();
}

/**
 * The reader shows the notebook's opening paragraph as the page lead, so it is
 * taken out of the first cell. Only a plain paragraph qualifies; a cell that
 * opens with a heading, list, table, quote, code or HTML keeps everything.
 */
export function splitIntro(markdown: string): { intro: string; rest: string } {
  const [first, ...others] = markdown.split(/\n\s*\n/);
  const text = first?.trim() ?? "";
  if (!text || /^[#+\-*[>|`<]/.test(text)) return { intro: "", rest: markdown };
  return {
    intro: inlineToText(text.split("\n").map((line) => line.trim()).join(" ")),
    rest: others.join("\n\n").trim(),
  };
}

/** Allocates heading ids in document order; a repeated title gets -2, -3, ... */
export function createIdAllocator() {
  const used = new Map<string, number>();
  return (title: string): string => {
    const base = anchorFor(title) || "section";
    const seen = used.get(base) ?? 0;
    used.set(base, seen + 1);
    return seen === 0 ? base : `${base}-${seen + 1}`;
  };
}

export type OutlineItem = { type: "heading"; title: string } | { type: "paragraph"; text: string };

/**
 * Level-2 headings and top-level paragraphs of one markdown cell, in order, as
 * marked sees them (so a "## " inside fenced code is not a heading). The reader
 * renders with the same lexer, which keeps heading ids in step.
 */
export function outlineOf(markdown: string): OutlineItem[] {
  return marked.lexer(markdown).flatMap((token: Token): OutlineItem[] => {
    if (token.type === "heading" && (token as Tokens.Heading).depth === 2) {
      return [{ type: "heading", title: inlineToText((token as Tokens.Heading).text) }];
    }
    if (token.type === "paragraph") {
      const text = inlineToText((token as Tokens.Paragraph).text.replace(/\s*\n\s*/g, " "));
      return text ? [{ type: "paragraph", text }] : [];
    }
    return [];
  });
}

export function cellKindOf(cellType: string, source: string): CellKind {
  if (cellType === "markdown") return "markdown";
  if (source.trimStart().startsWith(SETUP_PREFIX)) return "setup";
  return /\bassert\b/.test(source) ? "check" : "code";
}

function countWords(text: string): number {
  return text.split(/\s+/).filter(Boolean).length;
}

export function estimateMinutes(markdownWords: number, codeLines: number): number {
  return Math.max(1, Math.round(markdownWords / WORDS_PER_MINUTE + codeLines / CODE_LINES_PER_MINUTE));
}

export function parseNotebook(raw: RawNotebook, fallbackTitle: string): ParsedNotebook {
  const rawCells = raw.cells ?? [];
  const allMarkdown = rawCells
    .filter((cell) => (cell.cell_type ?? "markdown") === "markdown")
    .map((cell) => sourceToString(cell.source))
    .join("\n\n");

  const allocate = createIdAllocator();
  const sections: Section[] = [];
  const cells: ParsedCell[] = [];
  let markdownWords = 0;
  let codeLines = 0;
  let firstMarkdownSeen = false;
  let intro = "";

  rawCells.forEach((cell, index) => {
    const cellType = cell.cell_type ?? "markdown";
    let source = sourceToString(cell.source);
    if (cellType === "markdown" && !firstMarkdownSeen) {
      firstMarkdownSeen = true;
      const split = splitIntro(stripTitleBlock(source));
      intro = split.intro;
      source = split.rest;
    }
    if (!source.trim()) return;

    const kind = cellKindOf(cellType, source);
    if (kind === "markdown") {
      markdownWords += countWords(source);
      for (const item of outlineOf(source)) {
        const last = sections.at(-1);
        if (item.type === "heading") {
          sections.push({ id: allocate(item.title), title: item.title, snippet: "" });
        } else if (last && !last.snippet && item.text.length >= MIN_SNIPPET_LENGTH) {
          last.snippet = truncateAtWord(item.text, MAX_SNIPPET_LENGTH);
        }
      }
    } else if (kind !== "setup") {
      codeLines += source.split("\n").length;
    }
    cells.push({ index, kind, source });
  });

  return {
    title: titleFromMarkdown(allMarkdown, fallbackTitle),
    description: descriptionFromMarkdown(allMarkdown),
    intro,
    sections,
    cells,
    checks: cells.filter((cell) => cell.kind === "check").length,
    minutes: estimateMinutes(markdownWords, codeLines),
  };
}

/** Vendor prefixes that would make many monograms identical. */
const MONOGRAM_SKIP = new Set(["apache", "google", "amazon", "aws", "azure", "the"]);

/** Two-letter monogram for a tile, e.g. "Apache Iceberg" -> "Ic", "Data quality" -> "DQ". */
export function monogram(title: string): string {
  const all = title.replace(/[^A-Za-z0-9 ]+/g, " ").split(/\s+/).filter(Boolean);
  const kept = all.filter((word) => !MONOGRAM_SKIP.has(word.toLowerCase()));
  const words = kept.length > 0 ? kept : all;
  if (words.length === 0) return "?";
  if (words.length === 1) {
    const word = words[0];
    const isAcronym = word === word.toUpperCase();
    return word[0].toUpperCase() + (isAcronym ? (word[1] ?? "") : (word[1] ?? "").toLowerCase());
  }
  return (words[0][0] + words[1][0]).toUpperCase();
}
