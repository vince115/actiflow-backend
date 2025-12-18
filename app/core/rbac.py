# app/core/rbac.py

from typing import Iterable, Callable, Optional
from fastapi import Depends, HTTPException, status

from app.api.auth.dependencies import get_current_user


# =====================================================
# Internal helpers (pure logic)
# =====================================================

def _get_system_memberships(user: dict) -> list[dict]:
    return [
        m for m in user.get("memberships", [])
        if m.get("type") == "system"
    ]


def _get_organizer_memberships(user: dict, organizer_uuid: Optional[str] = None) -> list[dict]:
    memberships = [
        m for m in user.get("memberships", [])
        if m.get("type") == "organizer"
    ]

    if organizer_uuid:
        memberships = [
            m for m in memberships
            if m.get("organizer_uuid") == organizer_uuid
        ]

    return memberships


def _system_role_allowed(
    user: dict,
    allowed_roles: Iterable[str],
) -> bool:
    for m in _get_system_memberships(user):
        if m.get("status") != "active":
            continue
        if m.get("role") in allowed_roles:
            return True
    return False


def _organizer_role_allowed(
    user: dict,
    organizer_uuid: str,
    allowed_roles: Iterable[str],
) -> bool:
    for m in _get_organizer_memberships(user, organizer_uuid):
        if m.get("membership_role") in allowed_roles:
            return True
    return False


# =====================================================
# Public dependencies (FastAPI friendly)
# =====================================================

def require_system_role(
    role: str | Iterable[str],
) -> Callable:
    """
    Usage:
        Depends(require_system_role("admin"))
        Depends(require_system_role(["admin", "support"]))
    """
    allowed_roles = {role} if isinstance(role, str) else set(role)

    def dependency(
        current_user: dict = Depends(get_current_user),
    ):
        if not _system_role_allowed(current_user, allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient system permissions",
            )
        return current_user

    return dependency


def require_organizer_role(
    role: str | Iterable[str],
):
    """
    Organizer-level RBAC.
    Organizer UUID must be passed from path params.
    """
    allowed_roles = {role} if isinstance(role, str) else set(role)

    def dependency(
        organizer_uuid: str,
        current_user: dict = Depends(get_current_user),
    ):
        if not _organizer_role_allowed(current_user, organizer_uuid, allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient organizer permissions",
            )
        return current_user

    return dependency
