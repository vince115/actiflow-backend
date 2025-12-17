# app/models/activity/activity_template_rule.py

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
    from app.models.activity.activity_template import ActivityTemplate
    from app.models.activity.activity_rule import ActivityRule
# ---------------------------------------------------------


class ActivityTemplateRule(BaseModel, Base):
    __tablename__ = "activity_template_rules"

    # ---------------------------------------------------------
    # 外鍵：ActivityTemplate
    # ---------------------------------------------------------
    template_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("activity_templates.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 外鍵：ActivityRule
    # ---------------------------------------------------------
    rule_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("activity_rules.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 規則參數覆寫（JSON）
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    template: Mapped["ActivityTemplate"] = relationship(
        "ActivityTemplate",
        back_populates="rules",
        lazy="selectin",
    )

    rule: Mapped["ActivityRule"] = relationship(
        "ActivityRule",
        back_populates="template_rules",
        lazy="selectin",
    )
