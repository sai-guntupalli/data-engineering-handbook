"use client";

import { createContext, useContext, useEffect, useSyncExternalStore, type ReactNode } from "react";

const SEARCH_EVENT = "de-handbook:searchchange";

type SearchState = {
  query: string;
  setQuery: (query: string) => void;
};

const SearchContext = createContext<SearchState>({ query: "", setQuery: () => {} });

function subscribeSearch(callback: () => void) {
  window.addEventListener(SEARCH_EVENT, callback);
  window.addEventListener("popstate", callback);
  return () => {
    window.removeEventListener(SEARCH_EVENT, callback);
    window.removeEventListener("popstate", callback);
  };
}

/** The URL `?q=` parameter is the store. Primitives compare by value, so the
 * snapshot identity is stable across calls. */
function getQuerySnapshot(): string {
  return new URLSearchParams(window.location.search).get("q") ?? "";
}

const getServerQuerySnapshot = () => "";

function notifySearchChanged() {
  window.dispatchEvent(new Event(SEARCH_EVENT));
}

/**
 * Single shared search state: the sticky site header owns the input, and the
 * notebook explorer below filters on it. The query lives in the URL so a
 * filtered view stays shareable, and / focuses the input from anywhere.
 */
export function SearchProvider({ children }: { children: ReactNode }) {
  const query = useSyncExternalStore(subscribeSearch, getQuerySnapshot, getServerQuerySnapshot);

  const setQuery = (value: string) => {
    const url = value
      ? `${window.location.pathname}?q=${encodeURIComponent(value)}`
      : window.location.pathname;
    window.history.replaceState(null, "", url);
    notifySearchChanged();
  };

  // Next's <Link> and router navigations mutate history via pushState and
  // replaceState, which fire no event React can observe. Patch both so the
  // URL-query store also updates across client-side navigation (e.g. leaving
  // /search?q=… through a link must clear the header input).
  useEffect(() => {
    const originalPushState = window.history.pushState.bind(window.history);
    const originalReplaceState = window.history.replaceState.bind(window.history);
    window.history.pushState = (...args) => {
      originalPushState(...args);
      notifySearchChanged();
    };
    window.history.replaceState = (...args) => {
      originalReplaceState(...args);
      notifySearchChanged();
    };
  }, []);

  // Press / to jump to the search input from anywhere.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable)
      ) {
        return;
      }
      event.preventDefault();
      document.getElementById("notebook-search")?.focus();
    };
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, []);

  return <SearchContext.Provider value={{ query, setQuery }}>{children}</SearchContext.Provider>;
}

export function useSearch(): SearchState {
  return useContext(SearchContext);
}