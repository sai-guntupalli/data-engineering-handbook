import type { Metadata } from "next";
import { AppShell } from "@/components/AppShell";
import { SearchView } from "@/components/SearchView";
import { getNotebookList, getSearchEntries } from "@/lib/notebooks";
import { siteUrl } from "@/lib/site";

export const metadata: Metadata = {
  title: "Search",
  alternates: { canonical: `${siteUrl}/search/` },
};

export default function SearchPage() {
  // Build-time notebook list; the ?q= parameter filters it in the browser.
  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "Search" }]}>
      <SearchView notebooks={getNotebookList()} initialEntries={getSearchEntries()} />
    </AppShell>
  );
}
