# app/api/system/settings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_identity

from app.crud.system.crud_system_settings import system_settings_crud
from app.schemas.system.system_settings import SystemSettingsResponse

router = APIRouter(
    prefix="/system/settings",
    tags=["System - Settings"],
)


@router.get("/", response_model=SystemSettingsResponse)
def get_system_settings(
    db: Session = Depends(get_db),
    identity=Depends(get_current_identity),
):
    """
    取得系統設定（所有登入者可讀）
    """
    settings = system_settings_crud.get_singleton(db)

    if not settings:
        raise HTTPException(404, "System settings not found")

    return settings
