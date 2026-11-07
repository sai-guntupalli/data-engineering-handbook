"use client";

import { useSyncExternalStore } from "react";

const STARRED_KEY = "de-handbook:starred";
const STARRED_EVENT = "de-handbook:starredchange";
const EMPTY_STARRED = new Set<string>();

// Stable snapshot cache: getSnapshot must return the same identity while the
// raw storage value is unchanged, or React would re-render forever.
let starredRaw: string | null | undefined;
let starredCache: Set<string> = EMPTY_STARRED;

function subscribeStarred(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(STARRED_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(STARRED_EVENT, callback);
  };
}

function getStarredSnapshot(): Set<string> {
  let raw: string | null = null;
  try {
    raw = window.localStorage.getItem(STARRED_KEY);
  } catch {
    // storage unavailable: treat as empty
  }
  if (raw !== starredRaw) {
    starredRaw = raw;
    let list: string[] = [];
    try {
      if (raw) list = JSON.parse(raw) as string[];
    } catch {
      list = [];
    }
    starredCache = new Set(list);
  }
  return starredCache;
}

const getServerStarredSnapshot = (): Set<string> => EMPTY_STARRED;

/** The set of starred notebook paths (localStorage-backed, hydration-safe). */
export function useStarred(): Set<string> {
  return useSyncExternalStore(subscribeStarred, getStarredSnapshot, getServerStarredSnapshot);
}

export function toggleStar(repoPath: string) {
  const next = new Set(getStarredSnapshot());
  if (next.has(repoPath)) {
    next.delete(repoPath);
  } else {
    next.add(repoPath);
  }
  try {
    window.localStorage.setItem(STARRED_KEY, JSON.stringify([...next]));
  } catch {
    // storage may be unavailable (private mode quota); starring still works live
  }
  window.dispatchEvent(new Event(STARRED_EVENT));
}