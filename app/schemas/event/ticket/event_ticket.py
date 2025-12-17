# app/schemas/event/ticket/event_ticket.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.schemas.common.base import BaseSchema


class EventTicketBase(BaseModel):
    ticket_name: str
    price: float
    capacity: Optional[int] = None
    remaining: Optional[int] = None
    sale_start: Optional[datetime] = None
    sale_end: Optional[datetime] = None


class EventTicketCreate(EventTicketBase):
    event_uuid: UUID


class EventTicketUpdate(BaseModel):
    ticket_name: Optional[str] = None
    price: Optional[float] = None
    capacity: Optional[int] = None
    remaining: Optional[int] = None
    sale_start: Optional[datetime] = None
    sale_end: Optional[datetime] = None
    is_active: Optional[bool] = None


class EventTicketResponse(EventTicketBase, BaseSchema):
    event_uuid: UUID
    model_config = {"from_attributes": True}
