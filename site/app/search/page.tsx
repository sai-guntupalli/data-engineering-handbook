import type { Metadata } from "next";
import { AppShell } from "@/components/AppShell";
import { SearchView } from "@/components/SearchView";
import { getNotebookList } from "@/lib/notebooks";

export const metadata: Metadata = {
  title: "Search",
};

export default function SearchPage() {
  // Build-time notebook list; the ?q= parameter filters it in the browser.
  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "Search" }]}>
      <SearchView notebooks={getNotebookList()} />
    </AppShell>
  );
}
