#!/usr/bin/env python3
"""Offline validation of ETEMAD frozen v1.0 JSON Schemas and example records."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError


def validate_contracts(contracts_dir: Path) -> tuple[int, int]:
    schemas_dir = contracts_dir / "schemas"
    examples_dir = contracts_dir / "examples"
    schemas = sorted(schemas_dir.glob("*.schema.json"))
    examples = sorted(examples_dir.glob("*.example.json"))
    errors = 0
    checked = 0
    if not schemas:
        print(f"FAIL: no schemas found in {schemas_dir}")
        return (0, 1)
    schema_names = {p.name.removesuffix(".schema.json") for p in schemas}
    example_names = {p.name.removesuffix(".example.json") for p in examples}
    for name in sorted(schema_names ^ example_names):
        print(f"FAIL {name}: missing {'schema' if name in example_names else 'example'}")
        errors += 1
    for schema_file in schemas:
        name = schema_file.name.removesuffix(".schema.json")
        example_file = examples_dir / f"{name}.example.json"
        try:
            schema = json.loads(schema_file.read_text(encoding="utf-8-sig"))
            if not isinstance(schema, dict):
                raise ValueError("schema must be a JSON object")
            if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                raise ValueError("not JSON Schema Draft 2020-12")
            Draft202012Validator.check_schema(schema)
            if not example_file.exists():
                continue  # already counted as missing
            example = json.loads(example_file.read_text(encoding="utf-8-sig"))
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            violations = sorted(validator.iter_errors(example), key=lambda error: str(error.json_path))
            checked += 1
            if violations:
                errors += len(violations)
                for violation in violations:
                    print(f"FAIL {name} at {violation.json_path}: {violation.message}")
            else:
                print(f"PASS {name}")
        except (OSError, ValueError, json.JSONDecodeError, SchemaError) as exc:
            errors += 1
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    print(f"SUMMARY: {checked} examples validated; {len(schemas)} schemas; {errors} errors")
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--contracts-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "source" / "contracts",
        help="Path containing schemas/ and examples/ directories",
    )
    args = parser.parse_args()
    _checked, errors = validate_contracts(args.contracts_dir)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
