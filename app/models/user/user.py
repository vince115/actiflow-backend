# app/models/user/user.py

# ---------------------------------------------------------
# Standard Model Header (SQLAlchemy 2.0)
# ---------------------------------------------------------
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
)
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
    """
    系統使用者（帳號主體）

    設計原則：
    - User 只保存「狀態」
    - 所有一次性流程（email 驗證、reset、session）都在獨立表
    """

    __tablename__ = "users"

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
        comment="使用者登入 email",
    )

    # ---------------------------------------------------------
    # Email verification STATE（最終狀態）
    # ---------------------------------------------------------
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        comment="是否已完成 email 驗證",
    )

    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="email 驗證完成時間",
    )

    # ---------------------------------------------------------
    # Account status
    # ---------------------------------------------------------
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
        comment="帳號是否啟用",
    )

    # ---------------------------------------------------------
    # Relationships（保留完整系統關聯）
    # ---------------------------------------------------------
    profile: Mapped[Optional["UserProfile"]] = relationship(
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )

    system_memberships: Mapped[List["SystemMembership"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    organizer_memberships: Mapped[List["OrganizerMembership"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    submissions: Mapped[List["Submission"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    #   EmailVerification 是 流程紀錄不再天然屬於 User
    # email_verifications: Mapped[List["EmailVerification"]] = relationship(
    #     back_populates="user",
    #     cascade="all, delete-orphan",
    #     lazy="selectin",
    # )

    password_resets: Mapped[List["PasswordReset"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    sessions: Mapped[List["UserSession"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    auth_logs: Mapped[List["AuthLog"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    settings: Mapped[Optional["UserSettings"]] = relationship(
        back_populates="user",
        uselist=False,
        lazy="selectin",
    )

    event_staffs: Mapped[List["EventStaff"]] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    # ---------------------------------------------------------
    # Timestamp
    # ---------------------------------------------------------
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default="CURRENT_TIMESTAMP",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
