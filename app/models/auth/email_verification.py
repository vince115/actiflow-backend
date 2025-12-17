# app/models/auth/email_verification.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import List, Optional,TYPE_CHECKING
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
    from app.models.user.user import User
# ---------------------------------------------------------

class EmailVerification(BaseModel, Base):
    """
    郵件驗證紀錄
    """

    __tablename__ = "email_verifications"

    # ---------------------------------------------------------
    # Foreign Key → User
    # ---------------------------------------------------------
    user_uuid: Mapped[PyUUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Verification info
    # ---------------------------------------------------------
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
    )

    token: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_verifications",
        lazy="selectin",
    )
