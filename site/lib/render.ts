/**
 * Build-time HTML for the notebook reader: markdown through marked, code through
 * highlight.js. Notebook content is the repository's own, so raw HTML in a
 * markdown cell is passed through as Jupyter would show it.
 */
import { Marked, type Tokens } from "marked";
import hljs from "highlight.js/lib/core";
import bash from "highlight.js/lib/languages/bash";
import java from "highlight.js/lib/languages/java";
import json from "highlight.js/lib/languages/json";
import python from "highlight.js/lib/languages/python";
import scala from "highlight.js/lib/languages/scala";
import sql from "highlight.js/lib/languages/sql";
import yaml from "highlight.js/lib/languages/yaml";

hljs.registerLanguage("bash", bash);
hljs.registerLanguage("java", java);
hljs.registerLanguage("json", json);
hljs.registerLanguage("python", python);
hljs.registerLanguage("scala", scala);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("yaml", yaml);

const LANGUAGE_ALIASES: Record<string, string> = {
  py: "python",
  pyspark: "python",
  sh: "bash",
  shell: "bash",
  console: "bash",
  yml: "yaml",
  sparksql: "sql",
};

function escapeHtml(text: string): string {
  return text.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

/** Highlighted HTML for one code block. Unknown languages are escaped as plain text. */
export function highlightCode(code: string, language = "python"): string {
  const name = LANGUAGE_ALIASES[language.toLowerCase()] ?? language.toLowerCase();
  if (!hljs.getLanguage(name)) return escapeHtml(code);
  return hljs.highlight(code, { language: name, ignoreIllegals: true }).value;
}

/**
 * Notebooks link to each other by file, as Jupyter and GitHub expect:
 * `pyspark-02-dataframe-essentials.ipynb#joins` or `../sql/sql-01-basics.ipynb`.
 * On the site each notebook lives at /notebooks/<file name>/, so a relative
 * .ipynb link becomes that reader URL, keeping its anchor. Every other href is
 * returned unchanged.
 */
export function notebookHref(href: string, basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? ""): string {
  const match = /^(?![a-z][a-z0-9+.-]*:|\/|#)(?:[^#?]*\/)?([^/#?]+)\.ipynb(#.*)?$/i.exec(href);
  if (!match) return href;
  return `${basePath}/notebooks/${match[1]}/${match[2] ?? ""}`;
}

/**
 * Render one markdown cell. `nextSectionId` hands out the ids that
 * parseNotebook allocated, in the same order, so the table of contents and the
 * headings agree. Level-1 headings after the title render as level 2 without
 * an id, so they never shift the section numbering.
 */
export function renderMarkdown(source: string, nextSectionId: () => string): string {
  const marked = new Marked({
    gfm: true,
    renderer: {
      heading({ tokens, depth }: Tokens.Heading) {
        const inner = this.parser.parseInline(tokens);
        if (depth === 2) return `<h2 id="${nextSectionId()}">${inner}</h2>\n`;
        const level = depth === 1 ? 2 : depth;
        return `<h${level}>${inner}</h${level}>\n`;
      },
      code({ text, lang }: Tokens.Code) {
        const language = (lang ?? "").split(/\s+/)[0] || "python";
        return `<pre><code class="hljs">${highlightCode(text, language)}</code></pre>\n`;
      },
      link({ href: rawHref, title, tokens }: Tokens.Link) {
        const inner = this.parser.parseInline(tokens);
        const href = notebookHref(rawHref);
        const external = /^https?:\/\//.test(href);
        const titleAttribute = title ? ` title="${escapeHtml(title)}"` : "";
        const target = external ? ' target="_blank" rel="noreferrer"' : "";
        return `<a href="${escapeHtml(href)}"${titleAttribute}${target}>${inner}</a>`;
      },
    },
  });
  return marked.parse(source, { async: false });
}
