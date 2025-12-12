# app/models/event/event_ticket.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


class EventTicket(BaseModel, Base):
    """
    活動票券（報名者或團報成員所持的入場憑證）
    - 對應 event + submission + price(票種)
    - 可用於 QRCode 入場掃描
    """

    __tablename__ = "event_tickets"

    # ---------------------------------------------------------
    # 外鍵：Event
    # ---------------------------------------------------------
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 外鍵：Submission（主要購買者）
    # ---------------------------------------------------------
    submission_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("submissions.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 外鍵：票種（可為 None，若該活動沒有票種設定）
    # ---------------------------------------------------------
    price_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("event_prices.uuid", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # ---------------------------------------------------------
    # 票券資訊
    # ---------------------------------------------------------
    ticket_code = Column(String(100), unique=True, nullable=False, index=True)
    """
    建議格式：
    EVT-2025-00001-TK0001
    （或自動 uuid，但代碼更適合讓現場人員讀取）
    """

    # 票券使用者（可為團報成員，因此不一定等於 submission.user）
    holder_name = Column(String(255), nullable=False)
    holder_email = Column(String(255), nullable=True)
    holder_phone = Column(String(50), nullable=True)

    # 是否已入場（刷 QR）
    checked_in = Column(Boolean, default=False)
    checked_in_at = Column(DateTime, nullable=True)

    # 是否取消（退款 / 改期）
    is_cancelled = Column(Boolean, default=False)
    cancelled_at = Column(DateTime, nullable=True)

    # 票券狀態：valid / used / cancelled / expired
    status = Column(String(50), default="valid", nullable=False, index=True)

    # 額外資訊（座位號碼、分組、衣服尺寸、補給站編號等）
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="tickets",
        lazy="selectin"
    )

    submission = relationship(
        "Submission",
        back_populates="tickets",
        lazy="selectin"
    )

    price = relationship(
        "EventPrice",
        lazy="selectin"
    )
