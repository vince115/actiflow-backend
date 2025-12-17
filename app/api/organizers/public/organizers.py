# app/api/organizers/organizers.py  # organizer 自己的 CRUD

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.schemas.organizer.organizer_create import OrganizerCreate
from app.schemas.organizer.organizer_update import OrganizerUpdate
from app.schemas.organizer.organizer_response import OrganizerResponse

from app.crud.organizer.crud_organizer import organizer_crud
from app.crud.membership.crud_organizer_membership import (
    get_membership_by_user_and_organizer,
    list_user_memberships,
)
from app.crud.membership.crud_system_membership import get_system_membership


router = APIRouter(prefix="/organizers", tags=["Organizers"])


# -------------------------------------------------------------------
# Utility: Check system_admin
# -------------------------------------------------------------------
def require_system_admin(user, db: Session):
    membership = get_system_membership(db, user.uuid)
    if not membership or membership.role != "system_admin":
        raise HTTPException(403, "System admin permission required")


# -------------------------------------------------------------------
# Utility: Check organizer_owner/admin
# -------------------------------------------------------------------
def require_organizer_admin(user, organizer_uuid: str, db: Session):
    mem = get_membership_by_user_and_organizer(db, user.uuid, organizer_uuid)

    if not mem:
        raise HTTPException(403, "You are not a member of this organizer")

    if mem.role not in ["owner", "admin"]:
        raise HTTPException(403, "Organizer admin or owner permission required")


# -------------------------------------------------------------------
# Create Organizer  (system_admin only)
# -------------------------------------------------------------------
@router.post("/", response_model=OrganizerResponse)
def create_new_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity)
):
    require_system_admin(current_user, db)
    return organizer_crud.create(db, data)


# -------------------------------------------------------------------
# Update Organizer （owner/admin OR system_admin）
# -------------------------------------------------------------------
def update_organizer_info(
    organizer_uuid: str,
    data: OrganizerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity)
):
    organizer = organizer_crud.get_organizer_by_uuid(db, organizer_uuid)

    if not organizer or organizer.is_deleted:
        raise HTTPException(404, "Organizer not found")

    # system_admin 可以直接修改
    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        return organizer_crud.update(db, organizer, data)

    # 其他使用者必須是 owner/admin
    require_organizer_admin(current_user, organizer_uuid, db)
    return organizer_crud.update(db, organizer, data)


# -------------------------------------------------------------------
# Get Organizer
# -------------------------------------------------------------------
@router.get("/{organizer_uuid}", response_model=OrganizerResponse)
def get_single_organizer(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity)
):
    organizer = organizer_crud.get_organizer_by_uuid(db, organizer_uuid)

    if not organizer or organizer.is_deleted:
        raise HTTPException(404, "Organizer not found")

    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        return organizer

    mem = get_membership_by_user_and_organizer(
        db,
        current_user.uuid,
        organizer_uuid
    )

    if not mem:
        raise HTTPException(403, "You don't have permission to view this organizer")

    return organizer

# -------------------------------------------------------------------
# List Organizers
# -------------------------------------------------------------------
@router.get("/", response_model=list[OrganizerResponse])
def list_all_organizers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_identity)
):
    system_mem = get_system_membership(db, current_user.uuid)

    if system_mem and system_mem.role == "system_admin":
        return organizer_crud.list(db)

    memberships = list_user_memberships(
        db,
        current_user.uuid
    )

    organizers = []
    for m in memberships:
        organizer = organizer_crud.get_organizer_by_uuid(db, m.organizer_uuid)
        if organizer and not organizer.is_deleted:
            organizers.append(organizer)

    return organizers