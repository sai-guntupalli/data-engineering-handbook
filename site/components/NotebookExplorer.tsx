"use client";

import { useMemo } from "react";
import { anchorFor } from "@/lib/notebook-groups";
import type { NotebookGroupView } from "@/lib/notebooks";
import { NotebookRow } from "./NotebookRow";
import { starredFirst, useStarred } from "./starred";

/**
 * The library: a topic index beside every group in declared order. On narrow
 * screens the index becomes a horizontally scrolling strip above the groups.
 */
export function NotebookExplorer({ groups }: { groups: NotebookGroupView[] }) {
  const starred = useStarred();

  const sections = useMemo(
    () => groups.map((group) => ({ ...group, notebooks: starredFirst(group.notebooks, starred) })),
    [groups, starred],
  );

  return (
    <div className="library">
      <nav className="library-index" aria-label="Topics">
        <p className="eyebrow">Topics</p>
        <ul>
          {groups.map((group) => (
            <li key={group.label}>
              <a href={`#${anchorFor(group.label)}`}>{group.label}</a>
            </li>
          ))}
        </ul>
      </nav>
      <div className="library-groups">
        {starred.size > 0 ? (
          <p className="starred-note">Starred notebooks are listed first within their topic.</p>
        ) : null}
        {sections.map((group) => (
          <section key={group.label} id={anchorFor(group.label)} className="topic-section">
            <h2 className="topic-heading">{group.label}</h2>
            <ol className="notebook-list">
              {group.notebooks.map((notebook, index) => (
                <NotebookRow key={notebook.repoPath} notebook={notebook} position={index + 1} />
              ))}
            </ol>
          </section>
        ))}
      </div>
    </div>
  );
}
