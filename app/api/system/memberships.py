# app/api/system/memberships.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.schemas.system_membership.system_membership_response import (
    SystemMembershipResponse
)

router = APIRouter(
    prefix="/system/memberships",
    tags=["System - Memberships"],
)


@router.get("/me", response_model=SystemMembershipResponse | None)
def get_my_system_membership(
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    """
    取得目前使用者的 system_membership（RBAC）
    """
    return identity.system_membership
