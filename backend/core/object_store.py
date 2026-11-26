"""B01/P26 object storage interface with a local, path-safe implementation.

Keys are scoped and content-addressed. A key can never escape the storage root,
which is the failure mode that turns "store a file" into "write anywhere".
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

_SAFE_KEY = re.compile(r"^[a-z0-9][a-z0-9/_.-]{0,255}$")


class InvalidObjectKey(ValueError):
    """Key is absolute, contains traversal, or has an unsafe character."""


def validate_key(key: str) -> str:
    if not isinstance(key, str) or not _SAFE_KEY.fullmatch(key):
        raise InvalidObjectKey("object key must be lowercase [a-z0-9/_.-] and relative")
    if ".." in key.split("/"):
        raise InvalidObjectKey("object key must not contain '..'")
    return key


class ObjectStore(Protocol):
    def put(self, key: str, data: bytes, *, content_type: str = "application/octet-stream") -> str:
        """Store bytes and return the final key."""

    def get(self, key: str) -> bytes | None:
        ...

    def exists(self, key: str) -> bool:
        ...


@dataclass
class LocalObjectStore:
    """Filesystem-backed fixture store; production uses S3-compatible storage."""

    root: Path

    def __post_init__(self) -> None:
        self.root = Path(self.root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        target = (self.root / validate_key(key)).resolve()
        if not str(target).startswith(str(self.root) + os.sep):
            raise InvalidObjectKey("resolved path escapes the storage root")
        return target

    def put(self, key: str, data: bytes, *, content_type: str = "application/octet-stream") -> str:
        digest = hashlib.sha256(data).hexdigest()
        final_key = f"{validate_key(key)}"
        target = self._path(final_key)
        target.parent.mkdir(parents=True, exist_ok=True)
        handle, temp_name = tempfile.mkstemp(dir=str(target.parent), prefix=".tmp-")
        try:
            with os.fdopen(handle, "wb") as fh:
                fh.write(data)
            os.replace(temp_name, target)
        except BaseException:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
            raise
        sidecar = target.with_suffix(target.suffix + ".sha256")
        sidecar.write_text(digest, encoding="ascii")
        return final_key

    def get(self, key: str) -> bytes | None:
        path = self._path(key)
        if not path.is_file():
            return None
        return path.read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).is_file()
