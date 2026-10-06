import { DownloadSimple, Notebook } from "@phosphor-icons/react/dist/ssr";
import { getAllNotebookSummaries } from "@/lib/notebooks";

export const metadata = {
  title: "Notebooks",
};

export default function NotebooksPage() {
  const notebooks = getAllNotebookSummaries();
  const practice = notebooks.filter((notebook) => notebook.group === "Practice");
  const topics = notebooks.filter((notebook) => notebook.group === "Topic");
  const markdown = notebooks.filter((notebook) => notebook.group === "Markdown");

  return (
    <main className="content-shell page-top">
      <div className="page-heading">
        <p className="kicker">Google Colab notebooks</p>
        <h1>Run the examples, don&apos;t just read them.</h1>
        <p>Every Markdown file is converted into a Colab-friendly notebook. Open in Colab to execute cells, or download the notebook for Jupyter, VS Code, or Databricks.</p>
      </div>
      <section className="topic-group">
        <h2>Hands-on practice notebooks</h2>
        <div className="topic-grid compact">
          {practice.map((notebook) => (
            <a key={notebook.downloadHref} href={notebook.colabHref} target="_blank" rel="noreferrer" className="topic-card">
              <Notebook size={22} weight="bold" />
              <strong>{notebook.title}</strong>
              <p>
                {notebook.codeCells} code cells, {notebook.assertCount} checks
              </p>
              <span>
                Open in Colab
              </span>
            </a>
          ))}
        </div>
      </section>
      <section className="topic-group">
        <h2>Topic notebooks generated from content</h2>
        <div className="topic-grid compact">
          {topics.map((notebook) => (
            <a key={notebook.downloadHref} href={notebook.colabHref} target="_blank" rel="noreferrer" className="topic-card">
              <Notebook size={22} weight="bold" />
              <strong>{notebook.title}</strong>
              <p>
                {notebook.markdownCells} notes, {notebook.codeCells} code cells
              </p>
              <span>
                Open in Colab
              </span>
            </a>
          ))}
        </div>
      </section>
      <section className="topic-group">
        <h2>Repository markdown notebooks</h2>
        <div className="topic-grid compact">
          {markdown.map((notebook) => (
            <a key={notebook.downloadHref} href={notebook.colabHref} target="_blank" rel="noreferrer" className="topic-card">
              <DownloadSimple size={22} weight="bold" />
              <strong>{notebook.title}</strong>
              <p>
                {notebook.markdownCells} notes, {notebook.codeCells} code cells
              </p>
              <span>Open in Colab</span>
            </a>
          ))}
        </div>
      </section>
    </main>
  );
}
