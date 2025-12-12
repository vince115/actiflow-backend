# app/schemas/system_membership/system_membership_base.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class SystemMembershipBase(BaseModel):
    """
    平台層級的角色關聯：
    - super_admin
    - system_admin
    - support
    - auditor
    """
    user_uuid: UUID
    role: str  # ex: super_admin / system_admin / support / auditor

    # 狀態欄位
    is_active: bool = True
    is_deleted: bool = False

    # 稽核欄位
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_by: Optional[str] = None

    created_by_role: Optional[str] = None
    updated_by_role: Optional[str] = None
    deleted_by_role: Optional[str] = None
