"use client";

import { useMemo, useState } from "react";
import { MagnifyingGlass, X } from "@phosphor-icons/react";
import { anchorFor } from "@/lib/notebook-groups";

export type ExplorerNotebook = {
  repoPath: string;
  slug: string;
  title: string;
  description: string;
  githubHref: string;
};

export type ExplorerGroup = {
  label: string;
  notebooks: ExplorerNotebook[];
};

export function NotebookExplorer({ groups }: { groups: ExplorerGroup[] }) {
  const [query, setQuery] = useState("");
  const q = query.trim().toLowerCase();

  const filtered = useMemo(() => {
    if (!q) return groups;
    return groups
      .map((group) => ({
        ...group,
        notebooks: group.notebooks.filter((notebook) =>
          `${notebook.title} ${notebook.description} ${notebook.slug} ${notebook.repoPath} ${group.label}`
            .toLowerCase()
            .includes(q),
        ),
      }))
      .filter((group) => group.notebooks.length > 0);
  }, [groups, q]);

  const count = filtered.reduce((total, group) => total + group.notebooks.length, 0);

  return (
    <div className="explorer">
      <div className="search-bar">
        <MagnifyingGlass size={17} weight="bold" />
        <input
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search notebooks and topics…"
          aria-label="Search notebooks and topics"
        />
        {query ? (
          <button type="button" className="search-clear" onClick={() => setQuery("")}>
            <X size={13} weight="bold" />
            Clear
          </button>
        ) : null}
      </div>
      {q ? (
        <p className="results-meta">
          {count} {count === 1 ? "match" : "matches"} for <strong>“{query.trim()}”</strong>
          {" across "}
          {filtered.length} {filtered.length === 1 ? "group" : "groups"}
        </p>
      ) : null}
      {count === 0 ? (
        <div className="search-empty">
          <p>
            Nothing matches <strong>“{query.trim()}”</strong>.
          </p>
          <p>
            Try a topic name such as <code>sql</code>, <code>spark</code> or <code>kafka</code>, or{" "}
            <button type="button" onClick={() => setQuery("")}>
              clear the search
            </button>
            .
          </p>
        </div>
      ) : (
        filtered.map((group) => (
          <section key={group.label} className="topic-group" id={anchorFor(group.label)}>
            <div className="section-heading">
              <h2>{group.label}</h2>
              <p>
                {group.notebooks.length} {group.notebooks.length === 1 ? "notebook" : "notebooks"}
              </p>
            </div>
            <div className="topic-grid">
              {group.notebooks.map((notebook) => (
                <article key={notebook.repoPath} className="topic-card">
                  <strong>{notebook.title}</strong>
                  {notebook.description ? <p>{notebook.description}</p> : null}
                  <div className="notebook-links">
                    <a href={notebook.githubHref} target="_blank" rel="noreferrer">
                      GitHub
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))
      )}
    </div>
  );
}