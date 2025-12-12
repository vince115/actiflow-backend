# app/api/submissions/submissions_admin.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin

from crud.submission.submission import (
    get_submission_by_uuid,
    list_submissions_by_event,
    update_submission,
    update_submission_status,
    soft_delete_submission,
)

from app.schemas.submission.submission import (
    SubmissionUpdate,
    SubmissionStatusUpdate,
    SubmissionResponse,
)

router = APIRouter(
    prefix="/submissions/admin",
    tags=["Admin - Submissions"],
)


# ------------------------------------------------------------
# List submissions for an event
# ------------------------------------------------------------
@router.get("/", response_model=list[SubmissionResponse])
def api_list_submissions(
    event_uuid: str = Query(...),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    return list_submissions_by_event(db, event_uuid, status)


# ------------------------------------------------------------
# Get single submission
# ------------------------------------------------------------
@router.get("/{submission_uuid}", response_model=SubmissionResponse)
def api_get_submission(
    submission_uuid: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin),
):
    sub = get_submission_by_uuid(db, submission_uuid)
    if not sub:
        raise HTTPException(404, "Submission not found")
    return sub


# ------------------------------------------------------------
# Update submission (notes, metadata…)
# ------------------------------------------------------------
@router.put("/{submission_uuid}", response_model=SubmissionResponse)
def api_update_submission(
    submission_uuid: str,
    data: SubmissionUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin),
):
    updated = update_submission(
        db=db,
        submission_uuid=submission_uuid,
        data=data,
        updater_uuid=str(admin.uuid),
        updater_role="super_admin",
    )
    if not updated:
        raise HTTPException(404, "Submission not found")
    return updated


# ------------------------------------------------------------
# Update status (approved / rejected)
# ------------------------------------------------------------
@router.put("/{submission_uuid}/status", response_model=SubmissionResponse)
def api_update_status(
    submission_uuid: str,
    data: SubmissionStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin),
):
    updated = update_submission_status(
        db=db,
        submission_uuid=submission_uuid,
        data=data,
        updater_uuid=str(admin.uuid),
        updater_role="super_admin",
    )
    if not updated:
        raise HTTPException(404, "Submission not found")
    return updated


# ------------------------------------------------------------
# Soft delete submission
# ------------------------------------------------------------
@router.delete("/{submission_uuid}")
def api_delete_submission(
    submission_uuid: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin),
):
    deleted = soft_delete_submission(
        db=db,
        submission_uuid=submission_uuid,
        deleter_uuid=str(admin.uuid),
        deleter_role="super_admin",
    )
    if not deleted:
        raise HTTPException(404, "Submission not found")

    return {
        "message": "Submission deleted",
        "submission_uuid": submission_uuid
    }
