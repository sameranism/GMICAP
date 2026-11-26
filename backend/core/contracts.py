"""B01/P01 read-only validation of versioned wire contracts."""

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

_SCHEMA_DIR = Path(__file__).resolve().parents[2] / "source" / "contracts" / "schemas"
_SCHEMA_NAME = re.compile(r"^[a-z][a-z0-9_]*$")
_VERSION = "1.0"


class ContractError(ValueError):
    """A boundary validation failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


@lru_cache(maxsize=64)
def _validator(schema_name: str) -> Draft202012Validator:
    if not _SCHEMA_NAME.fullmatch(schema_name):
        raise ContractError("contract_unknown", "Unknown contract")
    path = _SCHEMA_DIR / f"{schema_name}.schema.json"
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError("contract_unavailable", "Contract cannot be loaded") from exc
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ContractError("contract_invalid", "Contract schema is invalid") from exc
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_payload(schema_name: str, payload: Mapping[str, Any]) -> None:
    """Reject invalid data without coercing or changing the supplied record."""
    if not isinstance(payload, Mapping):
        raise ContractError("contract_invalid", "Payload must be an object")
    if payload.get("schema_version") != _VERSION:
        raise ContractError("contract_version", "Unsupported contract version")
    validator = _validator(schema_name)
    error = next(validator.iter_errors(payload), None)
    if error is not None:
        location = "/".join(str(part) for part in error.absolute_path)
        raise ContractError("contract_invalid", f"Invalid payload at {location or '/'}") from error
