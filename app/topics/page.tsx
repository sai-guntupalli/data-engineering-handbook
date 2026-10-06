import Link from "next/link";
import { TopicSearch } from "@/components/TopicSearch";
import { getAllTopics, getGroupedTopics } from "@/lib/topics";

export const metadata = {
  title: "Topics",
};

export default function TopicsPage() {
  const topics = getAllTopics();
  const groups = getGroupedTopics();

  return (
    <main className="content-shell page-top">
      <div className="page-heading">
        <p className="kicker">Topic index</p>
        <h1>Every topic in the guide.</h1>
        <p>Use search for quick access, or follow the grouped paths for structured study.</p>
      </div>
      <TopicSearch topics={topics} />
      {groups.map((group) => (
        <section key={group.label} className="topic-group">
          <h2>{group.label}</h2>
          <div className="topic-grid">
            {group.topics.map((topic) => (
              <Link key={topic.slug} className="topic-card" href={`/topics/${topic.slug}`}>
                <span>{topic.questionCount} questions</span>
                <strong>{topic.title}</strong>
                <p>{topic.summary}</p>
              </Link>
            ))}
          </div>
        </section>
      ))}
    </main>
  );
}
