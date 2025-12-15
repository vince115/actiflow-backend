# app/schemas/event/field/event_field_update.py

from pydantic import BaseModel
from typing import Optional, List, Any


class EventFieldUpdate(BaseModel):
    """
    更新 EventField 用 Schema。
    event_uuid 與 field_key 不能修改。
    """

    label: Optional[str] = None
    field_type: Optional[str] = None
    required: Optional[bool] = None
    options: Optional[List[Any]] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
