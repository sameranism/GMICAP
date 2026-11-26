"""B01/P28 server-side access decision; no role implies a broad grant."""

from collections.abc import Callable
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

Role = str
GrantLookup = Callable[[str, Role, str, str, str], bool]
_ROLES = frozenset({"owner", "editor_in_chief", "staff"})


def decide_access(
    principal_id: str,
    role: Role,
    resource_type: str,
    resource_id: str,
    action: str,
    grant_lookup: GrantLookup,
    *,
    classification: str = "internal",
    request_id: str | None = None,
) -> dict[str, object]:
    """Return the access_decision v1.0 shape.

    The caller must obtain role and classification from trusted server state,
    never request parameters. Grant lookup must use authoritative P28 storage.
    """
    allowed = False
    reason = "DENY_DEFAULT"
    if not all((principal_id, resource_type, resource_id, action)) or role not in _ROLES:
        reason = "INVALID_CONTEXT"
    elif classification == "executive_private" or resource_type == "private_report":
        if role != "editor_in_chief" or action != "read" or resource_type != "private_report":
            reason = "EXECUTIVE_PRIVATE"
        elif grant_lookup(principal_id, role, resource_type, resource_id, action):
            allowed, reason = True, "ROLE_ALLOWED"
        else:
            reason = "GRANT_REQUIRED"
    elif grant_lookup(principal_id, role, resource_type, resource_id, action):
        allowed, reason = True, "ROLE_ALLOWED"

    return {
        "schema_version": "1.0",
        "request_id": request_id or str(uuid4()),
        "principal_id": principal_id or "anonymous",
        "role": role or "unknown",
        "resource_type": resource_type or "unknown",
        "resource_id": resource_id or "unknown",
        "action": action or "unknown",
        "allowed": allowed,
        "reason_code": reason,
        "decided_at": datetime.now(timezone.utc).isoformat(),
    }


def require_access(decision: dict[str, object]) -> None:
    """Reject a direct API request; conceal private object existence."""
    if decision.get("allowed") is True:
        return
    private = decision.get("resource_type") == "private_report"
    raise HTTPException(status_code=404 if private else 403, detail="Access denied")
