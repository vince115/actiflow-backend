# app/models/organizer/organizer.py

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
    from app.models.event.event import Event
    from app.models.membership.organizer_membership import OrganizerMembership
# ---------------------------------------------------------

class Organizer(BaseModel, Base):
    """
    活動主辦單位（Organizer）
    - 企業級設計：id + uuid
    - uuid 為業務識別碼
    """

    __tablename__ = "organizers"

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------
    status: Mapped[str] = mapped_column(
        String,
        default="pending",  # pending / approved / rejected
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Organization profile (non-auth)
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    email: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    address: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    website: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Media
    # ---------------------------------------------------------
    logo_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    banner_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Config
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="organizer_memberships",
        viewonly=True,
        lazy="selectin",
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="organizer",
        lazy="selectin",
    )

    memberships: Mapped[list["OrganizerMembership"]] = relationship(
        "OrganizerMembership",
        back_populates="organizer",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
