# app/schemas/event/staff/event_staff_create.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel


# ------------------------------------------------------------
# Event Staff Create
# ------------------------------------------------------------
class EventStaffCreate(BaseModel):
    event_uuid: UUID
    user_uuid: UUID

    role: str
    title: Optional[str] = None
