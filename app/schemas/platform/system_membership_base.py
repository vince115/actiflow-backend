# app/schemas/platform/system_membership_base.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class SystemMembershipBase(BaseModel):
    """
    平台層級角色（非 organizer 成員）
    """

    user_uuid: UUID
    role: str                      # super_admin / system_admin / support / auditor
    is_active: bool = True

    assigned_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
