# app/models/event/event_field.py

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
    from app.models.submission.submission_value import SubmissionValue
# ---------------------------------------------------------
class EventField(BaseModel, Base):
    """
    活動複製自模板的欄位（最終報名表單）
    """
    __tablename__ = "event_fields"

    # ---------------------------------------------------------
    # 外鍵：Event
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 基本欄位資訊（從 Template 複製）
    # ---------------------------------------------------------
    field_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    placeholder: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    field_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ---------------------------------------------------------
    # 選項與設定
    # ---------------------------------------------------------
    options: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )

    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    validation: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # 狀態
    # ---------------------------------------------------------
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        back_populates="fields",
        lazy="selectin",
    )

    submission_values: Mapped[list["SubmissionValue"]] = relationship(
        back_populates="field",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
