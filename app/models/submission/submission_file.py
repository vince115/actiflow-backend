# app/models/submission/submission_file.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class SubmissionFile(BaseModel, Base):
    """
    Submission file model
    檔案附加在 submission 上的中介表：
    - 一個 submission 可以有多個檔案
    - 一個 file 可能被不同 submission 使用（取決於你的架構）
    """
    __tablename__ = "submission_files"

    # Submission UUID
    submission_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    submission = relationship(
        "Submission", 
        back_populates="files", 
        lazy="selectin"
    )

    # 所屬欄位（哪個 EventField 的 File input）
    submission_value_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("submission_values.uuid", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    submission_value = relationship(
        "SubmissionValue",
        back_populates="files",
        lazy="selectin"
    )


    # File UUID
    file_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("files.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    file = relationship(
        "File",
        back_populates="submissions",
        lazy="selectin"
    )
    uploaded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )