"""B01/P01 versioned API router (``/v1``).

Every privileged route resolves the principal from a signed bearer token and
records an audit entry. Route code never decides access on its own: it asks
``permissions.decide_access`` with a grant lookup from the services container.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from backend.app.dependencies import Services, get_services
from backend.core.auth import Principal, SessionInvalid, bearer_token, verify_session
from backend.core.errors import APIError, ErrorCode
from backend.core.health import health_report
from backend.core.permissions import decide_access, require_access
from backend.modules.domestic.api import build_router as build_domestic_router

router = APIRouter(prefix="/v1")


class SourceInput(BaseModel):
    source_id: str = Field(min_length=1, max_length=64)
    site_url: str = Field(min_length=1, max_length=2048)
    feed_url: str | None = Field(default=None, max_length=2048)
    country: str = Field(min_length=2, max_length=8)
    language: str = Field(min_length=2, max_length=16)
    stream: str = Field(min_length=1, max_length=16)
    license_scope: str = Field(min_length=1, max_length=32)
    enabled: bool = False


class ConfigUpdate(BaseModel):
    value: dict[str, Any]
    scope: str = Field(default="global", max_length=32)
    expected_revision: int = Field(ge=0)


def current_principal(request: Request, services: Services = Depends(get_services)) -> Principal:
    token = bearer_token(request.headers.get("Authorization"))
    if not token:
        raise APIError(ErrorCode.UNAUTHORIZED)
    try:
        return verify_session(token, services.session_key)
    except SessionInvalid as exc:
        raise APIError(ErrorCode.UNAUTHORIZED) from exc


def _correlation_id(request: Request) -> str:
    """Use the caller's id when supplied, otherwise create one (never empty)."""
    supplied = request.headers.get("X-Correlation-ID", "").strip()
    return supplied or str(uuid4())


def _authorize(
    services: Services,
    principal: Principal,
    *,
    resource_type: str,
    resource_id: str,
    action: str,
    correlation_id: str,
) -> None:
    decision = decide_access(
        principal.subject_id,
        principal.role,
        resource_type,
        resource_id,
        action,
        services.grants,
        request_id=correlation_id,
    )
    services.auditor.record(
        action=f"{resource_type}.{action}",
        actor_id=principal.subject_id,
        actor_role=principal.role,
        resource_type=resource_type,
        resource_id=resource_id,
        decision=str(decision["reason_code"]),
        correlation_id=correlation_id,
        details={"allowed": decision["allowed"]},
    )
    require_access(decision)


@router.get("/health", tags=["ops"])
def health(services: Services = Depends(get_services)) -> dict[str, Any]:
    """Liveness plus dependency configuration; no secrets, no credentials."""
    return health_report(databases=services.registry)


@router.get("/sources", tags=["sources"])
def list_sources(
    request: Request,
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="source_registry",
        resource_id="default",
        action="read",
        correlation_id=correlation_id,
    )
    return {"schema_version": "1.0", "sources": services.sources.list()}


@router.post("/sources", status_code=201, tags=["sources"])
def register_source(
    payload: SourceInput,
    request: Request,
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="source_registry",
        resource_id=payload.source_id,
        action="write",
        correlation_id=correlation_id,
    )
    try:
        source = services.sources.register(payload.model_dump())
    except Exception as exc:  # noqa: BLE001 - contract errors become 400
        raise APIError(ErrorCode.CONTRACT_INVALID) from exc
    return {"schema_version": "1.0", "source": source}


@router.get("/config/{contract_name}/{config_id}", tags=["config"])
def read_config(
    contract_name: str,
    config_id: str,
    request: Request,
    scope: str = "global",
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="config",
        resource_id=f"{contract_name}:{scope}:{config_id}",
        action="read",
        correlation_id=correlation_id,
    )
    try:
        revision = services.settings.get_latest(contract_name, config_id, scope)
    except Exception as exc:  # noqa: BLE001 - unknown contract must be a 400, not a 500
        raise APIError(ErrorCode.CONTRACT_INVALID) from exc
    if revision is None:
        raise APIError(ErrorCode.NOT_FOUND)
    return {
        "schema_version": "1.0",
        "contract_name": contract_name,
        "config_id": config_id,
        "scope": scope,
        "revision": revision.revision,
        "value": revision.value,
    }


@router.put("/config/{contract_name}/{config_id}", tags=["config"])
def update_config(
    contract_name: str,
    config_id: str,
    payload: ConfigUpdate,
    request: Request,
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="config",
        resource_id=f"{contract_name}:{payload.scope}:{config_id}",
        action="update",
        correlation_id=correlation_id,
    )
    try:
        revision = services.settings.update(
            contract_name=contract_name,
            config_id=config_id,
            scope=payload.scope,
            value=payload.value,
            expected_revision=payload.expected_revision,
            actor_id=principal.subject_id,
            actor_role=principal.role,
        )
    except APIError:
        raise
    except Exception as exc:  # noqa: BLE001 - surfaced as a safe 400
        raise APIError(ErrorCode.CONTRACT_INVALID) from exc
    return {
        "schema_version": "1.0",
        "contract_name": contract_name,
        "config_id": config_id,
        "scope": payload.scope,
        "revision": revision.revision,
    }


@router.get("/news", tags=["news"])
def news_feed(
    request: Request,
    limit: int = 50,
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    """Newsroom feed built from real contract records (no synthetic data)."""
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="newsroom",
        resource_id="feed",
        action="read",
        correlation_id=correlation_id,
    )
    services.pipeline.process_pending()
    items = services.pipeline.feed(limit=max(1, min(limit, 200)))
    return {"schema_version": "1.0", "count": len(items), "items": items}


@router.get("/news/{news_id}", tags=["news"])
def news_item(
    news_id: str,
    request: Request,
    principal: Principal = Depends(current_principal),
    services: Services = Depends(get_services),
) -> dict[str, Any]:
    correlation_id = _correlation_id(request)
    _authorize(
        services,
        principal,
        resource_type="newsroom",
        resource_id=news_id,
        action="read",
        correlation_id=correlation_id,
    )
    item = services.pipeline.item(news_id)
    if item is None:
        raise APIError(ErrorCode.NOT_FOUND)
    return {"schema_version": "1.0", **item}


# Domestic ingest routes live in the package module; the app supplies auth and audit.
router.include_router(
    build_domestic_router(
        services_dep=get_services,
        principal_dep=current_principal,
        authorize=_authorize,
    )
)
