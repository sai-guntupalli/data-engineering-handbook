import type { MetadataRoute } from "next";
import { siteUrl } from "@/lib/site";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { changeFrequency: "weekly", priority: 1, url: siteUrl },
    { changeFrequency: "yearly", priority: 0.3, url: `${siteUrl}/license/` },
  ];
}