"""B01/P01 secret access by reference.

Secrets never live in the repository, in logs or in contract payloads. Records
carry a ``credential_ref``; the store maps that reference to a value at runtime.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Mapping, Protocol

_REF = re.compile(r"^[a-z][a-z0-9_]{1,31}/[a-z0-9][a-z0-9_./-]{0,95}$")


class SecretUnavailable(RuntimeError):
    """The reference is unknown or the backing store is not configured."""


class InvalidSecretReference(ValueError):
    """The reference is malformed; never echo the value or the secret."""


def validate_ref(ref: str) -> str:
    """Accept ``namespace/name`` in lower snake-kebab form only."""
    if not isinstance(ref, str) or not _REF.fullmatch(ref):
        raise InvalidSecretReference("credential_ref must look like 'namespace/name'")
    return ref


class SecretStore(Protocol):
    def get(self, ref: str) -> str | None:
        """Return the secret value or ``None``; implementations must not log it."""


class InMemorySecretStore:
    """Fixture store for tests and local dry runs only."""

    def __init__(self, values: Mapping[str, str] | None = None) -> None:
        self._values = {validate_ref(k): v for k, v in (values or {}).items()}

    def get(self, ref: str) -> str | None:
        return self._values.get(validate_ref(ref))

    def put(self, ref: str, value: str) -> None:
        if not value:
            raise ValueError("secret value must not be empty")
        self._values[validate_ref(ref)] = value


@dataclass(frozen=True)
class EnvSecretStore:
    """Maps ``namespace/name`` to ``ETEMAD_SECRET_NAMESPACE_NAME``.

    This keeps local development possible without a vault while preserving the
    reference contract. Production replaces it with a vault-backed store.
    """

    environ: Mapping[str, str] = field(default_factory=lambda: os.environ)

    def get(self, ref: str) -> str | None:
        name = "ETEMAD_SECRET_" + validate_ref(ref).replace("/", "_").replace("-", "_").upper()
        value = self.environ.get(name, "")
        return value or None


def require_secret(store: SecretStore, ref: str) -> str:
    """Resolve a reference or fail closed with a non-leaking error."""
    value = store.get(ref)
    if not value:
        raise SecretUnavailable(f"secret not available for reference {ref!r}")
    return value
