"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef } from "react";
import { Hash, MagnifyingGlass } from "@phosphor-icons/react";
import type { NotebookSummary } from "@/lib/notebooks";
import { toneStyle } from "@/lib/tone";
import { highlightParts, matchNotebooks, searchEntries, type SearchEntry } from "@/lib/search";
import { CatalogTable } from "./CatalogTable";
import { useSearchIndex } from "./search-index";
import { setUrlParam, useUrlParam } from "./url-state";

const SECTION_LIMIT = 60;

function Marked({ text, query }: { text: string; query: string }) {
  return (
    <>
      {highlightParts(text, query).map((part, index) =>
        part.match ? (
          <mark key={index} className="search-mark">
            {part.text}
          </mark>
        ) : (
          <span key={index}>{part.text}</span>
        ),
      )}
    </>
  );
}

/** Full search results: matching notebooks as catalog rows, then matching sections. */
export function SearchView({ notebooks, initialEntries }: { notebooks: NotebookSummary[]; initialEntries: SearchEntry[] }) {
  const query = useUrlParam("q");
  const trimmed = query.trim();
  const inputRef = useRef<HTMLInputElement>(null);
  const { entries, failed } = useSearchIndex(true, initialEntries);

  useEffect(() => inputRef.current?.focus(), []);

  const matched = useMemo(() => (trimmed ? matchNotebooks(notebooks, trimmed) : notebooks), [notebooks, trimmed]);
  const sections = useMemo(
    () => (trimmed && entries ? searchEntries(entries, trimmed, { notebooks: 0, sections: SECTION_LIMIT }).sections : []),
    [entries, trimmed],
  );

  return (
    <>
      <section className="page-head">
        <div>
          <h1>{trimmed ? `Results for “${trimmed}”` : "Search the handbook"}</h1>
          <p className="lead">
            {trimmed
              ? `${matched.length} ${matched.length === 1 ? "notebook" : "notebooks"} and ${sections.length} ${sections.length === 1 ? "section" : "sections"} match.`
              : "Search every notebook title and section heading. Every notebook is listed below until you type."}
          </p>
        </div>
      </section>

      <label className="search-trigger search-field">
        <MagnifyingGlass size={16} aria-hidden />
        <input
          ref={inputRef}
          type="search"
          value={query}
          onChange={(event) => setUrlParam("q", event.target.value)}
          placeholder="Try window functions, partition, kafka…"
          aria-label="Search notebooks and sections"
          autoComplete="off"
        />
      </label>

      <div className="section-head">
        <h2>Notebooks</h2>
      </div>
      <section className="panel catalog" aria-label="Matching notebooks">
        {matched.length > 0 ? (
          <CatalogTable notebooks={matched} caption="Matching notebooks" />
        ) : (
          <div className="empty-state">
            <h2>No notebook titles match</h2>
            <p>Matching sections are listed below, when there are any.</p>
          </div>
        )}
      </section>

      {trimmed ? (
        <>
          <div className="section-head">
            <h2>Sections</h2>
          </div>
          <section className="panel catalog" aria-label="Matching sections">
            {failed ? (
              <div className="empty-state">
                <p>The section index did not load. Reload the page to try again.</p>
              </div>
            ) : sections.length > 0 ? (
              <ul className="section-results">
                {sections.map((section) => (
                  <li key={section.href}>
                    <Link className="nb" href={section.href}>
                      <span className="mono-tile" style={toneStyle(section.tone, "--tile")} aria-hidden>
                        <Hash size={14} weight="bold" />
                      </span>
                      <span>
                        <strong>
                          <Marked text={section.title} query={trimmed} />
                        </strong>
                        <small>
                          {section.notebookTitle}
                          {section.snippet ? ": " : ""}
                          {section.snippet}
                        </small>
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="empty-state">
                <h2>{entries ? "No section headings match" : "Loading sections…"}</h2>
                {entries ? (
                  <p>
                    Try a broader word, or <Link className="text-link" href="/">browse the library</Link>.
                  </p>
                ) : null}
              </div>
            )}
          </section>
        </>
      ) : null}
    </>
  );
}
