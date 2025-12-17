# app/api/system/organizer_approval.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity
from app.crud.organizer.crud_organizer import organizer_crud

router = APIRouter(
    prefix="/system/organizers",
    tags=["System - Organizer Approval"]
)

# ------------------------------------------------------------
# Approve Organizer（僅 system_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/approve")
def approve_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    identity = Depends(get_current_identity)
):
    # RBAC: 只有 system_admin 可以審核
    if identity.role != "system_admin":
        raise HTTPException(status_code=403, detail="Only system admin can approve organizers")

    organizer = organizer_crud.get_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    organizer.status = "approved"
    organizer.updated_by = str(identity.uuid)
    organizer.updated_by_role = identity.role

    db.commit()
    db.refresh(organizer)

    return {
        "status": "approved",
        "organizer_uuid": uuid
    }


# ------------------------------------------------------------
# Reject Organizer（僅 system_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/reject")
def reject_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    identity = Depends(get_current_identity)
):
    # RBAC: 只有 system_admin 可以審核
    if identity.role != "system_admin":
        raise HTTPException(status_code=403, detail="Only system admin can reject organizers")

    organizer = organizer_crud.get_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")

    organizer.status = "rejected"
    organizer.updated_by = str(identity.uuid)
    organizer.updated_by_role = identity.role

    db.commit()
    db.refresh(organizer)

    return {
        "status": "rejected",
        "organizer_uuid": uuid
    }
