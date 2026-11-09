import { AppShell, catalogHref } from "@/components/AppShell";
import { Catalog } from "@/components/Catalog";
import { ContinueRow, type Starter } from "@/components/ContinueRow";
import { HomeHero } from "@/components/HomeHero";
import { LearningMap } from "@/components/LearningMap";
import { INTERVIEW_GROUP, anchorFor } from "@/lib/notebook-groups";
import { getLearningMap, getNotebookGroups, type NotebookGroupView } from "@/lib/notebooks";

/** The first notebook of a group, as a starting-point card. */
function starterFor(group: NotebookGroupView | undefined, text: string): Starter[] {
  const first = group?.notebooks[0];
  return group && first ? [{ title: first.title, text, href: first.href, tone: group.tone, group: group.label }] : [];
}

export default function Home() {
  const groups = getNotebookGroups();
  const notebooks = groups.flatMap((group) => group.notebooks);
  const byLabel = (label: string) => groups.find((group) => group.label === label);
  const python = byLabel("Python learning path");
  const sql = byLabel("SQL learning path");
  const practice = byLabel(INTERVIEW_GROUP.label);

  const starters = [
    ...starterFor(python, "Values, types and the standard library habits every pipeline depends on."),
    ...starterFor(sql, "Chapters from SELECT to window functions, each checked as it runs."),
    ...starterFor(practice, "Interview questions with model answers and runnable checks."),
  ];

  return (
    <AppShell crumbs={[{ label: "Library" }]} current="library">
      <HomeHero
        notebooks={notebooks}
        pythonStart={python!.notebooks[0]}
        sqlStart={sql!.notebooks[0]}
        practiceHref={catalogHref(anchorFor(INTERVIEW_GROUP.label))}
      />
      <LearningMap map={getLearningMap()} />
      <ContinueRow notebooks={notebooks} starters={starters} />

      <div className="section-head" id="catalog">
        <div>
          <h2>Catalog</h2>
          <p>
            {notebooks.length} notebooks in {groups.length} groups, each one runnable top to bottom
          </p>
        </div>
      </div>
      <Catalog groups={groups} />
    </AppShell>
  );
}
