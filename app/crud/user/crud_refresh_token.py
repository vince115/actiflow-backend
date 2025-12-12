# app/crud/user/crud_refresh_token.py

from sqlalchemy.orm import Session
from typing import Optional

from app.crud.base.crud_base import CRUDBase
from app.models.user.refresh_token import RefreshToken
from app.schemas.user.refresh_token_create import RefreshTokenCreate


class CRUDRefreshToken(CRUDBase[RefreshToken]):
    """
    RefreshToken CRUD
    -------------------------------------------------
    只管 DB，不做 JWT 驗證
    """

    def create(self, db: Session, data: RefreshTokenCreate) -> RefreshToken:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def revoke(self, db: Session, token: RefreshToken) -> RefreshToken:
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
        return (
            db.query(self.model)
            .filter(
                self.model.token == token,
                self.model.is_revoked == False,
                self.model.is_deleted == False,
            )
            .first()
        )


refresh_token_crud = CRUDRefreshToken(RefreshToken)
