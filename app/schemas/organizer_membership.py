# app/schemas/organizer_membership.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


# --- Base (response/view 用) ---
class OrganizerMembershipBase(BaseModel):
    role: str = "member"         # owner / admin / editor / viewer / member
    status: str = "active"       # active / suspended
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
# Create （POST Body）
# ※ organizer_uuid 不需要出現在 Body（由 URL path 提供）
# ------------------------------------------------------------
class OrganizerMembershipCreate(BaseModel):
    user_uuid: UUID
    role: str = "member"
    status: Optional[str] = "active"

    created_by: Optional[str] = None
    created_by_role: Optional[str] = None


# ------------------------------------------------------------
# Update
# ------------------------------------------------------------
class OrganizerMembershipUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

    updated_by: Optional[str] = None
    updated_by_role: Optional[str] = None

    model_config = {"from_attributes": True}


# ------------------------------------------------------------
# Response
# ------------------------------------------------------------
class OrganizerMembershipResponse(OrganizerMembershipBase):
    uuid: UUID
    organizer_uuid: UUID
    user_uuid: UUID

    model_config = {"from_attributes": True}
