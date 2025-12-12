# app/api/system/system_settings.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin
from app.schemas.user.settings import SystemSettingsResponse, SystemSettingsUpdate
from app.crud.settings import get_system_settings, update_system_settings

router = APIRouter(prefix="/system/settings", tags=["System Settings"])


@router.get("/", response_model=SystemSettingsResponse)
def fetch_settings(
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    return get_system_settings(db)


@router.put("/", response_model=SystemSettingsResponse)
def update_settings(
    data: SystemSettingsUpdate,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    return update_system_settings(db, data)
