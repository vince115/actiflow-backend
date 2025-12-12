# app/models/auth/auth_log.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
from app.models.base.base_model import BaseModel

class AuthLog(BaseModel, Base):
    """
    登入 / 登出 / refresh token / 驗證錯誤紀錄
    """
    __tablename__ = "auth_logs"

    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    event = Column(String, nullable=False)  
    """
    login_success
    login_failed
    logout
    refresh
    password_reset_request
    password_reset_success
    email_verified
    """

    ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    detail = Column(String, nullable=True)

    user = relationship("User", lazy="selectin")