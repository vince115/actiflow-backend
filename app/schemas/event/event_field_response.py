# app/schemas/event/event_field_response.py

from uuid import UUID
from typing import Optional, List, Any
from app.schemas.base.base_model import BaseSchema


class EventFieldResponse(BaseSchema):
    event_uuid: UUID
    field_key: str
    label: str
    field_type: str
    required: bool
    options: Optional[List[Any]]
    sort_order: int

    model_config = {"from_attributes": True}
