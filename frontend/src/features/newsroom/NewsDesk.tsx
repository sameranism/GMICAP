import { useState } from "react";

export type NewsRecord = {
  schema_version: "1.0";
  news_id: string;
  stream: "domestic" | "foreign" | "manual";
  source_id: string;
  original_url: string;
  original_title: string;
  original_text: string | null;
  language: string;
  source_country?: string | null;
  subject_countries: string[];
  published_at?: string | null;
  collected_at: string;
  content_scope: "metadata" | "summary" | "full_text";
  reuse_permission: "unverified" | "licensed" | "link_only" | "blocked";
  source_payload_ref?: string | null;
  normalized_text?: string | null;
  fingerprint: string;
  normalization_version: string;
};

// Existing /v1/news projection: no invented normalized-contract fields.
export type NewsFeedRecord = Pick<NewsRecord,
  "news_id" | "stream" | "source_id" | "original_url" | "collected_at" |
  "reuse_permission" | "content_scope"
> & { title: string; event_id: string; desks: string[] };

type DeskRecord = NewsRecord | NewsFeedRecord;
type Props = { items: readonly DeskRecord[]; state?: "ready" | "loading" | "error" | "forbidden" };
type Stream = "all" | NewsRecord["stream"];

const streamNames: Record<Stream, string> = {
  all: "همه", domestic: "داخلی", foreign: "خارجی", manual: "دستی",
};

function safeHttpUrl(value: string): string | null {
  try {
    const url = new URL(value);
    return url.protocol === "https:" || url.protocol === "http:" ? url.href : null;
  } catch {
    return null;
  }
}

export default function NewsDesk({ items, state = "ready" }: Props) {
  const [stream, setStream] = useState<Stream>("all");
  const visible = items.filter((item) => item.stream === stream || stream === "all");

  return (
    <section aria-labelledby="news-heading" className="news-desk">
      <div className="section-heading">
        <div>
          <p className="eyebrow">رصد و بررسی</p>
          <h2 id="news-heading">ورودی خبر</h2>
        </div>
        <span className="count" aria-live="polite">{visible.length.toLocaleString("fa-IR")} مورد</span>
      </div>
      <div className="filters" role="group" aria-label="فیلتر جریان خبر">
        {(["all", "domestic", "foreign", "manual"] as Stream[]).map((value) => (
          <button key={value} type="button" aria-pressed={stream === value}
            onClick={() => setStream(value)}>{streamNames[value]}</button>
        ))}
      </div>
      {state === "loading" && <p role="status" className="message">در حال دریافت خبرها…</p>}
      {state === "error" && <p role="alert" className="message">دریافت خبرها ناموفق بود.</p>}
      {state === "forbidden" && <p role="alert" className="message">دسترسی به این میز مجاز نیست.</p>}
      {state === "ready" && visible.length === 0 && <p className="message">در این جریان خبری نیست.</p>}
      {state === "ready" && visible.length > 0 && (
        <ul className="news-list">
          {visible.map((item) => {
            const sourceUrl = safeHttpUrl(item.original_url);
            return (
            <li key={item.news_id} className="news-item">
              <div className="news-meta">
                <span>{streamNames[item.stream]}</span>
                <span dir="ltr">{item.news_id}</span>
                <span dir="ltr">{item.source_id}</span>
                <time dateTime={item.collected_at}>
                  {new Intl.DateTimeFormat("fa-IR", { dateStyle: "medium", timeStyle: "short", timeZone: "Asia/Tehran" }).format(new Date(item.collected_at))}
                </time>
              </div>
              <h3 dir="auto">{"original_title" in item ? item.original_title : item.title}</h3>
              {"event_id" in item && (
                <p dir="auto">رویداد: {item.event_id} · سرویس: {item.desks.join("، ")}</p>
              )}
              <p>{item.reuse_permission === "unverified" ? "حق بازنشر تأیید نشده" : "وضعیت حق استفاده: " + item.reuse_permission}</p>
              {sourceUrl ? (
                <a href={sourceUrl} target="_blank" rel="noopener noreferrer">
                  منبع خبر <span className="sr-only">(در پنجره جدید)</span>
                </a>
              ) : <span>نشانی منبع نامعتبر است</span>}
            </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
