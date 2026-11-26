"""S02-001..007: domestic feed parsing, collection, polling state, storage."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from backend.modules.domestic.collector import (
    FeedParseError,
    collect,
    parse_feed,
    to_raw_news,
)
from backend.modules.domestic.feed_client import (
    FeedError,
    FeedResponse,
    FixtureFeedTransport,
    fetch_with_retry,
    validate_feed_url,
)
from backend.modules.domestic.repository import RawNewsRepository
from backend.modules.domestic.scheduler import (
    BASE_INTERVAL_SECONDS,
    MAX_INTERVAL_SECONDS,
    PollStateStore,
    next_interval_seconds,
    record_failure,
    record_success,
    should_poll,
)

RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>fixture</title>
<item><title>جلسه شورای شهر تهران</title>
<link>https://example.com/news/1</link>
<description><![CDATA[<p>شهرداری درباره بودجه جلسه داشت.</p>]]></description>
<pubDate>Mon, 23 Nov 2026 06:00:00 GMT</pubDate></item>
<item><title>رشد شاخص بورس</title>
<link>https://example.com/news/2</link>
<description>بورس تهران امروز رشد کرد.</description>
<pubDate>Mon, 23 Nov 2026 07:30:00 GMT</pubDate></item>
</channel></rss>""".encode("utf-8")

ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>atom fixture</title>
<entry><title>خبر خارجی</title><link href="https://example.com/atom/1"/>
<summary>summary text</summary><updated>2026-11-23T08:00:00Z</updated></entry></feed>""".encode("utf-8")

SOURCE = {
    "source_id": "SRC-IR-01",
    "site_url": "https://example.com",
    "feed_url": "https://example.com/rss",
    "api_base_url": None,
    "country": "IR",
    "language": "fa",
    "stream": "domestic",
    "auth_ref": None,
    "license_scope": "summary",
    "enabled": True,
}


def test_rss_parse_keeps_entries_in_order() -> None:
    entries = parse_feed(RSS)
    assert [entry.link for entry in entries] == [
        "https://example.com/news/1",
        "https://example.com/news/2",
    ]
    assert entries[0].published_at.startswith("2026-11-23T06:00:00")


def test_atom_parse_supported() -> None:
    entries = parse_feed(ATOM)
    assert entries[0].link == "https://example.com/atom/1"
    assert entries[0].summary == "summary text"


def test_junk_is_rejected() -> None:
    with pytest.raises(FeedParseError):
        parse_feed(b"<html><body>not a feed</body></html>")
    with pytest.raises(FeedParseError):
        parse_feed(b"")


def test_collect_maps_license_to_scope_and_rights(example_dir: Path) -> None:
    records = collect(RSS, source=SOURCE)
    assert len(records) == 2
    first = records[0]
    assert first["stream"] == "domestic"
    assert first["content_scope"] == "summary"
    assert first["reuse_permission"] == "unverified"
    assert "<p>" not in str(first["original_text"])
    assert first["original_title"] == "جلسه شورای شهر تهران"

    blocked = collect(RSS, source=dict(SOURCE, license_scope="unknown"))[0]
    assert blocked["content_scope"] == "metadata"
    assert blocked["reuse_permission"] == "blocked"


def test_news_id_is_deterministic() -> None:
    first = to_raw_news(parse_feed(RSS)[0], source=SOURCE, collected_at="2026-11-23T09:00:00Z")
    second = to_raw_news(parse_feed(RSS)[0], source=SOURCE, collected_at="2026-11-23T10:00:00Z")
    assert first["news_id"] == second["news_id"]
    assert first["news_id"].startswith("NEWS-")


def test_feed_url_validation() -> None:
    assert validate_feed_url("https://example.com/rss") == "https://example.com/rss"
    with pytest.raises(FeedError):
        validate_feed_url("ftp://example.com/rss")
    with pytest.raises(FeedError):
        validate_feed_url("https://user:pass@example.com/rss")


def test_retry_gives_up_after_attempts() -> None:
    transport = FixtureFeedTransport(responses={}, failures={"https://example.com/rss": "boom"})
    with pytest.raises(FeedError):
        fetch_with_retry(transport, "https://example.com/rss", attempts=3)


def test_conditional_fetch_returns_not_modified() -> None:
    response = FeedResponse(
        url="https://example.com/rss",
        status_code=200,
        body=RSS,
        etag='W/"v1"',
    )
    transport = FixtureFeedTransport(responses={"https://example.com/rss": response})
    fresh = fetch_with_retry(transport, "https://example.com/rss")
    assert fresh.not_modified is False
    cached = fetch_with_retry(transport, "https://example.com/rss", etag='W/"v1"')
    assert cached.not_modified is True


def test_repository_is_idempotent() -> None:
    repo = RawNewsRepository()
    records = collect(RSS, source=SOURCE)
    created, skipped = repo.upsert_many(records)
    assert (created, skipped) == (2, 0)
    assert repo.upsert_many(records) == (0, 2)
    assert len(repo) == 2
    assert len(repo.list(stream="domestic")) == 2
    assert repo.list(stream="foreign") == []


def test_backoff_doubles_and_caps() -> None:
    assert next_interval_seconds(0) == BASE_INTERVAL_SECONDS
    assert next_interval_seconds(1) == BASE_INTERVAL_SECONDS * 2
    assert next_interval_seconds(2) == BASE_INTERVAL_SECONDS * 4
    assert next_interval_seconds(10) == MAX_INTERVAL_SECONDS


def test_poll_state_success_and_failure() -> None:
    store = PollStateStore()
    state = store.get_or_create("SRC-IR-01")
    now = datetime(2026, 11, 23, 9, 0, tzinfo=timezone.utc)
    assert should_poll(state, now) is True

    record_failure(state, error="timeout", now=now)
    assert state.consecutive_failures == 1
    assert state.next_poll_at > now.isoformat()
    assert should_poll(state, now + timedelta(seconds=10)) is False

    record_success(state, etag='W/"2"', last_modified=None, now=now)
    assert state.consecutive_failures == 0
    assert state.etag == 'W/"2"'
    store.save(state)
    assert store.all()[0]["source_id"] == "SRC-IR-01"
