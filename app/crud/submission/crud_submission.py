# app/crud/submission/crud_submission.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.submission.submission import Submission
from app.schemas.submission.submission_create import SubmissionCreate
from app.schemas.submission.submission_update import SubmissionUpdate


class CRUDSubmission(CRUDBase[Submission]):
    """
    Submission CRUD
    -------------------------------------------------
    用途：
    - 活動報名主資料
    - 一次提交對應多個 SubmissionValue
    """

    def create(
        self,
        db: Session,
        data: SubmissionCreate
    ) -> Submission:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: Submission,
        data: SubmissionUpdate
    ) -> Submission:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


submission_crud = CRUDSubmission(Submission)
