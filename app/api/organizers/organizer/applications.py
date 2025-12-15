# app/api/organizers/organizer/applications.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import require_organizer_admin

from app.crud.organizer.crud_organizer_application import (
    list_organizer_applications,
)
from app.schemas.organizer_application.organizer_application_response import (
    OrganizerApplicationResponse,
)

router = APIRouter(
    prefix="/organizers/applications",
    tags=["Organizer Applications"],
)


# ------------------------------------------------------------
# List applications（Organizer 後台）
# ------------------------------------------------------------
@router.get("/", response_model=List[OrganizerApplicationResponse])
def list_applications(
    db: Session = Depends(get_db),
    membership=Depends(require_organizer_admin),
):
    """
    Organizer admin / owner
    列出自己 organizer 的所有申請紀錄
    """

    return list_organizer_applications(
        db=db,
        organizer_uuid=membership.organizer_uuid,
    )
