"use client";

import Link from "next/link";
import type { NotebookSummary } from "@/lib/notebooks";
import { toolStarKey } from "@/lib/sidebar";
import { toneStyle } from "@/lib/tone";
import { CatalogTable } from "./CatalogTable";
import { useStarred } from "./starred";

export type StarredTool = { folder: string; label: string; description: string; href: string; tone: string; count: number };

/** Tools and notebooks this browser has starred, in library order. */
export function StarredList({ tools, notebooks }: { tools: StarredTool[]; notebooks: NotebookSummary[] }) {
  const starred = useStarred();
  const starredTools = tools.filter((tool) => starred.has(toolStarKey(tool.folder)));
  const starredNotebooks = notebooks.filter((notebook) => starred.has(notebook.repoPath));

  if (starredTools.length === 0 && starredNotebooks.length === 0) {
    return (
      <div className="panel empty-state">
        <h2>Nothing starred yet</h2>
        <p>Star a topic from the sidebar, or a notebook from its row or its page. Stars stay on this device.</p>
      </div>
    );
  }

  return (
    <>
      {starredTools.length > 0 ? (
        <section className="tool-section" aria-labelledby="starred-topics">
          <h2 id="starred-topics">
            Topics <span className="count">{starredTools.length}</span>
          </h2>
          <ul className="tool-grid">
            {starredTools.map((tool) => (
              <li key={tool.folder}>
                <Link className="tool-card" href={tool.href}>
                  <span className="tool-card-head">
                    <span className="dot" style={toneStyle(tool.tone, "--dot")} aria-hidden />
                    <strong>{tool.label}</strong>
                    <span className="count">{tool.count}</span>
                  </span>
                  <span className="tool-card-text">{tool.description}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
      {starredNotebooks.length > 0 ? (
        <section className="tool-section" aria-labelledby="starred-notebooks">
          <h2 id="starred-notebooks">
            Notebooks <span className="count">{starredNotebooks.length}</span>
          </h2>
          <div className="panel">
            <CatalogTable notebooks={starredNotebooks} caption="Starred notebooks" />
          </div>
        </section>
      ) : null}
    </>
  );
}
