"""S01-019: the contract layer must accept every example and reject bad data."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.core.contracts import ContractError, validate_payload
from backend.core.settings_service import InMemoryRevisionStore, SettingsService


def test_every_schema_and_example_is_valid(schema_dir: Path, example_dir: Path) -> None:
    sys_path = Path(__file__).resolve().parents[2]
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "validate_contracts", sys_path / "tools" / "validate_contracts.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    failures = module.validate(schema_dir, example_dir)
    assert failures == [], f"contract layer is not clean: {failures}"


def test_all_thirty_contracts_are_present(schema_dir: Path) -> None:
    assert len(sorted(schema_dir.glob("*.schema.json"))) == 30


def test_unknown_contract_is_unavailable() -> None:
    with pytest.raises(ContractError) as caught:
        validate_payload("no_such_contract", {"schema_version": "1.0"})
    assert caught.value.code == "contract_unavailable"


def test_wrong_schema_version_is_rejected(example_dir: Path) -> None:
    payload = json.loads((example_dir / "raw_news.example.json").read_text(encoding="utf-8"))
    payload["schema_version"] = "2.0"
    with pytest.raises(ContractError) as caught:
        validate_payload("raw_news", payload)
    assert caught.value.code == "contract_version"


def test_missing_required_field_is_rejected(example_dir: Path) -> None:
    payload = json.loads((example_dir / "raw_news.example.json").read_text(encoding="utf-8"))
    payload.pop("news_id", None)
    with pytest.raises(ContractError) as caught:
        validate_payload("raw_news", payload)
    assert caught.value.code == "contract_invalid"


def test_unknown_field_is_rejected(example_dir: Path) -> None:
    payload = json.loads((example_dir / "raw_news.example.json").read_text(encoding="utf-8"))
    payload["unexpected_field"] = "x"
    with pytest.raises(ContractError):
        validate_payload("raw_news", payload)


def test_settings_service_accepts_a_real_output_controls_revision(example_dir: Path) -> None:
    payload = json.loads(
        (example_dir / "output_controls.example.json").read_text(encoding="utf-8")
    )
    payload["revision"] = 1
    payload["updated_by"] = "user-001"

    service = SettingsService(
        InMemoryRevisionStore(),
        lambda principal, role, resource_type, resource_id, action: True,
    )
    revision = service.update(
        contract_name="output_controls",
        config_id="controls-main",
        scope="global",
        value=payload,
        expected_revision=0,
        actor_id="user-001",
        actor_role="editor_in_chief",
    )
    assert revision.revision == 1
    assert revision.updated_by == "user-001"
