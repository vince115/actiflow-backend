# app/models/event/event_price.py

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.db import Base
from app.models.base.base_model import BaseModel


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
    event_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("events.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ---------------------------------------------------------
    # 價格名稱（例如：早鳥票 / 一般票）
    # ---------------------------------------------------------
    label = Column(String(255), nullable=False)

    # 提交表單時使用的 key（例如：EARLY_BIRD）
    price_key = Column(String(100), nullable=False, index=True)

    # 顯示排序（越小越前）
    sort_order = Column(Integer, default=0)

    # ---------------------------------------------------------
    # 價格設定
    # ---------------------------------------------------------
    price = Column(Numeric(10, 2), nullable=False)

    # 名額限制（None 表示無限制）
    quota = Column(Integer, nullable=True)

    # 已售出（你之後會用在報名邏輯）
    sold = Column(Integer, default=0)

    # ---------------------------------------------------------
    # 期限設定（常用於早鳥票）
    # ---------------------------------------------------------
    start_at = Column(DateTime, nullable=True)
    end_at = Column(DateTime, nullable=True)

    # 是否啟用這個價格
    is_enabled = Column(Boolean, default=True)

    # ---------------------------------------------------------
    # 票種其他設定
    # 可放：
    #  - 身份分類限制（學生限定）
    #  - 需要提交證明文件
    #  - 優惠碼限制
    #  - 團報規則
    # ---------------------------------------------------------
    config = Column(JSONB, default=lambda: {})

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    event = relationship(
        "Event",
        back_populates="prices",
        lazy="selectin"
    )
