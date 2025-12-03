# app/schemas/activity_type.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


# --- Base (response/view 用) ---
class ActivityTypeBase(BaseModel):
    category_key: str
    label: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 100
    config: Dict[str, Any] = {}

    # --- 狀態欄位 ---
    is_active: bool = True
    is_deleted: bool = False

    # --- 稽核欄位 ---
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
class ActivityTypeCreate(BaseModel):
    category_key: str
    label: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str, Any]] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# --- Update ---
class ActivityTypeUpdate(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# --- Response ---
class ActivityTypeResponse(ActivityTypeBase):
    uuid: UUID

    class Config:
        from_attributes = True
