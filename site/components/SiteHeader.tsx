"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useRef, useState, type KeyboardEvent, type ReactNode } from "react";
import { GithubLogo, MagnifyingGlass, X } from "@phosphor-icons/react";
import { repositoryHref } from "@/lib/site";
import { matchNotebooks, type SearchableNotebook } from "@/lib/search";
import { useSearch } from "./search-context";

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
 * Sticky header. Typing opens a suggestions panel under the search field; Enter
 * on a highlighted suggestion opens that notebook, plain Enter opens /search?q=….
 */
export function SiteHeader({
  index,
  autoFocus = false,
  panelOnFocus = true,
}: {
  index: SearchableNotebook[];
  autoFocus?: boolean;
  /** Open the suggestions panel when the input gains focus. The /search page
   * sets this false so its results stay the focus until the user types. */
  panelOnFocus?: boolean;
}) {
  const { query, setQuery } = useSearch();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(-1);
  const rootRef = useRef<HTMLDivElement>(null);
  const trimmed = query.trim();

  useEffect(() => {
    if (autoFocus) document.getElementById("notebook-search")?.focus();
  }, [autoFocus]);

  const matches = useMemo(() => {
    const found = matchNotebooks(index, query);
    return { rows: found.slice(0, MAX_SUGGESTIONS), total: found.length };
  }, [index, query]);

  const panelOpen = open && trimmed.length > 0;

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

  function closePanel() {
    setOpen(false);
    setActive(-1);
  }

  function commitSearch() {
    router.push(`/search?q=${encodeURIComponent(trimmed)}`);
    closePanel();
  }

  function onKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Escape" && open) {
      closePanel();
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
        window.open(picked.githubHref, "_blank", "noopener");
        closePanel();
      } else {
        commitSearch();
      }
    }
  }

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <Link className="brand" href="/" aria-label="Data Engineering Handbook, home">
          <span className="brand-mark" aria-hidden>
            DE
          </span>
          <span className="brand-name">Handbook</span>
        </Link>
        <div className="header-search" ref={rootRef}>
          <MagnifyingGlass size={16} weight="bold" aria-hidden />
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
            placeholder="Search notebooks and topics"
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
                closePanel();
              }}
              aria-label="Clear search"
            >
              <X size={12} weight="bold" aria-hidden />
            </button>
          ) : null}
          {panelOpen ? (
            <div className="suggest-panel" id="search-suggestions" role="listbox">
              {matches.rows.length > 0 ? (
                matches.rows.map((row, position) => (
                  <a
                    key={row.repoPath}
                    href={row.githubHref}
                    target="_blank"
                    rel="noreferrer"
                    className={position === active ? "suggest-item is-active" : "suggest-item"}
                    role="option"
                    aria-selected={position === active}
                    onMouseEnter={() => setActive(position)}
                    onClick={closePanel}
                  >
                    <span className="suggest-title">
                      <Highlighted text={row.title} query={trimmed} />
                    </span>
                    <span className="suggest-group">{row.groupLabel}</span>
                  </a>
                ))
              ) : (
                <p className="suggest-empty">Nothing matches “{trimmed}”.</p>
              )}
              <Link className="suggest-all" href={`/search?q=${encodeURIComponent(trimmed)}`} onClick={closePanel}>
                {matches.total > 0
                  ? `See all ${matches.total} ${matches.total === 1 ? "match" : "matches"}`
                  : "Search everything"}
              </Link>
            </div>
          ) : null}
        </div>
        <a className="header-github" href={repositoryHref} target="_blank" rel="noreferrer" aria-label="GitHub repository">
          <GithubLogo size={18} weight="regular" aria-hidden />
          <span>GitHub</span>
        </a>
      </div>
    </header>
  );
}
