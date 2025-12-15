# app/schemas/membership/system_membership_create.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SystemMembershipCreate(BaseModel):
    user_uuid: UUID
    role: str = "user"
    status: Optional[str] = "active"

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None
