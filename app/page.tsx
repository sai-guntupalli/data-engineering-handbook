import { Code, GithubLogo, Lightning, Notebook } from "@phosphor-icons/react/dist/ssr";
import { getNotebookGroups, getNotebookStats, repositoryHref } from "@/lib/notebooks";

export default function Home() {
  const groups = getNotebookGroups();
  const stats = getNotebookStats();

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="kicker">Data engineering interview notebooks</p>
          <h1>Every topic is a notebook you can run.</h1>
          <p>
            Notes and code live together as Jupyter notebooks. Open one in Colab to run the cells, or read the
            source on GitHub. No separate documentation to keep in sync.
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
        <div className="hero-panel" aria-label="Notebook statistics">
          <div>
            <Notebook size={24} weight="bold" />
            <strong>{stats.notebooks}</strong>
            <span>notebooks</span>
          </div>
          <div>
            <Code size={24} weight="bold" />
            <strong>{stats.codeCells.toLocaleString()}</strong>
            <span>code cells</span>
          </div>
          <div>
            <GithubLogo size={24} weight="bold" />
            <strong>{stats.checks.toLocaleString()}</strong>
            <span>self-checks</span>
          </div>
        </div>
      </section>

      <div className="content-shell page-top">
        {groups.map((group) => (
          <section key={group.label} className="topic-group" id={anchorFor(group.label)}>
            <div className="section-heading">
              <h2>{group.label}</h2>
              <p>
                {group.notebooks.length} {group.notebooks.length === 1 ? "notebook" : "notebooks"}
              </p>
            </div>
            <div className="topic-grid">
              {group.notebooks.map((notebook) => (
                <article key={notebook.repoPath} className="topic-card">
                  <span>{notebook.codeCells} code cells</span>
                  <strong>{notebook.title}</strong>
                  {notebook.description ? <p>{notebook.description}</p> : null}
                  <div className="notebook-links">
                    <a href={notebook.colabHref} target="_blank" rel="noreferrer">
                      Open in Colab
                    </a>
                    <a href={notebook.githubHref} target="_blank" rel="noreferrer">
                      GitHub
                    </a>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}

function anchorFor(label: string) {
  return label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
