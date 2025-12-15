# app/api/organizers/admin/organizers.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin
from app.crud.organizer.crud_organizer import organizer_crud

router = APIRouter(
    prefix="/admin/organizers",
    tags=["Admin Organizer Moderation"]
)


# ------------------------------------------------------------
# Approve Organizer（僅 super_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/approve")
def approve_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    user = Depends(require_organizer_admin)
):
    # RBAC: 只有 super_admin 才能審核
    if user.role != "super_admin":
        raise HTTPException(403, "Only super admin can approve organizers")
    
    organizer = organizer_crud.get_organizer_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(404, "Organizer not found")

    organizer.status = "approved"
    organizer.updated_by = user.uuid
    organizer.updated_by_role = user.role

    db.commit()
    db.refresh(organizer)

    return {"status": "approved", "organizer_uuid": uuid}


# ------------------------------------------------------------
# Reject Organizer（僅 super_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/reject")
def reject_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    user = Depends(require_organizer_admin)
):
    if user.role != "super_admin":
        raise HTTPException(403, "Only super admin can reject organizers")
    
    organizer = organizer_crud.get_organizer_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(404, "Organizer not found")

    organizer.status = "rejected"
    organizer.updated_by = user.uuid
    organizer.updated_by_role = user.role

    db.commit()
    db.refresh(organizer)

    return {"status": "rejected", "organizer_uuid": uuid}