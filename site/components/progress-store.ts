"use client";

import { useSyncExternalStore } from "react";
import { EMPTY_PROGRESS, markSectionRead, migrateProgress, parseProgress, setDone, type ProgressState } from "@/lib/progress";
import { RETIRED_PATHS } from "@/lib/retired";

const PROGRESS_KEY = "de-handbook:progress";
const PROGRESS_EVENT = "de-handbook:progresschange";

// getSnapshot must return the same object while the stored string is unchanged.
let cachedRaw: string | null | undefined;
let cachedState: ProgressState = EMPTY_PROGRESS;

function subscribe(callback: () => void) {
  window.addEventListener("storage", callback);
  window.addEventListener(PROGRESS_EVENT, callback);
  return () => {
    window.removeEventListener("storage", callback);
    window.removeEventListener(PROGRESS_EVENT, callback);
  };
}

function readSnapshot(): ProgressState {
  let raw: string | null;
  try {
    raw = window.localStorage.getItem(PROGRESS_KEY);
  } catch {
    return cachedState;
  }
  if (raw !== cachedRaw) {
    cachedRaw = raw;
    cachedState = migrateProgress(parseProgress(raw), RETIRED_PATHS);
  }
  return cachedState;
}

function write(next: ProgressState) {
  if (next === cachedState) return;
  cachedState = next;
  try {
    const raw = JSON.stringify(next);
    window.localStorage.setItem(PROGRESS_KEY, raw);
    cachedRaw = raw;
  } catch {
    // Storage can be unavailable (private mode); progress still updates for this visit.
  }
  window.dispatchEvent(new Event(PROGRESS_EVENT));
}

/** Reading progress for this browser; empty during server rendering. */
export function useProgress(): ProgressState {
  return useSyncExternalStore(subscribe, readSnapshot, () => EMPTY_PROGRESS);
}

export function recordSectionRead(repoPath: string, sectionId: string, total: number) {
  write(markSectionRead(readSnapshot(), repoPath, sectionId, total, new Date()));
}

export function recordDone(repoPath: string, done: boolean, total: number) {
  write(setDone(readSnapshot(), repoPath, done, total, new Date()));
}
