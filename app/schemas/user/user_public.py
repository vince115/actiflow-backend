# app/schemas/user/user_public.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from uuid import UUID

from app.schemas.membership.organizer.organizer_membership_public import OrganizerMembershipPublic
from app.schemas.membership.system.system_membership_public import SystemMembershipPublic


class UserPublic(BaseModel):
    """
    前台 /auth/me 回傳登入者資訊（安全範圍內）
    """
    uuid: UUID
    email: EmailStr
    name: Optional[str] = None
    role: str = "user"

    memberships: List[
        Union[
            SystemMembershipPublic,
            OrganizerMembershipPublic,
        ]
    ] = Field(default_factory=list)

    model_config = {"from_attributes": True}
