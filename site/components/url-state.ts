"use client";

import { useSyncExternalStore } from "react";

const URL_EVENT = "de-handbook:urlchange";
let historyPatched = false;

/**
 * Next's router changes the URL through pushState and replaceState, which fire
 * no event. Wrap both once so URL-backed state follows client navigation.
 * The event is deferred so no store updates while React is rendering.
 */
function patchHistory() {
  if (historyPatched) return;
  historyPatched = true;
  for (const method of ["pushState", "replaceState"] as const) {
    const original = window.history[method].bind(window.history);
    window.history[method] = (...args: Parameters<History["pushState"]>) => {
      original(...args);
      queueMicrotask(() => window.dispatchEvent(new Event(URL_EVENT)));
    };
  }
}

function subscribe(callback: () => void) {
  patchHistory();
  window.addEventListener(URL_EVENT, callback);
  window.addEventListener("popstate", callback);
  return () => {
    window.removeEventListener(URL_EVENT, callback);
    window.removeEventListener("popstate", callback);
  };
}

/** A query-string parameter as React state. Empty on the server and when absent. */
export function useUrlParam(name: string): string {
  return useSyncExternalStore(
    subscribe,
    () => new URLSearchParams(window.location.search).get(name) ?? "",
    () => "",
  );
}

/** The URL fragment without the "#", decoded. Empty on the server. */
export function useUrlHash(): string {
  return useSyncExternalStore(
    subscribe,
    () => decodeURIComponent(window.location.hash.slice(1)),
    () => "",
  );
}

/** Replace one query parameter without adding a history entry. */
export function setUrlParam(name: string, value: string) {
  const url = new URL(window.location.href);
  if (value) {
    url.searchParams.set(name, value);
  } else {
    url.searchParams.delete(name);
  }
  window.history.replaceState(window.history.state, "", url);
}
