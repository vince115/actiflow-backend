# app/models/base/base_model.py

from uuid import UUID as PyUUID, uuid4
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column
from sqlalchemy.sql import func


@declarative_mixin
class BaseModel:
    """
    企業級 BaseModel（SQLAlchemy 2.x）
    所有資料表共通欄位
    """

    # ---------------------------------------------------------
    # Primary Key
    # ---------------------------------------------------------
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # ---------------------------------------------------------
    # Timestamps
    # ---------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ---------------------------------------------------------
    # Audit (Who did what)
    # ---------------------------------------------------------
    created_by: Mapped[PyUUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    updated_by: Mapped[PyUUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    deleted_by: Mapped[PyUUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    created_by_role: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    updated_by_role: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    deleted_by_role: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Optimistic Lock
    # ---------------------------------------------------------
    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )
