# app/models/organizer_application.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from app.core.db import Base
from app.models.base_model import BaseModel


class OrganizerApplication(BaseModel, Base):
    """
    User 提交 Organizer 申請
    """
    __tablename__ = "organizer_applications"

    # 企業級 Primary Key
    application_uuid = Column(String, unique=True, nullable=False, index=True)

    # 申請者 user_uuid
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship("User")

    # 申請的 organizer
    organizer_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("organizers.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    organizer = relationship("Organizer")

    # 狀態
    status = Column(String, default="pending")   # pending / approved / rejected

    # 申請理由（選填）
    reason = Column(String, nullable=True)

    submitted_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewer_uuid = Column(UUID(as_uuid=True), nullable=True)
    reviewer_role = Column(String, nullable=True)
