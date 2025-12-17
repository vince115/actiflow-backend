# app/models/activity/activity_rule.py

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
    from app.models.activity.activity_template_rule import ActivityTemplateRule
# ---------------------------------------------------------
class ActivityRule(BaseModel, Base):
    __tablename__ = "activity_rules"

    # ---------------------------------------------------------
    # 規則基本資訊
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # JSON 規則設定
    # e.g. {"age_min": 18, "age_max": 60, "requires_medical": true}
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # 是否啟用規則
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    template_rules: Mapped[list["ActivityTemplateRule"]] = relationship(
        "ActivityTemplateRule",
        back_populates="rule",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
