# app/api/auth/me.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import decode_access_token

from app.models.user.user import User
from app.models.organizer.organizer import Organizer
from app.models.membership.organizer_membership import OrganizerMembership
from app.models.membership.system_membership import SystemMembership


router = APIRouter(tags=["Auth"])


@router.get("/me")
def get_me(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    回傳目前登入使用者資訊（Auth Context）
    - 不使用 response_model（避免 Pydantic Union 問題）
    - 回傳 system + organizer memberships（RBAC 使用）
    """

    # -------------------------------------------------
    # 1. 從 Cookie 取 access_token
    # -------------------------------------------------
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # -------------------------------------------------
    # 2. Decode JWT
    # -------------------------------------------------
    payload = decode_access_token(access_token)
    user_uuid = payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=401, detail="Invalid token")

    # -------------------------------------------------
    # 3. 查詢使用者
    # -------------------------------------------------
    current_user = (
        db.query(User)
        .filter(
            User.uuid == user_uuid,
            User.is_deleted == False,
        )
        .first()
    )

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # -------------------------------------------------
    # 4. 查詢 System Memberships
    # -------------------------------------------------
    system_memberships = (
        db.query(SystemMembership)
        .filter(
            SystemMembership.user_uuid == current_user.uuid,
            SystemMembership.is_deleted == False,
            SystemMembership.is_active == True,
            SystemMembership.is_suspended == False,
        )
        .all()
    )

    # -------------------------------------------------
    # 5. 查詢 Organizer Memberships
    # -------------------------------------------------
    organizer_memberships = (
        db.query(OrganizerMembership)
        .join(
            Organizer,
            Organizer.uuid == OrganizerMembership.organizer_uuid,
        )
        .filter(
            OrganizerMembership.user_uuid == current_user.uuid,
            OrganizerMembership.is_deleted == False,
            Organizer.is_deleted == False,
        )
        .all()
    )

    # -------------------------------------------------
    # 6. 組合 memberships（純 dict，避免 Pydantic Union 雷）
    # -------------------------------------------------
    memberships: list[dict] = []

    for m in system_memberships:
        memberships.append({
            "type": "system",
            "role": m.role,
            "status": (
                "suspended"
                if m.is_suspended
                else "active" if m.is_active else "inactive"
            ),
        })

    for m in organizer_memberships:
        memberships.append({
            "type": "organizer",
            "organizer_uuid": str(m.organizer_uuid),
            "organizer_name": m.organizer.name,
            "membership_role": m.role,
        })

    # -------------------------------------------------
    # 7. 回傳 Auth Context
    # -------------------------------------------------
    return {
        "uuid": str(current_user.uuid),
        "email": current_user.email,
        "name": current_user.name,
        "role": "user",
        "memberships": memberships,
    }
