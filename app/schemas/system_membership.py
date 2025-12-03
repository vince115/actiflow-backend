# app/schemas/system_membership.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# ------------------------------------------------------------
# Base (for view / response)
# ------------------------------------------------------------
class SystemMembershipBase(BaseModel):
    role: str = "support"       # system_admin / site_admin / support / auditor
    status: str = "active"      # active / suspended

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
# Create
# ------------------------------------------------------------
class SystemMembershipCreate(BaseModel):
    user_uuid: UUID
    role: str = "support"
    status: Optional[str] = "active"

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ------------------------------------------------------------
# Update
# ------------------------------------------------------------
class SystemMembershipUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None


# ------------------------------------------------------------
# Response
# ------------------------------------------------------------
class SystemMembershipResponse(SystemMembershipBase):
    uuid: UUID
    user_uuid: UUID

    class Config:
        from_attributes = True
