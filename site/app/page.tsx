import { AppShell } from "@/components/AppShell";
import { siteUrl } from "@/lib/site";
export const metadata = { alternates: { canonical: `${siteUrl}/` } };
import { ContinueRow, type Starter } from "@/components/ContinueRow";
import { HomeHero } from "@/components/HomeHero";
import { LearningMap } from "@/components/LearningMap";
import { ToolGrid } from "@/components/ToolGrid";
import { getLearningPath, getNotebookList, getTool, getToolCategories, getTools, type ToolView } from "@/lib/notebooks";

/** The first subtopic of a tool, as a starting-point card. */
function starterFor(tool: ToolView | null, text: string): Starter[] {
  const first = tool?.notebooks[0];
  return tool && first ? [{ title: first.title, text, href: first.href, tone: tool.tone, tool: tool.label }] : [];
}

export default function Home() {
  const tools = getTools();
  const notebooks = getNotebookList();
  const python = getTool("python");
  const sql = getTool("sql");
  const interview = getTool("interview-questions");

  const starters = [
    ...starterFor(python, "Values, types and the standard library habits every pipeline depends on."),
    ...starterFor(sql, "Chapters from SELECT to window functions, each checked as it runs."),
    ...starterFor(interview, "Interview questions with model answers and runnable checks."),
  ];

  return (
    <AppShell crumbs={[{ label: "Library" }]} current="library">
      <HomeHero
        notebooks={notebooks}
        pythonStart={python!.notebooks[0]}
        sqlStart={sql!.notebooks[0]}
        practiceHref={interview!.href}
      />
      <LearningMap path={getLearningPath()} />
      <ContinueRow notebooks={notebooks} starters={starters} />

      <div className="section-head" id="topics">
        <div>
          <h2>Topics</h2>
          <p>
            {tools.length} topics and {notebooks.length} notebooks, grouped by what they cover. Open a topic to see its notebooks.
          </p>
        </div>
      </div>
      <ToolGrid categories={getToolCategories()} />
    </AppShell>
  );
}
