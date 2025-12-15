# app/crud/user/crud_user.py

from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import hash_password
import secrets

from app.crud.base.crud_base import CRUDBase
from app.models.user.user import User
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_update import UserUpdate


class CRUDUser(CRUDBase[User]):
    """
    User CRUD
    -------------------------------------------------
    帳號本體（登入用）
    """

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return (
            db.query(self.model)
            .filter(
                self.model.email == email,
                self.model.is_deleted == False,
            )
            .first()
        )

    def create(self, db: Session, data: UserCreate) -> User:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(self, db: Session, db_obj: User, data: UserUpdate) -> User:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )

    def force_reset_password(self, db: Session, user_uuid: str) -> Optional[str]:
        user = self.get(db, user_uuid)
        if not user:
            return None

        new_password = secrets.token_urlsafe(10)
        user.password_hash = hash_password(new_password)

        db.add(user)
        db.commit()
        db.refresh(user)

        return new_password

user_crud = CRUDUser(User)
