# app/api/events/activity/types.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import (
    require_organizer_admin,
    require_super_admin,
)

from app.crud.activity.crud_activity_type import activity_type_crud

from app.schemas.activity_type.activity_type_create import ActivityTypeCreate
from app.schemas.activity_type.activity_type_update import ActivityTypeUpdate
from app.schemas.activity_type.activity_type_response import ActivityTypeResponse

router = APIRouter(
    prefix="/events/activity/types",
    tags=["Event Activity Types"],
)


# ------------------------------------------------------------
# List types (Organizer admin can read)
# ------------------------------------------------------------
@router.get(
    "",
    response_model=List[ActivityTypeResponse],
)
def list_types(
    active_only: bool = Query(False, description="是否只列出 is_active=True 的分類"),
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    filters: dict[str, bool] = {}
    if active_only:
        filters["is_active"] = True

    objs = activity_type_crud.get_multi(db, filters=filters)
    return [ActivityTypeResponse.model_validate(o) for o in objs]


# ------------------------------------------------------------
# Get type (Organizer admin can read)
# ------------------------------------------------------------
@router.get(
    "/{type_uuid}",
    response_model=ActivityTypeResponse,
)
def get_type(
    type_uuid: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    obj = activity_type_crud.get_by_uuid(db, uuid=type_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Type not found")
    return ActivityTypeResponse.model_validate(obj)


# ------------------------------------------------------------
# Create type (Super admin only)
# ------------------------------------------------------------
@router.post(
    "",
    response_model=ActivityTypeResponse,
)
def create_type(
    data: ActivityTypeCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    # ✅ 帶 audit 欄位（如果你的 crud 會接）
    obj = activity_type_crud.create(
        db=db,
        data=data,
        creator_uuid=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        created_by_role=getattr(admin, "role", "super_admin"),
    )
    return ActivityTypeResponse.model_validate(obj)


# ------------------------------------------------------------
# Update type (Super admin only)
# ------------------------------------------------------------
@router.put(
    "/{type_uuid}",
    response_model=ActivityTypeResponse,
)
def update_type(
    type_uuid: UUID,
    data: ActivityTypeUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_type_crud.get_by_uuid(db, uuid=type_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Type not found")

    updated = activity_type_crud.update(
        db=db,
        db_obj=obj,
        data=data,
        updated_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        updated_by_role=getattr(admin, "role", "super_admin"),
    )
    return ActivityTypeResponse.model_validate(updated)


# ------------------------------------------------------------
# Delete type (soft delete, Super admin only)
# ------------------------------------------------------------
@router.delete("/{type_uuid}")
def delete_type(
    type_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_type_crud.get_by_uuid(db, uuid=type_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Type not found")

    # ✅ 統一 soft delete（你系統大量使用 is_deleted）
    activity_type_crud.soft_delete(
        db=db,
        db_obj=obj,
        deleted_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        deleted_by_role=getattr(admin, "role", "super_admin"),
    )

    return {"deleted": True}