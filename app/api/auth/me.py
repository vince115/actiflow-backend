# app/api/auth/me.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user

from app.schemas.user.user_public import UserPublic
from app.schemas.membership.organizer.organizer_membership_public import OrganizerMembershipPublic

from app.models.membership.organizer_membership import OrganizerMembership
from app.models.organizer.organizer import Organizer

router = APIRouter()


@router.get("/me", response_model=UserPublic)
def get_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    回傳目前登入使用者資訊（UserPublic）
    包含其所屬的 Organizer Memberships
    """

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
            status=m.status,
        )
        for m in memberships
    ]

    return UserPublic(
        uuid=current_user.uuid,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        memberships=memberships_public,
    )
