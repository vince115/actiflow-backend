# app/schemas/event/core/event_list_item.py

from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class OrganizerEventListItem(BaseModel):
    uuid: UUID
    title: str
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    submissions_count: int
