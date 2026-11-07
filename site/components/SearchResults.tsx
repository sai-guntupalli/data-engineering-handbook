"use client";

import Link from "next/link";
import { useMemo } from "react";
import type { NotebookListItem } from "@/lib/notebooks";
import { matchNotebooks } from "@/lib/search";
import { NotebookRow } from "./NotebookRow";
import { useSearch } from "./search-context";
import { starredFirst, useStarred } from "./starred";

/**
 * The /search results page: results start at the top of the page, react live to
 * the query in the URL, and keep starred notebooks first.
 */
export function SearchResults({ notebooks }: { notebooks: NotebookListItem[] }) {
  const { query, setQuery } = useSearch();
  const starred = useStarred();
  const trimmed = query.trim();

  const matches = useMemo(
    () => starredFirst(trimmed ? matchNotebooks(notebooks, trimmed) : notebooks, starred),
    [notebooks, trimmed, starred],
  );

  if (matches.length === 0) {
    return (
      <div className="search-empty">
        <h1>No notebooks match “{trimmed}”</h1>
        <p>
          Try a topic such as <code>sql</code>, <code>spark</code> or <code>kafka</code>, or{" "}
          <button type="button" className="text-button" onClick={() => setQuery("")}>
            clear the search
          </button>
          .
        </p>
      </div>
    );
  }

  return (
    <>
      <header className="page-heading">
        <h1>{trimmed ? `Results for “${trimmed}”` : "Every notebook"}</h1>
        <p className="page-lede">
          {matches.length} {matches.length === 1 ? "notebook" : "notebooks"}
          {trimmed ? "" : ", starred first"}.{" "}
          <Link href="/" className="text-link">
            Browse by topic
          </Link>
        </p>
      </header>
      <ol className="notebook-list">
        {matches.map((notebook) => (
          <NotebookRow key={notebook.repoPath} notebook={notebook} showGroup />
        ))}
      </ol>
    </>
  );
}
