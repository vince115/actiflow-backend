# app/crud/organizer/crud_organizer.py

from sqlalchemy.orm import Session
from typing import Optional

from app.crud.base.crud_base import CRUDBase
from app.models.organizer.organizer import Organizer
from app.schemas.organizer.organizer_create import OrganizerCreate
from app.schemas.organizer.organizer_update import OrganizerUpdate


class CRUDOrganizer(CRUDBase[Organizer]):
    """
    Organizer CRUD
    -------------------------------------------------
    用途：
    - 管理主辦單位基本資料
    - 不處理申請流程（那是 OrganizerApplication 模組）
    """

    def create(
        self,
        db: Session,
        data: OrganizerCreate
    ) -> Organizer:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: Organizer,
        data: OrganizerUpdate
    ) -> Organizer:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )

    # -----------------------------------------------
    # ⭐ 同義方法：標準 CRUD 命名 get_by_uuid()
    #    讓 CRUD 介面保持一致性
    # -----------------------------------------------

    def get_by_uuid(self, db: Session, uuid: str) -> Optional[Organizer]:
        return (
            db.query(Organizer)
            .filter(
                Organizer.uuid == uuid,
                Organizer.is_deleted == False
            )
            .first()
        )


# 實例化 CRUD
organizer_crud = CRUDOrganizer(Organizer)
