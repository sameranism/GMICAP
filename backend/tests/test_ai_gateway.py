"""S01-022: AI gateway gating, budgets and provenance (no network)."""

from __future__ import annotations

import pytest

from backend.core.ai_gateway import (
    BudgetExceeded,
    FakeProvider,
    Gateway,
    GatewayDisabled,
    ModelBinding,
    UnknownTask,
)

BINDING = ModelBinding(task="translate", provider="fake", model="fake-1", run_budget_usd=0.01)


def _gateway(*, enabled: bool = True, budget: float = 1.0, provider: FakeProvider | None = None) -> Gateway:
    return Gateway(
        bindings={"translate": BINDING},
        providers={"fake": provider or FakeProvider()},
        enabled=enabled,
        monthly_budget_usd=budget,
    )


def test_disabled_gateway_makes_no_call() -> None:
    with pytest.raises(GatewayDisabled):
        _gateway(enabled=False).call("translate", "hello")


def test_unknown_task_is_rejected() -> None:
    with pytest.raises(UnknownTask):
        _gateway().call("narrate", "hello")


def test_call_returns_provenance_and_tracks_spend() -> None:
    gateway = _gateway()
    result = gateway.call("translate", "سلام")
    assert result.text.startswith("fixture-output")
    assert result.model == "fake-1"
    assert len(result.prompt_sha256) == 64
    provenance = result.provenance()
    assert set(provenance) == {
        "task",
        "provider",
        "model",
        "prompt_sha256",
        "request_id",
        "occurred_at",
        "cost_usd",
    }
    assert gateway.spent_usd == pytest.approx(0.001)


def test_monthly_budget_blocks_further_calls() -> None:
    gateway = _gateway(budget=0.002)
    gateway.call("translate", "one")
    gateway.call("translate", "two")
    with pytest.raises(BudgetExceeded):
        gateway.call("translate", "three")


def test_run_budget_is_enforced() -> None:
    expensive = FakeProvider(cost_per_call=0.5)
    gateway = _gateway(provider=expensive, budget=10.0)
    with pytest.raises(BudgetExceeded):
        gateway.call("translate", "hello")


def test_binding_naming_unknown_provider_fails_at_construction() -> None:
    with pytest.raises(ValueError):
        Gateway(
            bindings={"translate": ModelBinding("translate", "missing", "m")},
            providers={"fake": FakeProvider()},
            enabled=True,
        )


def test_prompt_must_be_bounded() -> None:
    with pytest.raises(ValueError):
        _gateway().call("translate", "")
    with pytest.raises(ValueError):
        _gateway().call("translate", "x" * 200_001)
