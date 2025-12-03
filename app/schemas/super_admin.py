# app/schemas/super_admin.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


# ------------------------------------------------------------
# Base（回傳用）
# ------------------------------------------------------------
class SuperAdminBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None

    role: str = "super_admin"        # 目前只有 super_admin
    status: str = "active"           # active / suspended

    # 狀態欄位
    is_active: bool = True
    is_deleted: bool = False

    # Audit 欄位
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
# Create（建立用）
# ------------------------------------------------------------
class SuperAdminCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str
    phone: Optional[str] = None

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ------------------------------------------------------------
# Update（基本資料更新）
# ------------------------------------------------------------
class SuperAdminUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None      # active / suspended
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# ------------------------------------------------------------
# Update Role（調整角色用）
# 通常只有 system_admin / 根帳號會使用
# ------------------------------------------------------------
class SuperAdminUpdateRole(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# ------------------------------------------------------------
# Response（回傳用）
# ------------------------------------------------------------
class SuperAdminResponse(SuperAdminBase):
    uuid: UUID

    class Config:
        from_attributes = True
