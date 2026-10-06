import Link from "next/link";
import { repositoryHref } from "@/lib/notebooks";

export function SiteHeader() {
  return (
    <header className="site-header">
      <Link className="brand" href="/">
        <span>DE</span>
        Interview Notebooks
      </Link>
      <nav aria-label="Primary navigation">
        <Link href="/#hands-on-practice">Practice</Link>
        <Link href="/#core-pipeline-skills">Core</Link>
        <Link href="/#lakehouse-and-formats">Lakehouse</Link>
        <Link href="/#cloud-and-platforms">Cloud</Link>
        <a href={repositoryHref} target="_blank" rel="noreferrer">
          GitHub
        </a>
      </nav>
    </header>
  );
}
