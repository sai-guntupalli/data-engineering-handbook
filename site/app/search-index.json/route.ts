import { getSearchEntries } from "@/lib/notebooks";

// Written once at build time; the command palette fetches it on first open.
export const dynamic = "force-static";

export function GET() {
  return Response.json(getSearchEntries());
}
