# app/schemas/event/core/event_base.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

# 前端 Event 核心欄位，不含 audit 與 uuid。
class EventBase(BaseModel):
    """
    Event 的核心欄位，不含 audit 與 uuid。
    """

    event_code: str
    organizer_uuid: UUID
    activity_template_uuid: Optional[UUID] = None

    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    status: str = "draft"                    # draft / published / closed

    config: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


# Organizer 後台 Event 核心欄位，不含 audit 與 uuid。
class OrganizerEventBase(BaseModel):
    """
    Organizer 後台建立/更新 Event 的核心欄位（不含 organizer_uuid / event_code / audit）
    - organizer_uuid：後端從 membership 注入
    - event_code：後端生成
    """

    activity_template_uuid: UUID

    name: str
    description: Optional[str] = None

    start_date: datetime
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    status: str = "draft"

    config: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}
