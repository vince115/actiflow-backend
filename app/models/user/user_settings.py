# app/models/user/user_settings.py

from sqlalchemy import Column, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class UserSettings(BaseModel, Base):
    """
    使用者個人偏好設定（1 對 1）
    """

    __tablename__ = "user_settings"

    # 使用 uuid 作為 FK（與全系統一致）
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )

    # --- 基本偏好設定 ---
    dark_mode = Column(Boolean, default=False)
    locale = Column(String, default="zh-Hant")

    # --- 通知設定 ---
    notify_email = Column(Boolean, default=True)
    notify_sms = Column(Boolean, default=False)
    notify_marketing = Column(Boolean, default=False)

    # --- 前端 UI 偏好 ---
    ui_preferences = Column(JSONB, default=lambda: {})

    # --- 其他可擴充設定 ---
    config = Column(JSONB, default=lambda: {})

    # 回到 User 的關聯
    user = relationship("User", back_populates="settings", lazy="selectin")