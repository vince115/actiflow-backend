# app/schemas/event/core/organizer/organizer_event_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class OrganizerEventBase(BaseModel):
    """
    Organizer 後台 Event 核心欄位（Create / Update 共用）

    ❌ 不包含：
    - organizer_uuid（由後端 membership 注入）
    - event_code（由後端產生）
    - audit 欄位

    ✅ 僅包含 organizer 可管理的 domain 欄位
    """

    activity_template_uuid: UUID

    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    # 注意：實際狀態轉換需經過 guard
    status: str = "draft"

    config: Optional[Dict[str, Any]] = None

    model_config = {
        "from_attributes": True
    }
