# app/models/user/user_profile.py

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
# ---------------------------------------------------------

class UserProfile(BaseModel, Base):
    __tablename__ = "user_profiles"

    # ---------------------------------------------------------
    # 1:1 FK → User
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Profile fields
    # ---------------------------------------------------------
    birthday: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    address: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    school: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    employment: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    job_title: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    blood_type: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
        lazy="selectin",
    )
