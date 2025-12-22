# app/api/organizers/organizer/profile.py
# Organizer 個人資料（Profile / Me）API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.schemas.organizer.organizer_response import OrganizerResponse

from app.crud.organizer.crud_organizer import organizer_crud
from app.crud.membership.crud_organizer_membership import (
    get_membership_by_user_and_organizer,
)
from app.crud.membership.crud_system_membership import get_system_membership


router = APIRouter(
    prefix="/me",
    tags=["Organizer Profile"],
)


# -------------------------------------------------------------------
# Get current organizer profile
# owner / admin / system_admin
# -------------------------------------------------------------------
@router.get("", response_model=OrganizerResponse)
def get_my_organizer_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity),
):
    """
    取得目前登入者所屬的 Organizer 資料

    - system_admin：回傳第一個關聯 organizer（或之後可擴充）
    - organizer owner / admin：回傳所屬 organizer
    """

    # system admin：允許查看
    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        organizer = organizer_crud.get_first_active_organizer(db)
        if not organizer:
            raise HTTPException(status_code=404, detail="Organizer not found")
        return organizer

    # organizer member（owner / admin）
    membership = organizer_crud.get_primary_membership_by_user(
        db,
        user_uuid=current_user.uuid,
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of any organizer",
        )

    organizer = organizer_crud.get_organizer_by_uuid(
        db,
        membership.organizer_uuid,
    )

    if not organizer or organizer.is_deleted:
        raise HTTPException(status_code=404, detail="Organizer not found")

    return organizer
