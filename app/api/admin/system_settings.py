# app/api/admin/system_settings.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin
from app.schemas.system.system_settings import (
    SystemSettingsUpdate,
    SystemSettingsResponse
)
from app.crud.system.crud_system_settings import system_settings_crud

router = APIRouter(
    prefix="/admin/system-settings",
    tags=["Admin - System Settings"]
)


# ------------------------------------------------------------
# 取得系統設定（Super Admin 可用）
# ------------------------------------------------------------
@router.get("/", response_model=SystemSettingsResponse)
def admin_get_system_settings(
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    settings = system_settings_crud.get_singleton(db)

    if not settings:
        raise HTTPException(
            status_code=404, 
            detail="Settings not found"
        )

    return settings


# ------------------------------------------------------------
# 更新系統設定（Super Admin 可用）
# ------------------------------------------------------------
@router.put("/", response_model=SystemSettingsResponse)
def admin_update_system_settings(
    data: SystemSettingsUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_super_admin)
):
    settings = system_settings_crud.update_singleton(db, data)

    if not settings:
        raise HTTPException(
            status_code=404, 
            detail="Settings not found"
        )

    return settings
