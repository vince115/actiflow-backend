# app/crud/base/crud_base.py

from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import Session

from app.models.base.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    """
    ActiFlow Backend — 標準 CRUD Base
    -------------------------------------------------
    責任：
    - 單純 DB 操作
    - 不處理 Auth / HTTP / Schema Response
    - 全系統共用
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # =========================================================
    # Read
    # =========================================================
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(
                self.model.id == id,
                self.model.is_deleted == False,
            )
            .first()
        )

    def get_by_uuid(self, db: Session, uuid) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(
                self.model.uuid == uuid,
                self.model.is_deleted == False,
            )
            .first()
        )

    def list(self, db: Session) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.is_deleted == False)
            .all()
        )

    # =========================================================
    # Create
    # =========================================================
    def create(self, db: Session, *, obj_in: dict) -> ModelType:
        """
        建立資料（給子類包裝用）
        """
        obj = self.model(**obj_in)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    # =========================================================
    # Update
    # =========================================================
    def update(self, db: Session, *, db_obj: ModelType, obj_in: dict) -> ModelType:
        """
        更新資料（給子類包裝用）
        """
        for field, value in obj_in.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # =========================================================
    # Soft Delete
    # =========================================================
    def soft_delete(self, db: Session, *, db_obj: ModelType) -> ModelType:
        """
        軟刪除（全系統統一行為）
        """
        db_obj.is_deleted = True
        db_obj.is_active = False

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
