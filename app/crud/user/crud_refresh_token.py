# app/crud/user/crud_refresh_token.py

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import secrets

from app.crud.base.crud_base import CRUDBase
from app.models.auth.refresh_token import RefreshToken
from app.core.config import settings


class CRUDRefreshToken(CRUDBase[RefreshToken]):
    """
    RefreshToken CRUD
    -------------------------------------------------
    只管 DB，不做 JWT 驗證
    """
    def create_token(
        self,
        db: Session,
        *,
        user_id: int,
        user_agent: str,
    ) -> RefreshToken:
        """
        建立新的 refresh token（登入 / refresh 時使用）
        """
        token_str = secrets.token_urlsafe(48)

        token = RefreshToken(
            user_id=user_id,
            token=token_str,
            user_agent=user_agent,
            is_revoked=False,
            is_deleted=False,
            expires_at=datetime.utcnow() + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
            if hasattr(RefreshToken, "expires_at")
            else None,
        )

        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def revoke(self, db: Session, token: RefreshToken) -> RefreshToken:
        """
        註銷 refresh token（logout / refresh rotation）
        """
        token.is_revoked = True
        db.add(token)
        db.commit()
        db.refresh(token)
        return token

    def get_valid_token(
        self,
        db: Session,
        token: str
    ) -> Optional[RefreshToken]:
        """
        取得尚未被註銷、未刪除、未過期的 refresh token
        """
        q = (
            db.query(self.model)
            .filter(
                self.model.token == token,
                self.model.is_revoked == False,
                self.model.is_deleted == False,
            )
        )

        if hasattr(self.model, "expires_at"):
            q = q.filter(self.model.expires_at > datetime.utcnow())
        return q.first()


refresh_token_crud = CRUDRefreshToken(RefreshToken)
