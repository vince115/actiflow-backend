# app/models/submission/submission.py

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
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import sqlalchemy as sa

from app.core.db import Base
from app.models.base.base_model import BaseModel
from app.models.submission.enums import SubmissionStatus
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.event.event import Event
    from app.models.user.user import User
    from app.models.submission.submission_value import SubmissionValue
    from app.models.event.event_ticket import EventTicket
    from app.models.submission.submission_file import SubmissionFile
# ---------------------------------------------------------

class Submission(BaseModel, Base):
    """
    報名紀錄模型
    """
    __tablename__ = "submissions"

    __table_args__ = (
        sa.UniqueConstraint(
            "event_uuid",
            "submission_code",
            name="uq_submission_event_code",
        ),
    )

    # ---------------------------------------------------------
    # Business identifiers
    # ---------------------------------------------------------
    submission_code: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Event reference
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="submissions",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Applicant info
    # ---------------------------------------------------------
    user_email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    user_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="submissions",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------
    status:Mapped[SubmissionStatus] = mapped_column(
        SAEnum(SubmissionStatus, name="submission_status"),
        default=SubmissionStatus.pending,
        nullable=False,
    )

    status_reason: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Internal notes
    # ---------------------------------------------------------
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Security / audit info
    # ---------------------------------------------------------
    ip_address: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ---------------------------------------------------------
    # Extra data
    # ---------------------------------------------------------
    extra_data: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        server_default="{}",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------


    values: Mapped[list["SubmissionValue"]] = relationship(
        "SubmissionValue",
        back_populates="submission",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    tickets: Mapped[list["EventTicket"]] = relationship(
        "EventTicket",
        back_populates="submission",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    files: Mapped[list["SubmissionFile"]] = relationship(
        "SubmissionFile",
        back_populates="submission",
        lazy="selectin",
        cascade="all, delete-orphan",
    )