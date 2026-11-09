import Link from "next/link";
import { Fragment, type ReactNode } from "react";
import { CaretRight, GithubLogo, SquaresFour, Star } from "@phosphor-icons/react/dist/ssr";
import { getToolCategories } from "@/lib/notebooks";
import { authorHref, authorName, licenseName, repositoryHref } from "@/lib/site";
import { SearchTrigger, SidebarSearchButton } from "./palette";
import { SidebarTools } from "./SidebarTools";
import { SidebarToggle } from "./panels";
import { ThemeToggle } from "./theme";

export type Crumb = { label: string; href?: string };

/** The handbook's mark: two inputs flowing into one node, like a tiny DAG. */
export function BrandMark() {
  return (
    <span className="brand-mark" aria-hidden>
      <svg viewBox="0 0 20 20">
        <path className="edge-line" d="M5 5.5C10 5.5 10 10 15 10M5 14.5C10 14.5 10 10 15 10" />
        <circle className="node-a" cx="5" cy="5.5" r="2.4" />
        <circle className="node-a" cx="5" cy="14.5" r="2.4" />
        <circle className="node-b" cx="15" cy="10" r="2.8" />
      </svg>
    </span>
  );
}

/**
 * Sidebar, top bar and footer around every page. On narrow screens the sidebar
 * becomes a scrolling strip above the top bar.
 */
export function AppShell({
  crumbs,
  current,
  tool,
  children,
}: {
  crumbs: Crumb[];
  /** Which primary nav item is the current page. */
  current?: "library" | "starred";
  /** Folder of the tool this page belongs to; its sidebar group opens and its link is marked current. */
  tool?: string;
  children: ReactNode;
}) {
  const categories = getToolCategories();
  const total = categories.reduce((sum, category) => sum + category.tools.reduce((n, tool) => n + tool.notebooks.length, 0), 0);

  return (
    <div className="app">
      <aside className="sidebar" id="app-sidebar" aria-label="Handbook navigation">
        <Link className="brand" href="/" aria-label="Data Engineering Handbook, home">
          <BrandMark />
          <span>
            Handbook<small>Data engineering</small>
          </span>
        </Link>

        <Link
          className="nav-link"
          data-tip="Library"
          href="/"
          aria-current={current === "library" ? "page" : undefined}
        >
          <SquaresFour size={16} aria-hidden />
          <span className="nav-text">Library</span>
          <span className="nav-count">{total}</span>
        </Link>
        <Link
          className="nav-link"
          data-tip="Starred"
          href="/starred/"
          aria-current={current === "starred" ? "page" : undefined}
        >
          <Star size={16} aria-hidden />
          <span className="nav-text">Starred</span>
        </Link>
        <SidebarSearchButton />

        <div className="nav-label">Tools</div>
        <SidebarTools
          currentTool={tool}
          categories={categories.map((category) => ({
            id: category.id,
            label: category.label,
            tools: category.tools.map((entry) => ({
              folder: entry.folder,
              label: entry.label,
              href: entry.href,
              tone: entry.tone,
              count: entry.notebooks.length,
            })),
          }))}
        />

        <p className="sidebar-foot">
          An open handbook by{" "}
          <a href={authorHref} target="_blank" rel="noreferrer">
            {authorName}
          </a>
          , free to reuse under <Link href="/license/">{licenseName}</Link>.
        </p>
      </aside>

      <div className="main">
        <header className="topbar">
          <SidebarToggle />
          <nav className="crumbs" aria-label="Breadcrumb">
            {crumbs.map((crumb, index) => {
              const last = index === crumbs.length - 1;
              return (
                <Fragment key={crumb.label}>
                  {index > 0 ? <CaretRight size={13} aria-hidden /> : null}
                  {last || !crumb.href ? (
                    <span aria-current={last ? "page" : undefined}>{crumb.label}</span>
                  ) : (
                    <Link href={crumb.href}>{crumb.label}</Link>
                  )}
                </Fragment>
              );
            })}
          </nav>
          <SearchTrigger />
          <ThemeToggle />
          <a
            className="btn btn-ghost btn-icon"
            href={repositoryHref}
            target="_blank"
            rel="noreferrer"
            aria-label="GitHub repository"
          >
            <GithubLogo size={18} aria-hidden />
          </a>
        </header>

        <main id="main-content" className="content">
          {children}
        </main>

        <footer className="site-footer">
          <p>
            Built by{" "}
            <a href={authorHref} target="_blank" rel="noreferrer">
              {authorName}
            </a>
            . Licensed under <Link href="/license/">{licenseName}</Link>.
          </p>
          <nav aria-label="Footer">
            <Link href="/license/">License</Link>
            <a href={repositoryHref} target="_blank" rel="noreferrer">
              Repository
            </a>
          </nav>
        </footer>
      </div>
    </div>
  );
}
