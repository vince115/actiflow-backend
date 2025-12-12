# app/schemas/template/template_field_update.py

from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID


class TemplateFieldUpdate(BaseModel):
    """
    更新 TemplateField 用 Schema。
    只允許更新欄位本身，不允許更新 template_uuid。
    """

    label: Optional[str] = None
    field_type: Optional[str] = None
    required: Optional[bool] = None
    options: Optional[List[Any]] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
