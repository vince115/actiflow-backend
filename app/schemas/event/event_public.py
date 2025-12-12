# app/schemas/event/event_public.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.schemas.event.event_field_response import EventFieldResponse
from app.schemas.event.event_ticket import EventTicketResponse
from app.schemas.event.event_schedule import EventScheduleResponse


class EventPublic(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None

    fields: List[EventFieldResponse] = []
    tickets: List[EventTicketResponse] = []
    schedules: List[EventScheduleResponse] = []

    model_config = {"from_attributes": True}
