# app/schemas/user/user_response.py

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

from app.schemas.user.user_base import UserBase
from app.schemas.user.user_settings_response import UserSettingsResponse
from app.schemas.membership.organizer.organizer_membership_public import OrganizerMembershipPublic
from app.schemas.common.base import BaseSchema


class UserResponse(UserBase, BaseSchema):
    """
    完整使用者資料（後台 / Auth 用）
    """

    uuid: UUID
    role: str                      # user / organizer / system_admin / super_admin
    is_active: bool = True

    settings: Optional[UserSettingsResponse] = None
    memberships: List[OrganizerMembershipPublic] = []

    model_config = {"from_attributes": True}
