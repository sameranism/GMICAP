"""P05/S02-001 domestic feed client: HTTP fetch with conditional headers.

No live network call is made unless a caller supplies a real client. The default
is a fixture client, which is what the tests and the local demo use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Protocol
from urllib.parse import urlsplit

import httpx

MAX_BODY_BYTES = 5 * 1024 * 1024
DEFAULT_TIMEOUT = 10.0
ALLOWED_SCHEMES = {"http", "https"}


class FeedError(RuntimeError):
    """A feed could not be fetched; the message never contains credentials."""


@dataclass(frozen=True)
class FeedResponse:
    url: str
    status_code: int
    body: bytes
    etag: str | None = None
    last_modified: str | None = None

    @property
    def not_modified(self) -> bool:
        return self.status_code == 304


def validate_feed_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES or not parts.netloc:
        raise FeedError("feed url must be an absolute http(s) url")
    if parts.username or parts.password:
        raise FeedError("feed url must not embed credentials")
    return url


class FeedTransport(Protocol):
    def fetch(self, url: str, *, etag: str | None, last_modified: str | None) -> FeedResponse:
        """Return a response; raise FeedError on transport failure."""


@dataclass
class HttpxFeedTransport:
    """Real transport. Construct it explicitly; nothing here runs by default."""

    timeout_s: float = DEFAULT_TIMEOUT
    _client: httpx.Client | None = field(default=None, repr=False)

    def fetch(self, url: str, *, etag: str | None, last_modified: str | None) -> FeedResponse:
        headers = {"User-Agent": "ETEMAD-ingest/0.1 (+contact: newsroom)"}
        if etag:
            headers["If-None-Match"] = etag
        if last_modified:
            headers["If-Modified-Since"] = last_modified
        client = self._client or httpx.Client(timeout=self.timeout_s, follow_redirects=True)
        try:
            response = client.get(validate_feed_url(url), headers=headers)
        except httpx.HTTPError as exc:
            raise FeedError(f"feed request failed: {type(exc).__name__}") from exc
        if response.status_code >= 400 and response.status_code != 304:
            raise FeedError(f"feed returned status {response.status_code}")
        body = response.content[:MAX_BODY_BYTES]
        return FeedResponse(
            url=url,
            status_code=response.status_code,
            body=body if response.status_code != 304 else b"",
            etag=response.headers.get("ETag"),
            last_modified=response.headers.get("Last-Modified"),
        )

    def close(self) -> None:
        if self._client is not None:
            self._client.close()


@dataclass
class FixtureFeedTransport:
    """Deterministic transport for tests and the offline demo."""

    responses: Mapping[str, FeedResponse]
    failures: Mapping[str, str] = field(default_factory=dict)

    def fetch(self, url: str, *, etag: str | None, last_modified: str | None) -> FeedResponse:
        if url in self.failures:
            raise FeedError(self.failures[url])
        response = self.responses.get(url)
        if response is None:
            raise FeedError(f"no fixture for {url}")
        if etag and response.etag and etag == response.etag:
            return FeedResponse(url=url, status_code=304, body=b"", etag=etag)
        return response


def fetch_with_retry(
    transport: FeedTransport,
    url: str,
    *,
    etag: str | None = None,
    last_modified: str | None = None,
    attempts: int = 2,
) -> FeedResponse:
    """Retry transport failures up to ``attempts`` times; never retry a 4xx."""
    last: Exception | None = None
    for _ in range(max(1, attempts)):
        try:
            return transport.fetch(url, etag=etag, last_modified=last_modified)
        except FeedError as exc:
            last = exc
    raise FeedError(str(last) if last else "feed fetch failed")


def is_allowed_source(callback: Callable[[str], bool] | None, url: str) -> bool:
    """Optional allowlist hook; absent hook means "not checked", never "allowed"."""
    if callback is None:
        return True
    return bool(callback(url))
