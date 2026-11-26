#!/usr/bin/env python3
"""S00-055 companion - preflight a task before an agent is allowed to start.

Fails closed: when a required attachment or contract is absent, the task must
stop. This is the mechanism that prevents "plausible code on a missing
contract" (the settings_service failure).

Usage:
    python tools/preflight.py S02-001
    python tools/preflight.py S02-001 --pack docs/pack
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = REPO_ROOT / "docs" / "pack"
SCHEMA_DIR = REPO_ROOT / "source" / "contracts" / "schemas"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _resolve(pack: Path, relative: str) -> Path | None:
    for base in (pack, REPO_ROOT):
        candidate = base / relative
        if candidate.is_file():
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight an ETEMAD task id.")
    parser.add_argument("task_id", help="task id, for example S02-001")
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK, help="pack root")
    args = parser.parse_args(argv)

    task_id = args.task_id.strip()
    tasks_csv = args.pack / "manifests" / "tasks.csv"
    attachments_csv = args.pack / "manifests" / "attachments_by_task.csv"
    if not tasks_csv.is_file() or not attachments_csv.is_file():
        print(f"BLOCKED: pack manifests not found under {args.pack}", file=sys.stderr)
        print("  vendor the pack first (for example: docs/pack/source, docs/pack/manifests)", file=sys.stderr)
        return 2

    task = next((row for row in _rows(tasks_csv) if row.get("id") == task_id), None)
    if task is None:
        print(f"BLOCKED: unknown task id {task_id!r}", file=sys.stderr)
        return 2

    required = [
        row for row in _rows(attachments_csv)
        if row.get("task_id") == task_id and row.get("must_exist", "").lower() == "true"
    ]
    missing = [row["file_to_attach_or_reference"] for row in required
               if _resolve(args.pack, row["file_to_attach_or_reference"]) is None]

    problems: list[str] = []
    if not SCHEMA_DIR.is_dir():
        problems.append(f"contract directory missing: {SCHEMA_DIR.relative_to(REPO_ROOT)}")
    else:
        schema_count = len(list(SCHEMA_DIR.glob("*.schema.json")))
        if schema_count < 30:
            problems.append(f"contracts incomplete: {schema_count}/30 schemas in source/contracts/schemas")

    target = task.get("target", "")
    warnings: list[str] = []
    if target and not (REPO_ROOT / target).parent.is_dir():
        warnings.append(f"target directory will be created by this task: {Path(target).parent.as_posix()}/")

    if missing or problems:
        print(f"BLOCKED: {task_id} ({task.get('title', '')})", file=sys.stderr)
        for path in missing:
            print(f"  missing attachment: {path}", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print("  action: stop, report this list, do not invent stubs", file=sys.stderr)
        return 2

    print(f"PASS: {task_id} | target={target} | attachments={len(required)}")
    for warning in warnings:
        print(f"  note: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
