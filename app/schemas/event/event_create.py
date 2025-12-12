# app/schemas/event/event_create.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class EventCreate(BaseModel):
    event_code: str
    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    activity_template_uuid: Optional[UUID] = None
    organizer_uuid: UUID

    config: Optional[Dict[str, Any]] = None
