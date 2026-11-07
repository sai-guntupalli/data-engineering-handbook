import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono, Newsreader } from "next/font/google";
import "./globals.css";
import { SearchProvider } from "@/components/search-context";
import { authorHref, authorName, licenseName, repositoryHref, siteUrl } from "@/lib/site";

const geist = Geist({
  variable: "--font-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

const newsreader = Newsreader({
  variable: "--font-serif",
  subsets: ["latin"],
  style: ["normal", "italic"],
});

const siteName = "Data Engineering Handbook";
const siteDescription =
  "An open handbook of runnable Jupyter notebooks for data engineering: Python, SQL, PySpark, lakehouse formats, streaming, cloud platforms, warehousing, AI foundations and more.";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: siteName,
    template: `%s | ${siteName}`,
  },
  description: siteDescription,
  authors: [{ name: authorName, url: authorHref }],
  creator: authorName,
  openGraph: {
    type: "website",
    siteName,
    title: siteName,
    description: siteDescription,
  },
  twitter: {
    card: "summary",
    title: siteName,
    description: siteDescription,
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geist.variable} ${geistMono.variable} ${newsreader.variable}`}>
      <body>
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <SearchProvider>
          {children}
          <footer className="site-footer">
            <div className="site-footer-inner">
              <p>
                Built by{" "}
                <a href={authorHref} target="_blank" rel="noreferrer">
                  {authorName}
                </a>
                . Licensed under{" "}
                <Link href="/license">{licenseName}</Link>.
              </p>
              <nav aria-label="Footer navigation">
                <Link href="/license">License</Link>
                <a href={repositoryHref} target="_blank" rel="noreferrer">
                  Repository
                </a>
              </nav>
            </div>
          </footer>
        </SearchProvider>
      </body>
    </html>
  );
}
