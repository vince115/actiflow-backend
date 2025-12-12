# app/api/submissions/submissions_public.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user

from crud.submission.submission import (
    create_submission,
    get_submission_by_code,
    list_submissions_by_user,
)
from app.schemas.submission.submission import (
    SubmissionCreate,
    SubmissionResponse,
)

router = APIRouter(
    prefix="/submissions",
    tags=["Public - Submissions"],
)


# ------------------------------------------------------------
# Create submission (User submit form)
# ------------------------------------------------------------
@router.post("/", response_model=SubmissionResponse)
def api_create_submission(
    data: SubmissionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    submission = create_submission(
        db=db,
        data=data,
        creator_uuid=str(user.uuid),
        creator_role=user.role,
    )
    return submission


# ------------------------------------------------------------
# Get submission by submission_code (public tracking)
# ------------------------------------------------------------
@router.get("/code/{submission_code}", response_model=SubmissionResponse)
def api_get_submission_by_code(
    submission_code: str,
    db: Session = Depends(get_db),
):
    submission = get_submission_by_code(db, submission_code)
    if not submission:
        raise HTTPException(404, "Submission not found")
    return submission


# ------------------------------------------------------------
# List all submissions of current user
# ------------------------------------------------------------
@router.get("/my", response_model=list[SubmissionResponse])
def api_list_my_submissions(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return list_submissions_by_user(db, str(user.uuid))
