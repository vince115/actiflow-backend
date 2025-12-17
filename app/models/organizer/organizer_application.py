# app/models/organizer/organizer_application.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
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

class OrganizerApplication(BaseModel, Base):
    """
    User 申請成為 Organizer（建立新主辦單位）
    審核後才會真的建立 Organizer
    """

    __tablename__ = "organizer_applications"

    # ---------------------------------------------------------
    # Applicant
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user: Mapped["User"] = relationship(
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Application data (JSON snapshot before Organizer creation)
    # ---------------------------------------------------------
    application_data: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Review status
    # ---------------------------------------------------------
    status: Mapped[str] = mapped_column(
        String,
        default="pending",  # pending / approved / rejected
    )

    reason: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reviewer_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        nullable=True,
    )

    reviewer_role: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
