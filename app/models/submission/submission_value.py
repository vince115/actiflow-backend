# app/models/submission/submission_value.py

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
    from app.models.event.event_field import EventField
    from app.models.submission.submission import Submission
    from app.models.submission.submission_file import SubmissionFile
# ---------------------------------------------------------

class SubmissionValue(BaseModel, Base):
    """
    Submission 的欄位值
    - 對應一個 EventField
    - 可附帶多個 SubmissionFile（例如上傳附件）
    """
    __tablename__ = "submission_values"

    # ---------------------------------------------------------
    # Submission reference
    # ---------------------------------------------------------
    submission_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    submission: Mapped["Submission"] = relationship(
        back_populates="values",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Event field reference
    # ---------------------------------------------------------
    event_field_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("event_fields.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    field: Mapped["EventField"] = relationship(
        back_populates="submission_values",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Field value
    # ---------------------------------------------------------
    field_key: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    raw_value: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    value: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Files (attachments)
    # ---------------------------------------------------------
    files: Mapped[list["SubmissionFile"]] = relationship(
        back_populates="submission_value",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
