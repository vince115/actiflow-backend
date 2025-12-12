# app/crud/submission/crud_submission_value.py

from sqlalchemy.orm import Session
from typing import List

from app.crud.base.crud_base import CRUDBase
from app.models.submission.submission_value import SubmissionValue
from app.schemas.submission.submission_value_create import SubmissionValueCreate
from app.schemas.submission.submission_value_update import SubmissionValueUpdate


class CRUDSubmissionValue(CRUDBase[SubmissionValue]):
    """
    SubmissionValue CRUD
    -------------------------------------------------
    用途：
    - 儲存單一欄位填寫值
    - 隸屬於 Submission
    """

    def create(
        self,
        db: Session,
        data: SubmissionValueCreate
    ) -> SubmissionValue:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: SubmissionValue,
        data: SubmissionValueUpdate
    ) -> SubmissionValue:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )

    # -------------------------------------------------
    # 常用擴充（非常實際）
    # -------------------------------------------------
    def list_by_submission(
        self,
        db: Session,
        submission_id: int
    ) -> List[SubmissionValue]:
        return (
            db.query(self.model)
            .filter(
                self.model.submission_id == submission_id,
                self.model.is_deleted == False,
            )
            .all()
        )


submission_value_crud = CRUDSubmissionValue(SubmissionValue)
