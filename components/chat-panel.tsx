"use client";

import { CircleNotch, PaperPlaneTilt, Sliders } from "@phosphor-icons/react";
import { useEffect, useRef, useState } from "react";

import {
  fetchChatSettings,
  streamChat,
  type ChatMessage,
  type ChatSettings,
} from "@/lib/interactive-api";

/** Mirrors backend/chat_config.py's PROVIDER_ENV_KEYS; only used to name the
 *  missing variable in the popover (OpenRouter first, matching the backend's
 *  default provider). */
const PROVIDER_ENV_KEYS: Record<string, string> = {
  openrouter: "OPENROUTER_API_KEY",
  ollama: "OLLAMA_API_KEY",
};

/** One rendered chat turn; error turns are backend-refusal bubbles that must
 *  stay out of the history sent with the next message. */
type ChatBubble = { role: "user" | "assistant"; content: string; error?: boolean };

const chatHistory = (bubbles: ChatBubble[]): ChatMessage[] =>
  bubbles.filter((bubble) => bubble.error !== true && bubble.content !== "").map((bubble) => ({ role: bubble.role, content: bubble.content }));

/**
 * Per-notebook chat: streamed replies from the local backend (`mode: "chat"`
 * with the running history in state — nothing persists server-side), a
 * provider/model popover, and errors surfaced inline as error bubbles with the
 * input left enabled so a failed turn can simply be retried.
 */
export function ChatPanel({
  notebookTitle,
  outline,
  visibleSection,
}: {
  notebookTitle: string;
  outline: string[];
  visibleSection?: string;
}) {
  const [bubbles, setBubbles] = useState<ChatBubble[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [settings, setSettings] = useState<ChatSettings | null>(null);
  const [settingsFailed, setSettingsFailed] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const logRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let alive = true;
    fetchChatSettings().then(
      (summary) => {
        if (alive) setSettings(summary);
      },
      () => {
        if (alive) setSettingsFailed(true);
      },
    );
    return () => {
      alive = false;
    };
  }, []);

  // Keep the newest turn in view while a reply streams in.
  useEffect(() => {
    const log = logRef.current;
    if (log) log.scrollTop = log.scrollHeight;
  }, [bubbles]);

  const send = () => {
    const message = draft.trim();
    if (!message || busy) return;
    const history = chatHistory(bubbles);
    setBubbles((current) => [...current, { role: "user", content: message }, { role: "assistant", content: "" }]);
    setDraft("");
    setBusy(true);
    const appendDelta = (text: string) =>
      setBubbles((current) => {
        if (current.length === 0) return current;
        const last = current[current.length - 1]!;
        return [...current.slice(0, -1), { ...last, content: last.content + text }];
      });
    void streamChat(
      {
        mode: "chat",
        notebook_title: notebookTitle,
        outline,
        ...(visibleSection ? { visible_section: visibleSection } : {}),
        history,
        message,
      },
      appendDelta,
    ).then((error) => {
      if (error !== null) {
        // Surface the failure instead of finishing the turn; an already-started
        // streaming bubble keeps its partial text and gets a sibling error bubble.
        setBubbles((current) => {
          const last = current[current.length - 1];
          if (last?.role === "assistant" && last.content === "" && last.error !== true) {
            return [...current.slice(0, -1), { role: "assistant", content: error, error: true }];
          }
          return [...current, { role: "assistant", content: error, error: true }];
        });
      }
      setBusy(false);
    });
  };

  return (
    <aside className="chat-panel">
      <div className="chat-head">
        <span className="chat-title">Chat</span>
        <button
          type="button"
          className="chat-settings-toggle"
          onClick={() => setSettingsOpen((open) => !open)}
          aria-expanded={settingsOpen}
          aria-label="Chat model settings"
          title="Shows the backend's chat provider and model"
        >
          <Sliders size={14} weight="bold" />
        </button>
      </div>
      {settingsOpen ? (
        <div className="chat-settings" role="region" aria-label="Chat model settings">
          {settings !== null ? (
            <dl className="chat-settings-list">
              <div className="chat-settings-item">
                <dt className="chat-settings-label">Provider</dt>
                <dd className="chat-settings-value">{settings.provider}</dd>
              </div>
              <div className="chat-settings-item">
                <dt className="chat-settings-label">Model</dt>
                <dd className="chat-settings-value">{settings.model}</dd>
              </div>
            </dl>
          ) : settingsFailed ? (
            <p className="chat-settings-note">
              Could not reach the chat backend — run <code>make dev-local</code> to check the configuration.
            </p>
          ) : (
            <p className="chat-settings-note">Checking the chat configuration…</p>
          )}
          {settings !== null && !settings.key_present ? (
            <p className="chat-settings-warning">
              {PROVIDER_ENV_KEYS[settings.provider] ?? "OPENROUTER_API_KEY"} is not set; export it in the
              environment to use chat.
            </p>
          ) : null}
        </div>
      ) : null}
      <div className="chat-log" role="log" aria-label="Chat with the notebook tutor" aria-live="polite">
        {bubbles.length === 0 ? (
          <p className="chat-empty">Ask about this notebook — the tutor sees its outline as context.</p>
        ) : (
          bubbles.map((bubble, index) => {
            const waiting =
              bubble.role === "assistant" && bubble.content === "" && busy && index === bubbles.length - 1;
            const className = bubble.error
              ? "chat-bubble chat-bubble-error"
              : bubble.role === "user"
                ? "chat-bubble chat-bubble-user"
                : waiting
                  ? "chat-bubble chat-bubble-waiting"
                  : "chat-bubble";
            return (
              <p key={index} className={className}>
                {waiting ? "Thinking…" : bubble.content}
              </p>
            );
          })
        )}
      </div>
      <form
        className="chat-composer"
        onSubmit={(event) => {
          event.preventDefault();
          send();
        }}
      >
        <textarea
          className="chat-input"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              send();
            }
          }}
          rows={1}
          placeholder="Ask about this notebook…"
          aria-label="Message the notebook tutor"
        />
        <button type="submit" className="chat-send" disabled={busy} title="Sends the message to the tutor">
          {busy ? <CircleNotch size={14} className="cell-spin" /> : <PaperPlaneTilt size={14} weight="bold" />}
          Send
        </button>
      </form>
    </aside>
  );
}