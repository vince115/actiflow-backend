# app/schemas/activity_template/activity_template_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class ActivityTemplateUpdate(BaseModel):
    """
    允許更新的欄位。
    updated_by 由後端自動處理，不由前端提供。
    """

    activity_type_uuid: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    template_code: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str,Any]] = None
    is_active: Optional[bool] = None
