# app/schemas/user/user_profile_response.py

from typing import Optional
from uuid import UUID
from datetime import datetime

from .user_profile_base import UserProfileBase


class UserProfileResponse(UserProfileBase):
    """
    後台 / admin 使用，含系統欄位
    """

    uuid: UUID
    user_uuid: UUID

    is_active: bool
    is_deleted: bool

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None