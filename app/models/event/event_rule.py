# app/models/event/event_rule.py

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventRule(BaseModel, Base):
    """
    活動最終使用的規則（從 ActivityTemplateRule 複製而來）
    用於：
    - 活動參加條件
    - 報名驗證
    - 活動安全規範
    - 年齡 / 性別 / 身份限制
    """

    __tablename__ = "event_rules"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 外鍵：規則庫（複製來源）
    # ---------------------------------------------------------
    rule_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("activity_rules.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # ---------------------------------------------------------
    # 規則名稱 + 描述（複製靜態）
    # ---------------------------------------------------------
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    # ---------------------------------------------------------
    # 規則設定（複製後可修改，不影響模板）
    # e.g. {"age_min": 18, "age_max": 60}
    # e.g. {"requires_medical": true}
    # e.g. {"team_size_min": 2}
    # ---------------------------------------------------------
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="rules",
        lazy="selectin"
    )

    activity_rule = relationship(
        "ActivityRule",
        lazy="selectin"
    )
