# app/crud/user/crud_user_profile.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.user.user_profile import UserProfile
from app.schemas.user.user_profile_create import UserProfileCreate
from app.schemas.user.user_profile_update import UserProfileUpdate


class CRUDUserProfile(CRUDBase[UserProfile]):
    """
    UserProfile CRUD
    -------------------------------------------------
    非登入必要的個人資料
    """

    def create(self, db: Session, data: UserProfileCreate) -> UserProfile:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: UserProfile,
        data: UserProfileUpdate
    ) -> UserProfile:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


user_profile_crud = CRUDUserProfile(UserProfile)
