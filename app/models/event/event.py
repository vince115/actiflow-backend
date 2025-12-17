# app/models/event/event.py （活動主表）

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
    from app.models.organizer.organizer import Organizer
    from app.models.activity.activity_template import ActivityTemplate
    from app.models.event.event_price import EventPrice
    from app.models.event.event_field import EventField
    from app.models.event.event_price import EventPrice
    from app.models.event.event_media import EventMedia
    from app.models.event.event_question import EventQuestion
    from app.models.event.event_rule import EventRule
    from app.models.event.event_schedule import EventSchedule
    from app.models.event.event_staff import EventStaff
    from app.models.event.event_report import EventReportCache
    from app.models.event.event_ticket import EventTicket
    from app.models.submission.submission import Submission
# ---------------------------------------------------------

class Event(BaseModel, Base):
    """
    活動主表（企業級）
    - id / uuid：由 BaseModel 提供（PK）
    - event_code：業務代號（例如 EVT-2025-001）
    - organizer_uuid：主辦單位
    - activity_template_uuid：所套用的活動模板
    """
    __tablename__ = "events"

    # ---------------------------------------------------------
    # 業務用活動代號（外部顯示、不變）
    # ---------------------------------------------------------
    event_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # 活動狀態：draft / published / closed
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
        index=True,
    )

    # ---------------------------------------------------------
    # 外鍵：主辦單位
    # ---------------------------------------------------------
    organizer_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organizer: Mapped["Organizer"] = relationship(
        back_populates="events",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # 外鍵：所套用的活動模板
    # ---------------------------------------------------------
    activity_template_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("activity_templates.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    activity_template: Mapped[Optional["ActivityTemplate"]] = relationship(
        back_populates="events",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # 活動基本資訊
    # ---------------------------------------------------------
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # 報名截止日
    registration_deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # 活動其他設定
    config: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict,
    )


    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    fields: Mapped[List["EventField"]] = relationship(
        "EventField",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    media: Mapped[List["EventMedia"]] = relationship(
        "EventMedia",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    prices: Mapped[List["EventPrice"]] = relationship(
        "EventPrice",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    questions: Mapped[List["EventQuestion"]] = relationship(
        "EventQuestion",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    rules: Mapped[List["EventRule"]] = relationship(
        "EventRule",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    schedules: Mapped[List["EventSchedule"]] = relationship(
        "EventSchedule",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    staffs: Mapped[List["EventStaff"]] = relationship(
        "EventStaff",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    report_cache: Mapped[Optional["EventReportCache"]] = relationship(
        "EventReportCache",
        back_populates="event",
        uselist=False,
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    tickets: Mapped[List["EventTicket"]] = relationship(
        "EventTicket",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="event",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


    