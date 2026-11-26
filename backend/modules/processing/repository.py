"""P07/P08/P09 repository for processed records.

One record per news id, holding the normalised form, its cluster result and its
classification. Writes are idempotent so a retried poll cannot fork history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any, Mapping

from backend.core.contracts import validate_payload

_CONTRACTS = {
    "news": "normalized_news",
    "cluster": "cluster_result",
    "classification": "classified_news",
}


@dataclass
class ProcessingItem:
    news: dict[str, Any]
    cluster: dict[str, Any]
    classification: dict[str, Any]
    extraction: dict[str, Any] = field(default_factory=dict)
    routing: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "news": dict(self.news),
            "cluster": dict(self.cluster),
            "classification": dict(self.classification),
            "extraction": dict(self.extraction),
            "routing": dict(self.routing),
        }


@dataclass
class ProcessingRepository:
    """Fixture store; production writes the three contract tables in central."""

    _items: dict[str, ProcessingItem] = field(default_factory=dict, repr=False)
    _lock: Lock = field(default_factory=Lock, repr=False)

    def save(
        self,
        *,
        news: Mapping[str, Any],
        cluster: Mapping[str, Any],
        classification: Mapping[str, Any],
        extraction: Mapping[str, Any] | None = None,
        routing: Mapping[str, Any] | None = None,
    ) -> ProcessingItem:
        validate_payload(_CONTRACTS["news"], news)
        validate_payload(_CONTRACTS["cluster"], cluster)
        validate_payload(_CONTRACTS["classification"], classification)
        item = ProcessingItem(
            news=dict(news),
            cluster=dict(cluster),
            classification=dict(classification),
            extraction=dict(extraction or {}),
            routing=dict(routing or {}),
        )
        with self._lock:
            self._items[str(news["news_id"])] = item
        return item

    def get(self, news_id: str) -> ProcessingItem | None:
        with self._lock:
            return self._items.get(news_id)

    def contains(self, news_id: str) -> bool:
        with self._lock:
            return news_id in self._items

    def by_event(self, event_id: str) -> list[ProcessingItem]:
        with self._lock:
            return [item for item in self._items.values() if item.cluster.get("event_id") == event_id]

    def by_desk(self, desk: str) -> list[ProcessingItem]:
        with self._lock:
            return [item for item in self._items.values() if desk in item.classification.get("desks", [])]

    def list(self, *, limit: int = 50) -> list[ProcessingItem]:
        with self._lock:
            values = list(self._items.values())
        values.sort(key=lambda item: str(item.news["collected_at"]), reverse=True)
        return values[:limit]

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
