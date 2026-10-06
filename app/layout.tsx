import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SiteHeader } from "@/components/SiteHeader";

const geist = Geist({
  variable: "--font-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Data Engineering Interview Notebooks",
    template: "%s | Data Engineering Interview Notebooks",
  },
  description:
    "Collection of runnable Jupyter notebooks for data engineering interviews: Python, SQL, PySpark, lakehouse formats, streaming, cloud platforms, warehousing, AI foundations and more.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${geist.variable} ${geistMono.variable}`}>
      <body>
        <SiteHeader />
        {children}
      </body>
    </html>
  );
}
