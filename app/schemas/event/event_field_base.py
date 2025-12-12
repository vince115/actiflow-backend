# app/schemas/event/event_field_base.py

from pydantic import BaseModel, field_validator
from typing import Optional, List, Any


class EventFieldBase(BaseModel):
    field_key: str
    label: str
    field_type: str
    required: bool = False
    options: Optional[List[Any]] = None
    sort_order: int = 0

    @field_validator("field_key")
    def validate_key(cls, v):
        if not v or not v.strip():
            raise ValueError("field_key cannot be empty")
        return v
