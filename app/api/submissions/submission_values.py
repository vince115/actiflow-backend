# app/api/submissions/submission_values.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin

from app.crud.submission_value import (
    get_submission_value,
    list_submission_values,
    update_submission_value,
    soft_delete_submission_value,
)
from app.schemas.submission_value import (
    SubmissionValueUpdate,
    SubmissionValueResponse,
)

router = APIRouter(
    prefix="/submissions/admin/values",
    tags=["Admin - Submission Values"],
)


# ------------------------------------------------------------
# Get all values for a submission
# ------------------------------------------------------------
@router.get("/submission/{submission_uuid}", response_model=list[SubmissionValueResponse])
def api_get_submission_values(
    submission_uuid: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    return list_submission_values(db, submission_uuid)


# ------------------------------------------------------------
# Get single submission value
# ------------------------------------------------------------
@router.get("/{value_uuid}", response_model=SubmissionValueResponse)
def api_get_submission_value(
    value_uuid: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    value = get_submission_value(db, value_uuid)
    if not value:
        raise HTTPException(404, "Submission value not found")
    return value


# ------------------------------------------------------------
# Update submission value
# ------------------------------------------------------------
@router.put("/{value_uuid}", response_model=SubmissionValueResponse)
def api_update_submission_value(
    value_uuid: str,
    data: SubmissionValueUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    updated = update_submission_value(
        db=db,
        value_uuid=value_uuid,
        data=data,
        updater_uuid=str(admin.uuid),
        updater_role="super_admin",
    )

    if not updated:
        raise HTTPException(404, "Submission value not found")

    return updated


# ------------------------------------------------------------
# Soft delete submission value
# ------------------------------------------------------------
@router.delete("/{value_uuid}")
def api_delete_submission_value(
    value_uuid: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    deleted = soft_delete_submission_value(
        db=db,
        value_uuid=value_uuid,
        deleter_uuid=str(admin.uuid),
        deleter_role="super_admin",
    )

    if not deleted:
        raise HTTPException(404, "Submission value not found")

    return {"message": "Submission value deleted", "value_uuid": value_uuid}
