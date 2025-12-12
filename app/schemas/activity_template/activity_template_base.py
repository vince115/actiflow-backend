# app/schemas/activity_template/activity_template_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class ActivityTemplateBase(BaseModel):
    """
    ActivityTemplate 的核心欄位（不含狀態與稽核欄位）
    給 Create / Update / Response 共用。
    """

    template_code: Optional[str] = None               # e.g. TPL-2025-001
    activity_type_uuid: UUID                          # FK to ActivityType.uuid
    name: str                                         # 模板名稱
    description: Optional[str] = None                 # 說明
    sort_order: int = 100                             # 排序
    config: Dict[str, Any] = {}                       # JSONB 設定（欄位順序、樣式）
