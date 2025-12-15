# app/schemas/event/staff/event_staff_base.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


# ------------------------------------------------------------
# Event Staff Base（共用）
# ------------------------------------------------------------
class EventStaffBase(BaseModel):
    event_uuid: UUID
    user_uuid: UUID

    role: str                    # organizer / staff / checkin / admin
    title: Optional[str] = None
