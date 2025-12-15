# app/api/admin/organizers.py  # 平台管理 organizer

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin

from app.crud.organizer.crud_organizer import organizer_crud

from app.schemas.organizer.organizer_create import OrganizerCreate
from app.schemas.organizer.organizer_update import OrganizerUpdate
from app.schemas.organizer.organizer_public import OrganizerPublic


router = APIRouter(
    prefix="/admin/organizers",
    tags=["Admin - Organizers"],
)


# ------------------------------------------------------------
# 1. 列出所有 Organizer（僅 super admin）
# ------------------------------------------------------------
@router.get("/", response_model=list[OrganizerPublic])
def admin_list_organizers(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin),
):
    organizers = organizer_crud.get_multi(db)
    return organizers


# ------------------------------------------------------------
# 2. 查看單一 Organizer
# ------------------------------------------------------------
@router.get("/{uuid}", response_model=OrganizerPublic)
def admin_get_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin),
):
    organizer = organizer_crud.get_organizer_by_uuid(db, uuid)
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return organizer


# ------------------------------------------------------------
# 3. Admin 建立 Organizer（super admin 直接建立）
# ------------------------------------------------------------
@router.post("/", response_model=OrganizerPublic)
def admin_create_organizer(
    data: OrganizerCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin),
):
    organizer = organizer_crud.create(db, obj_in=data)
    return organizer


# ------------------------------------------------------------
# 4. 更新 Organizer
# ------------------------------------------------------------
@router.put("/{uuid}", response_model=OrganizerPublic)
def admin_update_organizer(
    uuid: str,
    data: OrganizerUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin),
):
    db_obj = organizer_crud.get_by_uuid(db, uuid)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Organizer not found")

    updated = organizer_crud.update(
        db,
        db_obj=db_obj,
        data=data,
    )
    return updated


# ------------------------------------------------------------
# 5. 假刪除 Organizer
# ------------------------------------------------------------
@router.delete("/{uuid}")
def admin_soft_delete_organizer(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin),
):
    ok = organizer_crud.delete(db, uuid)
    if not ok:
        raise HTTPException(status_code=404, detail="Organizer not found")

    return {
        "message": "Organizer soft-deleted", 
        "uuid": uuid
    }