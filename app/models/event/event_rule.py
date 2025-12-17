# app/models/event/event_rule.py

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
    from app.models.event.event import Event
    from app.models.activity.activity_rule import ActivityRule
# ---------------------------------------------------------
class EventRule(BaseModel, Base):
    """
    活動最終使用的規則（從 ActivityRule 複製而來）
    """

    __tablename__ = "event_rules"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 外鍵：規則庫（複製來源）
    # ---------------------------------------------------------
    rule_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        ForeignKey("activity_rules.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ---------------------------------------------------------
    # 規則名稱 + 描述（複製靜態）
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    # ---------------------------------------------------------
    # 規則設定（複製後可修改）
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        back_populates="rules",
        lazy="selectin",
    )

    activity_rule: Mapped[Optional["ActivityRule"]] = relationship(
        lazy="selectin",
    )
