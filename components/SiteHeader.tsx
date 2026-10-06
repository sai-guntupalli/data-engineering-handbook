import Link from "next/link";

export function SiteHeader() {
  return (
    <header className="site-header">
      <Link className="brand" href="/">
        <span>DE</span>
        Interview Guide
      </Link>
      <nav aria-label="Primary navigation">
        <Link href="/topics">Topics</Link>
        <Link href="/topics/spark">PySpark</Link>
        <Link href="/questions">Questions</Link>
        <Link href="/topics/iceberg">Iceberg</Link>
        <Link href="/notebooks">Notebooks</Link>
      </nav>
    </header>
  );
}
