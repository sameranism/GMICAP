#!/usr/bin/env python3
"""S00-055 - static boundary check for ETEMAD packages.

Flags two classes of violation without pretending to be a full AST policy engine:
1. cross-package imports that bypass the shared core (architecture boundary);
2. hard-coded database/queue connection strings or inline passwords (secrets boundary).

Run:  python tools/check_boundaries.py [--root .] [--self-test]
Exit: 0 clean, 1 violations found, 2 self-test failure.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
import tempfile
from pathlib import Path

SKIP_DIRS = {"node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".git", "tests"}
CONNECTION_MARKERS = ("postgresql://", "postgres://", "redis://", "amqp://", "mongodb://")
_INLINE_PASSWORD = re.compile(
    r"""(?i)(password|passwd|pwd)\s*=\s*["'][^"']{3,}["']"""
)


def package_of(path: Path, root: Path) -> str:
    parts = path.relative_to(root).parts
    if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "modules":
        return f"modules.{parts[2]}"
    if len(parts) >= 2 and parts[0] == "backend":
        return parts[1]
    return "unknown"


def imported_names(tree: ast.AST) -> list[str]:
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def check_file(path: Path, root: Path) -> list[str]:
    rel = path.relative_to(root).as_posix()
    owner = package_of(path, root)
    problems: list[str] = []
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{rel}: unreadable ({exc})"]

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return [f"{rel}: syntax error ({exc.msg} line {exc.lineno})"]

    for module in imported_names(tree):
        if not module.startswith("backend.modules."):
            continue
        target = module.split(".")[2]
        if owner.startswith("modules.") and owner.split(".", 1)[1] != target:
            problems.append(f"{rel}: cross-package import of backend.modules.{target}")

    lowered = source.lower()
    for marker in CONNECTION_MARKERS:
        if marker in lowered:
            problems.append(f"{rel}: hard-coded connection string ({marker})")
    if _INLINE_PASSWORD.search(source) and "credential_ref" not in lowered:
        problems.append(f"{rel}: inline credential literal in a password assignment")

    return problems


def scan(root: Path) -> list[str]:
    problems: list[str] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if "tools" in path.relative_to(root).parts:
            continue
        problems.extend(check_file(path, root))
    return problems


def self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        good = root / "backend" / "modules" / "domestic" / "ok.py"
        good.parent.mkdir(parents=True)
        good.write_text("from backend.core.contracts import validate_payload\n", encoding="utf-8")
        bad = root / "backend" / "modules" / "domestic" / "bad.py"
        bad.write_text(
            "import backend.modules.foreign.collector\n"
            "DSN = 'postgresql://user:secret@db/etemad'\n",
            encoding="utf-8",
        )
        found = scan(root)
        if not found:
            print("SELF-TEST: FAIL (violations not detected)", file=sys.stderr)
            return 2
        print(f"SELF-TEST: PASS ({len(found)} violations detected in fixtures)")
        return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ETEMAD package boundary check.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    problems = scan(args.root)
    if problems:
        print("BOUNDARIES: FAIL", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("BOUNDARIES: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
