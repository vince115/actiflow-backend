# app/api/organizers/organizer/events.py

# Organizer 後台 - Event CRUD（owner / admin）
# Canonical Organizer API

from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import require_current_organizer_admin

from app.core.constants.event_status import EventStatus
from app.core.domain.event_status_guard import assert_event_status_transition

from app.schemas.event.core.organizer.organizer_event_create import OrganizerEventCreate
from app.schemas.event.core.organizer.organizer_event_update import OrganizerEventUpdate

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
        status=EventStatus.DRAFT,
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
    data: OrganizerEventUpdate,
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

    # 禁止透過 update API 變更狀態
    if "status" in update_data:
        raise HTTPException(
            status_code=400,
            detail="Event status must be changed via publish/unpublish/close APIs",
        )

    for field, value in update_data.items():
        setattr(event, field, value)

    event.updated_by = membership.user_uuid
    event.updated_by_role = membership.role

    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)



# -------------------------------------------------------------------
# Publish  event (draft -> published)
# -------------------------------------------------------------------
@router.patch("/{event_uuid}/publish", response_model=EventResponse)
def publish_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    event = _get_event_or_404(db, event_uuid, membership.organizer_uuid)

    assert_event_status_transition(
        current=EventStatus(event.status),
        target=EventStatus.PUBLISHED,
    )

    event.status = EventStatus.PUBLISHED
    event.updated_by = membership.user_uuid
    event.updated_by_role = membership.role

    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Unpublish event (published -> draft)
# -------------------------------------------------------------------
@router.patch("/{event_uuid}/unpublish", response_model=EventResponse)
def unpublish_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    event = _get_event_or_404(db, event_uuid, membership.organizer_uuid)

    assert_event_status_transition(
        current=EventStatus(event.status),
        target=EventStatus.DRAFT,
    )

    event.status = EventStatus.DRAFT
    event.updated_by = membership.user_uuid
    event.updated_by_role = membership.role

    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)


# -------------------------------------------------------------------
# Close event (published -> closed)
# -------------------------------------------------------------------
@router.patch("/{event_uuid}/close", response_model=EventResponse)
def close_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    event = _get_event_or_404(db, event_uuid, membership.organizer_uuid)

    assert_event_status_transition(
        current=EventStatus(event.status),
        target=EventStatus.CLOSED,
    )

    event.status = EventStatus.CLOSED
    event.updated_by = membership.user_uuid
    event.updated_by_role = membership.role

    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)
   

# -------------------------------------------------------------------
# Utilities
# -------------------------------------------------------------------
def generate_event_code() -> str:
    """
    事件代碼產生（簡易版）
    例：EVT-20260105123045
    """
    return f"EVT-{datetime.utcnow():%Y%m%d%H%M%S}"


def _get_event_or_404(
    db: Session,
    event_uuid: UUID,
    organizer_uuid: UUID,
) -> Event:
    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.organizer_uuid == organizer_uuid,
            Event.is_deleted == False,
        )
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event
