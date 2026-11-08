"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
  type ReactNode,
} from "react";
import { ArrowSquareOut, CaretRight, Hash, KeyReturn, MagnifyingGlass } from "@phosphor-icons/react";
import { recentInProgress } from "@/lib/progress";
import { highlightParts, searchEntries, type SearchEntry } from "@/lib/search";
import { toneStyle } from "@/lib/tone";
import { useProgress } from "./progress-store";
import { useSearchIndex } from "./search-index";
import { StatusPill } from "./StatusPill";

type PaletteState = { open: () => void };
const PaletteContext = createContext<PaletteState>({ open: () => {} });

const LIMITS = { notebooks: 6, sections: 12 };
const STARTING_POINTS = ["notebooks/topics/python-01-values-and-types.ipynb", "notebooks/topics/sql-01-basics.ipynb"];

type Scope = "all" | "notebook" | "section";

function isTyping(target: EventTarget | null): boolean {
  const element = target as HTMLElement | null;
  return !!element && (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.isContentEditable);
}

/** Owns the palette's open state and the ⌘K / Ctrl+K and / shortcuts. */
export function PaletteProvider({ children }: { children: ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const open = useCallback(() => setIsOpen(true), []);

  useEffect(() => {
    const onKeyDown = (event: globalThis.KeyboardEvent) => {
      const modK = event.key.toLowerCase() === "k" && (event.metaKey || event.ctrlKey);
      const slash = event.key === "/" && !event.metaKey && !event.ctrlKey && !event.altKey && !isTyping(event.target);
      if (modK || slash) {
        event.preventDefault();
        setIsOpen(true);
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []);

  const value = useMemo(() => ({ open }), [open]);
  return (
    <PaletteContext.Provider value={value}>
      {children}
      {isOpen ? <CommandPalette onClose={() => setIsOpen(false)} /> : null}
    </PaletteContext.Provider>
  );
}

export function usePalette(): PaletteState {
  return useContext(PaletteContext);
}

/** The search field in the top bar: a button that opens the palette. */
export function SearchTrigger() {
  const { open } = usePalette();
  return (
    <button type="button" className="search-trigger" onClick={open} aria-label="Search notebooks and sections">
      <MagnifyingGlass size={16} aria-hidden />
      <span>Search notebooks and sections</span>
      <kbd aria-hidden>⌘</kbd>
      <kbd aria-hidden>K</kbd>
    </button>
  );
}

export function SidebarSearchButton() {
  const { open } = usePalette();
  return (
    <button type="button" className="nav-link" onClick={open}>
      <MagnifyingGlass size={16} aria-hidden />
      <span className="nav-text">Search</span>
      <span className="nav-count">/</span>
    </button>
  );
}

function Highlighted({ text, query }: { text: string; query: string }) {
  return (
    <>
      {highlightParts(text, query).map((part, index) =>
        part.match ? <mark key={index}>{part.text}</mark> : <span key={index}>{part.text}</span>,
      )}
    </>
  );
}

function ResultRow({
  entry,
  id,
  query,
  selected,
  onHover,
  onPick,
}: {
  entry: SearchEntry;
  id: string;
  query: string;
  selected: boolean;
  onHover: () => void;
  onPick: () => void;
}) {
  const tile = toneStyle(entry.tone, "--tile");
  return (
    <div
      id={id}
      role="option"
      aria-selected={selected}
      className="result"
      onMouseMove={onHover}
      onClick={onPick}
    >
      <span className="mono-tile" style={tile} aria-hidden>
        {entry.kind === "section" ? <Hash size={14} weight="bold" /> : entry.monogram}
      </span>
      <span className="meta">
        <strong>
          <Highlighted text={entry.title} query={query} />
        </strong>
        <small>{entry.kind === "section" ? entry.notebookTitle : entry.groupLabel}</small>
      </span>
      <KeyReturn size={16} className="enter" aria-hidden />
    </div>
  );
}

function Preview({ entry, query, onOpen }: { entry: SearchEntry; query: string; onOpen: () => void }) {
  const progress = useProgress();
  return (
    <div className="preview" aria-live="polite">
      <div className="preview-path">
        <span className="dot" style={toneStyle(entry.tone, "--dot")} aria-hidden />
        {entry.kind === "section" ? (
          <>
            {entry.notebookTitle}
            <CaretRight size={12} aria-hidden />
            Section
          </>
        ) : (
          entry.groupLabel
        )}
      </div>
      <h3>{entry.title}</h3>
      {entry.snippet ? (
        <p>
          <Highlighted text={entry.snippet} query={query} />
        </p>
      ) : null}
      <div className="meta-row">
        <StatusPill entry={progress.notebooks[entry.repoPath]} />
        {entry.kind === "section" ? <span className="tag">{entry.groupLabel}</span> : null}
      </div>
      <div className="actions">
        <Link className="btn btn-primary" href={entry.href} onClick={onOpen}>
          {entry.kind === "section" ? "Open section" : "Open notebook"}
        </Link>
        <a className="btn" href={entry.colabHref} target="_blank" rel="noreferrer">
          <ArrowSquareOut size={15} aria-hidden />
          Open in Colab
        </a>
      </div>
    </div>
  );
}

function CommandPalette({ onClose }: { onClose: () => void }) {
  const router = useRouter();
  const progress = useProgress();
  const { entries, failed } = useSearchIndex(true);
  const [query, setQuery] = useState("");
  const [scope, setScope] = useState<Scope>("all");
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  // Lock page scroll and put focus back where it was when the palette closes.
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    inputRef.current?.focus();
    return () => {
      document.body.style.overflow = overflow;
      previous?.focus?.();
    };
  }, []);

  const results = useMemo(() => searchEntries(entries ?? [], query, LIMITS), [entries, query]);

  // With no query, offer the notebooks the reader is in the middle of, or two starting points.
  const suggestions = useMemo(() => {
    if (!entries) return [];
    const recent = recentInProgress(progress, 4);
    const wanted = recent.length > 0 ? recent : STARTING_POINTS;
    return wanted.flatMap((repoPath) => entries.filter((e) => e.kind === "notebook" && e.repoPath === repoPath));
  }, [entries, progress]);

  const hasQuery = query.trim().length > 0;
  const groups: { label: string; items: SearchEntry[] }[] = hasQuery
    ? [
        { label: "Notebooks", items: scope === "section" ? [] : results.notebooks },
        { label: "Sections", items: scope === "notebook" ? [] : results.sections },
      ].filter((group) => group.items.length > 0)
    : suggestions.length > 0
      ? [{ label: recentInProgress(progress, 1).length > 0 ? "Continue reading" : "Good places to start", items: suggestions }]
      : [];
  const flat = groups.flatMap((group) => group.items);
  const selectedIndex = Math.min(active, Math.max(flat.length - 1, 0));
  const selected = flat[selectedIndex];

  useEffect(() => {
    document.getElementById(`palette-option-${selectedIndex}`)?.scrollIntoView({ block: "nearest" });
  }, [selectedIndex]);

  function pick(entry: SearchEntry | undefined) {
    if (!entry) return;
    onClose();
    router.push(entry.href);
  }

  function onKeyDown(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key === "Escape") {
      event.preventDefault();
      onClose();
    } else if (event.key === "ArrowDown" && flat.length) {
      event.preventDefault();
      setActive((selectedIndex + 1) % flat.length);
    } else if (event.key === "ArrowUp" && flat.length) {
      event.preventDefault();
      setActive((selectedIndex - 1 + flat.length) % flat.length);
    } else if (event.key === "Enter" && selected) {
      event.preventDefault();
      if (event.metaKey || event.ctrlKey) {
        window.open(selected.colabHref, "_blank", "noopener");
      } else {
        pick(selected);
      }
    } else if (event.key === "Tab") {
      // Keep focus in the dialog: the input drives every control.
      event.preventDefault();
      inputRef.current?.focus();
    }
  }

  const counts = {
    all: results.notebooks.length + results.sections.length,
    notebook: results.notebooks.length,
    section: results.sections.length,
  };

  let optionIndex = -1;

  return (
    <div
      className="scrim"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <div className="palette" role="dialog" aria-modal="true" aria-label="Search the handbook" onKeyDown={onKeyDown}>
        <div className="palette-input">
          <MagnifyingGlass size={20} aria-hidden />
          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
              setActive(0);
            }}
            placeholder="Search notebooks and sections"
            aria-label="Search notebooks and sections"
            role="combobox"
            aria-expanded="true"
            aria-controls="palette-results"
            aria-activedescendant={selected ? `palette-option-${selectedIndex}` : undefined}
            autoComplete="off"
            spellCheck={false}
          />
          <button type="button" onClick={onClose} aria-label="Close search">
            <kbd>esc</kbd>
          </button>
        </div>

        {hasQuery ? (
          <div className="palette-scope" role="group" aria-label="Result type">
            {(
              [
                ["all", "All"],
                ["notebook", "Notebooks"],
                ["section", "Sections"],
              ] as const
            ).map(([value, label]) => (
              <button
                key={value}
                type="button"
                className="scope"
                aria-pressed={scope === value}
                onClick={() => {
                  setScope(value);
                  setActive(0);
                  inputRef.current?.focus();
                }}
              >
                {label} <span className="count">{counts[value]}</span>
              </button>
            ))}
          </div>
        ) : null}

        <div className="palette-split">
          <div className="palette-list" id="palette-results" role="listbox" aria-label="Results">
            {failed ? (
              <p className="palette-empty">The search index did not load. Check your connection and reopen search.</p>
            ) : !entries ? (
              <p className="palette-empty">Loading the index…</p>
            ) : hasQuery && flat.length === 0 ? (
              <p className="palette-empty">
                Nothing matches “{query.trim()}”. Try a tool such as <strong>spark</strong> or a concept such as{" "}
                <strong>window</strong>.
              </p>
            ) : (
              groups.map((group) => (
                <div key={group.label} role="group" aria-label={group.label}>
                  <div className="palette-section">{group.label}</div>
                  {group.items.map((entry) => {
                    optionIndex += 1;
                    const index = optionIndex;
                    return (
                      <ResultRow
                        key={`${entry.kind}-${entry.href}`}
                        id={`palette-option-${index}`}
                        entry={entry}
                        query={query}
                        selected={index === selectedIndex}
                        onHover={() => setActive(index)}
                        onPick={() => pick(entry)}
                      />
                    );
                  })}
                </div>
              ))
            )}
          </div>
          {selected ? (
            <Preview entry={selected} query={query} onOpen={onClose} />
          ) : (
            <div className="preview">
              <p>Type to search every notebook title and section heading in the handbook.</p>
            </div>
          )}
        </div>

        <div className="palette-foot">
          <span>
            <kbd>↑</kbd>
            <kbd>↓</kbd> Move
          </span>
          <span>
            <kbd>↵</kbd> Open
          </span>
          <span>
            <kbd>⌘</kbd>
            <kbd>↵</kbd> Open in Colab
          </span>
          {hasQuery && results.total > 0 ? (
            <Link href={`/search/?q=${encodeURIComponent(query.trim())}`} onClick={onClose}>
              See all {results.total} results
            </Link>
          ) : null}
        </div>
      </div>
    </div>
  );
}
