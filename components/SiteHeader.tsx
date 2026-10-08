import Link from "next/link";
import { NAV_ITEMS } from "@/lib/notebook-groups";
import { repositoryHref } from "@/lib/notebooks";

export function SiteHeader() {
  return (
    <header className="site-header">
      <Link className="brand" href="/">
        <span>DE</span>
        Interview Notebooks
      </Link>
      <nav aria-label="Primary navigation">
        {NAV_ITEMS.map((item) => (
          <Link key={item.href} href={item.href}>
            {item.label}
          </Link>
        ))}
        <a href={repositoryHref} target="_blank" rel="noreferrer">
          GitHub
        </a>
      </nav>
    </header>
  );
}