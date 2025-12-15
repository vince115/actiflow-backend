# app/schemas/event/core/event_response.py

from typing import List, Optional
from uuid import UUID

from app.schemas.event.core.event_base import EventBase
from app.schemas.base.base_model import BaseSchema
from app.schemas.event.field.event_field_response import EventFieldResponse


class EventResponse(EventBase, BaseSchema):
    """
    回傳 Event 完整資訊：
    - 基本欄位（Base）
    - uuid + audit 欄位（BaseSchema）
    - fields（EventField 列表）
    """

    fields: List[EventFieldResponse] = []

    model_config = {"from_attributes": True}
