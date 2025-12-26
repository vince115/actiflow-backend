# app/models/membership/system_membership.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.user.user import User
# ---------------------------------------------------------


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
    - 企業級 RBAC
    - 每個 User 僅允許一筆 system role
    """

    __tablename__ = "system_memberships"

    __table_args__ = (
        UniqueConstraint("user_uuid", name="uq_system_user"),
    )

    # ---------------------------------------------------------
    # Foreign Key → User
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Platform role
    # ---------------------------------------------------------
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # User status（非 BaseModel 的 is_active）
    # ------------------------------------------------selector
    # ---------------------------------------------------------
    is_suspended: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    suspended_reason: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Config（平台權限、功能開關、UI 模式）
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        back_populates="system_memberships",
        lazy="selectin",
    )