# app/models/membership/system_membership.py

from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


SYSTEM_ROLES = (
    "super_admin",
    "system_admin",
    "site_admin",
    "support",
    "auditor",
)


class SystemMembership(BaseModel, Base):
    """
    平台層級會員角色（非 Organizer）
    企業級 RBAC：每個 User 僅一筆系統角色
    """

    __tablename__ = "system_memberships"

    __table_args__ = (
        UniqueConstraint("user_uuid", name="uq_system_user"),
    )

    # ---------------------------------------------------------
    # Foreign Key
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # Platform role（使用 String，避免 Enum deploy 問題）
    # ---------------------------------------------------------
    role = Column(
        String,
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # User status
    # ---------------------------------------------------------
    is_suspended = Column(Boolean, default=False)
    suspended_reason = Column(String, nullable=True)

    # ---------------------------------------------------------
    # Config（允許平台登入 / UI 權限等）
    # ---------------------------------------------------------
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user = relationship("User", back_populates="system_membership")