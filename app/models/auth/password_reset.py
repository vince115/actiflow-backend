# app/models/auth/password_reset.py 

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base
from app.models.base.base_model import BaseModel


class PasswordReset(BaseModel, Base):
    """
    密碼重設 Token（一次性）
    - 使用時失效（或過期失效）
    """

    __tablename__ = "password_resets"

    # ---------------------------------------------------------
    # 外鍵：User
    # ---------------------------------------------------------
    user_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 重設目標 email
    email = Column(String, nullable=False, index=True)

    # 存放加密或原生 token 字串（你會寄給使用者的那個）
    token = Column(String, nullable=False, index=True)

    # Token 有效期限
    expires_at = Column(DateTime, nullable=False)

    # Token 是否已使用（reset 完後必須標記 true）
    used = Column(Boolean, default=False)

    # ---------------------------------------------------------
    # Relationship
    # ---------------------------------------------------------
    user = relationship(
        "User",
        back_populates="password_resets",
        lazy="selectin"
    )
