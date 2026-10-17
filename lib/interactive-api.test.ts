import { afterEach, describe, expect, it, vi } from "vitest";

import { BACKEND_URL, executeCell, resetKernel } from "./interactive-api";

afterEach(() => {
  vi.unstubAllGlobals();
});

/** A refusal like the backend's HTTP 400s/404s: JSON {detail} and nothing else. */
const refusal = (status: number, detail: string) => ({
  ok: false,
  status,
  json: async () => ({ detail }),
});

const execResult = (status: string, stdout: string) => ({
  ok: true,
  status: 200,
  json: async () => ({
    status,
    stdout,
    stderr: "",
    traceback: null,
    elapsed_seconds: 0.05,
  }),
});

describe("executeCell", () => {
  it("runs one /execute POST and returns the backend's result", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => execResult("ok", "42\n"));
    vi.stubGlobal("fetch", fetch);

    const result = await executeCell("spark", "notebooks/topics/spark.ipynb", 214, null);

    expect(fetch).toHaveBeenCalledOnce();
    expect(fetch.mock.calls[0]![0]).toBe(`${BACKEND_URL}/execute`);
    expect(JSON.parse(String((fetch.mock.calls[0]![1] as RequestInit).body))).toEqual({
      notebook: "spark",
      path: "notebooks/topics/spark.ipynb",
      cell_index: 214,
      code: null,
    });
    expect(result.status).toBe("ok");
    expect(result.stdout).toBe("42\n");
  });

  it("maps an HTTP refusal to error with the refusal detail, keeping crashed for transport only", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => refusal(400, "cell 3 is not a code cell"));
    vi.stubGlobal("fetch", fetch);

    const result = await executeCell("spark", "notebooks/topics/spark.ipynb", 3, null);

    expect(result.status).toBe("error");
    expect(result.traceback).toContain("HTTP 400");
    expect(result.traceback).toContain("cell 3 is not a code cell");
    expect(result.stdout).toBe("");
  });

  it("keeps crashed for a transport failure (backend unreachable)", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => {
      throw new TypeError("fetch failed");
    });
    vi.stubGlobal("fetch", fetch);

    const result = await executeCell("spark", "notebooks/topics/spark.ipynb", 0, null);

    expect(result.status).toBe("crashed");
    expect(result.traceback).toContain("make dev-local");
  });
});

describe("resetKernel", () => {
  it("POSTs the notebook slug to /reset and reports the backend's answer", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => execResult("ok", ""));
    vi.stubGlobal("fetch", fetch);

    const result = await resetKernel("spark");

    expect(fetch).toHaveBeenCalledOnce();
    expect(fetch.mock.calls[0]![0]).toBe(`${BACKEND_URL}/reset`);
    expect(JSON.parse(String((fetch.mock.calls[0]![1] as RequestInit).body))).toEqual({
      notebook: "spark",
    });
    expect(result?.status).toBe("ok");
  });

  it("survives an unreachable backend by resolving to null", async () => {
    const fetch = vi.fn(async (_url: string, _init: RequestInit) => {
      throw new TypeError("fetch failed");
    });
    vi.stubGlobal("fetch", fetch);

    await expect(resetKernel("spark")).resolves.toBeNull();
    expect(fetch).toHaveBeenCalledOnce();
  });
});
