# app/schemas/membership/organizer_membership_base.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizerMembershipBase(BaseModel):
    role: str = "member"        # owner / admin / editor / viewer / member
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

    model_config = {"from_attributes": True}
