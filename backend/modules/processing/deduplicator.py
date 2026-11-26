"""P08/S03-003..006..007 duplicate detection and event clustering.

Two levels, both deterministic and explainable:
1. identical fingerprint -> duplicate;
2. token overlap above a threshold -> related, linked to the same event.

No model call is involved, so the result is reproducible from the contract data.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Mapping

from backend.core.contracts import validate_payload

SIMILARITY_METHOD = "url-and-text-v1"
RELATED_THRESHOLD = 0.75
_TOKEN = re.compile(r"[\w\u0600-\u06ff]{2,}")


def tokens(text: str | None) -> set[str]:
    return {match.group(0).lower() for match in _TOKEN.finditer(text or "")}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def event_id_for(fingerprint: str) -> str:
    return "EVENT-" + fingerprint.removeprefix("fp-")[:12].upper()


@dataclass
class Clusterer:
    """Fixture cluster store; production uses ``cluster_result`` rows."""

    _by_fingerprint: dict[str, str] = field(default_factory=dict, repr=False)
    _by_event: dict[str, list[str]] = field(default_factory=dict, repr=False)
    _text_by_id: dict[str, set[str]] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def cluster(self, record: Mapping[str, Any], *, created_at: str | None = None) -> dict[str, Any]:
        validate_payload("normalized_news", record)
        news_id = str(record["news_id"])
        fingerprint = str(record["fingerprint"])
        text_tokens = tokens(record.get("normalized_text") or record.get("original_title"))

        with self._lock:
            duplicate_of = self._by_fingerprint.get(fingerprint)
            if duplicate_of is not None and duplicate_of != news_id:
                event_id = event_id_for(fingerprint)
                result = self._result(
                    news_id=news_id,
                    event_id=event_id,
                    duplicate_of=duplicate_of,
                    related=self._by_event.get(event_id, []),
                    created_at=created_at,
                )
                return result

            event_id = event_id_for(fingerprint)
            related = []
            for other_id, other_tokens in self._text_by_id.items():
                if other_id == news_id:
                    continue
                if jaccard(text_tokens, other_tokens) >= RELATED_THRESHOLD:
                    related.append(other_id)

            self._by_fingerprint[fingerprint] = news_id
            self._text_by_id[news_id] = text_tokens
            self._by_event.setdefault(event_id, [])
            if news_id not in self._by_event[event_id]:
                self._by_event[event_id].append(news_id)

            return self._result(
                news_id=news_id,
                event_id=event_id,
                duplicate_of=None,
                related=related,
                created_at=created_at,
            )

    def _result(
        self,
        *,
        news_id: str,
        event_id: str,
        duplicate_of: str | None,
        related: list[str],
        created_at: str | None,
    ) -> dict[str, Any]:
        result = {
            "schema_version": "1.0",
            "news_id": news_id,
            "event_id": event_id,
            "duplicate_of": duplicate_of,
            "related_news_ids": [item for item in dict.fromkeys(related) if item != news_id],
            "similarity_method": SIMILARITY_METHOD,
            "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        }
        validate_payload("cluster_result", result)
        return result

    def event_members(self, event_id: str) -> list[str]:
        with self._lock:
            return list(self._by_event.get(event_id, []))
