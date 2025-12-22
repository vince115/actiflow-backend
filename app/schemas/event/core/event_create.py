# app/schemas/event/core/event_create.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from app.schemas.event.core.event_base import OrganizerEventBase

# Frontend scoped
class EventCreate(BaseModel):
    """
    （可選）Frontend scoped 建立 Event：通常不建議直接暴露
    若你沒有 public 建立 event 的需求，可以不用這個 schema。
    """

    event_code: str
    organizer_uuid: UUID
    activity_template_uuid: Optional[UUID] = None

    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    status: str = "draft"
    config: Optional[Dict[str, Any]] = None

# Organizer scoped
class OrganizerEventCreate(OrganizerEventBase):
    """
    建立 Event（Organizer scoped）
    """
    pass