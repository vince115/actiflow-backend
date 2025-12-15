# app/schemas/activity_template/activity_template_field_update.py

from typing import Optional, List, Any
from pydantic import BaseModel


class ActivityTemplateFieldUpdate(BaseModel):
    """
    更新 ActivityTemplateField
    不允許更新 template_uuid / field_key
    """

    label: Optional[str] = None
    field_type: Optional[str] = None
    required: Optional[bool] = None
    options: Optional[List[Any]] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
