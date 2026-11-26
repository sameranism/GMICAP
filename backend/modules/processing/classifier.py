"""P09/S03-004..005 rule-based desk and topic classification.

Everything is keyword-driven and versioned (``rules_version``), so a change of
classification rules is visible in the output and can be reviewed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from backend.core.contracts import validate_payload

RULES_VERSION = "classification-v1"

DESK_RULES: dict[str, tuple[str, ...]] = {
    "politics": ("دولت", "مجلس", "وزیر", "رئیس‌جمهور", "انتخابات", "سیاست", "شورای نگهبان"),
    "economy": ("بورس", "دلار", "تورم", "بانک", "نفت", "اقتصاد", "بودجه", "یارانه"),
    "international": ("سازمان ملل", "آمریکا", "اروپا", "روسیه", "چین", "بین‌الملل", "تحریم"),
    "society": ("شهرداری", "آموزش", "بهداشت", "حوادث", "جامعه", "پلیس", "دادگاه"),
    "sports": ("فوتبال", "لیگ", "ورزش", "بازی", "المپیک"),
    "culture": ("سینما", "کتاب", "موسیقی", "تئاتر", "فرهنگ", "هنر"),
    "technology": ("فناوری", "اینترنت", "هوش مصنوعی", "استارتاپ", "دیجیتال", "موبایل"),
    "health": ("کرونا", "بیماری", "درمان", "واکسن", "سلامت"),
}

TOPIC_RULES: dict[str, tuple[str, ...]] = {
    "energy": ("نفت", "گاز", "برق", "انرژی"),
    "inflation": ("تورم", "گرانی", "قیمت"),
    "elections": ("انتخابات", "رأی", "نامزد"),
    "justice": ("دادگاه", "محکوم", "پرونده", "قاضی"),
    "foreign_policy": ("مذاکره", "توافق", "سفیر", "دیپلماسی"),
    "technology_policy": ("فیلترینگ", "اینترنت", "داده"),
}

URGENT_MARKERS = ("فوری", "فوت", "کشته", "انفجار", "زلزله", "بحران", "حمله")
DEFAULT_DESK = "general"


def _matches(text: str, rules: Mapping[str, tuple[str, ...]]) -> list[str]:
    lowered = text.lower()
    return [name for name, words in rules.items() if any(word.lower() in lowered for word in words)]


def classify(
    record: Mapping[str, Any],
    *,
    event_id: str,
    classified_at: str | None = None,
    priority: str | None = None,
) -> dict[str, Any]:
    """Return a validated ``classified_news`` record."""
    validate_payload("normalized_news", record)
    haystack = " ".join(
        filter(None, [str(record.get("original_title", "")), str(record.get("normalized_text") or "")])
    )
    desks = _matches(haystack, DESK_RULES) or [DEFAULT_DESK]
    topics = _matches(haystack, TOPIC_RULES)

    if priority is None:
        priority = "urgent" if any(word in haystack for word in URGENT_MARKERS) else "normal"

    result = {
        "schema_version": "1.0",
        "news_id": str(record["news_id"]),
        "stream": str(record["stream"]),
        "desks": desks,
        "topics": topics,
        "subject_countries": list(record.get("subject_countries") or []),
        "event_id": event_id,
        "operational_priority": priority,
        "rules_version": RULES_VERSION,
        "classified_at": classified_at or datetime.now(timezone.utc).isoformat(),
    }
    validate_payload("classified_news", result)
    return result
