# app/schemas/activity_type/activity_type_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any


class ActivityTypeBase(BaseModel):
    category_key: str                  # e.g. HIKING / MARATHON
    label: str                         # 顯示名稱
    description: Optional[str] = None
    color: Optional[str] = None        # 標籤顏色（可選）
    icon: Optional[str] = None         # Icon 名稱
    sort_order: int = 100              # 排序
    config: Optional[Dict[str, Any]] = None    # 進階設定