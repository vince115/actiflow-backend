# app/crud/user/crud_user_settings.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.user.user_settings import UserSettings
from app.schemas.user.user_settings_create import UserSettingsCreate
from app.schemas.user.user_settings_update import UserSettingsUpdate


class CRUDUserSettings(CRUDBase[UserSettings]):
    """
    UserSettings CRUD
    -------------------------------------------------
    UI / 通知 / 偏好設定
    """

    def create(self, db: Session, data: UserSettingsCreate) -> UserSettings:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: UserSettings,
        data: UserSettingsUpdate
    ) -> UserSettings:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


user_settings_crud = CRUDUserSettings(UserSettings)
