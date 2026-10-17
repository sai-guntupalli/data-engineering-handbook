// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";

import { BACKEND_URL } from "../lib/interactive-api";
import { ChatPanel } from "./chat-panel";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  FakeIntersectionObserver.instances = [];
});

const jsonResponse = (payload: unknown) => ({
  ok: true,
  status: 200,
  json: async () => payload,
});

/** A fake SSE response whose body hands out the chunks one read() at a time. */
function sseResponse(chunks: string[]) {
  const encode = (text: string) => Uint8Array.from(text, (char) => char.charCodeAt(0));
  let index = 0;
  return {
    ok: true,
    status: 200,
    body: {
      getReader: () => ({
        read: async () =>
          index < chunks.length
            ? { done: false, value: encode(chunks[index++]) }
            : { done: true, value: undefined },
      }),
    },
  };
}

/** A backend mock: /chat/settings answers the given summary, each /chat call
 *  consumes the next chunk list. */
const mockBackend = (chatChunks: string[][], settings: object = { provider: "openrouter", model: "anthropic/claude-sonnet-4.5", key_present: true }) =>
  vi.fn(async (url: string, _init: RequestInit) => {
    if (String(url).endsWith("/chat/settings")) return jsonResponse(settings);
    return sseResponse(chatChunks.shift() ?? []);
  });

/** The parsed JSON body of one recorded call. */
function sentBody(mock: { mock: { calls: unknown[][] } }, call: number): Record<string, unknown> {
  const init = mock.mock.calls[call]![1] as RequestInit;
  return JSON.parse(String(init.body)) as Record<string, unknown>;
}

const INPUT_LABEL = /message the notebook tutor/i;

function typeAndSend(message: string) {
  const input = screen.getByLabelText(INPUT_LABEL) as HTMLTextAreaElement;
  fireEvent.change(input, { target: { value: message } });
  fireEvent.click(screen.getByRole("button", { name: /send/i }));
}

/** jsdom has no IntersectionObserver, so ChatPanel cannot see the sections
 *  unless a stub is installed; `emit` fakes one intersection batch. */
class FakeIntersectionObserver {
  static instances: FakeIntersectionObserver[] = [];
  readonly observed: Element[] = [];
  private readonly callback: IntersectionObserverCallback;

  constructor(callback: IntersectionObserverCallback) {
    this.callback = callback;
    FakeIntersectionObserver.instances.push(this);
  }

  observe(target: Element): void {
    this.observed.push(target);
  }

  disconnect(): void {}

  unobserve(): void {}

  emit(target: Element, geometry: { isIntersecting: boolean; top: number }): void {
    this.callback(
      [
        {
          target,
          isIntersecting: geometry.isIntersecting,
          boundingClientRect: { top: geometry.top },
        } as unknown as IntersectionObserverEntry,
      ],
      this as unknown as IntersectionObserver,
    );
  }
}

