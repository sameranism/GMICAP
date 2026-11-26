"""Regression tests for task preflight from any working directory."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "tools" / "preflight.py"


def test_default_pack_is_repository_root(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PREFLIGHT), "S00-001"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "PASS: S00-001" in result.stdout
    assert "attachments=9" in result.stdout


def test_unknown_task_fails_closed(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PREFLIGHT), "NO-SUCH-TASK"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "BLOCKED: unknown task id" in result.stderr


def test_missing_pack_fails_closed(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PREFLIGHT), "S00-001", "--pack", str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "BLOCKED: pack manifests not found" in result.stderr
