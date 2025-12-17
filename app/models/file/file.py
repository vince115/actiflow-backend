# app/models/file/file.py

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
    from app.models.submission.submission_file import SubmissionFile
# ---------------------------------------------------------


class File(BaseModel, Base):
    """
    企業級 File Storage
    - 可被 Submission / Event / User / Media 等模組共用
    """

    __tablename__ = "files"

    # ---------------------------------------------------------
    # File 基本資訊
    # ---------------------------------------------------------
    url: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    name: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    mime_type: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    size_bytes: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    submissions: Mapped[list["SubmissionFile"]] = relationship(
        back_populates="file",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
