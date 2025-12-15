# app/api/events/organizer/events.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.crud.event.crud_event import event_crud

from app.schemas.event.core.event_create import EventCreate
from app.schemas.event.core.event_update import EventUpdate
from app.schemas.event.core.event_response import EventResponse
from app.schemas.common.pagination import PaginatedResponse


router = APIRouter(
    prefix="/organizer/events",
    tags=["Organizer - Events"],
)


# -------------------------------------------------------------------
# List organizer events
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse[EventResponse])
def list_organizer_events(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    objs, total = event_crud.list_by_organizer(
        db,
        organizer_uuid=membership.organizer_uuid,
        page=page,
        page_size=page_size,
    )

    return PaginatedResponse(
        items=[EventResponse.model_validate(o) for o in objs],
        total=total,
        page=page,
        page_size=page_size,
    )


# -------------------------------------------------------------------
# Create event
# -------------------------------------------------------------------
@router.post("", response_model=EventResponse)
def create_event(
    data: EventCreate,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    obj = event_crud.create_by_organizer(
        db,
        organizer_uuid=membership.organizer_uuid,
        data=data,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )

    return EventResponse.model_validate(obj)

# -------------------------------------------------------------------
# Update event
# -------------------------------------------------------------------
@router.patch("/{event_uuid}", response_model=EventResponse)
def update_event(
    event_uuid: UUID,
    data: EventUpdate,
    db: Session = Depends(get_db),
    membership = Depends(require_organizer_admin),
):
    obj = event_crud.get_by_uuid(db, event_uuid)

    if not obj or obj.organizer_uuid != membership.organizer_uuid:
        raise HTTPException(404, "Event not found")

    obj = event_crud.update(
        db,
        db_obj=obj,
        data=data,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    return EventResponse.model_validate(obj)