# app/core/dependencies.py ← FastAPI DI 注入元件

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from dataclasses import dataclass
from typing import Optional

from app.core.db import get_db
from app.core.jwt import decode_access_token

from app.models.user.user import User
from app.models.organizer.organizer import Organizer
from app.models.membership.organizer_membership import OrganizerMembership

# ============================================================
# Identity（新核心）
# ============================================================
@dataclass
class Identity:
    user: Optional[User] = None
    organizer: Optional[Organizer] = None
    membership: Optional[OrganizerMembership] = None

# 核心入口（全系統唯一）
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
    organizer_uuid = payload.get("organizer_uuid")

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
# Guard 1：Super Admin
# ============================================================
def require_super_admin(
    identity: Identity = Depends(get_current_identity),
):
    if identity.user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin permission required",
        )

    return None

# ============================================================
# Guard 2：Organizer Admin / Owner（寫入權限）
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
# Guard 3：Organizer Member（讀取權限）
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


