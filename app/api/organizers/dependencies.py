#   app/api/organizers/dependencies.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.models.user.user import User
from app.models.organizer.organizer import Organizer
from app.models.membership.organizer_membership import OrganizerMembership

# 基礎：Super Admin Guard
def require_super_admin(
    identity = Depends(get_current_identity),
):
    """
    僅允許 super_admin 存取
    """
    user: User | None = identity.user

    if not user or user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin only",
        )

    # 不回傳 user，避免污染 router
    return None

# Organizer Membership Guard（共用）
def get_organizer_membership(
    organizer_uuid: str,
    db: Session,
    user_uuid: str,
) -> OrganizerMembership | None:
    return (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.organizer_uuid == organizer_uuid,
            OrganizerMembership.user_uuid == user_uuid,
            OrganizerMembership.is_deleted == False,
        )
        .first()
    )

# Organizer Admin / Owner Guard（最常用）
def require_organizer_admin(
    db: Session = Depends(get_db),
    identity = Depends(get_current_identity),
):
    """
    Organizer admin / owner 才能通過
    - organizer_uuid 來自 identity（不是 URL）
    """
    user: User | None = identity.user
    organizer: Organizer | None = identity.organizer

    if not user or not organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer access required",
        )

    membership = get_organizer_membership(
        organizer_uuid=organizer.uuid,
        db=db,
        user_uuid=user.uuid,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an organizer member",
        )

    if membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer admin only",
        )

    return membership

# Organizer 一般成員（read-only）
def require_organizer_member(
    db: Session = Depends(get_db),
    identity = Depends(get_current_identity),
):
    """
    任一 organizer member（含 staff）
    """
    user: User | None = identity.user
    organizer: Organizer | None = identity.organizer

    if not user or not organizer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer access required",
        )

    membership = get_organizer_membership(
        organizer_uuid=organizer.uuid,
        db=db,
        user_uuid=user.uuid,
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an organizer member",
        )

    return membership

