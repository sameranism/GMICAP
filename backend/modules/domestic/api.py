"""P05/S02-005 domestic HTTP surface.

The router is built with injected dependencies so the module never imports the
application layer: authorization and audit stay in ``backend.app``, this file only
shapes the domestic endpoints.
"""

from __future__ import annotations

from typing import Any, Callable
from uuid import uuid4

from fastapi import APIRouter, Depends, Request

Authorize = Callable[..., None]


def _correlation_id(request: Request) -> str:
    return request.headers.get("X-Correlation-ID", "").strip() or str(uuid4())


def build_router(
    *,
    services_dep: Callable[..., Any],
    principal_dep: Callable[..., Any],
    authorize: Authorize,
) -> APIRouter:
    """Return the domestic ingest router; mounted under ``/v1`` by the app."""
    router = APIRouter(prefix="/ingest", tags=["ingest"])

    @router.post("/{source_id}/poll")
    def poll_source(
        source_id: str,
        request: Request,
        principal: Any = Depends(principal_dep),
        services: Any = Depends(services_dep),
    ) -> dict[str, Any]:
        """Poll one domestic source with the configured transport (fixture by default)."""
        authorize(
            services,
            principal,
            resource_type="source_registry",
            resource_id=source_id,
            action="poll",
            correlation_id=_correlation_id(request),
        )
        result = services.pipeline.poll_source(source_id)
        return {
            "schema_version": "1.0",
            "source_id": result.source_id,
            "status": result.status,
            "collected": result.collected,
            "error": result.error,
            "state": dict(result.state),
        }

    @router.get("/{source_id}/poll-state")
    def poll_state(
        source_id: str,
        request: Request,
        principal: Any = Depends(principal_dep),
        services: Any = Depends(services_dep),
    ) -> dict[str, Any]:
        """Current poll state for one source (no secret, no credentials)."""
        authorize(
            services,
            principal,
            resource_type="source_registry",
            resource_id=source_id,
            action="read",
            correlation_id=_correlation_id(request),
        )
        try:
            services.sources.get(source_id)
        except Exception:  # noqa: BLE001 - unknown source is a plain 404 at the app layer
            return {"schema_version": "1.0", "source_id": source_id, "known": False}
        state = services.pipeline.poll_states.get_or_create(source_id)
        return {
            "schema_version": "1.0",
            "source_id": source_id,
            "known": True,
            "state": state.as_dict(),
        }

    return router
