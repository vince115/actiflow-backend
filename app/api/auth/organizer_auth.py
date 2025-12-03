# app/api/auth/organizer_auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user, get_current_system_admin
from app.schemas.organizer import OrganizerCreate, OrganizerResponse
from app.crud.organizer import create_organizer
from app.crud.organizer_membership import create_membership

router = APIRouter(prefix="/auth/organizers", tags=["Organizer Auth"])


# -----------------------------------------------------------
# 建立 Organizer（公司）
# 只有 system_admin 才能建立公司
# -----------------------------------------------------------
@router.post("/register", response_model=OrganizerResponse)
def register_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    """
    system_admin 才能建立主辦單位。
    OrganizerCreate 不包含 password。
    """

    organizer = create_organizer(db, data)

    # 建立一個 membership：system_admin 自己也加入 organizer，角色 owner
    create_membership(db, {
        "user_uuid": admin.user_uuid,
        "organizer_uuid": organizer.uuid,
        "role": "owner",
        "created_by": admin.user_uuid,
        "created_by_role": "system_admin"
    })

    return organizer
