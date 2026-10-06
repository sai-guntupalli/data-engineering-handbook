import fs from "node:fs";
import path from "node:path";
import { NextResponse } from "next/server";

const contentTypes: Record<string, string> = {
  ".ico": "image/x-icon",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
  ".webp": "image/webp",
};

export async function GET(_request: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path: parts } = await params;
  const safeParts = parts.filter((part) => part !== ".." && !part.includes("/"));
  const allowedRoot = path.join(process.cwd(), "img");
  const scopedParts = safeParts[0] === "img" ? safeParts.slice(1) : safeParts;
  const file = path.join(allowedRoot, ...scopedParts);

  if (!file.startsWith(allowedRoot) || !fs.existsSync(file)) {
    return new NextResponse("Asset not found", { status: 404 });
  }

  const ext = path.extname(file).toLowerCase();
  return new NextResponse(fs.readFileSync(file), {
    headers: {
      "content-type": contentTypes[ext] ?? "application/octet-stream",
      "cache-control": "public, max-age=31536000, immutable",
    },
  });
}
