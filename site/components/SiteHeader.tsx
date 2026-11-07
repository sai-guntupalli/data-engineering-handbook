"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { MagnifyingGlass, X } from "@phosphor-icons/react";
import { TopicsMenu } from "./TopicsMenu";
import { repositoryHref } from "@/lib/site";
import { useSearch } from "./search-context";

/** Slim row for the suggestions panel; the /search page holds the full data. */
export type SearchIndexItem = {
  slug: string;
  title: string;
  groupLabel: string;
  repoPath: string;
  githubHref: string;
};

const MAX_SUGGESTIONS = 8;

function Highlighted({ text, query }: { text: string; query: string }) {
  if (!query) return <>{text}</>;
  const lower = text.toLowerCase();
  const needle = query.toLowerCase();
  const parts: ReactNode[] = [];
  let from = 0;
  while (from <= text.length) {
    const at = needle ? lower.indexOf(needle, from) : -1;
    if (at === -1) {
      parts.push(text.slice(from));
      break;
    }
    if (at > from) parts.push(text.slice(from, at));
    parts.push(<mark key={at}>{text.slice(at, at + needle.length)}</mark>);
    from = at + needle.length;
  }
  return <>{parts}</>;
}

/**
 * Sticky app header. Typing opens a suggestions panel right under the input
 * (visible above anything else); Enter with a highlighted suggestion opens
 * that notebook, plain Enter commits the search to /search?q=….
 */
export function SiteHeader({
  index,
  autoFocus = false,
  panelOnFocus = true,
}: {
  index: SearchIndexItem[];
  autoFocus?: boolean;
  /** Open the suggestions panel when the input gains focus. The /search page
   * sets this false: its results are already on screen, so the panel should
   * wait for actual typing. */
  panelOnFocus?: boolean;
}) {
  const { query, setQuery } = useSearch();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const rootRef = useRef<HTMLDivElement>(null);
  const q = query.trim().toLowerCase();

  useEffect(() => {
    if (autoFocus) document.getElementById("notebook-search")?.focus();
  }, [autoFocus]);

  const matches = useMemo(() => {
    if (!q) return { rows: [], total: 0 };
    const ranked = index
      .map((item) => {
        const title = item.title.toLowerCase();
        if (title.startsWith(q)) return { item, rank: 0 };
        if (title.includes(q)) return { item, rank: 1 };
        if (`${item.groupLabel} ${item.slug}`.toLowerCase().includes(q)) return { item, rank: 2 };
        return null;
      })
      .filter((row): row is { item: SearchIndexItem; rank: number } => row !== null)
      .sort((a, b) => a.rank - b.rank);
    return { rows: ranked.slice(0, MAX_SUGGESTIONS), total: ranked.length };
  }, [index, q]);

  const panelOpen = open && q.length > 0;

  useEffect(() => {
    if (!panelOpen) return;
    const onPointerDown = (event: PointerEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) {
        setOpen(false);
        setActive(-1);
      }
    };
    document.addEventListener("pointerdown", onPointerDown);
    return () => document.removeEventListener("pointerdown", onPointerDown);
  }, [panelOpen]);

  function commitSearch() {
    router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    setOpen(false);
    setActive(-1);
  }

  function onKeyDown(event: React.KeyboardEvent) {
    if (event.key === "Escape" && open) {
      setOpen(false);
      setActive(-1);
      return;
    }
    if (!panelOpen) return;
    const size = matches.rows.length;
    if (event.key === "ArrowDown" && size) {
      event.preventDefault();
      setActive((current) => (current + 1) % size);
    } else if (event.key === "ArrowUp" && size) {
      event.preventDefault();
      setActive((current) => (current <= 0 ? size - 1 : current - 1));
    } else if (event.key === "Enter") {
      event.preventDefault();
      const picked = active >= 0 ? matches.rows[active] : null;
      if (picked) {
        window.open(picked.item.githubHref, "_blank", "noopener");
        setOpen(false);
        setActive(-1);
      } else {
        commitSearch();
      }
    }
  }

  return (
    <header className="site-header">
      <Link className="brand" href="/">
        <span>DE</span>
        Handbook
      </Link>
      <div className="header-search" ref={rootRef}>
        <MagnifyingGlass size={15} weight="bold" />
        <input
          id="notebook-search"
          type="search"
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setOpen(true);
            setActive(-1);
          }}
          onKeyDown={onKeyDown}
          onFocus={() => {
            if (panelOnFocus) setOpen(true);
          }}
          placeholder="Search notebooks and topics…"
          aria-label="Search notebooks and topics"
          title="Press / to focus"
          autoComplete="off"
          aria-expanded={panelOpen}
          aria-controls="search-suggestions"
          role="combobox"
        />
        {query ? (
          <button
            type="button"
            className="search-clear"
            onClick={() => {
              setQuery("");
              setOpen(false);
              setActive(-1);
            }}
            aria-label="Clear search"
          >
            <X size={12} weight="bold" />
          </button>
        ) : null}
        {panelOpen ? (
          <div className="suggest-panel" id="search-suggestions" role="listbox">
            {matches.rows.length > 0 ? (
              matches.rows.map((row, position) => (
                <a
                  key={row.item.repoPath}
                  href={row.item.githubHref}
                  target="_blank"
                  rel="noreferrer"
                  className={position === active ? "suggest-item active" : "suggest-item"}
                  role="option"
                  aria-selected={position === active}
                  onMouseEnter={() => setActive(position)}
                  onClick={() => {
                    setOpen(false);
                    setActive(-1);
                  }}
                >
                  <span className="suggest-title">
                    <Highlighted text={row.item.title} query={query.trim()} />
                  </span>
                  <span className="suggest-group">{row.item.groupLabel}</span>
                </a>
              ))
            ) : (
              <p className="suggest-empty">Nothing matches “{query.trim()}”.</p>
            )}
            <Link
              className="suggest-all"
              href={`/search?q=${encodeURIComponent(query.trim())}`}
              onClick={() => {
                setOpen(false);
                setActive(-1);
              }}
            >
              {matches.total > 0
                ? `See all ${matches.total} ${matches.total === 1 ? "match" : "matches"}`
                : "Search everything"}{" "}
              →
            </Link>
          </div>
        ) : null}
      </div>
      <div className="header-actions">
        <TopicsMenu />
        <a className="header-github" href={repositoryHref} target="_blank" rel="noreferrer">
          GitHub
        </a>
      </div>
    </header>
  );
}