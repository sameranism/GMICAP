"""B01/P01 API errors with safe, correlated response bodies.

Call ``install_exception_handlers(app)`` when composing an API. Error bodies
are deliberately independent of the event and workflow wire contracts.
"""

from __future__ import annotations

import logging
import re
import traceback
from enum import Enum
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

_LOG = logging.getLogger(__name__)
_CORRELATION_ID = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


class ErrorCode(str, Enum):
    CONTRACT_INVALID = "contract_invalid"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    METHOD_NOT_ALLOWED = "method_not_allowed"
    CONFLICT = "conflict"
    INVALID_STATE = "invalid_state"
    RATE_LIMITED = "rate_limited"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    INTERNAL_ERROR = "internal_error"


_STATUS = {
    ErrorCode.CONTRACT_INVALID: 400,
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.METHOD_NOT_ALLOWED: 405,
    ErrorCode.CONFLICT: 409,
    ErrorCode.INVALID_STATE: 422,
    ErrorCode.RATE_LIMITED: 429,
    ErrorCode.DEPENDENCY_UNAVAILABLE: 503,
    ErrorCode.INTERNAL_ERROR: 500,
}

_SAFE_MESSAGES = {
    ErrorCode.CONTRACT_INVALID: "Invalid request contract",
    ErrorCode.UNAUTHORIZED: "Authentication required",
    ErrorCode.FORBIDDEN: "Access denied",
    ErrorCode.NOT_FOUND: "Not found",
    ErrorCode.METHOD_NOT_ALLOWED: "Method not allowed",
    ErrorCode.CONFLICT: "Revision conflict",
    ErrorCode.INVALID_STATE: "Invalid state",
    ErrorCode.RATE_LIMITED: "Rate limit exceeded",
    ErrorCode.DEPENDENCY_UNAVAILABLE: "Service unavailable",
    ErrorCode.INTERNAL_ERROR: "Internal server error",
}


class APIError(Exception):
    """A public error code; private causes belong only in safe server logs.

    ``details`` must be a deliberately public mapping. Server errors always
    discard it and use a fixed message, even when the caller passes one.
    """

    def __init__(
        self,
        code: ErrorCode,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        if not isinstance(code, ErrorCode):
            raise TypeError("code must be an ErrorCode")
        self.code = code
        self.details = None if _STATUS[code] >= 500 else details
        super().__init__(_SAFE_MESSAGES[code])


def correlation_id_for(request: Request) -> str:
    """Accept a short safe request ID or create one without echoing bad input."""
    supplied = request.headers.get("X-Correlation-ID", "")
    return supplied if _CORRELATION_ID.fullmatch(supplied) else str(uuid4())


def error_response(
    code: ErrorCode,
    correlation_id: str,
    *,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    """Build the common response envelope; never expose server internals."""
    if not _CORRELATION_ID.fullmatch(correlation_id):
        raise ValueError("Invalid correlation ID")
    status = _STATUS[code]
    return JSONResponse(
        status_code=status,
        content={
            "code": code.value,
            "message": _SAFE_MESSAGES[code],
            "correlation_id": correlation_id,
            "details": details if status < 500 else None,
        },
        headers={"X-Correlation-ID": correlation_id},
    )


def install_exception_handlers(app: FastAPI) -> None:
    """Use one stable envelope for known errors and unexpected failures."""

    @app.exception_handler(APIError)
    async def api_error(request: Request, exc: APIError) -> JSONResponse:
        return error_response(
            exc.code, correlation_id_for(request), details=exc.details
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(
        request: Request, _exc: RequestValidationError
    ) -> JSONResponse:
        # Framework validation details may contain submitted secret values.
        return error_response(ErrorCode.CONTRACT_INVALID, correlation_id_for(request))

    @app.exception_handler(StarletteHTTPException)
    async def http_error(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        code = {
            400: ErrorCode.CONTRACT_INVALID,
            401: ErrorCode.UNAUTHORIZED,
            403: ErrorCode.FORBIDDEN,
            404: ErrorCode.NOT_FOUND,
            405: ErrorCode.METHOD_NOT_ALLOWED,
            409: ErrorCode.CONFLICT,
            422: ErrorCode.INVALID_STATE,
            429: ErrorCode.RATE_LIMITED,
            503: ErrorCode.DEPENDENCY_UNAVAILABLE,
        }.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
        return error_response(code, correlation_id_for(request))

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception) -> JSONResponse:
        correlation_id = correlation_id_for(request)
        frames = traceback.extract_tb(exc.__traceback__)
        origin = frames[-1] if frames else None
        _LOG.error(
            "Unexpected API failure correlation_id=%s type=%s origin=%s:%s",
            correlation_id,
            type(exc).__name__,
            origin.name if origin else "unknown",
            origin.lineno if origin else 0,
        )
        return error_response(ErrorCode.INTERNAL_ERROR, correlation_id)
