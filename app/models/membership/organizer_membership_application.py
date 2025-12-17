# app/models/membership/organizer_membership_application.py

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


MEMBERSHIP_APPLICATION_STATUS = (
    "pending",
    "approved",
    "rejected",
)


class OrganizerMembershipApplication(BaseModel, Base):
    """
    使用者申請加入 Organizer 的申請紀錄（Application / Process）

    狀態流：
    - pending   → 等待 Organizer 審核
    - approved  → 建立 OrganizerMembership
    - rejected  → 結案
    """

    __tablename__ = "organizer_membership_applications"

    # ---------------------------------------------------------
    # Foreign Keys
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    organizer_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Requested role
    # ---------------------------------------------------------
    requested_role: Mapped[str] = mapped_column(
        String,
        default="member",
    )

    # ---------------------------------------------------------
    # Application status
    # ---------------------------------------------------------
    status: Mapped[str] = mapped_column(
        String,
        default="pending",
        index=True,
    )

    # ---------------------------------------------------------
    # Review info
    # ---------------------------------------------------------
    reviewed_by: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )

    reviewed_by_role: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    rejection_reason: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Extra data
    # ---------------------------------------------------------
    extra_data: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        "User",
        lazy="selectin",
    )

    organizer: Mapped["Organizer"] = relationship(
        "Organizer",
        lazy="selectin",
    )
