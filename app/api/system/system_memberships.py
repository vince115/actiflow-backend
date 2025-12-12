# app/api/system/system_memberships.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin
from app.schemas.platform.super_admin import SuperAdminResponse, SuperAdminCreate
from app.crud.platform.super_admin import (
    create_super_admin,
    list_super_admins,
    update_super_admin_role,
    delete_super_admin
)

router = APIRouter(prefix="/system/admins", tags=["System Admins"])


@router.get("/", response_model=list[SuperAdminResponse])
def get_admins(
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    return list_super_admins(db)


@router.post("/", response_model=SuperAdminResponse)
def add_admin(
    data: SuperAdminCreate,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    return create_super_admin(db, data)


@router.put("/{admin_uuid}/role")
def update_role(
    admin_uuid: str,
    role: str,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    return update_super_admin_role(db, admin_uuid, role)


@router.delete("/{admin_uuid}")
def delete_admin(
    admin_uuid: str,
    db: Session = Depends(get_db),
    _admin = Depends(get_current_super_admin)
):
    delete_super_admin(db, admin_uuid)
    return {"message": "System admin removed"}
