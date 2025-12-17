# app/models/event/event_ticket.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import Optional, TYPE_CHECKING
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
    from app.models.event.event_price import EventPrice
    from app.models.submission.submission import Submission
# ---------------------------------------------------------

class EventTicket(BaseModel, Base):
    """
    活動票券（報名者或團報成員所持的入場憑證）
    """

    __tablename__ = "event_tickets"

    # ---------------------------------------------------------
    # Foreign Keys
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    submission_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    price_uuid: Mapped[Optional[PyUUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("event_prices.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # ---------------------------------------------------------
    # Ticket Info
    # ---------------------------------------------------------
    ticket_code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    holder_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    holder_email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    holder_phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------
    checked_in: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    checked_in_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    is_cancelled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    cancelled_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="valid",
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Extra
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        server_default="{}",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="tickets",
        lazy="selectin",
    )

    price: Mapped[Optional["EventPrice"]] = relationship(
        "EventPrice",
        back_populates="tickets",
        lazy="selectin",
    )

    submission: Mapped["Submission"] = relationship(
        "Submission",
        back_populates="tickets",
        lazy="selectin",
    )   
