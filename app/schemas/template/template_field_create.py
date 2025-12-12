# app/schemas/template/template_field_create.py

from pydantic import BaseModel
from typing import Optional, List, Any
from uuid import UUID


class TemplateFieldCreate(BaseModel):
    """
    建立 TemplateField 用 Schema。
    template_uuid 必填，用來掛在某個 ActivityTemplate 下。
    """

    template_uuid: UUID
    field_key: str
    label: str
    field_type: str
    required: bool = False
    options: Optional[List[Any]] = None
    sort_order: int = 0
