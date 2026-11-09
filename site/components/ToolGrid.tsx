import Link from "next/link";
import type { ToolCategoryView } from "@/lib/notebooks";
import { toneStyle } from "@/lib/tone";

/** Tools as cards under their category headings. Each card links to its tool page, which lists the subtopics. */
export function ToolGrid({ categories }: { categories: ToolCategoryView[] }) {
  return (
    <div className="tool-categories">
      {categories.map((category) => (
        <section key={category.id} className="tool-category" aria-labelledby={`category-${category.id}`}>
          <h3 id={`category-${category.id}`}>{category.label}</h3>
          <ul className="tool-grid">
            {category.tools.map((tool) => (
              <li key={tool.folder}>
                <Link className="tool-card" href={tool.href}>
                  <span className="tool-card-head">
                    <span className="dot" style={toneStyle(tool.tone, "--dot")} aria-hidden />
                    <strong>{tool.label}</strong>
                    <span className="count">{tool.notebooks.length}</span>
                  </span>
                  <span className="tool-card-text">{tool.description}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}
