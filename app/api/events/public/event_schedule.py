# app/api/events/public/event_schedule.py # 活動場次 / 時程

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.db import get_db

from app.schemas.event.schedule.event_schedule import (
    EventScheduleResponse,
)

from app.models.event.event import Event
from app.models.event.event_schedule import EventSchedule


router = APIRouter(
    prefix="/events",
    tags=["Public Events"],
)


# ============================================================
# Public Event Schedule
# ============================================================
@router.get(
    "/{event_uuid}/schedule",
    response_model=List[EventScheduleResponse],
)
def get_public_event_schedule(
    event_uuid: UUID,
    db: Session = Depends(get_db),
):
    """
    公開活動場次 / 時程表（不需登入）

    條件：
    - event 必須存在
    - event.is_active = True
    - event.is_deleted = False
    - 只回傳未刪除的場次
    """

    # 1. 確認活動存在且可公開
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

    # 2. 取得活動場次 / 時程
    schedules = (
        db.query(EventSchedule)
        .filter(
            EventSchedule.event_uuid == event_uuid,
            EventSchedule.is_deleted == False,
        )
        .order_by(EventSchedule.start_time.asc())
        .all()
    )

    return [
        EventScheduleResponse.model_validate(s)
        for s in schedules
    ]
