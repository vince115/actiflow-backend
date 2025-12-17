# app/models/submission/submission_file.py

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
    from app.models.submission.submission import Submission
    from app.models.submission.submission_value import SubmissionValue
    from app.models.file.file import File
# ---------------------------------------------------------

class SubmissionFile(BaseModel, Base):
    """
    Submission 檔案中介表（Attachment / Upload）
    - 一個 Submission 可有多個檔案
    - 一個 SubmissionValue（欄位）也可附多個檔案
    - File 為實體檔案（可被多處引用）
    """
    __tablename__ = "submission_files"

    # ---------------------------------------------------------
    # Submission
    # ---------------------------------------------------------
    submission_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    submission: Mapped["Submission"] = relationship(
        back_populates="files",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Optional: belongs to which field (file input)
    # ---------------------------------------------------------
    submission_value_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("submission_values.uuid", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    submission_value: Mapped[Optional["SubmissionValue"]] = relationship(
        back_populates="files",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # File entity
    # ---------------------------------------------------------
    file_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("files.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file: Mapped["File"] = relationship(
        back_populates="submissions",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
