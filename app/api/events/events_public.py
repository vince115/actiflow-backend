# app/api/events/events_public.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

from app.schemas.event.event import EventResponse
from app.schemas.event.event_field_base import EventFieldResponse

from crud.event.event import (
    get_event_by_uuid,
    list_public_events,
)
from crud.event.event_field import list_public_event_fields


router = APIRouter(
    prefix="/events",
    tags=["Public - Events"]
)


# ------------------------------------------------------------
# 公開：取得所有可公開活動
# ------------------------------------------------------------
@router.get("/", response_model=list[EventResponse])
def public_list_events(db: Session = Depends(get_db)):
    """
    公開取得所有活動：
    - 只取 is_active=True
    - 不取 is_deleted=True
    """
    events = list_public_events(db)
    return events


# ------------------------------------------------------------
# 公開：取得活動詳情
# ------------------------------------------------------------
@router.get("/{event_uuid}", response_model=EventResponse)
def public_get_event_detail(event_uuid: str, db: Session = Depends(get_db)):
    event = get_event_by_uuid(db, event_uuid)

    if not event or event.is_deleted or not event.is_active:
        raise HTTPException(404, "Event not found")

    return event


# ------------------------------------------------------------
# 公開：取得活動欄位（報名表單）
# ------------------------------------------------------------
@router.get("/{event_uuid}/fields", response_model=list[EventFieldResponse])
def public_get_event_fields(event_uuid: str, db: Session = Depends(get_db)):
    fields = list_public_event_fields(db, event_uuid)
    return fields
