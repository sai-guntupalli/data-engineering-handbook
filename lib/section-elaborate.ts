import type { NotebookSection } from "./notebook-content";

/** The intro (notebook title, author, how-to) is not tutor material. */
const INTRO_SECTION_ID = "intro";

/** Headings whose only job is navigation — a list of anchors, nothing to explain. */
const NAV_HEADING = /^(contents|table of contents|outline|index)$/i;

/** Combined prose under this length (link syntax stripped, no code blocks)
 *  reads as a bare link list, also not tutor material. */
const TINY_SECTION_CHARS = 400;

/**
 * Whether a streamed tutor explanation is worth a button for this section.
 * Excluded: the intro (title/author/how-to), pure-navigation sections (a
 * "Contents"-family heading, or a code-less section whose prose is a short
 * link list), and any other tiny code-less section. Everything with code, and
 * every section with real prose, passes.
 *
 * Lives in its own client-safe module (no node:fs) so the viewer can call it;
 * lib/notebook-content.ts re-exports it as the single section API.
 */
export function isElaboratable(section: NotebookSection): boolean {
  if (section.id === INTRO_SECTION_ID) return false;
  if (NAV_HEADING.test(section.heading)) return false;
  if (section.blocks.some((block) => block.kind === "code")) return true;
  const prose = [
    section.heading,
    ...section.blocks
      .filter((block) => block.kind === "markdown")
      .map((block) => block.source),
  ]
    .join("\n\n")
    .replace(/\]\([^)]*\)/g, "") // markdown link targets
    .replace(/[\[\]]/g, ""); // leftover link/image bracket syntax
  return prose.trim().length >= TINY_SECTION_CHARS;
}
