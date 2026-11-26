"""B01/P27 observability: one logging setup and one structured event helper.

Log lines carry identifiers and decisions, never request bodies, prompts or
secrets. The same redaction rules as the audit trail apply.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from backend.core.audit import sanitize

_LOGGER_NAME = "etemad.observability"


def configure_logging(level: str = "INFO") -> None:
    """Idempotent logging setup usable from the API and from workers."""
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper(), logging.INFO))


def get_logger(name: str = _LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(name)


def log_event(event: str, **fields: Any) -> None:
    """Structured, redacted log line: ``event {json}``."""
    safe = sanitize(fields)
    get_logger().info("%s %s", event, json.dumps(safe, ensure_ascii=False, sort_keys=True))


def correlation_scope(correlation_id: str, **fields: Any) -> dict[str, Any]:
    """Build a log context dict; keeps the id first and never mutates input."""
    context = {"correlation_id": correlation_id}
    context.update(fields)
    return context
