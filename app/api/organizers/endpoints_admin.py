# app/api/organizers/endpoints_admin.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_system_admin
from app.crud.organizer import get_organizer_by_uuid

router = APIRouter(
    prefix="/admin/organizers",
    tags=["Admin Organizer Moderation"]
)

# ------------------------------------------------------------
# Approve Organizer
# ------------------------------------------------------------
@router.post("/{uuid}/approve")
def approve_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    organizer = get_organizer_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(404, "Organizer not found")

    organizer.status = "approved"
    organizer.updated_by = admin.uuid
    organizer.updated_by_role = "system_admin"

    db.commit()
    db.refresh(organizer)

    return {"status": "approved", "organizer_uuid": uuid}


# ------------------------------------------------------------
# Reject Organizer
# ------------------------------------------------------------
@router.post("/{uuid}/reject")
def reject_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    organizer = get_organizer_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(404, "Organizer not found")

    organizer.status = "rejected"
    organizer.updated_by = admin.uuid
    organizer.updated_by_role = "system_admin"

    db.commit()
    db.refresh(organizer)

    return {"status": "rejected", "organizer_uuid": uuid}
