"""Shared fixtures for the ETEMAD backend tests (S01-030).

The repository uses namespace packages (no ``__init__.py``), so the repository
root must be importable: ``backend.core...`` resolves from there.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture()
def schema_dir(repo_root: Path) -> Path:
    return repo_root / "source" / "contracts" / "schemas"


@pytest.fixture()
def example_dir(repo_root: Path) -> Path:
    return repo_root / "source" / "contracts" / "examples"
