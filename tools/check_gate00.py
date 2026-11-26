#!/usr/bin/env python3
"""Run reproducible Gate-00 source, attachment, and negative contract checks."""

import csv
import hashlib
import json
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker

from preflight import REPO_ROOT, main as preflight
from validate_contracts import DEFAULT_EXAMPLES, DEFAULT_SCHEMAS, validate


def check_inventory():
    with (REPO_ROOT / "manifests/tasks.csv").open(encoding="utf-8-sig", newline="") as handle:
        tasks = list(csv.DictReader(handle))
    phase_zero = [task for task in tasks if task["phase"] == "0"]
    expected_ids = {f"S00-{index:03d}" for index in range(1, 63)}
    if len(phase_zero) != len(expected_ids) or {task["id"] for task in phase_zero} != expected_ids:
        raise ValueError("Gate-00 task inventory must contain S00-001 through S00-062 exactly once")
    targets = {task["target"] for task in phase_zero}
    if len(targets) != len(phase_zero):
        raise ValueError("Gate-00 targets must be unique")
    tracked = set(subprocess.check_output(["git", "ls-files", "-z"], cwd=REPO_ROOT, text=True).split("\0"))
    for task in phase_zero:
        for field in ("target", "prompt_path", "attachments_path"):
            path = task[field]
            if path not in tracked or not (REPO_ROOT / path).is_file():
                raise ValueError(f"{task['id']}: missing tracked {field}: {path}")
        if preflight([task["id"], "--pack", str(REPO_ROOT)]):
            raise ValueError(f"{task['id']}: preflight failed")
    return len(phase_zero)


def check_contracts():
    expected_hashes = json.loads((REPO_ROOT / "quality/SCHEMA_SHA256.json").read_text(encoding="utf-8"))
    if len(expected_hashes) != 30:
        raise ValueError("Gate-00 needs the frozen inventory of 30 schema hashes")
    if failures := validate(DEFAULT_SCHEMAS, DEFAULT_EXAMPLES):
        raise ValueError("\n".join(failures))
    negative_cases = 0
    for filename, expected in sorted(expected_hashes.items()):
        path = DEFAULT_SCHEMAS / filename
        source = path.read_bytes()
        if hashlib.sha256(source).hexdigest() != expected:
            raise ValueError(f"Frozen schema checksum changed: {filename}")
        name = filename.removesuffix(".schema.json")
        schema = Draft202012Validator(json.loads(source), format_checker=FormatChecker())
        example = json.loads((DEFAULT_EXAMPLES / f"{name}.example.json").read_text(encoding="utf-8"))
        for required in schema.schema["required"]:
            if required not in example or schema.is_valid({
                field: value for field, value in example.items() if field != required
            }):
                raise ValueError(f"{name}: missing required field {required} was not rejected")
            negative_cases += 1
        for label, invalid in (
            ("unknown version", example | {"schema_version": "0.0-invalid"}),
            ("unknown root field", example | {"_gate00_unknown": True}),
        ):
            if schema.is_valid(invalid):
                raise ValueError(f"{name}: {label} was not rejected")
            negative_cases += 1
    return negative_cases


def main():
    try:
        tasks = check_inventory()
        negative_cases = check_contracts()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"Gate-00 foundation checks: FAIL — {exc}", file=sys.stderr)
        return 1
    print(f"Gate-00 foundation checks: PASS ({tasks} task preflights; {negative_cases} negative contract cases)")
    print("See docs/gates/GATE-00.md for semantic, security, and integration evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
