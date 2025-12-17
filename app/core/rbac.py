# app/core/rbac.py  ← Role-based access control 工具

from fastapi import Depends, HTTPException, status
from uuid import UUID
from functools import wraps

from sqlalchemy.orm import Session
from typing import List, Callable

from app.core.db import get_db
from app.core.dependencies import get_current_identity
from app.crud.membership.crud_system_membership import get_system_membership
from app.crud.membership.crud_organizer_membership import get_organizer_membership


# ============================================================
# SUPER ADMIN
# ============================================================
def require_super_admin(func: Callable):
    @wraps(func)
    def wrapper(*args, db: Session = Depends(get_db), current_user=Depends(get_current_identity), **kwargs):
        if current_user.role != "super_admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Super admin role required"
            )
        return func(*args, db=db, current_user=current_user, **kwargs)

    return wrapper

# ============================================================
# ORGANIZER ROLE
# ============================================================
def require_organizer_member(
    db: Session,
    user,
    organizer_uuid,
    allowed_roles: list[str] | None = None,
):
    """
    檢查使用者是否為 organizer 成員
    預設允許 owner / admin / member
    """

    if allowed_roles is None:
        allowed_roles = ["owner", "admin", "member"]

    membership = get_organizer_membership(db, user.uuid, organizer_uuid)

    if (
        not membership
        or membership.is_deleted
        or not membership.is_active
        or membership.role not in allowed_roles
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Organizer role required: {allowed_roles}",
        )

    return membership

# ============================================================
# PLATFORM ROLE (SystemMembership)
# ------------------------------------------------------------
# system_admin / support / auditor
# ============================================================
def require_platform_role(required_role: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, db: Session = Depends(get_db), current_user=Depends(get_current_identity), **kwargs):

            membership = get_system_membership(db, current_user.uuid)

            if not membership or membership.is_deleted or not membership.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Platform membership required"
                )

            if membership.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Platform role '{required_role}' required"
                )

            return func(*args, db=db, current_user=current_user, system_membership=membership, **kwargs)

        return wrapper

    return decorator


# ============================================================
# ORGANIZER ROLE
# ------------------------------------------------------------
# owner / admin / member
# 需要綁定 organizer_uuid 來比對 membership
# ============================================================
def require_organizer_role(allowed_roles: List[str]):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(
            organizer_uuid: str,
            *args,
            db: Session = Depends(get_db),
            current_user=Depends(get_current_identity),
            **kwargs,
        ):

            membership = get_organizer_membership(db, current_user.uuid, organizer_uuid)

            if (
                not membership
                or membership.is_deleted
                or not membership.is_active
                or membership.role not in allowed_roles
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Organizer role required: {allowed_roles}"
                )

            return func(
                organizer_uuid,
                *args,
                db=db,
                current_user=current_user,
                organizer_membership=membership,
                **kwargs
            )

        return wrapper

    return decorator
