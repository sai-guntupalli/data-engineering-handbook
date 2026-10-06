"use client";

import { MagnifyingGlass } from "@phosphor-icons/react";
import Link from "next/link";
import { useMemo, useState } from "react";
import type { Topic } from "@/lib/topics";

export function TopicSearch({ topics }: { topics: Topic[] }) {
  const [query, setQuery] = useState("");
  const normalized = query.trim().toLowerCase();
  const results = useMemo(() => {
    if (!normalized) return topics.slice(0, 10);
    return topics
      .filter((topic) =>
        `${topic.title} ${topic.summary} ${topic.group}`.toLowerCase().includes(normalized),
      )
      .slice(0, 12);
  }, [normalized, topics]);

  return (
    <section className="search-panel" aria-label="Search topics">
      <label className="search-box">
        <MagnifyingGlass size={20} weight="bold" aria-hidden="true" />
        <span className="sr-only">Search topics</span>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search PySpark, CDC, Airflow, Iceberg..."
        />
      </label>
      <div className="search-results">
        {results.map((topic) => (
          <Link key={topic.slug} href={`/topics/${topic.slug}`}>
            <span>{topic.group}</span>
            <strong>{topic.title}</strong>
            <small>{topic.questionCount} questions</small>
          </Link>
        ))}
      </div>
    </section>
  );
}
