# app/crud/submission/crud_submission.py

from sqlalchemy.orm import Session
from typing import List, Optional

from app.crud.base.crud_base import CRUDBase
from app.models.submission.submission import Submission
from app.schemas.submission.submission_create import SubmissionCreate
from app.schemas.submission.submission_update import (
    SubmissionUpdate,
    SubmissionStatusUpdate,
    SubmissionStatus,
)


class CRUDSubmission(CRUDBase[Submission]):
    """
    Submission CRUD
    -------------------------------------------------
    用途：
    - 活動報名主資料
    - 一次提交對應多個 SubmissionValue
    """

    # -------------------------------------------------
    # 建立 Submission（Public）
    # -------------------------------------------------
    def create(
        self,
        db: Session,
        data: SubmissionCreate,
        *,
        creator_uuid: str | None = None,
        creator_role: str | None = None,
    ) -> Submission:
        obj_in = data.model_dump()
        if creator_uuid:
            obj_in["created_by"] = creator_uuid
            obj_in["created_by_role"] = creator_role

        return super().create(db, obj_in=obj_in)
    
    # -------------------------------------------------
    # 一般更新（notes / extra_data / status）
    # -------------------------------------------------
    def update(
        self,
        db: Session,
        db_obj: Submission,
        data: SubmissionUpdate,
        *,
        updater_uuid: str | None = None,
        updater_role: str | None = None,
    ) -> Submission:
        obj_in = data.model_dump(exclude_unset=True)
        if updater_uuid:
            obj_in["updated_by"] = updater_uuid
            obj_in["updated_by_role"] = updater_role

        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    # -------------------------------------------------
    # 更新狀態（流程用）
    # -------------------------------------------------
    def update_status(
        self,
        db: Session,
        db_obj: Submission,
        data: SubmissionStatusUpdate,
        *,
        updater_uuid: str | None = None,
        updater_role: str | None = None,
    ) -> Submission:
        obj_in = {
            "status": data.status.value,
            "status_reason": data.status_reason,
        }

        if updater_uuid:
            obj_in["updated_by"] = updater_uuid
            obj_in["updated_by_role"] = updater_role

        return super().update(db, db_obj=db_obj, obj_in=obj_in)
    
     # -------------------------------------------------
    # 依 UUID 取得（共用）
    # -------------------------------------------------
    def get_by_uuid(
        self,
        db: Session,
        uuid: str,
    ) -> Optional[Submission]:
        return (
            db.query(self.model)
            .filter(
                self.model.uuid == uuid,
                self.model.is_deleted == False,
            )
            .first()
        )

    # -------------------------------------------------
    # 依 submission_code 查詢（Public tracking）
    # -------------------------------------------------
    def get_by_code(
        self,
        db: Session,
        submission_code: str,
    ) -> Optional[Submission]:
        return (
            db.query(self.model)
            .filter(
                self.model.submission_code == submission_code,
                self.model.is_deleted == False,
            )
            .first()
        )

    # -------------------------------------------------
    # 使用者自己的 submissions
    # -------------------------------------------------
    def list_by_user_uuid(
        self,
        db: Session,
        user_uuid: str,
    ) -> List[Submission]:
        return (
            db.query(self.model)
            .filter(
                self.model.user_uuid == user_uuid,
                self.model.is_deleted == False,
            )
            .order_by(self.model.created_at.desc())
            .all()
        )

    # -------------------------------------------------
    # Admin：依 event + status 列表
    # -------------------------------------------------
    def list_submissions_by_event(
        self,
        db: Session,
        event_uuid: str,
        status: str | None = None,
    ) -> List[Submission]:
        q = (
            db.query(self.model)
            .filter(
                self.model.event_uuid == event_uuid,
                self.model.is_deleted == False,
            )
        )

        if status:
            q = q.filter(self.model.status == status)

        return q.order_by(self.model.created_at.desc()).all()

    # -------------------------------------------------
    # Soft delete（流程刪除）
    # -------------------------------------------------
    def soft_delete(
        self,
        db: Session,
        db_obj: Submission,
        *,
        deleter_uuid: str | None = None,
        deleter_role: str | None = None,
    ) -> Submission:
        obj_in = {
            "is_deleted": True,
            "status": SubmissionStatus.DELETED.value,
        }

        if deleter_uuid:
            obj_in["deleted_by"] = deleter_uuid
            obj_in["deleted_by_role"] = deleter_role

        return super().update(db, db_obj=db_obj, obj_in=obj_in)



submission_crud = CRUDSubmission(Submission)
