# app/models/membership/organizer_membership.py

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
    from app.models.organizer.organizer import Organizer
# ---------------------------------------------------------


ORGANIZER_ROLES = (
    "owner",
    "admin",
    "editor",
    "viewer",
    "member",
)


class OrganizerMembership(BaseModel, Base):
    """
    使用者加入主辦單位的 Membership（多對多）
    - 一個 user 可以加入多個 organizer
    - 每個 organizer 內只能有一種角色
    """

    __tablename__ = "organizer_memberships"

    __table_args__ = (
        UniqueConstraint("user_uuid", "organizer_uuid", name="uq_user_organizer"),
    )

    # ---------------------------------------------------------
    # Foreign Keys
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organizer_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 組織內角色
    # ---------------------------------------------------------
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        default="member",
    )

    # ---------------------------------------------------------
    # 成員狀態（非資料列 is_active）
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
    # 擴充設定（例如：限定可管理哪些 event）
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        back_populates="memberships",
        lazy="selectin",
    )

    organizer: Mapped["Organizer"] = relationship(
        back_populates="memberships",
        lazy="selectin",
    )
