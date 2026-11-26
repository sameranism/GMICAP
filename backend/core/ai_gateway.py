"""B01/P19 AI gateway: one doorway to every model provider (ADR-006).

Feature code never imports a provider SDK. The gateway enforces the configured
binding, a budget ceiling and provenance, and it is **off by default**: without
an explicit enable plus a configured binding it makes no external call.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Mapping, Protocol
from uuid import uuid4


class GatewayDisabled(RuntimeError):
    """No external model call is allowed in this process."""


class BudgetExceeded(RuntimeError):
    """The per-run or monthly budget would be exceeded."""


class UnknownTask(RuntimeError):
    """No binding exists for the requested task."""


@dataclass(frozen=True)
class ModelBinding:
    task: str
    provider: str
    model: str
    timeout_s: float = 30.0
    run_budget_usd: float = 0.50


@dataclass(frozen=True)
class AiResult:
    text: str
    task: str
    provider: str
    model: str
    prompt_sha256: str
    request_id: str
    occurred_at: str
    cost_usd: float

    def provenance(self) -> dict[str, object]:
        """What gets stored next to a product record; no prompt, no secret."""
        return {
            "task": self.task,
            "provider": self.provider,
            "model": self.model,
            "prompt_sha256": self.prompt_sha256,
            "request_id": self.request_id,
            "occurred_at": self.occurred_at,
            "cost_usd": round(self.cost_usd, 6),
        }


class Provider(Protocol):
    name: str

    def complete(self, prompt: str, *, model: str, timeout_s: float) -> tuple[str, float]:
        """Return (text, cost_usd); implementations must not log the prompt."""


@dataclass
class FakeProvider:
    """Deterministic fixture provider; performs no network I/O."""

    name: str = "fake"
    reply: str = "fixture-output"
    cost_per_call: float = 0.001

    def complete(self, prompt: str, *, model: str, timeout_s: float) -> tuple[str, float]:
        return f"{self.reply}:{model}:{len(prompt)}", self.cost_per_call


@dataclass
class Gateway:
    bindings: Mapping[str, ModelBinding]
    providers: Mapping[str, Provider]
    enabled: bool = False
    monthly_budget_usd: float = 25.0
    _spent_usd: float = field(default=0.0, init=False, repr=False)
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def __post_init__(self) -> None:
        for binding in self.bindings.values():
            if binding.provider not in self.providers:
                raise ValueError(f"binding for {binding.task!r} names unknown provider {binding.provider!r}")

    @property
    def spent_usd(self) -> float:
        with self._lock:
            return round(self._spent_usd, 6)

    def call(self, task: str, prompt: str) -> AiResult:
        if not self.enabled:
            raise GatewayDisabled("AI gateway is disabled; no external call is permitted")
        binding = self.bindings.get(task)
        if binding is None:
            raise UnknownTask(f"no model binding for task {task!r}")
        if not prompt or len(prompt) > 200_000:
            raise ValueError("prompt must be non-empty and bounded")
        provider = self.providers[binding.provider]
        if self.spent_usd >= self.monthly_budget_usd:
            raise BudgetExceeded("monthly AI budget is exhausted")

        text, cost = provider.complete(prompt, model=binding.model, timeout_s=binding.timeout_s)
        if cost > binding.run_budget_usd:
            raise BudgetExceeded("run cost exceeded its binding budget")
        with self._lock:
            self._spent_usd += cost
        return AiResult(
            text=text,
            task=task,
            provider=binding.provider,
            model=binding.model,
            prompt_sha256=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            request_id=str(uuid4()),
            occurred_at=datetime.now(timezone.utc).isoformat(),
            cost_usd=cost,
        )
