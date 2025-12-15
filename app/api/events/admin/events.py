# app/api/events/admin/events.py

# 平台（SuperAdmin）管理所有 Event
# - 全平台檢視
# - 狀態管控（下架 / 封存）
# - 不處理 ActivityTemplate / Submission

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_super_admin

from app.models.event.event import Event
from app.schemas.event.core.event_response import EventResponse
from app.schemas.event.core.event_status_update import EventStatusUpdate
from app.schemas.common.pagination import PaginatedResponse


router = APIRouter(
    prefix="/admin/events",
    tags=["Admin - Events"],
)

# -------------------------------------------------------------------
# List all events (platform-wide)
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse[EventResponse])
def list_events_admin(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    """
    平台管理員：取得全平台 Event 列表
    """
    query = db.query(Event).filter(Event.is_deleted == False)

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
# Force update event status (admin control)
# -------------------------------------------------------------------
@router.patch("/{event_uuid}/status", response_model=EventResponse)
def update_event_status_admin(
    event_uuid: UUID,
    data: EventStatusUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    """
    平台強制變更 Event 狀態
    例如：published / closed / archived
    """

    event = (
        db.query(Event)
        .filter(Event.uuid == event_uuid, Event.is_deleted == False)
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.status = data.status
    db.commit()
    db.refresh(event)

    return EventResponse.model_validate(event)