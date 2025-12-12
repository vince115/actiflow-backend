# app/models/auth/email_verification.py

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EmailVerification(BaseModel, Base):
    """
    郵件驗證紀錄
    """
    __tablename__ = "email_verifications"

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
    # 郵件驗證資訊
    # ---------------------------------------------------------
    email = Column(String, nullable=False, index=True)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user = relationship(
        "User",
        back_populates="email_verifications",
        lazy="selectin"
    )