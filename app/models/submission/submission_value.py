# app/models/submission_value.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class SubmissionValue(BaseModel, Base):
    """
    Submission 的欄位值
    """
    __tablename__ = "submission_values"

    submission_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    submission = relationship(
        "Submission",
        back_populates="values",
        lazy="selectin"
    )

    event_field_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("event_fields.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    field = relationship("EventField", back_populates="submission_values")

    field_key = Column(String, nullable=False)

    raw_value = Column(String, nullable=True)
    value = Column(JSONB, nullable=True)

    # 🔥 保留這個（搭配 SubmissionFile）
    files = relationship(
        "SubmissionFile",
        back_populates="submission_value",
        lazy="selectin",
        cascade="all, delete-orphan"
    )