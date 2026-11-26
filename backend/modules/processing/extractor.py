"""P07/S03-001 content extraction before normalisation.

The extractor works on the stored source text only: it removes boilerplate that
feeds append, lifts quoted passages, and flags truncation. It never invents text
and never rewrites the original record.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping

_BOILERPLATE = (
    "ادامه مطلب",
    "بیشتر بخوانید",
    "منبع:",
    "کد خبر",
    "خبرگزاری",
    "اشتراک‌گذاری",
    "کپی لینک",
    "share this",
    "read more",
    "subscribe",
)
_QUOTE_PATTERNS = (
    re.compile(r"«([^»]{3,300})»"),
    re.compile(r"\u201c([^\u201d]{3,300})\u201d"),
    re.compile(r'"([^"]{3,300})"'),
)
_WHITESPACE = re.compile(r"[ \t\u00a0]+")
_MIN_BODY = 40
_MAX_QUOTES = 5


@dataclass(frozen=True)
class Extraction:
    text: str | None
    word_count: int
    quotes: tuple[str, ...] = field(default_factory=tuple)
    truncated: bool = False
    method: str = "feed-summary-v1"

    def as_dict(self) -> dict[str, Any]:
        return {
            "word_count": self.word_count,
            "quotes": list(self.quotes),
            "truncated": self.truncated,
            "method": self.method,
        }


def strip_boilerplate(value: str) -> str:
    kept: list[str] = []
    for line in value.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if any(marker in lowered for marker in _BOILERPLATE):
            continue
        kept.append(_WHITESPACE.sub(" ", stripped))
    return "\n".join(kept).strip()


def extract_quotes(value: str) -> tuple[str, ...]:
    quotes: list[str] = []
    for pattern in _QUOTE_PATTERNS:
        for match in pattern.finditer(value):
            quote = _WHITESPACE.sub(" ", match.group(1)).strip()
            if quote and quote not in quotes:
                quotes.append(quote)
            if len(quotes) >= _MAX_QUOTES:
                return tuple(quotes)
    return tuple(quotes)


def extract(raw: Mapping[str, Any]) -> Extraction:
    """Extract clean body text and evidence from one ``raw_news`` record."""
    original = raw.get("original_text")
    if not isinstance(original, str) or not original.strip():
        return Extraction(text=None, word_count=0, truncated=False)

    body = strip_boilerplate(original)
    truncated = bool(raw.get("content_scope") == "summary") or len(body) < _MIN_BODY
    if body.endswith(("…", "...")) and truncated is False:
        truncated = True

    return Extraction(
        text=body or None,
        word_count=len(body.split()) if body else 0,
        quotes=extract_quotes(body),
        truncated=truncated,
    )
