# app/schemas/organizer.py

from pydantic import BaseModel, HttpUrl, EmailStr, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


# --- Base (response/view 用) ---
class OrganizerBase(BaseModel):
    status: str = "active"
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)

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


# ----------------------
# 建立 Organizer（公司資料）
# ----------------------
class OrganizerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ----------------------
# 修改 Organizer
# ----------------------
class OrganizerUpdate(BaseModel):
    status: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    website: Optional[HttpUrl] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# ----------------------
# 回傳 Organizer
# ----------------------
class OrganizerResponse(OrganizerBase):
    uuid: UUID

    class Config:
        from_attributes = True
