# app/schemas/user/user_profile_public.py

from .user_profile_base import UserProfileBase


class UserProfilePublic(UserProfileBase):
    """
    對外顯示的 UserProfile（/me/profile）
    """
    pass