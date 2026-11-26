"""B01 API composition with an explicitly local synthetic-news adapter."""

import logging
import os
import re
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

_LOG = logging.getLogger(__name__)
_CORRELATION_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def create_app(*, expose_openapi: bool | None = None) -> FastAPI:
    if expose_openapi is None:
        expose_openapi = os.getenv("ETEMAD_EXPOSE_OPENAPI") == "1"

    app = FastAPI(
        title="ETEMAD API",
        version="0.1.0",
        docs_url="/docs" if expose_openapi else None,
        redoc_url=None,
        openapi_url="/openapi.json" if expose_openapi else None,
    )

    @app.get("/health", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    if os.getenv("ETEMAD_ENV") == "local" and os.getenv("ETEMAD_DEMO_MODE") == "1":
        from backend.app.demo_news import router as demo_router

        app.include_router(demo_router)

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, exc: Exception) -> JSONResponse:
        supplied = request.headers.get("X-Correlation-ID", "")
        correlation_id = supplied if _CORRELATION_ID.fullmatch(supplied) else str(uuid4())
        _LOG.error("Unhandled API error correlation_id=%s", correlation_id)
        return JSONResponse(
            status_code=500,
            content={
                "code": "internal_error",
                "message": "Internal server error",
                "correlation_id": correlation_id,
                "details": None,
            },
            headers={"X-Correlation-ID": correlation_id},
        )

    return app


app = create_app()
