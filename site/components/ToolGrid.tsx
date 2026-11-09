import Link from "next/link";
import type { ToolView } from "@/lib/notebooks";
import { toneStyle } from "@/lib/tone";

/** Every tool as a card. Each card links to its tool page, which lists the subtopics. */
export function ToolGrid({ tools }: { tools: ToolView[] }) {
  return (
    <ul className="tool-grid">
      {tools.map((tool) => (
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
  );
}
