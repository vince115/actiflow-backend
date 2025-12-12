# app/models/activity/activity_template_rule.py

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel


class ActivityTemplateRule(BaseModel, Base):

    __tablename__ = "activity_template_rules"

    template_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_templates.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    rule_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_rules.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 可選：規則參數覆寫
    config = Column(JSONB, default=lambda: {})

    # Relationship
    template = relationship("ActivityTemplate", back_populates="rules")
    rule = relationship("ActivityRule", back_populates="template_rules")
