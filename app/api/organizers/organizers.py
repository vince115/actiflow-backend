# app/api/organizers/organizers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.organizer.organizer import OrganizerCreate, OrganizerUpdate, OrganizerResponse
from crud.organizer.organizer import (
    create_organizer,
    get_organizer_by_uuid,
    list_organizers,
    update_organizer as update_org_in_db,
)
from crud.membership.organizer_membership import get_membership, get_user_memberships
from crud.membership.system_membership import get_system_membership
from app.core.dependencies import get_current_user


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
    mem = get_membership(db, user.uuid, organizer_uuid)

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
    current_user=Depends(get_current_user)
):
    require_system_admin(current_user, db)
    organizer = create_organizer(db, data)
    return organizer


# -------------------------------------------------------------------
# Update Organizer （owner/admin OR system_admin）
# -------------------------------------------------------------------
@router.put("/{organizer_uuid}", response_model=OrganizerResponse)
def update_organizer_info(
    organizer_uuid: str,
    data: OrganizerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    organizer = get_organizer_by_uuid(db, organizer_uuid)
    if not organizer or organizer.is_deleted:
        raise HTTPException(404, "Organizer not found")

    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        return update_org_in_db(db, organizer_uuid, data)

    require_organizer_admin(current_user, organizer_uuid, db)

    return update_org_in_db(db, organizer_uuid, data)


# -------------------------------------------------------------------
# Get Organizer
# -------------------------------------------------------------------
@router.get("/{organizer_uuid}", response_model=OrganizerResponse)
def get_single_organizer(
    organizer_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    organizer = get_organizer_by_uuid(db, organizer_uuid)

    if not organizer or organizer.is_deleted:
        raise HTTPException(404, "Organizer not found")

    system_mem = get_system_membership(db, current_user.uuid)
    if system_mem and system_mem.role == "system_admin":
        return organizer

    mem = get_membership(db, current_user.uuid, organizer_uuid)
    if not mem:
        raise HTTPException(403, "You don't have permission to view this organizer")

    return organizer


# -------------------------------------------------------------------
# List Organizers
# -------------------------------------------------------------------
@router.get("/", response_model=list[OrganizerResponse])
def list_all_organizers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    system_mem = get_system_membership(db, current_user.uuid)

    if system_mem and system_mem.role == "system_admin":
        return list_organizers(db)

    memberships = get_user_memberships(db, current_user.uuid)

    organizer_ids = {m.organizer_uuid for m in memberships}

    return [
        org
        for org_uuid in organizer_ids
        if (org := get_organizer_by_uuid(db, org_uuid))
        and not org.is_deleted
    ]
