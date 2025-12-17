# app/api/organizers/organizer/profile.py
# Organizer 個人資料（Profile）API

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
    prefix="/profile",
    tags=["Organizer Profile"]
)


# -------------------------------------------------------------------
# Get organizer profile (owner / admin / system_admin)
# -------------------------------------------------------------------
@router.get("/{organizer_uuid}", response_model=OrganizerResponse)
def get_organizer_profile(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity),
):
    organizer = organizer_crud.get_organizer_by_uuid(db, organizer_uuid)

    if not organizer or organizer.is_deleted:
        raise HTTPException(status_code=404, detail="Organizer not found")

    # system_admin 可直接存取
    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        return organizer

    # organizer owner / admin
    mem = get_membership_by_user_and_organizer(
        db,
        current_user.uuid,
        organizer_uuid,
    )

    if not mem:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this organizer",
        )

    if mem.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Organizer admin or owner permission required",
        )

    return organizer
