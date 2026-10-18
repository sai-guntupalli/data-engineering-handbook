import { marked } from "marked";

/**
 * Render repository-authored markdown to HTML. Content is committed to the
 * repository (trusted), so no sanitizer runs beyond marked's own defaults.
 * Synchronous by contract: blocks need their HTML at parse time, not lazily.
 */
export function renderMarkdown(md: string): string {
  return marked.parse(md, { async: false });
}

/** A statement-opening SQL keyword (case-insensitive) at the start of a line. */
const SQL_LINE = /^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|WITH|TRUNCATE|MERGE|EXPLAIN)\b/i;

/**
 * Sniff a notebook code cell's language from its first meaningful line: SQL
 * when an SQL keyword statement opens it, python otherwise. Blank lines,
 * python and SQL comment lines are stepped over, so a commented-out SQL
 * header does not flip a python cell (and a python cell "creating a view"
 * mid-line stays python).
 */
export function detectLanguage(source: string): "python" | "sql" {
  for (const raw of source.split("\n")) {
    const line = raw.trim();
    if (line === "" || line.startsWith("#") || line.startsWith("--") || line.startsWith("/*") || line.startsWith("*")) {
      continue;
    }
    return SQL_LINE.test(line) ? "sql" : "python";
  }
  return "python";
}
