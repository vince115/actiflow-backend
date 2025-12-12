# app/api/applications/organizer_applications＿admin.py 審核端點

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user  # ★ 新版 Auth
from app.schemas.organizer.organizer_application import (
    OrganizerApplicationResponse,
    OrganizerApplicationReview,
)

from crud.organizer.organizer_application import (
    get_application,
    list_applications,
    review_application,
)


router = APIRouter(prefix="/applications/organizers", tags=["Organizer Applications - Admin"])


# ----------------------------------------------------
# GET：列出 Organizer Applications（僅 system_admin）
# ----------------------------------------------------
@router.get("/", response_model=list[OrganizerApplicationResponse])
def get_organizer_applications(
    status: str | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    列出申請清單，可用 status 過濾：
    ?status=pending
    """
    apps = list_applications(db, status)
    return apps


# ----------------------------------------------------
# POST: approve（僅 system_admin）
# ----------------------------------------------------
@router.post("/{uuid}/approve", response_model=OrganizerApplicationResponse)
def approve_application(
    uuid: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    通過 Organizer 申請
    """
    # RBAC
    if user.role != "system_admin":
        raise HTTPException(403, "Only system admin can approve applications")
    
    app = get_application(db, uuid)
    if not app:
        raise HTTPException(404, "Application not found")
    
    app = get_application(db, uuid)
    if not app:
        raise HTTPException(404, "Application not found")

    if app.status != "pending":
        raise HTTPException(400, "Only pending applications can be approved")

    updated = review_application(
        db=db,
        app=app,
        new_status="approved",
        reviewer_uuid=user.user_uuid,
        reviewer_role=user.role
    )

    return updated


# ----------------------------------------------------
# POST: reject（僅 system_admin)
# ----------------------------------------------------
@router.post("/{uuid}/reject", response_model=OrganizerApplicationResponse)
def reject_application(
    uuid: str,
    review: OrganizerApplicationReview,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    駁回 Organizer 申請
    """
    # RBAC
    if user.role != "system_admin":
        raise HTTPException(403, "Only system admin can reject applications")
    
    app = get_application(db, uuid)
    if not app:
        raise HTTPException(404, "Application not found")

    if app.status != "pending":
        raise HTTPException(400, "Only pending applications can be rejected")

    updated = review_application(
        db=db,
        app=app,
        new_status="rejected",
        reviewer_uuid=user.user_uuid,
        reviewer_role=user.role,
        reason=review.reason
    )

    return updated
