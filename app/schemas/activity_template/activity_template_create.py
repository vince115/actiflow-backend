# app/schemas/activity_template/activity_template_create.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class ActivityTemplateCreate(BaseModel):
    """
    用於建立新的 ActivityTemplate。
    created_by 由後端透過 current_user 注入。
    """

    activity_type_uuid: UUID
    name: str
    description: Optional[str] = None
    template_code: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
