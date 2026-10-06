import fs from "node:fs";
import path from "node:path";
import { NextResponse } from "next/server";

export async function GET(_request: Request, { params }: { params: Promise<{ path: string[] }> }) {
  const { path: parts } = await params;
  const safeParts = parts.filter((part) => part !== ".." && !part.includes("/"));
  const file = path.join(process.cwd(), "notebooks", ...safeParts);

  if (!file.startsWith(path.join(process.cwd(), "notebooks")) || !file.endsWith(".ipynb") || !fs.existsSync(file)) {
    return new NextResponse("Notebook not found", { status: 404 });
  }

  const body = fs.readFileSync(file);
  return new NextResponse(body, {
    headers: {
      "content-type": "application/x-ipynb+json",
      "content-disposition": `attachment; filename="${path.basename(file)}"`,
    },
  });
}
