# app/api/organizers/admin/organizer_applications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.api.organizers.dependencies import require_super_admin

from app.crud.organizer.crud_organizer_application import (
    list_all_applications,
    get_application,
    review_application,
)
from app.schemas.organizer_application.organizer_application_response import OrganizerApplicationResponse

router = APIRouter(
    prefix="/admin/organizers/applications",
    tags=["Admin Organizer Applications"],
)

# ============================================================
# Organizer Application CRUD (for super_admin)
# ============================================================

# 1. 取得待審核 Organizer 申請列表
@router.get(
    "/pending",
    response_model=list[OrganizerApplicationResponse],
)
def list_pending_organizer_applications(
    db: Session = Depends(get_db),
    _: None = Depends(require_super_admin),
):
    """
    Super Admin 專用：
    取得所有尚未審核的 organizer applications
    """
    applications = list_all_applications(db)
    return [
        OrganizerApplicationResponse.model_validate(app)
        for app in applications
    ]

# 2. 取得單筆申請詳情
@router.get(
    "/{application_uuid}",
    response_model=OrganizerApplicationResponse,
)
def get_organizer_application(
    application_uuid: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_super_admin),
):
    """
    Super Admin 專用：
    查看單一 organizer application 詳情
    """
    application = get_application(db, application_uuid)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return OrganizerApplicationResponse.model_validate(application)

# 3. 批准 Organizer 申請
@router.post("/{application_uuid}/approve")
def approve_organizer_application(
    application_uuid: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_super_admin),
):
    """
    Super Admin 專用：
    核准 organizer 申請
    - 建立 organizer
    - 建立 organizer owner membership
    - 更新 application 狀態
    """
    application = get_application(db, application_uuid)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Application already processed",
        )
    review_application(db, application, status="approved")

    return {"status": "approved", "application_uuid": application_uuid}


# 4. 駁回 Organizer 申請
@router.post("/{application_uuid}/reject")
def reject_organizer_application(
    application_uuid: str,
    db: Session = Depends(get_db),
    _: None = Depends(require_super_admin),
):
    """
    Super Admin 專用：
    駁回 organizer 申請
    """
    application = get_application(db, application_uuid)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Application already processed",
        )
    review_application(db, application, status="rejected")

    return {"status": "rejected", "application_uuid": application_uuid}
