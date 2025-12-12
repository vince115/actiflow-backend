# app/schemas/event/event_field_create.py

from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID


class EventFieldCreate(BaseModel):
    event_uuid: UUID
    field_key: str
    label: str
    field_type: str
    required: bool = False
    options: Optional[List[Any]] = None
    sort_order: int = 0
