"""B01/P28 accounts, password hashing and signed session tokens.

Design constraints from ADR-005:
- individual first-use credentials, mandatory reset, no default or shared password;
- hashes only at rest (scrypt, per-user salt);
- signed, expiring session tokens; no server-side session table needed in phase 1.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from typing import Mapping

ROLES = frozenset({"owner", "editor_in_chief", "staff"})
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1
_SALT_BYTES = 16
_TOKEN_VERSION = "v1"
MIN_PASSWORD_LENGTH = 12


class AuthenticationError(Exception):
    """Generic authentication failure; the message never reveals which check failed."""


class SessionInvalid(AuthenticationError):
    """Token missing, malformed, tampered or expired."""


def generate_first_use_credential(length: int = 24) -> str:
    """High-entropy one-time credential; force a reset at first login."""
    return secrets.token_urlsafe(length)


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _unb64(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    """Return ``scrypt$n$r$p$salt$hash``; never store the plaintext."""
    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
    salt = salt or secrets.token_bytes(_SALT_BYTES)
    derived = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=32
    )
    return "scrypt${}${}${}${}${}".format(
        SCRYPT_N, SCRYPT_R, SCRYPT_P, _b64(salt), _b64(derived)
    )


def verify_password(password: str, encoded: str) -> bool:
    """Constant-time check; a malformed hash is a failed login, not a crash."""
    try:
        scheme, n, r, p, salt_b64, hash_b64 = encoded.split("$")
        if scheme != "scrypt":
            return False
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=_unb64(salt_b64),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(_unb64(hash_b64)),
        )
        return hmac.compare_digest(derived, _unb64(hash_b64))
    except (ValueError, TypeError):
        return False


@dataclass(frozen=True)
class Principal:
    subject_id: str
    role: str
    must_reset_password: bool = False

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"unknown role: {self.role!r}")


def _sign(key: bytes, body: bytes) -> str:
    return _b64(hmac.new(key, body, hashlib.sha256).digest())


def issue_session(principal: Principal, key: bytes, *, ttl_seconds: int = 3600) -> str:
    """Create a signed token: ``v1.<payload>.<signature>``."""
    if not key:
        raise ValueError("session key must not be empty")
    if ttl_seconds <= 0:
        raise ValueError("ttl_seconds must be positive")
    payload = {
        "sub": principal.subject_id,
        "role": principal.role,
        "reset": principal.must_reset_password,
        "exp": int(time.time()) + ttl_seconds,
    }
    body = _b64(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    return f"{_TOKEN_VERSION}.{body}.{_sign(key, body.encode('ascii'))}"


def verify_session(token: str, key: bytes, *, now: int | None = None) -> Principal:
    """Validate signature and expiry; raise ``SessionInvalid`` otherwise."""
    try:
        version, body, signature = token.split(".")
    except (AttributeError, ValueError) as exc:
        raise SessionInvalid("malformed token") from exc
    if version != _TOKEN_VERSION or not body or not signature:
        raise SessionInvalid("unsupported token")
    expected = _sign(key, body.encode("ascii"))
    if not hmac.compare_digest(signature, expected):
        raise SessionInvalid("bad signature")
    try:
        payload = json.loads(_unb64(body))
    except (ValueError, TypeError) as exc:
        raise SessionInvalid("malformed payload") from exc
    if not isinstance(payload, Mapping):
        raise SessionInvalid("malformed payload")
    if int(payload.get("exp", 0)) <= (int(time.time()) if now is None else now):
        raise SessionInvalid("expired token")
    try:
        return Principal(
            subject_id=str(payload["sub"]),
            role=str(payload["role"]),
            must_reset_password=bool(payload.get("reset", False)),
        )
    except (KeyError, ValueError) as exc:
        raise SessionInvalid("invalid claims") from exc


def bearer_token(authorization_header: str | None) -> str | None:
    """Extract a bearer token from an Authorization header; None when absent."""
    if not authorization_header:
        return None
    scheme, _, token = authorization_header.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip() or None
