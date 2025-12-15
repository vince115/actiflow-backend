# app/api/organizers/organizer/events.py
# Organizer 後台 - Event CRUD（owner / admin）

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.schemas.event.core.event_create import EventCreate
from app.schemas.event.core.event_update import EventUpdate
from app.schemas.event.core.event_response import EventResponse
from app.schemas.common.pagination import PaginatedResponse

from app.crud.event.crud_event import (
    create_event_by_organizer,
    get_event_by_uuid,
    list_events_by_organizer,
    update_event,
    soft_delete_event,
)

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
    """
    Organizer 後台：
    取得該 organizer 的活動列表
    """

    query = list_events_by_organizer(
        db=db,
        organizer_uuid=membership.organizer_uuid,
        query_only=True,  # 若你的 CRUD 支援，否則直接回 list
    )

    total = query.count()
    events = (
        query
        .order_by(query.column_descriptions[0]["entity"].created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedResponse(
        items=[EventResponse.model_validate(e) for e in events],
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
    """
    Organizer 後台：
    建立活動
    """

    event = create_event_by_organizer(
        db=db,
        organizer_uuid=membership.organizer_uuid,
        data=data,
        creator_uuid=membership.user_uuid,
    )

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Get single event
# -------------------------------------------------------------------
@router.get("/{event_uuid}", response_model=EventResponse)
def get_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    event = get_event_by_uuid(db, event_uuid)

    if (
        not event
        or event.is_deleted
        or event.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Event not found")

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Update event
# -------------------------------------------------------------------
@router.put("/{event_uuid}", response_model=EventResponse)
def update_event_handler(
    event_uuid: UUID,
    data: EventUpdate,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    event = get_event_by_uuid(db, event_uuid)

    if (
        not event
        or event.is_deleted
        or event.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Event not found")

    updated = update_event(
        db=db,
        event_uuid=event_uuid,
        data=data,
        updated_by=membership.user_uuid,
        updated_by_role=membership.role,
    )

    return EventResponse.model_validate(updated)


# -------------------------------------------------------------------
# Soft delete event
# -------------------------------------------------------------------
@router.delete("/{event_uuid}")
def delete_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    event = get_event_by_uuid(db, event_uuid)

    if (
        not event
        or event.is_deleted
        or event.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Event not found")

    soft_delete_event(
        db=db,
        event_uuid=event_uuid,
        deleted_by=membership.user_uuid,
        deleted_by_role=membership.role,
    )

    return {"deleted": True, "event_uuid": event_uuid}