describe("ChatPanel", () => {
  it("renders the message input, the Send button and the settings toggle", async () => {
    const fetch = mockBackend([]);
    vi.stubGlobal("fetch", fetch);
    render(<ChatPanel notebookTitle="Viewer Fixture" outline={["Load"]} sectionIds={["load"]} />);

    expect(screen.getByLabelText(INPUT_LABEL)).not.toBeNull();
    expect(screen.getByRole("button", { name: /send/i })).not.toBeNull();
    const settingsToggle = screen.getByRole("button", { name: /chat model settings/i });
    fireEvent.click(settingsToggle);
    expect(await screen.findByText("openrouter")).not.toBeNull();
    expect(await screen.findByText("anthropic/claude-sonnet-4.5")).not.toBeNull();
  });

  it("streams the reply into an assistant bubble and sends the accumulated history", async () => {
    const fetch = mockBackend([
      ["data: {\"delta\": \"Hello\"}\n\n", "data: {\"delta\": \" world\"}\n\n", "data: {\"done\": true}\n\n"],
      ["data: {\"delta\": \"Again\"}\n\n", "data: {\"done\": true}\n\n"],
    ]);
    vi.stubGlobal("fetch", fetch);
    vi.stubGlobal("IntersectionObserver", FakeIntersectionObserver);
    render(<ChatPanel notebookTitle="Viewer Fixture" outline={["Load", "Notes"]} sectionIds={["load", "notes"]} />);

    typeAndSend("What is a kernel?");

    expect(await screen.findByText("Hello world")).not.toBeNull();
    const firstChatIndex = fetch.mock.calls.findIndex(([url]) => String(url).endsWith("/chat"));
    expect(fetch.mock.calls[firstChatIndex]![0]).toBe(`${BACKEND_URL}/chat`);
    expect(sentBody(fetch, firstChatIndex)).toEqual({
      mode: "chat",
      notebook_title: "Viewer Fixture",
      outline: ["Load", "Notes"],
      visible_section: "load",
      history: [],
      message: "What is a kernel?",
    });

    typeAndSend("Explain that");
    expect(await screen.findByText("Again")).not.toBeNull();
    const secondChatIndex = fetch.mock.calls.findIndex(
      ([url], index) => index > firstChatIndex && String(url).endsWith("/chat"),
    );
    expect(sentBody(fetch, secondChatIndex)).toEqual({
      mode: "chat",
      notebook_title: "Viewer Fixture",
      outline: ["Load", "Notes"],
      visible_section: "load",
      history: [
        { role: "user", content: "What is a kernel?" },
        { role: "assistant", content: "Hello world" },
      ],
      message: "Explain that",
    });
  });

  it("sends the live visible section as visible_section", async () => {
    const fetch = mockBackend([["data: {\"delta\": \"Hi\"}\n\n", "data: {\"done\": true}\n\n"]]);
    vi.stubGlobal("fetch", fetch);
    vi.stubGlobal("IntersectionObserver", FakeIntersectionObserver);
    render(
      <div>
        <section data-nb-section-id="load" />
        <section data-nb-section-id="notes" />
        <ChatPanel notebookTitle="Viewer Fixture" outline={["Load", "Notes"]} sectionIds={["load", "notes"]} />
      </div>,
    );

    const observer = FakeIntersectionObserver.instances.at(-1)!;
    expect(observer.observed.map((target) => target.getAttribute("data-nb-section-id"))).toEqual([
      "load",
      "notes",
    ]);

    // The "notes" section scrolls in (its top is above "load"'s) mid-conversation.
    const notes = observer.observed[1]!;
    observer.emit(notes, { isIntersecting: true, top: 10 });
    observer.emit(observer.observed[0]!, { isIntersecting: false, top: 400 });

    typeAndSend("Where am I?");

    expect(await screen.findByText("Hi")).not.toBeNull();
    const chatIndex = fetch.mock.calls.findIndex(([url]) => String(url).endsWith("/chat"));
    expect(sentBody(fetch, chatIndex)).toMatchObject({ visible_section: "notes" });
  });

  it("surfaces a stream error as an error bubble and keeps the input enabled", async () => {
    const fetch = mockBackend([["data: {\"error\": \"openrouter request failed with HTTP 500\"}\n\n"]]);
    vi.stubGlobal("fetch", fetch);
    render(<ChatPanel notebookTitle="Viewer Fixture" outline={[]} sectionIds={[]} />);

    typeAndSend("What is a kernel?");

    const errorText = await screen.findByText(/openrouter request failed with HTTP 500/);
    expect(errorText.closest(".chat-bubble-error")).not.toBeNull();
    const input = screen.getByLabelText(INPUT_LABEL) as HTMLTextAreaElement;
    expect(input.disabled).toBe(false);

    // The failed turn must not poison the next request's history.
    typeAndSend("Try again");
    const chatCalls = fetch.mock.calls.filter(([url]) => String(url).endsWith("/chat"));
    expect(chatCalls).toHaveLength(2);
    const body = JSON.parse(String((chatCalls[1]![1] as RequestInit).body)) as {
      history: { role: string; content: string }[];
      message: string;
    };
    expect(body.message).toBe("Try again");
    expect(body.history).toEqual([{ role: "user", content: "What is a kernel?" }]);
  });

  it("shows a plain note bubble when the stream finishes without a single delta", async () => {
    const fetch = mockBackend([["data: {\"done\": true}\n\n"]]);
    vi.stubGlobal("fetch", fetch);
    render(<ChatPanel notebookTitle="Viewer Fixture" outline={[]} sectionIds={[]} />);

    typeAndSend("Say something");

    // A silent turn still has to leave something visible in the log.
    const note = await screen.findByText(/returned an empty reply/i);
    expect((note as HTMLElement).className).not.toContain("chat-bubble-error");
  });

  it("warns in the settings popover when the provider key is missing", async () => {
    const fetch = mockBackend([], { provider: "openrouter", model: "anthropic/claude-sonnet-4.5", key_present: false });
    vi.stubGlobal("fetch", fetch);
    render(<ChatPanel notebookTitle="Viewer Fixture" outline={[]} sectionIds={[]} />);

    fireEvent.click(screen.getByRole("button", { name: /chat model settings/i }));

    expect(await screen.findByText(/OPENROUTER_API_KEY/)).not.toBeNull();
    // The input stays usable without a key; the backend explains itself per request.
    expect((screen.getByLabelText(INPUT_LABEL) as HTMLTextAreaElement).disabled).toBe(false);
  });
});
