"use client";

import { useEffect, useState } from "react";
import type { SearchEntry } from "@/lib/search";

const INDEX_URL = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/search-index.json`;

let pending: Promise<SearchEntry[]> | null = null;
let cached: SearchEntry[] | null = null;

/** Fetch the notebook and section index once per page load; a failure can be retried. */
function loadSearchIndex(): Promise<SearchEntry[]> {
  pending ??= fetch(INDEX_URL)
    .then((response) => {
      if (!response.ok) throw new Error(`search index returned ${response.status}`);
      return response.json() as Promise<SearchEntry[]>;
    })
    .then((entries) => { cached = entries; return entries; })
    .catch((error: unknown) => {
      pending = null;
      throw error;
    });
  return pending;
}

export type SearchIndexState = { entries: SearchEntry[] | null; failed: boolean };

/** The search index, loaded the first time `enabled` is true. */
export function useSearchIndex(enabled: boolean, initial: SearchEntry[] | null = null): SearchIndexState {
  const [state, setState] = useState<SearchIndexState>({ entries: initial ?? cached, failed: false });

  useEffect(() => {
    if (!enabled || state.entries) return;
    let cancelled = false;
    loadSearchIndex().then(
      (entries) => {
        if (!cancelled) setState({ entries, failed: false });
      },
      () => {
        if (!cancelled) setState({ entries: null, failed: true });
      },
    );
    return () => {
      cancelled = true;
    };
  }, [enabled, state.entries]);

  return state;
}
