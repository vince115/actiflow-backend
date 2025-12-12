# app/schemas/event/event_schedule.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.schemas.base.base_model import BaseSchema


class EventScheduleBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    sort_order: int = 0


class EventScheduleCreate(EventScheduleBase):
    event_uuid: UUID


class EventScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class EventScheduleResponse(EventScheduleBase, BaseSchema):
    event_uuid: UUID
    model_config = {"from_attributes": True}
