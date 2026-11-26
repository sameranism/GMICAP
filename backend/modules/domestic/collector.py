"""P05/S02-002 feed parsing into ``raw_news`` records.

RSS 2.0 and Atom are supported with the standard library. The original title and
text are preserved byte-for-byte after XML decoding; nothing is summarised here.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

from backend.core.contracts import validate_payload

_ATOM = "{http://www.w3.org/2005/Atom}"
_TAG = re.compile(r"<[^>]+>")
_CONTENT_SCOPE_BY_LICENSE = {
    "metadata": "metadata",
    "summary": "summary",
    "full_text": "full_text",
    "unknown": "metadata",
}
_REUSE_BY_LICENSE = {
    "metadata": "link_only",
    "summary": "unverified",
    "full_text": "unverified",
    "unknown": "blocked",
}


class FeedParseError(ValueError):
    """The document is not a usable RSS/Atom feed."""


@dataclass(frozen=True)
class FeedEntry:
    title: str
    link: str
    summary: str
    published_at: str | None


def _text(node: ET.Element | None) -> str:
    return (node.text or "").strip() if node is not None else ""


def _strip_markup(value: str) -> str:
    return _TAG.sub(" ", value).strip()


def _iso(value: str | None) -> str | None:
    if not value:
        return None
    candidate = value.strip()
    # RSS 2.0 uses RFC 822 dates; Atom uses ISO 8601.
    try:
        from email.utils import parsedate_to_datetime

        parsed = parsedate_to_datetime(candidate)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        pass
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def parse_feed(body: bytes) -> list[FeedEntry]:
    """Parse RSS 2.0 or Atom; raise ``FeedParseError`` when neither applies."""
    if not body:
        raise FeedParseError("empty feed body")
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        raise FeedParseError(f"invalid XML: {exc}") from exc

    entries: list[FeedEntry] = []
    if root.tag == f"{_ATOM}feed":
        for item in root.findall(f"{_ATOM}entry"):
            link_node = item.find(f"{_ATOM}link")
            link = link_node.get("href", "") if link_node is not None else ""
            entries.append(
                FeedEntry(
                    title=_text(item.find(f"{_ATOM}title")),
                    link=link,
                    summary=_text(item.find(f"{_ATOM}summary")) or _text(item.find(f"{_ATOM}content")),
                    published_at=_iso(_text(item.find(f"{_ATOM}published")) or _text(item.find(f"{_ATOM}updated"))),
                )
            )
    elif root.tag == "rss":
        channel = root.find("channel")
        if channel is None:
            raise FeedParseError("rss feed has no channel")
        for item in channel.findall("item"):
            entries.append(
                FeedEntry(
                    title=_text(item.find("title")),
                    link=_text(item.find("link")),
                    summary=_text(item.find("description")),
                    published_at=_iso(_text(item.find("pubDate"))),
                )
            )
    else:
        raise FeedParseError("document is neither RSS 2.0 nor Atom")

    usable = [entry for entry in entries if entry.link.startswith(("http://", "https://")) and entry.title]
    if not usable:
        raise FeedParseError("feed contains no usable entries")
    return usable


def news_id_for(source_id: str, link: str) -> str:
    """Deterministic id: the same article never gets two identities."""
    digest = hashlib.sha256(f"{source_id}|{link}".encode("utf-8")).hexdigest()[:16]
    return f"NEWS-{digest.upper()}"


def to_raw_news(
    entry: FeedEntry,
    *,
    source: Mapping[str, Any],
    collected_at: str | None = None,
) -> dict[str, Any]:
    """Map one feed entry onto the frozen ``raw_news`` contract."""
    license_scope = str(source.get("license_scope", "unknown"))
    record: dict[str, Any] = {
        "schema_version": "1.0",
        "news_id": news_id_for(str(source["source_id"]), entry.link),
        "stream": "domestic",
        "source_id": str(source["source_id"]),
        "original_url": entry.link,
        "original_title": entry.title,
        "original_text": _strip_markup(entry.summary) or None,
        "language": str(source.get("language", "fa")),
        "source_country": str(source.get("country", "IR")),
        "subject_countries": [str(source.get("country", "IR"))],
        "published_at": entry.published_at,
        "collected_at": collected_at or datetime.now(timezone.utc).isoformat(),
        "content_scope": _CONTENT_SCOPE_BY_LICENSE.get(license_scope, "metadata"),
        "reuse_permission": _REUSE_BY_LICENSE.get(license_scope, "blocked"),
        "source_payload_ref": None,
    }
    validate_payload("raw_news", record)
    return record


def collect(
    body: bytes,
    *,
    source: Mapping[str, Any],
    collected_at: str | None = None,
) -> list[dict[str, Any]]:
    """Parse a feed and return validated ``raw_news`` records."""
    now = collected_at or datetime.now(timezone.utc).isoformat()
    return [to_raw_news(entry, source=source, collected_at=now) for entry in parse_feed(body)]


def host_of(url: str) -> str:
    return urlsplit(url).netloc.lower()


def dedupe_by_url(records: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    seen: set[str] = set()
    kept: list[Mapping[str, Any]] = []
    for record in records:
        key = str(record["original_url"])
        if key in seen:
            continue
        seen.add(key)
        kept.append(record)
    return kept
