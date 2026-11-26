"""B01/P01 API composition with an explicitly local synthetic-news adapter.

The application installs exactly one set of exception handlers (``errors.py``)
and one versioned router. A local demo router exists only when both
``ETEMAD_ENV=local`` and ``ETEMAD_DEMO_MODE=1`` are set.
"""

from __future__ import annotations

import os

from fastapi import FastAPI

from backend.app.api_router import router
from backend.app.dependencies import Services, build_services
from backend.core.errors import install_exception_handlers


def create_app(
    *,
    expose_openapi: bool | None = None,
    services: Services | None = None,
) -> FastAPI:
    if expose_openapi is None:
        expose_openapi = os.getenv("ETEMAD_EXPOSE_OPENAPI") == "1"

    app = FastAPI(
        title="ETEMAD API",
        version="0.1.0",
        docs_url="/docs" if expose_openapi else None,
        redoc_url=None,
        openapi_url="/openapi.json" if expose_openapi else None,
    )

    app.state.services = services if services is not None else build_services()
    install_exception_handlers(app)
    app.include_router(router)

    @app.get("/health", include_in_schema=False)
    async def liveness() -> dict[str, str]:
        """Process liveness only; dependency state lives at ``/v1/health``."""
        return {"status": "ok"}

    if os.getenv("ETEMAD_ENV") == "local" and os.getenv("ETEMAD_DEMO_MODE") == "1":
        from backend.app.demo_news import router as demo_router

        app.include_router(demo_router)

    return app


app = create_app()
