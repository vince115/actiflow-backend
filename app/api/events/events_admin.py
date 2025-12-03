# app/api/events/events_admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin

from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventResponse
)
from app.schemas.event_field import EventFieldResponse
from app.schemas.common import DeleteResponse   # ← 建議新增通用 schema

from app.crud.event import (
    create_event,
    get_event_by_uuid,
    list_events,
    update_event,
    soft_delete_event,
)
from app.crud.event_field import list_event_fields


router = APIRouter(
    prefix="/admin/events",
    tags=["Admin - Events"],
)


# ------------------------------------------------------------
# Create Event
# ------------------------------------------------------------
@router.post("/", response_model=EventResponse)
def admin_create_event(
    data: EventCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    event = create_event(
        db=db,
        data=data,
        created_by=str(admin.uuid),
        created_by_role="super_admin",
    )
    return event


# ------------------------------------------------------------
# List Events
# ------------------------------------------------------------
@router.get("/", response_model=list[EventResponse])
def admin_list_events(
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    return list_events(db)


# ------------------------------------------------------------
# Get Event Detail
# ------------------------------------------------------------
@router.get("/{event_uuid}", response_model=EventResponse)
def admin_get_event_detail(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    event = get_event_by_uuid(db, str(event_uuid))
    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")
    return event


# ------------------------------------------------------------
# Update Event
# ------------------------------------------------------------
@router.put("/{event_uuid}", response_model=EventResponse)
def admin_update_event(
    event_uuid: UUID,
    data: EventUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    event = update_event(
        db=db,
        event_uuid=str(event_uuid),
        data=data,
        updated_by=str(admin.uuid),
        updated_by_role="super_admin",
    )

    if not event:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found or inactive")

    return event


# ------------------------------------------------------------
# Delete Event (Soft Delete)
# ------------------------------------------------------------
@router.delete("/{event_uuid}", response_model=DeleteResponse)
def admin_delete_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    deleted = soft_delete_event(
        db=db,
        event_uuid=str(event_uuid),
        deleted_by=str(admin.uuid),
        deleted_by_role="super_admin",
    )

    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Event not found")

    return DeleteResponse(
        success=True,
        uuid=str(event_uuid),
        message="Event soft-deleted"
    )


# ------------------------------------------------------------
# List Event Fields
# ------------------------------------------------------------
@router.get("/{event_uuid}/fields", response_model=list[EventFieldResponse])
def admin_get_event_fields(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    return list_event_fields(db, str(event_uuid))
