# app/api/events/organizer/event_staff.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_member

from app.crud.event.crud_event_staff import event_staff_crud

from app.schemas.event.staff.event_staff_create import EventStaffCreate
from app.schemas.event.staff.event_staff_update import EventStaffUpdate
from app.schemas.event.staff.event_staff_response import EventStaffResponse


router = APIRouter(
    prefix="/organizer/events/{event_uuid}/staff",
    tags=["Organizer - Event Staff"],
)


# ------------------------------------------------------------
# List staff
# ------------------------------------------------------------
@router.get("", response_model=list[EventStaffResponse])
def list_event_staff(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_member),
):
    objs = event_staff_crud.list_by_event(
        db,
        event_uuid=event_uuid,
        organizer_uuid=membership.organizer_uuid,
    )
    return [EventStaffResponse.model_validate(o) for o in objs]


# ------------------------------------------------------------
# Create staff
# ------------------------------------------------------------
@router.post("", response_model=EventStaffResponse)
def create_event_staff(
    event_uuid: UUID,
    data: EventStaffCreate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_member),
):
    obj = event_staff_crud.create(
        db,
        event_uuid=event_uuid,
        organizer_uuid=membership.organizer_uuid,
        data=data,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )
    return EventStaffResponse.model_validate(obj)


# ------------------------------------------------------------
# Update staff
# ------------------------------------------------------------
@router.put("/{staff_uuid}", response_model=EventStaffResponse)
def update_event_staff(
    event_uuid: UUID,
    staff_uuid: UUID,
    data: EventStaffUpdate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_member),
):
    obj = event_staff_crud.update(
        db,
        event_uuid=event_uuid,
        staff_uuid=staff_uuid,
        organizer_uuid=membership.organizer_uuid,
        data=data,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    if not obj:
        raise HTTPException(status_code=404, detail="Staff not found")

    return EventStaffResponse.model_validate(obj)


# ------------------------------------------------------------
# Delete staff (soft delete)
# ------------------------------------------------------------
@router.delete("/{staff_uuid}")
def delete_event_staff(
    event_uuid: UUID,
    staff_uuid: UUID,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_member),
):
    ok = event_staff_crud.soft_delete(
        db,
        event_uuid=event_uuid,
        staff_uuid=staff_uuid,
        organizer_uuid=membership.organizer_uuid,
        deleted_by=membership.user_uuid,
        deleted_by_role=membership.role,
    )

    if not ok:
        raise HTTPException(status_code=404, detail="Staff not found")

    return {"deleted": True}
