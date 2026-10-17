import { marked } from "marked";

/**
 * Render repository-authored markdown to HTML. Content is committed to the
 * repository (trusted), so no sanitizer runs beyond marked's own defaults.
 * Synchronous by contract: blocks need their HTML at parse time, not lazily.
 */
export function renderMarkdown(md: string): string {
  return marked.parse(md, { async: false });
}