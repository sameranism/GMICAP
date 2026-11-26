"""S03-001..008: normalisation, dedupe and classification over real contracts."""

from __future__ import annotations

from pathlib import Path

import pytest

from backend.modules.processing.classifier import RULES_VERSION, classify
from backend.modules.processing.deduplicator import Clusterer, event_id_for, jaccard, tokens
from backend.modules.processing.extractor import extract, extract_quotes, strip_boilerplate
from backend.modules.processing.normalizer import (
    NORMALIZATION_VERSION,
    fingerprint_for,
    normalize,
    normalize_text,
)
from backend.modules.processing.repository import ProcessingRepository
from backend.modules.processing.router import route

SOURCE = {
    "source_id": "SRC-IR-01",
    "country": "IR",
    "language": "fa",
}


def _raw(title: str, text: str, *, news_id: str = "NEWS-1", url: str = "https://example.com/1") -> dict:
    return {
        "schema_version": "1.0",
        "news_id": news_id,
        "stream": "domestic",
        "source_id": "SRC-IR-01",
        "original_url": url,
        "original_title": title,
        "original_text": text,
        "language": "fa",
        "source_country": "IR",
        "subject_countries": ["IR"],
        "published_at": "2026-11-23T06:00:00+00:00",
        "collected_at": "2026-11-23T07:00:00+00:00",
        "content_scope": "summary",
        "reuse_permission": "unverified",
        "source_payload_ref": None,
    }


def test_normalize_text_collapses_noise() -> None:
    assert normalize_text("  سلام\u200b   دنیا  ") == "سلام دنیا"
    assert normalize_text("a\r\n\r\n\r\nb") == "a\n\nb"
    assert normalize_text(None) is None
    assert normalize_text("   ") is None


def test_fingerprint_is_stable_and_content_sensitive() -> None:
    first = fingerprint_for(language="fa", title="عنوان", text="متن")
    second = fingerprint_for(language="fa", title="عنوان", text="متن")
    changed = fingerprint_for(language="fa", title="عنوان", text="متن دیگر")
    assert first == second
    assert first != changed
    assert first.startswith("fp-")


def test_normalize_produces_valid_contract() -> None:
    normalized = normalize(_raw("جلسه شورای شهر", "شهرداری درباره بودجه جلسه داشت."))
    assert normalized["normalization_version"] == NORMALIZATION_VERSION
    assert normalized["fingerprint"].startswith("fp-")
    assert normalized["news_id"] == "NEWS-1"
    assert normalized["original_text"] == "شهرداری درباره بودجه جلسه داشت."


def test_identical_content_produces_identical_fingerprint_across_sources() -> None:
    left = normalize(_raw("یک خبر", "متن یکسان", news_id="NEWS-1", url="https://a.example/1"))
    right = normalize(_raw("یک خبر", "متن یکسان", news_id="NEWS-2", url="https://b.example/1"))
    assert left["fingerprint"] == right["fingerprint"]


def test_exact_duplicate_is_linked_to_the_first_record() -> None:
    clusterer = Clusterer()
    left = normalize(_raw("یک خبر", "متن یکسان", news_id="NEWS-1", url="https://a.example/1"))
    right = normalize(_raw("یک خبر", "متن یکسان", news_id="NEWS-2", url="https://b.example/1"))

    first = clusterer.cluster(left)
    second = clusterer.cluster(right)
    assert first["duplicate_of"] is None
    assert second["duplicate_of"] == "NEWS-1"
    assert second["event_id"] == first["event_id"]


def test_related_articles_share_an_event() -> None:
    clusterer = Clusterer()
    base = "شهرداری تهران درباره بودجه سال آینده جلسه برگزار کرد"
    left = normalize(_raw("بودجه شهرداری", base, news_id="NEWS-1", url="https://a.example/1"))
    right = normalize(
        _raw("جلسه بودجه شهرداری تهران", base + " و تصمیم گرفت", news_id="NEWS-2", url="https://b.example/1")
    )
    clusterer.cluster(left)
    second = clusterer.cluster(right)
    assert second["duplicate_of"] is None
    assert "NEWS-1" in second["related_news_ids"]


def test_jaccard_and_event_id_helpers() -> None:
    assert jaccard(tokens("alpha bravo charlie"), tokens("alpha bravo charlie")) == 1.0
    assert jaccard(tokens("alpha"), tokens("bravo")) == 0.0
    assert jaccard(set(), set()) == 0.0
    assert event_id_for("fp-abcdef1234567890").startswith("EVENT-")


