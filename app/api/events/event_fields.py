# app/api/events/event_fields.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import get_current_organizer_admin_factory

from crud.event.event import get_event_by_uuid
from crud.event.event_field import (
    create_event_field,
    list_event_fields,
    get_event_field_by_uuid,
    update_event_field,
    soft_delete_event_field,
)

from app.schemas.event.event_field_base import (
    EventFieldCreate,
    EventFieldUpdate,
    EventFieldResponse,
)


router = APIRouter(
    prefix="/events",
    tags=["Event Fields"],
)


# ------------------------------------------------------------
# Utility: check event permission
# ------------------------------------------------------------
def _check_event_permission(db: Session, event_uuid: str, membership):
    event = get_event_by_uuid(db, event_uuid)
    if not event:
        raise HTTPException(404, "Event not found")

    if str(event.organizer_uuid) != str(membership.organizer_uuid):
        raise HTTPException(403, "Not allowed for this organizer")

    return event


# ------------------------------------------------------------
# List all fields for an event
# ------------------------------------------------------------
@router.get("/{event_uuid}/fields", response_model=list[EventFieldResponse])
def api_list_event_fields(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_organizer_admin_factory()),
):
    _check_event_permission(db, str(event_uuid), admin)
    return list_event_fields(db, str(event_uuid))


# ------------------------------------------------------------
# Create event field
# ------------------------------------------------------------
@router.post("/{event_uuid}/fields", response_model=EventFieldResponse)
def api_create_event_field(
    event_uuid: UUID,
    data: EventFieldCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_organizer_admin_factory()),
):
    _check_event_permission(db, str(event_uuid), admin)

    field = create_event_field(
        db=db,
        event_uuid=str(event_uuid),
        data=data,
        created_by=str(admin.user_uuid),
        created_by_role=admin.role,
    )
    return field


# ------------------------------------------------------------
# Get single event field
# ------------------------------------------------------------
@router.get("/{event_uuid}/fields/{field_uuid}", response_model=EventFieldResponse)
def api_get_event_field(
    event_uuid: UUID,
    field_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_organizer_admin_factory()),
):
    _check_event_permission(db, str(event_uuid), admin)

    field = get_event_field_by_uuid(db, str(field_uuid))
    if not field or str(field.event_uuid) != str(event_uuid):
        raise HTTPException(404, "Event field not found")

    return field


# ------------------------------------------------------------
# Update event field
# ------------------------------------------------------------
@router.put("/{event_uuid}/fields/{field_uuid}", response_model=EventFieldResponse)
def api_update_event_field(
    event_uuid: UUID,
    field_uuid: UUID,
    data: EventFieldUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_organizer_admin_factory()),
):
    _check_event_permission(db, str(event_uuid), admin)

    field = get_event_field_by_uuid(db, str(field_uuid))
    if not field or str(field.event_uuid) != str(event_uuid):
        raise HTTPException(404, "Event field not found")

    updated = update_event_field(
        db=db,
        field_uuid=str(field_uuid),
        data=data,
        updated_by=str(admin.user_uuid),
        updated_by_role=admin.role,
    )

    return updated


# ------------------------------------------------------------
# Soft delete event field
# ------------------------------------------------------------
@router.delete("/{event_uuid}/fields/{field_uuid}")
def api_delete_event_field(
    event_uuid: UUID,
    field_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_current_organizer_admin_factory()),
):
    _check_event_permission(db, str(event_uuid), admin)

    field = get_event_field_by_uuid(db, str(field_uuid))
    if not field or str(field.event_uuid) != str(event_uuid):
        raise HTTPException(404, "Event field not found")

    soft_delete_event_field(
        db=db,
        field_uuid=str(field_uuid),
        deleter_uuid=str(admin.user_uuid),
        deleter_role=admin.role,
    )

    return {"success": True, "field_uuid": str(field_uuid)}
