# app/schemas/template/template_field_response.py

from datetime import datetime
from typing import Optional, List, Any
from uuid import UUID

from pydantic import BaseModel
from app.schemas.base.base_model import BaseSchema


class TemplateFieldResponse(BaseSchema):
    """
    回傳用的 TemplateField Schema：
    - 繼承 BaseSchema → uuid, is_active, is_deleted, audit 欄位
    - 再加上 TemplateField 自身欄位
    """

    template_uuid: UUID
    field_key: str
    label: str
    field_type: str
    required: bool
    options: Optional[List[Any]]
    sort_order: int

    # 如果你之後有額外欄位（例如 placeholder / help_text / config）
    # 可在這裡追加

    model_config = {"from_attributes": True}
