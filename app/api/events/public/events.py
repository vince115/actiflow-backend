# app/api/events/public/events.py    # 活動列表 / 搜尋

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db

from app.models.event.event import Event
from app.schemas.event.core.event_public import EventPublic
from app.schemas.common.pagination import PaginatedResponse


router = APIRouter(
    prefix="/public/events",
    tags=["Public - Events"],
)


# -------------------------------------------------------------------
# Public: List published events
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse)
def list_public_events(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    """
    公開活動列表（僅顯示已發布的活動）
    """

    query = (
        db.query(Event)
        .filter(
            Event.status == "published",
            Event.is_deleted == False,
        )
    )

    total = query.count()
    events = (
        query
        .order_by(Event.start_at.asc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedResponse(
        items=events,
        total=total,
        page=page,
        page_size=page_size,
    )


# -------------------------------------------------------------------
# Public: Get event detail
# -------------------------------------------------------------------
@router.get("/{event_uuid}", response_model=EventPublic)
def get_public_event(
    event_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    公開活動詳細頁
    """

    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.status == "published",
            Event.is_deleted == False,
        )
        .first()
    )

    if not event:
        raise HTTPException(404, "Event not found")

    return event
