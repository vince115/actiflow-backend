# app/models/submission_value.py

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base_model import BaseModel


class SubmissionValue(BaseModel, Base):
    """
    Submission 的欄位值（一筆 submission 對應多個 value）
    - 使用 BaseModel 提供 uuid / audit 欄位
    """
    __tablename__ = "submission_values"

    # ---------------------------------------------------------
    # 外鍵：對應哪一筆 Submission
    # ---------------------------------------------------------
    submission_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    submission = relationship("Submission", back_populates="values", lazy="selectin")

    # ---------------------------------------------------------
    # 外鍵：對應哪一個 EventField（動態欄位定義）
    # ---------------------------------------------------------
    event_field_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("event_fields.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    field = relationship("EventField", lazy="selectin")

    # field_key 由 EventField 自動帶出，不允許前端指定
    field_key = Column(String, nullable=False)

    # 支援多型態（文字、數字、選項、checkbox array…）
    value = Column(JSONB, nullable=True)

    uploaded_file = Column(String, nullable=True)
