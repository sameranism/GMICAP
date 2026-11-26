import { useEffect, useState } from "react";
import NewsDesk, { type NewsRecord } from "../features/newsroom/NewsDesk";

type LoadState = "ready" | "loading" | "error" | "forbidden";

export default function App() {
  const [items, setItems] = useState<NewsRecord[]>([]);
  const [state, setState] = useState<LoadState>("loading");

  useEffect(() => {
    const controller = new AbortController();
    fetch("/v1/demo/news", { signal: controller.signal, credentials: "same-origin" })
      .then(async (response) => {
        if (response.status === 403) { setState("forbidden"); return; }
        if (!response.ok) throw new Error("Demo news unavailable");
        const data: { mode: string; items: NewsRecord[] } = await response.json();
        if (data.mode !== "synthetic" || !Array.isArray(data.items)) throw new Error("Invalid demo response");
        setItems(data.items);
        setState("ready");
      })
      .catch((error: unknown) => {
        if (!(error instanceof DOMException && error.name === "AbortError")) setState("error");
      });
    return () => controller.abort();
  }, []);

  return (
    <div className="app-frame">
      <header className="masthead">
        <div>
          <p className="eyebrow">نمونه رابط تحریریه</p>
          <h1>اعتماد <span>· میز خبر</span></h1>
        </div>
        <span className="demo-label">داده‌های ساختگی · بدون انتشار</span>
      </header>
      <main>
        <NewsDesk items={items} state={state} />
      </main>
    </div>
  );
}
