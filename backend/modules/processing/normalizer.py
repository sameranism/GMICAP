"""P07/S03-001..002..008 raw to normalised news, with a stable fingerprint.

Normalisation is deliberately conservative: it never rewrites the original text
in place, it produces a parallel ``normalized_text`` and a fingerprint that the
dedupe stage can trust.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import datetime, timezone
from typing import Any, Mapping

from backend.core.contracts import validate_payload

NORMALIZATION_VERSION = "v1"
_ZERO_WIDTH = re.compile(r"[\u200b-\u200f\u202a-\u202e\ufeff]")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_SPACES = re.compile(r"[ \t\u00a0]+")
_NEWLINES = re.compile(r"\n{3,}")


def normalize_text(value: str | None) -> str | None:
    """NFKC, drop zero-width/control characters, collapse whitespace."""
    if value is None:
        return None
    text = unicodedata.normalize("NFKC", str(value))
    text = _ZERO_WIDTH.sub("", text)
    text = _CONTROL.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _SPACES.sub(" ", text)
    text = _NEWLINES.sub("\n\n", text)
    text = "\n".join(line.strip() for line in text.split("\n")).strip()
    return text or None


def fingerprint_for(*, language: str, title: str, text: str | None) -> str:
    """Content fingerprint; independent of source and collection time."""
    payload = "\u241f".join(
        [language.strip().lower(), normalize_text(title) or "", normalize_text(text) or ""]
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"fp-{digest[:32]}"


def normalize(raw: Mapping[str, Any], *, normalized_at: str | None = None) -> dict[str, Any]:
    """Return a validated ``normalized_news`` record derived from ``raw_news``."""
    validate_payload("raw_news", raw)
    title = normalize_text(raw.get("original_title")) or ""
    text = normalize_text(raw.get("original_text"))
    record: dict[str, Any] = {
        "schema_version": "1.0",
        "news_id": str(raw["news_id"]),
        "stream": str(raw["stream"]),
        "source_id": str(raw["source_id"]),
        "original_url": str(raw["original_url"]),
        "original_title": str(raw["original_title"]),
        "original_text": raw.get("original_text"),
        "language": str(raw["language"]),
        "source_country": raw.get("source_country"),
        "subject_countries": list(raw.get("subject_countries") or []),
        "published_at": raw.get("published_at"),
        "collected_at": str(raw["collected_at"]),
        "content_scope": str(raw["content_scope"]),
        "reuse_permission": str(raw["reuse_permission"]),
        "source_payload_ref": raw.get("source_payload_ref"),
        "normalized_text": text,
        "fingerprint": fingerprint_for(language=str(raw["language"]), title=title, text=text),
        "normalization_version": NORMALIZATION_VERSION,
    }
    validate_payload("normalized_news", record)
    return record


def normalize_many(raw_records: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [normalize(record) for record in raw_records]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
