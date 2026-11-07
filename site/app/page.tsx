import { CheckCircle, Code, Lightning, Notebook } from "@phosphor-icons/react/dist/ssr";
import { NotebookExplorer } from "@/components/NotebookExplorer";
import { SiteHeader } from "@/components/SiteHeader";
import { getNotebookGroups, getNotebookStats, getSearchIndex } from "@/lib/notebooks";
import { repositoryHref } from "@/lib/site";

// Locale-pinned so the prerendered HTML matches what the client hydrates.
const count = new Intl.NumberFormat("en-US");

const heroStats = [
  { icon: Notebook, label: "notebooks" },
  { icon: Code, label: "code cells" },
  { icon: CheckCircle, label: "self-checks" },
];

export default function Home() {
  const groups = getNotebookGroups();
  const stats = getNotebookStats();
  const values = [stats.notebooks, stats.codeCells, stats.checks];
  const headerIndex = getSearchIndex();

  return (
    <>
      <SiteHeader index={headerIndex} />
      <main id="main-content">
        <section className="hero">
          <div className="hero-copy">
            <p className="kicker">The data engineering handbook</p>
            <h1>Every topic is a notebook you can run.</h1>
            <p>
              Notes and code live together as Jupyter notebooks: one explanation per cell, a runnable example right
              below it, and self-checks that verify every claim. Every notebook opens in Google Colab and runs top to bottom with
              no local setup.
            </p>
            <div className="hero-actions">
              <a className="button primary" href="#hands-on-practice">
                Start with practice <Lightning size={18} weight="bold" />
              </a>
              <a className="button secondary" href={repositoryHref} target="_blank" rel="noreferrer">
                View on GitHub
              </a>
            </div>
          </div>
          <dl className="hero-panel" aria-label="Notebook statistics">
            {heroStats.map(({ icon: Icon, label }, index) => (
              <div key={label}>
                <dt>{label}</dt>
                <dd>
                  <Icon size={24} weight="bold" />
                  <strong>{count.format(values[index])}</strong>
                </dd>
              </div>
            ))}
          </dl>
        </section>

        <div className="content-shell page-top">
          <NotebookExplorer
            groups={groups.map((group) => ({
              label: group.label,
              notebooks: group.notebooks.map((notebook) => ({ ...notebook, groupLabel: group.label })),
            }))}
          />
        </div>
      </main>
    </>
  );
}