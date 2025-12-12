# app/schemas/system_membership/system_membership_create.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class SystemMembershipCreate(BaseModel):
    user_uuid: UUID
    role: str  # super_admin / system_admin / support / auditor

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None
