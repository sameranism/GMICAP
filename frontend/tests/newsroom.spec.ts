import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import App, { parseNewsFeed } from "../src/app/App";
import NewsDesk from "../src/features/newsroom/NewsDesk";

const item = {
  news_id: "NEWS-DB-1", title: "خبر واقعی از API آزمایشی",
  stream: "domestic", source_id: "SRC-1",
  original_url: "https://example.invalid/news/1",
  collected_at: "2026-11-23T07:00:00Z",
  reuse_permission: "unverified", content_scope: "summary",
  event_id: "EVENT-1", desks: ["economy"],
} as const;

const envelope = (items: unknown[]) => ({ schema_version: "1.0", count: items.length, items });

describe("authenticated newsroom projection", () => {
  it("accepts the existing real API envelope and renders source and title", () => {
    const items = parseNewsFeed(envelope([{ ...item, desks: [...item.desks] }]));
    const html = renderToStaticMarkup(createElement(NewsDesk, { items }));
    expect(html).toContain(item.title);
    expect(html).toContain(item.original_url);
    expect(html).toContain("EVENT-1");
    expect(html).not.toContain("منبع نمونه");
  });

  it("rejects malformed, synthetic-only and duplicate responses", () => {
    expect(() => parseNewsFeed({ mode: "synthetic", items: [item] })).toThrow();
    expect(() => parseNewsFeed(envelope([{ ...item, collected_at: "invalid" }]))).toThrow();
    expect(() => parseNewsFeed(envelope([item, item]))).toThrow();
    expect(() => parseNewsFeed({ ...envelope([item]), count: 0 })).toThrow();
  });

  it("renders empty and error states without showing stale news", () => {
    expect(renderToStaticMarkup(createElement(NewsDesk, { items: [] }))).toContain("خبری نیست");
    const items = parseNewsFeed(envelope([item]));
    for (const state of ["loading", "error", "forbidden"] as const) {
      const html = renderToStaticMarkup(createElement(NewsDesk, { items, state }));
      expect(html).not.toContain(item.title);
    }
  });

  it("requires a session before showing the feed", () => {
    const html = renderToStaticMarkup(createElement(App));
    expect(html).toContain("session-token");
    expect(html).not.toContain(item.title);
    expect(html).not.toContain("داده‌های ساختگی");
  });

  it("does not render non-HTTP source links", () => {
    const items = parseNewsFeed(envelope([{ ...item, original_url: "javascript:alert(1)" }]));
    const html = renderToStaticMarkup(createElement(NewsDesk, { items }));
    expect(html).not.toContain("javascript:");
    expect(html).toContain("نشانی منبع نامعتبر");
  });
});
