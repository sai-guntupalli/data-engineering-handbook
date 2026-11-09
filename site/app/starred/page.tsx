import type { Metadata } from "next";
import { AppShell } from "@/components/AppShell";
import { StarredList } from "@/components/StarredList";
import { getNotebookList } from "@/lib/notebooks";

export const metadata: Metadata = { title: "Starred notebooks" };

export default function StarredPage() {
  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "Starred" }]}>
      <header className="tool-head">
        <h1>Starred</h1>
        <p className="lead">Notebooks you starred on this device. Stars are stored in this browser only.</p>
      </header>
      <section className="panel">
        <StarredList notebooks={getNotebookList()} />
      </section>
    </AppShell>
  );
}
