# app/schemas/event/staff/event_staff_update.py

from typing import Optional
from pydantic import BaseModel


# ------------------------------------------------------------
# Event Staff Update
# ------------------------------------------------------------
class EventStaffUpdate(BaseModel):
    role: Optional[str] = None
    title: Optional[str] = None
    is_active: Optional[bool] = None
