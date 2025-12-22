# app/schemas/event/core/organizer/organizer_event_update.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class OrganizerEventUpdate(BaseModel):
    """
    Organizer scoped Event Update schema

    用於 Organizer 後台更新 Event 的「可編輯欄位」
    - 不允許直接變更 organizer_uuid / event_code
    - 不處理狀態轉換（status 由 command API 控制）
      - publish_event
      - unpublish_event
      - close_event
    """

    activity_template_uuid: Optional[UUID] = None

    name: Optional[str] = None
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    # ⚠️ status 僅允許 internal update（實務上應由 guard 限制）
    status: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    # 軟開關（管理用途）
    #is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }
