import { useEffect, useState, type FormEvent } from "react";
import NewsDesk, { type NewsFeedRecord } from "../features/newsroom/NewsDesk";

type LoadState = "ready" | "loading" | "error" | "forbidden";

function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isNewsItem(value: unknown): value is NewsFeedRecord {
  if (!isObject(value)) return false;
  return typeof value.news_id === "string" && value.news_id.length > 0 &&
    typeof value.title === "string" &&
    typeof value.source_id === "string" &&
    typeof value.original_url === "string" &&
    typeof value.collected_at === "string" &&
    Number.isFinite(Date.parse(value.collected_at)) &&
    (value.stream === "domestic" || value.stream === "foreign" || value.stream === "manual") &&
    (value.reuse_permission === "unverified" || value.reuse_permission === "licensed" ||
      value.reuse_permission === "link_only" || value.reuse_permission === "blocked") &&
    (value.content_scope === "metadata" || value.content_scope === "summary" ||
      value.content_scope === "full_text") &&
    typeof value.event_id === "string" &&
    Array.isArray(value.desks) && value.desks.every((desk: unknown) => typeof desk === "string");
}

export function parseNewsFeed(value: unknown): NewsFeedRecord[] {
  if (!isObject(value) || value.schema_version !== "1.0" ||
      !Array.isArray(value.items) || value.count !== value.items.length ||
      !value.items.every(isNewsItem)) {
    throw new Error("Invalid newsroom response");
  }
  const items: NewsFeedRecord[] = value.items;
  if (new Set(items.map((item) => item.news_id)).size !== items.length) {
    throw new Error("Duplicate newsroom identity");
  }
  return items;
}

export default function App() {
  const [items, setItems] = useState<NewsFeedRecord[]>([]);
  const [state, setState] = useState<LoadState>("forbidden");
  const [token, setToken] = useState("");
  const [draft, setDraft] = useState("");
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    if (!token) return;
    const controller = new AbortController();
    fetch("/v1/news", {
      signal: controller.signal,
      credentials: "same-origin",
      headers: { Authorization: "Bearer " + token, Accept: "application/json" },
      cache: "no-store",
      redirect: "error",
    })
      .then(async (response) => {
        if (controller.signal.aborted) return;
        if (response.status === 401 || response.status === 403) {
          setItems([]);
          setState("forbidden");
          return;
        }
        if (!response.ok) throw new Error("Newsroom unavailable");
        const data: unknown = await response.json();
        const next = parseNewsFeed(data);
        if (controller.signal.aborted) return;
        setItems(next);
        setState("ready");
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setItems([]);
          setState("error");
        }
      });
    return () => controller.abort();
  }, [token, attempt]);

  function connect(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const next = draft.trim();
    if (!next) return;
    setItems([]);
    setState("loading");
    setToken(next);
    setDraft("");
    setAttempt((value) => value + 1);
  }

  function disconnect() {
    setToken("");
    setDraft("");
    setItems([]);
    setState("forbidden");
  }

  return (
    <div className="app-frame" dir="rtl">
      <header className="masthead">
        <div>
          <p className="eyebrow">رابط تحریریه</p>
          <h1>اعتماد <span>· میز خبر</span></h1>
        </div>
        {token && <button type="button" onClick={disconnect}>قطع نشست</button>}
      </header>
      <main>
        {!token ? (
          <form onSubmit={connect}>
            <h2>اتصال به نشست مجاز تحریریه</h2>
            <label htmlFor="session-token">توکن نشست صادرشده توسط سامانه</label>
            <input id="session-token" type="password" dir="ltr" autoComplete="off"
              value={draft} onChange={(event) => setDraft(event.target.value)} required />
            <button type="submit" disabled={!draft.trim()}>اتصال</button>
            <p>توکن فقط در حافظه این صفحه نگهداری می‌شود.</p>
          </form>
        ) : (
          <>
            <NewsDesk items={items} state={state} />
            {state === "error" && (
              <button type="button" onClick={() => {
                setItems([]);
                setState("loading");
                setAttempt((value) => value + 1);
              }}>تلاش مجدد</button>
            )}
          </>
        )}
      </main>
    </div>
  );
}
