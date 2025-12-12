# app/models/system/system_settings.py

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from app.core.db import Base
from app.models.base.base_model import BaseModel

class SystemSettings(BaseModel, Base):
    """
    平台級系統設定（僅 super_admin 可修改）
    - 使用 BaseModel.uuid 做唯一識別
    - 系統通常只有一筆設定（未來可擴充版本化）
    """

    __tablename__ = "system_settings"

    # 平台名稱
    site_name = Column(String(255), default="ActiFlow")

    # LOGO
    logo_url = Column(String(500), nullable=True)

    # 客服/聯絡 Email
    support_email = Column(String(255), nullable=True)

    # 自訂設定（theme, SEO, SMTP config, OAuth provider config）
    config = Column(JSONB, default=lambda: {})

    # 是否為目前使用版本
    is_active = Column(Boolean, default=True)

    # 設定版本號（配合 SystemConfigVersion 使用）
    version = Column(Integer, default=1)