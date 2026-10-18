import hljs from "highlight.js/lib/core";
import bash from "highlight.js/lib/languages/bash";
import json from "highlight.js/lib/languages/json";
import plaintext from "highlight.js/lib/languages/plaintext";
import python from "highlight.js/lib/languages/python";
import sql from "highlight.js/lib/languages/sql";

import { detectLanguage } from "./markdown";

// A lean registration set: notebook cells are python or SQL (detectLanguage);
// json/bash/plaintext are there for the remaining source shapes.
hljs.registerLanguage("python", python);
hljs.registerLanguage("sql", sql);
hljs.registerLanguage("json", json);
hljs.registerLanguage("bash", bash);
hljs.registerLanguage("plaintext", plaintext);

/**
 * highlighted HTML for a notebook code cell. Pristine cells render this in a
 * `pre code.hljs` (styles live in app/globals.css); hljs escapes plain text
 * itself, so the markup is safe to inject.
 */
export function highlightCell(source: string): string {
  return hljs.highlight(source, { language: detectLanguage(source) }).value;
}