def test_classify_detects_desks_and_topics() -> None:
    normalized = normalize(_raw("رشد شاخص بورس تهران", "بورس و دلار امروز بالا رفت و تورم ادامه دارد"))
    classified = classify(normalized, event_id="EVENT-1")
    assert "economy" in classified["desks"]
    assert "inflation" in classified["topics"]
    assert classified["rules_version"] == RULES_VERSION
    assert classified["operational_priority"] == "normal"


def test_classify_marks_urgent_news() -> None:
    normalized = normalize(_raw("فوری: زلزله در شمال", "شمار کشته‌شدگان اعلام شد"))
    classified = classify(normalized, event_id="EVENT-2")
    assert classified["operational_priority"] == "urgent"


def test_unmatched_news_gets_default_desk() -> None:
    normalized = normalize(_raw("عنوان بی‌ربط", "متن کوتاه"))
    classified = classify(normalized, event_id="EVENT-3")
    assert classified["desks"] == ["general"]
    assert classified["topics"] == []


# --- extractor -----------------------------------------------------------------


def test_extractor_strips_boilerplate_and_counts_words() -> None:
    raw = _raw(
        "عنوان",
        "متن اصلی خبر است.\nادامه مطلب\nبیشتر بخوانید\nخط دوم خبر.",
    )
    result = extract(raw)
    assert "ادامه مطلب" not in str(result.text)
    assert "بیشتر بخوانید" not in str(result.text)
    assert result.word_count >= 5
    assert result.method == "feed-summary-v1"


def test_extractor_lifts_quotes() -> None:
    raw = _raw("عنوان", "وزیر گفت: «این تصمیم نهایی است» و بعد توضیح داد.")
    result = extract(raw)
    assert "این تصمیم نهایی است" in result.quotes


def test_extractor_flags_short_summary_as_truncated() -> None:
    raw = _raw("عنوان", "کوتاه")
    result = extract(raw)
    assert result.truncated is True


def test_extractor_handles_missing_text() -> None:
    result = extract(_raw("عنوان", None))
    assert result.text is None
    assert result.word_count == 0
    assert strip_boilerplate("ادامه مطلب") == ""
    assert extract_quotes("بدون نقل قول") == ()


# --- router --------------------------------------------------------------------


def test_router_sends_domestic_to_editorial() -> None:
    normalized = normalize(_raw("رشد بورس", "بورس تهران رشد کرد"))
    decision = route(classify(normalized, event_id="EVENT-1"))
    assert decision.target_project == "P13"
    assert decision.queue == "desk-economy"


def test_router_sends_foreign_to_translation() -> None:
    foreign = _raw("خبر خارجی", "متن خبر خارجی")
    foreign["stream"] = "foreign"
    normalized = normalize(foreign)
    decision = route(classify(normalized, event_id="EVENT-2"))
    assert decision.target_project == "P12"


def test_router_escalates_urgent_and_analysis() -> None:
    normalized = normalize(_raw("فوری: زلزله", "کشته شدگان و انتخابات"))
    decision = route(classify(normalized, event_id="EVENT-3"))
    assert decision.queue == "desk-urgent"
    assert decision.analysis_queue == "analysis-review"


def test_router_bulk_queue_for_low_priority() -> None:
    normalized = normalize(_raw("خبر عادی", "متن عادی خبر"))
    classified = classify(normalized, event_id="EVENT-4", priority="low")
    decision = route(classified)
    assert decision.queue == "bulk"


# --- processing repository -----------------------------------------------------


def test_repository_saves_and_queries_processed_items() -> None:
    repository = ProcessingRepository()
    normalized = normalize(_raw("رشد بورس", "بورس تهران رشد کرد"))
    cluster = Clusterer().cluster(normalized)
    classified = classify(normalized, event_id=str(cluster["event_id"]))

    item = repository.save(news=normalized, cluster=cluster, classification=classified)
    assert repository.contains("NEWS-1")
    assert len(repository) == 1
    assert repository.get("NEWS-1") is not None
    assert repository.by_event(str(cluster["event_id"]))[0].news["news_id"] == "NEWS-1"
    assert repository.by_desk("economy")[0].news["news_id"] == "NEWS-1"
    assert item.as_dict()["classification"]["rules_version"] == RULES_VERSION


def test_repository_rejects_invalid_contract() -> None:
    repository = ProcessingRepository()
    with pytest.raises(Exception):
        repository.save(news={"schema_version": "1.0"}, cluster={}, classification={})
