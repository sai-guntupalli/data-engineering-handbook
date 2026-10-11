import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SearchProvider } from "@/components/search-context";
import { repositoryHref, siteUrl } from "@/lib/site";

const geist = Geist({
  variable: "--font-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
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
  authors: [{ name: "Sai Guntupalli", url: "https://github.com/sai-guntupalli" }],
  creator: "Sai Guntupalli",
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
    <html lang="en" className={`${geist.variable} ${geistMono.variable}`}>
      <body>
        <a href="#main-content" className="skip-link">
          Skip to content
        </a>
        <SearchProvider>
          {children}
          <footer className="site-footer">
            <span>Built by</span>
            <a href="https://github.com/sai-guntupalli" target="_blank" rel="noreferrer">
              Sai Guntupalli
            </a>
            <nav aria-label="Footer navigation">
              <Link href="/license">License</Link>
              <a href={repositoryHref} target="_blank" rel="noreferrer">
                Repository
              </a>
            </nav>
          </footer>
        </SearchProvider>
      </body>
    </html>
  );
}
