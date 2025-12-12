# app/models/auth/refresh_token.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.db import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, unique=True, index=True)
    user_agent = Column(String, nullable=True)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expired_at = Column(DateTime)

    user = relationship("User", back_populates="refresh_tokens")

    user_sessions = relationship(
        "UserSession",
        back_populates="refresh_token",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
