import type { Metadata } from "next";
import { SiteHeader } from "@/components/SiteHeader";
import { SearchResults } from "@/components/SearchResults";
import { getNotebookList, getSearchIndex } from "@/lib/notebooks";

export const metadata: Metadata = {
  title: "Search",
};

export default function SearchPage() {
  // Build-time data, static export; the ?q= client store filters live.
  const notebooks = getNotebookList();
  const index = getSearchIndex();

  return (
    <>
      <SiteHeader index={index} autoFocus panelOnFocus={false} />
      <main id="main-content">
        <div className="content-shell prose-shell">
          <SearchResults notebooks={notebooks} />
        </div>
      </main>
    </>
  );
}