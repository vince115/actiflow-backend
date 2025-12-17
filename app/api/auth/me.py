# app/api/auth/me.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import decode_access_token

from app.schemas.user.user_public import UserPublic
from app.schemas.membership.organizer.organizer_membership_public import OrganizerMembershipPublic

from app.models.user.user import User
from app.models.membership.organizer_membership import OrganizerMembership
from app.models.organizer.organizer import Organizer

router = APIRouter(tags=["Auth"])

@router.get("/me", response_model=UserPublic)
def get_me(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    回傳目前登入使用者資訊（UserPublic）
    包含其所屬的 Organizer Memberships
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
    # 4. 查詢 Organizer Memberships（你原本的邏輯，完整保留）
    # -------------------------------------------------
    memberships = (
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

    memberships_public = [
        OrganizerMembershipPublic(
            organizer_uuid=m.organizer_uuid,
            organizer_name=m.organizer.name,
            membership_role=m.role,
        )
        for m in memberships
    ]

    # -------------------------------------------------
    # 5. 回傳 UserPublic
    # -------------------------------------------------
    return UserPublic(
        uuid=current_user.uuid,
        email=current_user.email,
        name=current_user.name,
        memberships=memberships_public,
    )