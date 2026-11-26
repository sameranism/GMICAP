#!/usr/bin/env python3
"""S00-017 - validate every ETEMAD contract schema and its example record.

Read-only: this tool never modifies source contracts. Exit code 1 means the
contract layer is not trustworthy and no product task may merge.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMAS = REPO_ROOT / "source" / "contracts" / "schemas"
DEFAULT_EXAMPLES = REPO_ROOT / "source" / "contracts" / "examples"
SUPPORTED_VERSION = "1.0"


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _example_for(schema_path: Path, example_dir: Path) -> Path:
    name = schema_path.name.removesuffix(".schema.json")
    return example_dir / f"{name}.example.json"


def validate(schema_dir: Path, example_dir: Path) -> list[str]:
    failures: list[str] = []
    schemas = sorted(schema_dir.glob("*.schema.json"))
    if not schemas:
        return [f"no *.schema.json found under {schema_dir}"]

    seen_ids: dict[str, str] = {}
    for schema_path in schemas:
        name = schema_path.name.removesuffix(".schema.json")
        try:
            schema = _load(schema_path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: unreadable schema ({exc})")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            failures.append(f"{name}: invalid Draft 2020-12 schema ({exc.message})")
            continue

        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            if schema_id in seen_ids:
                failures.append(f"{name}: duplicate $id also used by {seen_ids[schema_id]}")
            seen_ids[schema_id] = name

        example_path = _example_for(schema_path, example_dir)
        if not example_path.is_file():
            failures.append(f"{name}: example missing at {example_path.name}")
            continue
        try:
            example = _load(example_path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: unreadable example ({exc})")
            continue

        if not isinstance(example, dict) or example.get("schema_version") != SUPPORTED_VERSION:
            failures.append(f"{name}: example schema_version is not {SUPPORTED_VERSION!r}")
            continue

        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(example), key=lambda item: list(item.absolute_path))
        for error in errors[:3]:
            location = "/".join(str(part) for part in error.absolute_path) or "/"
            failures.append(f"{name}: example invalid at {location}: {error.message}")

    print(f"schemas: {len(schemas)}  examples: {len(list(example_dir.glob('*.example.json')))}")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ETEMAD contract schemas and examples.")
    parser.add_argument("--schemas", type=Path, default=DEFAULT_SCHEMAS)
    parser.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    args = parser.parse_args(argv)

    failures = validate(args.schemas, args.examples)
    if failures:
        print("\nCONTRACT-CHECK: FAIL", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("CONTRACT-CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
