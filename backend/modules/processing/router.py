"""P09/S03-005 routing a classified item to its owning desk project.

Routing is a pure function of the classification contract, so a re-run produces
the same destination. It never publishes anything and never calls a network.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from backend.core.contracts import validate_payload

ROUTING_RULES_VERSION = "routing-v1"
ANALYSIS_TOPICS = frozenset({"elections", "foreign_policy", "energy"})
DESK_QUEUE = {
    "politics": "desk-politics",
    "economy": "desk-economy",
    "international": "desk-international",
    "society": "desk-society",
    "sports": "desk-sports",
    "culture": "desk-culture",
    "technology": "desk-technology",
    "health": "desk-health",
    "general": "desk-general",
}
PRIORITY_QUEUE = {"urgent": "urgent", "normal": "standard", "low": "bulk"}


@dataclass(frozen=True)
class RoutingDecision:
    news_id: str
    target_project: str
    queue: str
    analysis_queue: str | None
    reasons: tuple[str, ...]
    rules_version: str = ROUTING_RULES_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "news_id": self.news_id,
            "target_project": self.target_project,
            "queue": self.queue,
            "analysis_queue": self.analysis_queue,
            "reasons": list(self.reasons),
            "rules_version": self.rules_version,
        }


def route(classified: Mapping[str, Any]) -> RoutingDecision:
    """Map ``classified_news`` onto a desk project and queue."""
    validate_payload("classified_news", classified)
    stream = str(classified["stream"])
    desks = [str(desk) for desk in classified["desks"]]
    topics = [str(topic) for topic in classified["topics"]]
    priority = str(classified["operational_priority"])

    reasons: list[str] = []
    if stream == "foreign":
        target = "P12"
        reasons.append("foreign stream -> translation project")
    elif stream == "manual":
        target = "P13"
        reasons.append("manual stream -> editorial project")
    else:
        target = "P13"
        reasons.append("domestic stream -> editorial project")

    desk = next((item for item in desks if item in DESK_QUEUE), "general")
    queue = DESK_QUEUE[desk] if priority != "urgent" else "desk-urgent"
    if priority == "urgent":
        reasons.append("urgent priority overrides desk queue")
    else:
        reasons.append(f"desk queue {queue}")

    analysis_queue = None
    if stream != "foreign" and any(topic in ANALYSIS_TOPICS for topic in topics):
        analysis_queue = "analysis-review"
        reasons.append("analysis topic queued for P15 review")

    if priority == "low":
        queue = PRIORITY_QUEUE["low"]
        reasons.append("low priority routed to bulk queue")

    return RoutingDecision(
        news_id=str(classified["news_id"]),
        target_project=target,
        queue=queue,
        analysis_queue=analysis_queue,
        reasons=tuple(reasons),
    )
