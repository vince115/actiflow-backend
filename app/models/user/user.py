# app/models/user/user.py

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
    Text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.base.base_model import BaseModel
# ---------------------------------------------------------
if TYPE_CHECKING:
    from app.models.user.user_profile import UserProfile
    from app.models.membership.system_membership import SystemMembership
    from app.models.membership.organizer_membership import OrganizerMembership
    from app.models.submission.submission import Submission
    from app.models.auth.refresh_token import RefreshToken
    from app.models.auth.email_verification import EmailVerification
    from app.models.auth.password_reset import PasswordReset
    from app.models.auth.user_session import UserSession
    from app.models.auth.auth_log import AuthLog
    from app.models.user.user_settings import UserSettings
    from app.models.event.event_staff import EventStaff
# ---------------------------------------------------------

class User(BaseModel, Base):
    __tablename__ = "users"

    # ---------------------------------------------------------
    # Account info
    # ---------------------------------------------------------
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        index=True,
    )

    avatar_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Auth
    # ---------------------------------------------------------
    auth_provider: Mapped[str] = mapped_column(
        String,
        default="local",
        nullable=False,
    )

    provider_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    password_hash: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    email_verification_token: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    email_verified_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_login_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ---------------------------------------------------------
    # Config
    # ---------------------------------------------------------
    config: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    system_membership: Mapped[Optional["SystemMembership"]] = relationship(
        "SystemMembership",
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )

    memberships: Mapped[list["OrganizerMembership"]] = relationship(
        "OrganizerMembership",
        back_populates="user",
        lazy="selectin",
    )

    submissions: Mapped[list["Submission"]] = relationship(
        "Submission",
        back_populates="user",
        lazy="selectin",
    )  

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Email verification records (1:N)
    # ---------------------------------------------------------
    email_verifications: Mapped[list["EmailVerification"]] = relationship(
        "EmailVerification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    #  Password reset records (1:N)
    # ---------------------------------------------------------
    password_resets: Mapped[list["PasswordReset"]] = relationship(
        "PasswordReset",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # User sessions (1:N)
    # ---------------------------------------------------------
    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Auth logs (1:N)
    # ---------------------------------------------------------
    auth_logs: Mapped[list["AuthLog"]] = relationship(
        "AuthLog",
        back_populates="user",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # User Settings
    # ---------------------------------------------------------
    settings: Mapped[Optional["UserSettings"]] = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # ---------------------------------------------------------

    event_staffs: Mapped[list["EventStaff"]] = relationship(
        "EventStaff",
        back_populates="user",
        lazy="selectin",
    )
