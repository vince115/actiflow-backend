# app/crud/system/crud_system_settings.py

from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.system.system_settings import SystemSettings
from app.schemas.system.system_settings import SystemSettingsUpdate


class CRUDSystemSettings(CRUDBase[SystemSettings]):
    """
    System Settings CRUD (Singleton)
    -------------------------------------------------
    全系統設定表，僅存在一筆資料
    """

    def get_singleton(self, db: Session) -> Optional[SystemSettings]:
        return (
            db.query(SystemSettings)
            .filter(SystemSettings.is_deleted == False)
            .first()
        )

    def update_singleton(
        self,
        db: Session,
        data: SystemSettingsUpdate,
    ) -> SystemSettings:
        obj = self.get_singleton(db)

        if not obj:
            # 若尚未建立，直接建立一筆
            obj = self.create(
                db,
                obj_in=data.model_dump(),
            )
        else:
            obj = self.update(
                db,
                db_obj=obj,
                obj_in=data.model_dump(exclude_unset=True),
            )

        return obj


# CRUD instance
system_settings_crud = CRUDSystemSettings(SystemSettings)
