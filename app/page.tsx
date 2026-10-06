import Link from "next/link";
import { ArrowRight, BookOpen, Code, GraduationCap, Notebook } from "@phosphor-icons/react/dist/ssr";
import { TopicSearch } from "@/components/TopicSearch";
import { getAllTopics, getGroupedTopics } from "@/lib/topics";

export default function Home() {
  const topics = getAllTopics();
  const groups = getGroupedTopics();
  const questionCount = topics.reduce((sum, topic) => sum + topic.questionCount, 0);
  const codeBlocks = topics.reduce((sum, topic) => sum + topic.codeBlockCount, 0);

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="kicker">Data engineering interview prep</p>
          <h1>Study the systems behind real pipelines.</h1>
          <p>
            Practical docs, runnable notebooks, and production-style examples for PySpark, SQL, lakehouse, cloud and orchestration.
          </p>
          <div className="hero-actions">
            <Link className="button primary" href="/topics">
              Browse topics <ArrowRight size={18} weight="bold" />
            </Link>
            <Link className="button secondary" href="/notebooks">
              Open notebooks
            </Link>
          </div>
        </div>
        <div className="hero-panel" aria-label="Guide statistics">
          <div>
            <BookOpen size={24} weight="bold" />
            <strong>{topics.length}</strong>
            <span>topics</span>
          </div>
          <div>
            <GraduationCap size={24} weight="bold" />
            <strong>{questionCount.toLocaleString()}</strong>
            <span>questions</span>
          </div>
          <div>
            <Code size={24} weight="bold" />
            <strong>{codeBlocks.toLocaleString()}</strong>
            <span>code examples</span>
          </div>
          <div>
            <Notebook size={24} weight="bold" />
            <strong>59</strong>
            <span>notebooks</span>
          </div>
        </div>
      </section>

      <div className="content-shell">
        <TopicSearch topics={topics} />

        <section className="path-grid" aria-label="Study paths">
          {[
            ["Core pipeline", "Python, SQL, PySpark, Spark tuning, Airflow and dbt", "/topics/spark"],
            ["Lakehouse", "Parquet, Delta, Iceberg, Hudi, CDC and modeling", "/topics/iceberg"],
            ["Cloud warehouse", "AWS, GCP, Azure, Databricks, Snowflake and Redshift", "/topics/aws"],
            ["All questions", "Scan the full question bank grouped by topic", "/questions"],
          ].map(([title, text, href]) => (
            <Link key={title} href={href}>
              <strong>{title}</strong>
              <span>{text}</span>
            </Link>
          ))}
        </section>

        <section className="group-list">
          <div className="section-heading">
            <h2>Browse by topic group</h2>
            <p>Each topic keeps the markdown source intact and renders as a polished app page.</p>
          </div>
          {groups.map((group) => (
            <section key={group.label} className="topic-group">
              <h3>{group.label}</h3>
              <div className="topic-grid">
                {group.topics.map((topic) => (
                  <Link key={topic.slug} href={`/topics/${topic.slug}`} className="topic-card">
                    <span>{topic.questionCount} questions</span>
                    <strong>{topic.title}</strong>
                    <p>{topic.summary}</p>
                  </Link>
                ))}
              </div>
            </section>
          ))}
        </section>
      </div>
    </main>
  );
}
