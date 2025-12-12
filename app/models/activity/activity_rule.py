# app/models/activity/activity_rule.py

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel


class ActivityRule(BaseModel, Base):

    __tablename__ = "activity_rules"

    # 規則名稱
    name = Column(String(255), nullable=False)

    # 規則描述（人類可讀）
    description = Column(String, nullable=True)

    # JSON 格式的規則設定
    # e.g. {"age_min": 18, "age_max": 60, "requires_medical": true}
    config = Column(JSONB, default=lambda: {})

    # 是否啟用規則
    is_active = Column(Boolean, default=True)

    # Activity Template 使用這些規則
    template_rules = relationship(
        "ActivityTemplateRule",
        back_populates="rule",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
