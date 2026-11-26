"""B01/P01 PostgreSQL engines for the three ETEMAD databases.

Ownership rule (ADR-003): central, domestic and foreign are separate databases.
A package may only reach its own role. No cross-database joins, no shared engine.

Engines are created lazily; importing this module never opens a connection and
never requires a database to be reachable.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from threading import Lock
from typing import Mapping
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

ROLE_ENV = {
    "central": "ETEMAD_DB_CENTRAL_URL",
    "domestic": "ETEMAD_DB_DOMESTIC_URL",
    "foreign": "ETEMAD_DB_FOREIGN_URL",
}


class DatabaseNotConfigured(RuntimeError):
    """The requested database role has no connection URL."""


def redact_url(url: str) -> str:
    """Return the URL with any password replaced; safe for logs and reports."""
    parts = urlsplit(url)
    if parts.password is None:
        return url
    netloc = parts.netloc.replace(f":{parts.password}@", ":***@", 1)
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


@dataclass
class DatabaseRegistry:
    """Lazily created, per-role engines with an explicit environment override."""

    environ: Mapping[str, str] = field(default_factory=lambda: os.environ)
    _engines: dict[str, Engine] = field(default_factory=dict, init=False, repr=False)
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def url_for(self, role: str) -> str:
        if role not in ROLE_ENV:
            raise KeyError(f"unknown database role: {role!r}")
        url = self.environ.get(ROLE_ENV[role], "").strip()
        if not url:
            raise DatabaseNotConfigured(
                f"{ROLE_ENV[role]} is not set; database role {role!r} is unavailable"
            )
        return url

    def engine(self, role: str) -> Engine:
        with self._lock:
            engine = self._engines.get(role)
            if engine is None:
                engine = create_engine(
                    self.url_for(role),
                    pool_pre_ping=True,
                    future=True,
                )
                self._engines[role] = engine
            return engine

    def describe(self) -> dict[str, str]:
        """Redacted configuration summary for health endpoints and reports."""
        summary: dict[str, str] = {}
        for role, env_name in ROLE_ENV.items():
            raw = self.environ.get(env_name, "").strip()
            summary[role] = redact_url(raw) if raw else "not_configured"
        return summary

    def dispose(self) -> None:
        with self._lock:
            for engine in self._engines.values():
                engine.dispose()
            self._engines.clear()


def configured_roles(environ: Mapping[str, str] | None = None) -> list[str]:
    """Roles that currently have a URL; used by startup checks, never by auth."""
    environ = os.environ if environ is None else environ
    return [role for role, name in ROLE_ENV.items() if environ.get(name, "").strip()]
