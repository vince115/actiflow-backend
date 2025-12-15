# app/schemas/user/user_settings_public.py

from .user_settings_base import UserSettingsBase


class UserSettingsPublic(UserSettingsBase):
    """
    對外顯示的 UserSettings（/me/settings）
    """
    pass
