import type { Metadata } from "next";
import { SiteHeader } from "@/components/SiteHeader";
import { SearchResults } from "@/components/SearchResults";
import { getNotebookGroups, getSearchIndex } from "@/lib/notebooks";

export const metadata: Metadata = {
  title: "Search",
};

export default function SearchPage() {
  // Build-time data, static export; the ?q= client store filters live.
  const notebooks = getNotebookGroups().flatMap((group) =>
    group.notebooks.map((notebook) => ({ ...notebook, groupLabel: group.label })),
  );
  const index = getSearchIndex();

  return (
    <>
      <SiteHeader index={index} autoFocus panelOnFocus={false} />
      <main id="main-content" className="search-page">
        <div className="content-shell page-top search-shell">
          <SearchResults notebooks={notebooks} />
        </div>
      </main>
    </>
  );
}