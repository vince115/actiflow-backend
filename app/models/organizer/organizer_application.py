# app/models/organizer/organizer_application.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base.base_model import BaseModel


class OrganizerApplication(BaseModel, Base):
    """
    User 申請成為 Organizer（建立新主辦單位）
    審核後才會真的建立 Organizer
    """

    __tablename__ = "organizer_applications"

    # ---------------------------------------------------------
    # 申請者
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", lazy="selectin")

    # ---------------------------------------------------------
    # 申請內容（未建立 Organizer 前都先暫存）
    # ---------------------------------------------------------
    application_data = Column(
        JSONB,
        default=lambda: {},
        nullable=False
    )
    # 例如：
    # {
    #   "name": "...",
    #   "email": "...",
    #   "phone": "...",
    #   "website": "...",
    #   "description": "...",
    #   "address": { ... }
    # }

    # ---------------------------------------------------------
    # 審核狀態
    # ---------------------------------------------------------
    status = Column(String, default="pending")  # pending / approved / rejected
    reason = Column(String, nullable=True)

    submitted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    reviewer_uuid = Column(UUID(as_uuid=True), nullable=True)
    reviewer_role = Column(String, nullable=True)