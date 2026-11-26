"""Synthetic read-only adapter for local UI development; never fetches live news."""

from functools import lru_cache

from fastapi import APIRouter

from backend.core.contracts import validate_payload

router = APIRouter(prefix="/v1/demo", tags=["local-demo"])

_NEWS: tuple[dict[str, object], ...] = (
    {
        "schema_version": "1.0",
        "news_id": "DEMO-001",
        "stream": "domestic",
        "source_id": "DEMO-SRC-IR",
        "original_url": "https://example.com/demo/1",
        "original_title": "نمونه ساختگی: نشست تحریریه درباره پوشش شهری",
        "original_text": "این متن صرفاً برای نمایش جریان کار آزمایشی است.",
        "language": "fa",
        "source_country": "IR",
        "subject_countries": ["IR"],
        "published_at": "2026-11-19T09:00:00Z",
        "collected_at": "2026-11-19T09:10:00Z",
        "content_scope": "summary",
        "reuse_permission": "unverified",
        "source_payload_ref": None,
        "normalized_text": None,
        "fingerprint": "demo:001",
        "normalization_version": "v1",
    },
    {
        "schema_version": "1.0",
        "news_id": "DEMO-002",
        "stream": "foreign",
        "source_id": "DEMO-SRC-GB",
        "original_url": "https://example.com/demo/2",
        "original_title": "Synthetic example: a regional transport discussion",
        "original_text": "Demonstration content only; not a report of an actual event.",
        "language": "en",
        "source_country": "GB",
        "subject_countries": ["GB"],
        "published_at": "2026-11-19T10:00:00Z",
        "collected_at": "2026-11-19T10:12:00Z",
        "content_scope": "summary",
        "reuse_permission": "unverified",
        "source_payload_ref": None,
        "normalized_text": None,
        "fingerprint": "demo:002",
        "normalization_version": "v1",
    },
)


@lru_cache(maxsize=1)
def _validated_news() -> tuple[dict[str, object], ...]:
    for record in _NEWS:
        validate_payload("normalized_news", record)
    return _NEWS


@router.get("/news")
async def demo_news() -> dict[str, object]:
    return {"schema_version": "1.0", "mode": "synthetic", "items": _validated_news()}
