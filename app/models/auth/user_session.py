# app/models/auth/user_session.py

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.core.db import Base
from app.models.base.base_model import BaseModel


class UserSession(BaseModel, Base):
    """
    使用者登入 Session（多裝置登入管理）
    - 紀錄每次 login 產生的 session
    - 可用於：設備管理、移除 session、異常登入偵測、後台審計
    """

    __tablename__ = "user_sessions"

    # ---------------------------------------------------------
    # 外鍵：User
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # Session 本體資訊
    # ---------------------------------------------------------

    # 例如：
    # Chrome on macOS
    # Mobile Safari on iPhone
    user_agent = Column(String, nullable=True)

    # IP address
    ip_address = Column(String, nullable=True)

    # Refresh token 的 UUID（非 token 本體）
    refresh_token_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("refresh_tokens.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Session 是否仍有效（登出後改為 False）
    is_active = Column(Boolean, default=True)

    # 最後一次使用時間（refresh 時更新）
    last_active_at = Column(DateTime, default=datetime.utcnow)

    # 自動登出時間（選用，看你是否要支援）
    expires_at = Column(DateTime, nullable=True)

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user = relationship(
        "User",
        back_populates="sessions",
        lazy="selectin"
    )

    refresh_token = relationship(
        "RefreshToken",
        lazy="selectin"
    )
