# app/models/base_model.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.dialects.postgresql import UUID


@declarative_mixin
class BaseModel:
    """
    企業級 BaseModel（所有資料表共通欄位）
    """

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    uuid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        nullable=False
    )

    # 狀態欄位
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    # 時間欄位
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # 行為記錄
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)

    created_by_role = Column(String, nullable=True)
    updated_by_role = Column(String, nullable=True)
    deleted_by_role = Column(String, nullable=True)
