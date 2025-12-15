# app/api/events/organizer/event_fields.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.crud.event.crud_event_field import event_field_crud

from app.schemas.event.field.event_field_create import EventFieldCreate
from app.schemas.event.field.event_field_response import EventFieldResponse


router = APIRouter(
    prefix="/organizer/{organizer_uuid}/events/{event_uuid}/fields",
    tags=["Organizer - Event Fields"],
)


# -------------------------------------------------------------------
# List event fields
# -------------------------------------------------------------------
@router.get("", response_model=list[EventFieldResponse])
def list_event_fields(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    objs = event_field_crud.list_by_event(db, event_uuid)
    return [EventFieldResponse.model_validate(o) for o in objs]


# -------------------------------------------------------------------
# Create event field
# -------------------------------------------------------------------
@router.post("", response_model=EventFieldResponse)
def create_event_field(
    event_uuid: UUID,
    data: EventFieldCreate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    obj = event_field_crud.create(
        db,
        event_uuid=event_uuid,
        data=data,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )
    return EventFieldResponse.model_validate(obj)
