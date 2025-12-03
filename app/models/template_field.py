# app/models/template_field.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.db import Base
from app.models.base_model import BaseModel


class TemplateField(BaseModel, Base):
    __tablename__ = "template_fields"

    # -----------------------------
    # Foreign Key → ActivityTemplate
    # -----------------------------
    template_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_templates.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # -----------------------------
    # Field Properties
    # -----------------------------
    field_key = Column(String(100), nullable=False)          # ex: "email"
    label = Column(String(255), nullable=False)              # ex: "聯絡信箱"
    placeholder = Column(String(255), nullable=True)         # ex: "請輸入 Email"
    description = Column(Text, nullable=True)                # 額外說明（可選）

    field_type = Column(String(50), nullable=False)          # text/email/select/file/date...

    required = Column(Boolean, default=False)
    options = Column(JSONB, default=lambda: [])              # select options ex: ["A", "B", "C"] for select
    sort_order = Column(Integer, default=0)

    # -----------------------------
    # Relationship
    # -----------------------------
    template = relationship(
        "ActivityTemplate",
        back_populates="fields",
        lazy="selectin",
    )
