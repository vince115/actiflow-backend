# app/api/events/public/event_detail.py # 單一活動公開頁

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db

from app.schemas.event.core.event_response import EventResponse
from app.models.event.event import Event

router = APIRouter(
    prefix="/events",
    tags=["Public Events"],
)


# ============================================================
# Public Event Detail
# ============================================================
@router.get("/{event_uuid}", response_model=EventResponse)
def get_public_event_detail(
    event_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    公開活動詳情頁（不需登入）

    條件：
    - event 必須存在
    - is_active = True
    - is_deleted = False
    """

    event = (
        db.query(Event)
        .filter(
            Event.uuid == event_uuid,
            Event.is_active == True,
            Event.is_deleted == False,
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found",
        )

    return EventResponse.model_validate(event)
