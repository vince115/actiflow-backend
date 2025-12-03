# app/api/applications/organizer_applications.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.schemas.organizer import OrganizerCreate, OrganizerResponse
from app.crud.organizer import create_organizer

router = APIRouter(
    prefix="/applications/organizers",
    tags=["Organizer Applications"]
)

@router.post("/", response_model=OrganizerResponse)
def apply_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    一般使用者申請成為 Organizer（狀態預設: pending）
    """

    organizer = create_organizer(db, data)

    organizer.status = "pending"
    organizer.created_by = current_user.uuid
    organizer.created_by_role = "user"

    db.commit()
    db.refresh(organizer)

    return organizer
