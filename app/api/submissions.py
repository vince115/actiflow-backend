# app/api/submissions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user

from app.schemas.submission import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionStatusUpdate,
    SubmissionResponse,
)
from app.crud.submission import (
    create_submission,
    get_submission_by_code,
    update_submission_data,
    update_submission_status,
    soft_delete_submission,
)

router = APIRouter(prefix="/submissions", tags=["Submissions"])


# -------------------------------------------------------
# 1. 列出所有 Submission（可加上管理用途）
# -------------------------------------------------------
@router.get("/", response_model=list[SubmissionResponse])
def get_submissions(db: Session = Depends(get_db)):
    submissions = db.query(Submission).filter(Submission.is_deleted == False).all()
    return submissions


@router.get("/{submission_code}")
def get_submission(submission_code: str):
    return {"message": "GET submission", "code": submission_code}

@router.post("/")
def create_submission(data: dict):
    return {"message": "Created submission", "data": data}

@router.put("/{submission_code}")
def update_submission(submission_code: str, data: dict):
    return {"message": "Updated submission", "code": submission_code, "data": data}

@router.delete("/{submission_code}")
def delete_submission(submission_code: str):
    return {"message": "Deleted submission", "code": submission_code}
