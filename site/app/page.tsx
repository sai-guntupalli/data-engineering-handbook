import { ArrowRight, BookOpenText, CheckCircle, Play } from "@phosphor-icons/react/dist/ssr";
import { NotebookExplorer } from "@/components/NotebookExplorer";
import { SiteHeader } from "@/components/SiteHeader";
import { getNotebookGroups, getSearchIndex } from "@/lib/notebooks";
import { anchorFor } from "@/lib/notebook-groups";

const principles = [
  {
    icon: BookOpenText,
    title: "Read",
    text: "A short explanation sits in its own cell, written the way a textbook would write it.",
  },
  {
    icon: Play,
    title: "Run",
    text: "The example directly below it runs on Spark, so you see the result before you trust it.",
  },
  {
    icon: CheckCircle,
    title: "Check",
    text: "Self-checks assert the claims in the text, so a wrong answer fails loudly.",
  },
];

/** A static picture of a notebook: a note, a query and its output, drawn in the handbook's own style. */
function NotebookPreview() {
  return (
    <figure className="preview" aria-hidden>
      <div className="preview-cell preview-note">
        <span className="preview-label">Note</span>
        <p>A window function keeps every row and adds a value computed over related rows.</p>
      </div>
      <div className="preview-cell preview-code">
        <span className="preview-label">In [3]</span>
        <pre>{`SELECT customer_id, order_id, amount,
       SUM(amount) OVER (
         PARTITION BY customer_id
         ORDER BY order_id
       ) AS running_total
FROM orders`}</pre>
      </div>
      <div className="preview-cell preview-output">
        <span className="preview-label">Out [3]</span>
        <table>
          <thead>
            <tr>
              <th>customer_id</th>
              <th>order_id</th>
              <th>amount</th>
              <th>running_total</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>101</td>
              <td>120</td>
              <td>120</td>
            </tr>
            <tr>
              <td>1</td>
              <td>104</td>
              <td>80</td>
              <td>200</td>
            </tr>
            <tr>
              <td>2</td>
              <td>102</td>
              <td>450</td>
              <td>450</td>
            </tr>
          </tbody>
        </table>
      </div>
    </figure>
  );
}

export default function Home() {
  const practiceAnchor = anchorFor("Interview practice");
  const sqlAnchor = anchorFor("SQL learning path");

  return (
    <>
      <SiteHeader index={getSearchIndex()} />
      <main id="main-content">
        <section className="hero">
          <div className="hero-copy">
            <h1>
              Learn data engineering by <em>running</em> it.
            </h1>
            <p className="lede">
              Every topic is a Jupyter notebook you can run. Read the explanation, execute the example beneath it, and
              check your understanding. Each notebook opens in Google Colab, so there is nothing to install.
            </p>
            <div className="hero-actions">
              <a className="button primary" href={`#${practiceAnchor}`}>
                Start with interview practice
                <ArrowRight size={16} weight="bold" aria-hidden />
              </a>
              <a className="button ghost" href={`#${sqlAnchor}`}>
                Follow the SQL path
              </a>
            </div>
          </div>
          <NotebookPreview />
        </section>

        <section className="principles" aria-label="How every notebook is built">
          {principles.map(({ icon: Icon, title, text }) => (
            <article key={title} className="principle">
              <span className="principle-icon" aria-hidden>
                <Icon size={20} weight="bold" />
              </span>
              <h2>{title}</h2>
              <p>{text}</p>
            </article>
          ))}
        </section>

        <div className="content-shell" id="library">
          <div className="section-intro">
            <h2>Pick a topic, open a notebook.</h2>
          </div>
          <NotebookExplorer groups={getNotebookGroups()} />
        </div>
      </main>
    </>
  );
}
