"use client";

import Link from "next/link";
import { useMemo } from "react";
import type { NotebookListItem } from "@/lib/notebooks";
import { matchNotebooks } from "@/lib/search";
import { NotebookCard } from "./NotebookCard";
import { useSearch } from "./search-context";
import { starredFirst, useStarred } from "./starred";

/**
 * The /search results page: results start at the top of the page (there is no
 * hero here), react live to the query in the URL, and keep starred first.
 */
export function SearchResults({ notebooks }: { notebooks: NotebookListItem[] }) {
  const { query, setQuery } = useSearch();
  const starred = useStarred();
  const q = query.trim().toLowerCase();

  const matches = useMemo(
    () => starredFirst(q ? matchNotebooks(notebooks, q) : notebooks, starred),
    [notebooks, q, starred],
  );

  return (
    <>
      <h1>{q ? "Search results" : "All notebooks"}</h1>
      {q ? (
        <p className="results-meta search-summary">
          {matches.length} {matches.length === 1 ? "match" : "matches"} for{" "}
          <strong>“{query.trim()}”</strong>
          {starred.size > 0 ? (
            <>
              {" · "}
              <span className="starred-hint">★ {starred.size} starred first</span>
            </>
          ) : null}{" "}
          — <Link href="/">browse by group instead</Link>
        </p>
      ) : (
        <p className="results-meta search-summary">
          {matches.length} notebooks, starred first. Search in the header, or{" "}
          <Link href="/">browse by group</Link>.
        </p>
      )}
      {matches.length === 0 ? (
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
        <div className="topic-grid search-grid">
          {matches.map((notebook) => (
            <NotebookCard key={notebook.repoPath} notebook={notebook} />
          ))}
        </div>
      )}
    </>
  );
}