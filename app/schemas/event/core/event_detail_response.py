# app/schemas/event/core/event_detail_response.py

from typing import List, Optional

from app.schemas.common.base import BaseSchema
from app.schemas.event.core.event_base import EventBase
from app.schemas.event.field.event_field_response import EventFieldResponse
from app.schemas.activity_template.activity_template_response import ActivityTemplateResponse


class EventDetailResponse(BaseSchema, EventBase):
    """
    Event 詳細回傳（帶 fields）
    """
    fields: List[EventFieldResponse] = []
    activity_template: Optional[ActivityTemplateResponse] = None

    model_config = {"from_attributes": True}
