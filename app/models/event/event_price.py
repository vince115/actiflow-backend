# app/models/event/event_price.py

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
    Numeric,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.event.event import Event
    from app.models.event.event_ticket import EventTicket
# ---------------------------------------------------------

class EventPrice(BaseModel, Base):
    """
    活動價格表 / 票種表：
    - 早鳥 / 一般 / VIP
    - 不同身份（成人 / 學生）
    - 可設定名額、期限、條件
    """

    __tablename__ = "event_prices"

    # ---------------------------------------------------------
    # 外鍵：活動
    # ---------------------------------------------------------
    event_uuid: Mapped[PyUUID] = mapped_column(
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # 價格名稱（例如：早鳥票 / 一般票）
    # ---------------------------------------------------------
    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # 提交表單時使用的 key（例如：EARLY_BIRD）
    price_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    # 顯示排序（越小越前）
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ---------------------------------------------------------
    # 價格設定
    # ---------------------------------------------------------
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # 名額限制（None 表示無限制）
    quota: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )

    # 已售出（你之後會用在報名邏輯）
    sold: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # ---------------------------------------------------------
    # 期限設定（常用於早鳥票）
    # ---------------------------------------------------------
    start_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )
    end_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # 是否啟用這個價格
    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # ---------------------------------------------------------
    # 票種其他設定
    # 可放：
    #  - 身份分類限制（學生限定）
    #  - 需要提交證明文件
    #  - 優惠碼限制
    #  - 團報規則
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="prices",
        lazy="selectin",
    )

    tickets: Mapped[List["EventTicket"]] = relationship(
        "EventTicket",
        back_populates="price",
        lazy="selectin",
    )
