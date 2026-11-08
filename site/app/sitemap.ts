import type { MetadataRoute } from "next";
import { getNotebookList } from "@/lib/notebooks";
import { siteUrl } from "@/lib/site";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { changeFrequency: "weekly", priority: 1, url: `${siteUrl}/` },
    ...getNotebookList().map((notebook) => ({
      changeFrequency: "weekly" as const,
      priority: 0.8,
      url: `${siteUrl}${notebook.href}`,
    })),
    { changeFrequency: "monthly", priority: 0.4, url: `${siteUrl}/search/` },
    { changeFrequency: "yearly", priority: 0.3, url: `${siteUrl}/license/` },
  ];
}
