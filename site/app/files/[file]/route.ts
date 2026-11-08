import fs from "node:fs";
import path from "node:path";
import { getNotebook, getNotebookSlugs } from "@/lib/notebooks";

// Each notebook is copied into the static site at /files/<slug>.ipynb, so the
// reader's download link is same-origin and the browser saves the file.
export const dynamic = "force-static";
export const dynamicParams = false;

const repoRoot = path.resolve(process.cwd(), "..");

export function generateStaticParams() {
  return getNotebookSlugs().map((slug) => ({ file: `${slug}.ipynb` }));
}

export async function GET(_request: Request, { params }: { params: Promise<{ file: string }> }) {
  const notebook = getNotebook((await params).file.replace(/\.ipynb$/, ""));
  if (!notebook) return new Response("Not found", { status: 404 });
  const body = fs.readFileSync(path.join(repoRoot, notebook.repoPath));
  return new Response(body, { headers: { "Content-Type": "application/x-ipynb+json" } });
}
