import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/SiteHeader";
import { repositoryHref } from "@/lib/notebooks";
import { siteUrl } from "@/lib/site";

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
  "A private handbook of runnable Jupyter notebooks for data engineering: Python, SQL, PySpark, lakehouse formats, streaming, cloud platforms, warehousing, AI foundations and more.";

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
        <SiteHeader />
        {children}
        <footer className="site-footer">
          <span>Built by</span>
          <a href="https://github.com/sai-guntupalli" target="_blank" rel="noreferrer">
            Sai Guntupalli
          </a>
          <nav aria-label="Footer navigation">
            <a href={repositoryHref} target="_blank" rel="noreferrer">
              Repository
            </a>
          </nav>
        </footer>
      </body>
    </html>
  );
}
