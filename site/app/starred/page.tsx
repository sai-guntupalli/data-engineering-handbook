import type { Metadata } from "next";
import { AppShell } from "@/components/AppShell";
import { StarredList } from "@/components/StarredList";
import { getNotebookList, getTools } from "@/lib/notebooks";

export const metadata: Metadata = { title: "Starred" };

export default function StarredPage() {
  const tools = getTools().map((tool) => ({
    folder: tool.folder,
    label: tool.label,
    description: tool.description,
    href: tool.href,
    tone: tool.tone,
    count: tool.notebooks.length,
  }));
  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: "Starred" }]} current="starred">
      <header className="tool-head">
        <h1>Starred</h1>
        <p className="lead">Tools and notebooks you starred on this device. Stars are stored in this browser only.</p>
      </header>
      <StarredList tools={tools} notebooks={getNotebookList()} />
    </AppShell>
  );
}
