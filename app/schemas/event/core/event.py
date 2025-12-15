# app/schemas/event/core/event.py

from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


# ------------------------------------------------------------
# Base Schema (shared by response)
# ------------------------------------------------------------
class EventBase(BaseModel):
    uuid: UUID                       # PK（由 BaseModel 提供）
    event_code: str                  # 新增：外部用活動代號

    organizer_uuid: UUID
    activity_template_uuid: Optional[UUID] = None

    name: str
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    location: Optional[str] = None
    banner_url: Optional[HttpUrl] = None

    config: Dict[str, Any] = {}
    status: str = "draft"

    # Common status fields
    is_active: bool = True
    is_deleted: bool = False

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None


# ------------------------------------------------------------
# Create Event（前端送這些資料即可）
# ------------------------------------------------------------
class EventCreate(BaseModel):
    event_code: str                      # 新增：建立活動時前端要提供業務代號

    name: str
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    location: Optional[str] = None
    banner_url: Optional[HttpUrl] = None

    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = "draft"

    organizer_uuid: UUID
    activity_template_uuid: UUID


# ------------------------------------------------------------
# Update Event（部分欄位可更新）
# ------------------------------------------------------------
class EventUpdate(BaseModel):
    # event_code ❌ 移除（避免業務代碼被亂改）
    name: Optional[str] = None
    description: Optional[str] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None

    location: Optional[str] = None
    banner_url: Optional[HttpUrl] = None

    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


# ------------------------------------------------------------
# Response
# ------------------------------------------------------------
class EventResponse(EventBase):
    class Config:
        from_attributes = True
