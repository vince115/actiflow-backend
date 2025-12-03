# app/core/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import decode_access_token
from app.crud.user import get_user_by_uuid
from app.crud.super_admin import get_super_admin_by_uuid
from app.crud.organizer_membership import get_membership
from app.crud.system_membership import get_system_membership


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ============================================================
# Helper - Token Validation
# ============================================================
def _decode_token(token: str):
    try:
        return decode_access_token(token)
    except Exception:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ============================================================
# Current User (Normal User)
# ============================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = _decode_token(token)

    user_uuid = payload.get("sub")
    if not user_uuid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing user identity")

    user = get_user_by_uuid(db, user_uuid)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")

    if user.is_deleted or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User inactive or deleted")

    return user


# ============================================================
# Super Admin（平台 root）
# ============================================================
def get_current_super_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = _decode_token(token)

    if payload.get("role") != "super_admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Super admin permission required")

    admin_uuid = payload.get("sub")
    if not admin_uuid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing admin identity")

    admin = get_super_admin_by_uuid(db, admin_uuid)
    if not admin or admin.is_deleted or not admin.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Super admin inactive or deleted")

    return admin


# ============================================================
# Platform-level Roles (SystemMembership)
# ============================================================
def _get_platform_membership(user, db: Session):
    membership = get_system_membership(db, user.uuid)
    if not membership or membership.is_deleted or not membership.is_active:
        return None
    return membership


def get_current_platform_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    membership = _get_platform_membership(user, db)

    if not membership:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Platform permission required")

    return membership


def get_current_system_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    membership = _get_platform_membership(user, db)

    if not membership or membership.role != "system_admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "System admin permission required")

    return membership


def get_current_support(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    membership = _get_platform_membership(user, db)

    if not membership or membership.role not in ["system_admin", "support"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Support permission required")

    return membership


def get_current_auditor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    membership = _get_platform_membership(user, db)

    if not membership or membership.role not in ["system_admin", "auditor"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditor permission required")

    return membership


# ============================================================
# Organizer Owner/Admin (per Organizer)
# ============================================================
def get_current_organizer_admin_factory():
    """
    用法：
    @router.get("/organizers/{organizer_uuid}/xxx")
    def xxx(
        organizer_uuid: str,
        admin = Depends(get_current_organizer_admin_factory())
    )
    """
    def dependency(
        organizer_uuid: str,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
    ):
        membership = get_membership(db, current_user.uuid, organizer_uuid)

        if (
            not membership
            or membership.is_deleted
            or not membership.is_active
            or membership.role not in ["owner", "admin"]
        ):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Organizer owner/admin permission required"
            )

        return membership

    return dependency
