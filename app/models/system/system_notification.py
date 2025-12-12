# app/models/system/system_notification.py

from sqlalchemy import Column, String, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class SystemNotification(BaseModel, Base):
    """
    全平台公告（維護、更新、重要訊息）
    """

    __tablename__ = "system_notifications"

    # 企業外部代碼
    notification_code = Column(String, unique=True, nullable=False, index=True)

    # 標題與內容
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    # 等級（通知類型）
    level = Column(
        String,
        nullable=False,
        default="info"  # info / warning / critical / success
    )

    # 是否公開顯示在前台
    is_published = Column(Boolean, default=False)

    # 額外設定，如：前台顯示方式、有效日期
    config = Column(JSONB, default=lambda: {})

    # 時間戳
    published_at = Column(DateTime(timezone=True), nullable=True)