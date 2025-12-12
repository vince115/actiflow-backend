# app/schemas/event/event_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    status: Optional[str] = None
    activity_template_uuid: Optional[UUID] = None
    config: Optional[Dict[str, Any]] = None

    is_active: Optional[bool] = None
