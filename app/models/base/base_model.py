# app/models/base/base_model.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


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
        nullable=False,
        index=True
    )

    # 狀態
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    # 時間戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # 行為記錄
    created_by = Column(UUID(as_uuid=True), nullable=True, index=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True, index=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True, index=True)

    created_by_role = Column(String, nullable=True)
    updated_by_role = Column(String, nullable=True)
    deleted_by_role = Column(String, nullable=True)

    # 版本號（可選，用於 optimistic locking）
    version = Column(Integer, default=1, nullable=False)
