import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { CatalogTable } from "@/components/CatalogTable";
import { getTool, getTools } from "@/lib/notebooks";

export const dynamicParams = false;

/** Learning before practice; anything else alphabetical after them. */
const SECTION_ORDER = ["", "learning", "practice"];

function compareSections(a: string, b: string) {
  const rank = (name: string) => (SECTION_ORDER.includes(name) ? SECTION_ORDER.indexOf(name) : SECTION_ORDER.length);
  return rank(a) - rank(b) || a.localeCompare(b);
}

function titleCase(name: string) {
  return name.charAt(0).toUpperCase() + name.slice(1);
}

export function generateStaticParams() {
  return getTools().map((tool) => ({ tool: tool.folder }));
}

export async function generateMetadata({ params }: { params: Promise<{ tool: string }> }): Promise<Metadata> {
  const tool = getTool((await params).tool);
  return { title: tool ? `${tool.label} notebooks` : "Tool not found" };
}

export default async function ToolPage({ params }: { params: Promise<{ tool: string }> }) {
  const tool = getTool((await params).tool);
  if (!tool) notFound();
  const count = tool.notebooks.length;
  // A tool folder with subfolders (python/learning, python/practice) gets one section per subfolder.
  const names = [...new Set(tool.notebooks.map((notebook) => notebook.subfolder))].sort(compareSections);
  const sections = names.map((name) => ({ name, notebooks: tool.notebooks.filter((notebook) => notebook.subfolder === name) }));

  return (
    <AppShell crumbs={[{ label: "Library", href: "/" }, { label: tool.label }]} tool={tool.folder}>
      <header className="tool-head">
        <h1>{tool.label}</h1>
        <p className="lead">{tool.description}</p>
        <p className="tool-meta">
          {count} {count === 1 ? "notebook" : "notebooks"}. Lessons come first, then drills, coding challenges and
          interview questions.
        </p>
      </header>
      {sections.map((section) =>
        sections.length > 1 ? (
          <section key={section.name} className="tool-section" aria-labelledby={`section-${section.name}`}>
            <h2 id={`section-${section.name}`}>
              {titleCase(section.name)} <span className="count">{section.notebooks.length}</span>
            </h2>
            <div className="panel">
              <CatalogTable notebooks={section.notebooks} caption={`${tool.label}: ${section.name}`} />
            </div>
          </section>
        ) : (
          <section key={section.name} className="tool-section panel">
            <CatalogTable notebooks={section.notebooks} caption={`${tool.label} subtopics`} />
          </section>
        ),
      )}
    </AppShell>
  );
}
