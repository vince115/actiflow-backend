# app/models/activity/activity_template_field.py

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
from app.models.base.base_model import BaseModel


class ActivityTemplateField(BaseModel, Base):
    __tablename__ = "activity_template_fields"

    template_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_templates.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    field_key = Column(String(100), nullable=False)
    label = Column(String(255), nullable=False)
    placeholder = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    field_type = Column(String(50), nullable=False)
    required = Column(Boolean, default=False)

    validation = Column(JSONB, default=lambda: {})
    config = Column(JSONB, default=lambda: {})

    is_enabled = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)

    template = relationship(
        "ActivityTemplate",
        back_populates="fields",
        lazy="selectin"
    )

    options_rel = relationship(
        "ActivityTemplateFieldOption",
        back_populates="field",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
