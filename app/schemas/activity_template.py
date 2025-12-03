# app/schemas/activity_template.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


# --- Base (response/view 用) ---
class ActivityTemplateBase(BaseModel):
    template_uuid: str
    name: str
    description: Optional[str] = None
    config: Dict[str, Any] = {}

    sort_order: int = 100

    # 狀態欄位
    is_active: bool = True
    is_deleted: bool = False

    # 審計欄位
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None  # super_admin / organizer
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None


# --- Create ---
class ActivityTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    # 新增：排序欄位
    sort_order: Optional[int] = 100

    # FK
    activity_type_uuid: UUID

    # 建立人資訊（可由後端自動帶入）
    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# --- Update ---
class ActivityTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    sort_order: Optional[int] = None
    
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# --- Response ---
class ActivityTemplateResponse(ActivityTemplateBase):
    uuid: UUID
    activity_type_uuid: UUID

    class Config:
        from_attributes = True
