# app/core/dependencies.py
# FastAPI DI 注入元件（安全升級版 / 向後相容）

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID

from app.crud.membership.crud_system_membership import get_system_membership

from app.core.db import get_db
from app.core.jwt import decode_access_token

from app.models.user.user import User
from app.models.organizer.organizer import Organizer
from app.models.membership.organizer_membership import OrganizerMembership

# ============================================================
# Identity（Base Identity，保持不變）
# ============================================================
@dataclass
class Identity:
    """
    Base Identity：
    - user：一定存在
    - organizer / membership：僅在 token 帶 organizer_uuid 時存在（legacy）
    """
    user: Optional[User] = None
    organizer: Optional[Organizer] = None
    membership: Optional[OrganizerMembership] = None


# ============================================================
# 核心入口（全系統唯一，保持原行為）
# ============================================================
def get_current_identity(
    request: Request,
    db: Session = Depends(get_db),
) -> Identity:
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing",
        )

    payload = decode_access_token(token)

    user_uuid = payload.get("sub")
    organizer_uuid = payload.get("organizer_uuid")  # legacy 行為，保留

    if not user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = (
        db.query(User)
        .filter(
            User.uuid == user_uuid,
            User.is_deleted == False,
            User.is_active == True,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    organizer = None
    membership = None

    # legacy：token 帶 organizer_uuid 才會填
    if organizer_uuid:
        organizer = (
            db.query(Organizer)
            .filter(
                Organizer.uuid == organizer_uuid,
                Organizer.is_deleted == False,
            )
            .first()
        )

        if organizer:
            membership = (
                db.query(OrganizerMembership)
                .filter(
                    OrganizerMembership.organizer_uuid == organizer_uuid,
                    OrganizerMembership.user_uuid == user.uuid,
                    OrganizerMembership.is_deleted == False,
                )
                .first()
            )

    return Identity(
        user=user,
        organizer=organizer,
        membership=membership,
    )


# ============================================================
# 🆕 Organizer Context Resolver（Canonical API 專用）
# ============================================================
def resolve_current_organizer_context(
    request: Request,
    identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db),
) -> OrganizerMembership:
    """
    Canonical Organizer Context Resolver

    使用時機：
    - /organizers/organizer/*
    - 不從 token 取 organizer_uuid
    - 從 DB memberships 推導 organizer context

    規則：
    1. Header X-Organizer-UUID（未來支援）
    2. 僅有一個 organizer → 自動選
    3. 多個 organizer → 明確拒絕（避免誤操作）
    """

    memberships: List[OrganizerMembership] = (
        db.query(OrganizerMembership)
        .filter(
            OrganizerMembership.user_uuid == identity.user.uuid,
            OrganizerMembership.is_deleted == False,
        )
        .all()
    )

    if not memberships:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer membership required",
        )

    # 🚧 未來預留：Header 指定 organizer
    header_org_uuid = request.headers.get("X-Organizer-UUID")
    if header_org_uuid:
        try:
            org_uuid = UUID(header_org_uuid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid X-Organizer-UUID header",
            )

        membership = next(
            (m for m in memberships if m.organizer_uuid == org_uuid),
            None,
        )

        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No access to this organizer",
            )

        return membership

    # 目前安全策略：只允許單 organizer
    if len(memberships) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Multiple organizers detected. Organizer context required.",
        )

    return memberships[0]


# ============================================================
# Guard 1：Super Admin（保持不變）
# ============================================================
def require_super_admin(
    identity: Identity = Depends(get_current_identity),
    db: Session = Depends(get_db),
):
    system_membership = get_system_membership(db, identity.user.uuid)

    if not system_membership or system_membership.role not in {"admin", "super_admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="System admin permission required",
        )

    return system_membership



# ============================================================
# Guard 2（Legacy）：Organizer Admin / Owner（token-based）
# 用於 /organizers/{uuid}/* 舊 API
# ============================================================
def require_organizer_admin(
    identity: Identity = Depends(get_current_identity),
) -> OrganizerMembership:
    if not identity.membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer access required",
        )

    if identity.membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer admin permission required",
        )

    return identity.membership


# ============================================================
# Guard 3（Legacy）：Organizer Member（token-based）
# ============================================================
def require_organizer_member(
    identity: Identity = Depends(get_current_identity),
) -> OrganizerMembership:
    if not identity.membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer member permission required",
        )

    return identity.membership


# ============================================================
# 🆕 Guard 4（Canonical）：Organizer Admin / Owner
# 用於 /organizers/organizer/* 新 API
# ============================================================
def require_current_organizer_admin(
    membership: OrganizerMembership = Depends(
        resolve_current_organizer_context
    ),
) -> OrganizerMembership:
    if membership.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organizer admin permission required",
        )

    return membership


# ============================================================
# 🆕 Guard 5（Canonical）：Organizer Member
# ============================================================
def require_current_organizer_member(
    membership: OrganizerMembership = Depends(
        resolve_current_organizer_context
    ),
) -> OrganizerMembership:
    return membership
