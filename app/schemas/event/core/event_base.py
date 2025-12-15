# app/schemas/event/core/event_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class EventBase(BaseModel):
    """
    Event 的核心欄位，不含 audit 與 uuid。
    """

    event_code: str
    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    status: str = "draft"                    # draft / published / closed

    activity_template_uuid: Optional[UUID] = None
    organizer_uuid: UUID

    config: Optional[Dict[str, Any]] = None
