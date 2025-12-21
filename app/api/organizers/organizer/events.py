# app/api/organizers/organizer/events.py
# Organizer 後台 - Event CRUD（owner / admin）
# Canonical Organizer API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.core.db import get_db
from app.core.dependencies import require_current_organizer_admin

from app.schemas.event.core.event_create import OrganizerEventCreate
from app.schemas.event.core.event_update import EventUpdate
from app.schemas.event.core.event_response import EventResponse
from app.schemas.common.pagination import PaginatedResponse

from app.models.event.event import Event


router = APIRouter(
    prefix="/events",
    tags=["Organizer - Events"],
)


# -------------------------------------------------------------------
# List events
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse[EventResponse])
def list_events(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    query = (
        db.query(Event)
        .filter(
            Event.organizer_uuid == membership.organizer_uuid,
            Event.is_deleted == False,
        )
    )

    total = query.count()
    events = (
        query
        .order_by(Event.created_at.desc())
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
    data: OrganizerEventCreate,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    event = Event(
        **data.model_dump(),
        organizer_uuid=membership.organizer_uuid,
        event_code=generate_event_code(),
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Update event（PUT / partial update）
# -------------------------------------------------------------------
@router.put("/{event_uuid}", response_model=EventResponse)
def update_event(
    event_uuid: UUID,
    data: EventUpdate,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.organizer_uuid == membership.organizer_uuid,
            Event.is_deleted == False,
        )
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 只更新有傳的欄位（partial update）
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(event, field, value)

    event.updated_by = membership.user_uuid
    event.updated_by_role = membership.role
    event.updated_at = datetime.utcnow()

    db.add(event)
    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Utils
# -------------------------------------------------------------------
def generate_event_code() -> str:
    """
    事件代碼產生（簡易版）
    例：EVT-20260105123045
    """
    return f"EVT-{datetime.utcnow():%Y%m%d%H%M%S}"
