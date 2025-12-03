# app/api/activity_types.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.db import get_db
from app.core.dependencies import get_current_system_admin
from app.schemas.activity_type import (
    ActivityTypeCreate,
    ActivityTypeUpdate,
    ActivityTypeResponse
)
from app.crud.activity_type import (
    create_activity_type,
    list_activity_types,
    get_activity_type,
    update_activity_type,
    soft_delete_activity_type
)

router = APIRouter(prefix="/activity-types", tags=["Activity Types"])


# -----------------------------------------------------------
# GET all Activity Types
# -----------------------------------------------------------
@router.get("/", response_model=List[ActivityTypeResponse])
def get_activity_types(
    active_only: bool = Query(False, description="是否只列出 is_active=True 的分類"),
    db: Session = Depends(get_db)
):
    types = list_activity_types(db, only_active=active_only)
    return types


# -----------------------------------------------------------
# GET single Activity Type
# -----------------------------------------------------------
@router.get("/{type_uuid}", response_model=ActivityTypeResponse)
def get_activity_type_detail(
    type_uuid: str,
    db: Session = Depends(get_db)
):
    item = get_activity_type(db, type_uuid)
    if not item:
        raise HTTPException(404, "Activity Type not found")

    return item


# -----------------------------------------------------------
# CREATE Activity Type（僅 system_admin）
# -----------------------------------------------------------
@router.post("/", response_model=ActivityTypeResponse)
def create_activity_type_api(
    data: ActivityTypeCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    new_item = create_activity_type(
        db=db,
        data=data,
        creator_uuid=admin.user_uuid
    )
    return new_item


# -----------------------------------------------------------
# UPDATE Activity Type（僅 system_admin）
# -----------------------------------------------------------
@router.put("/{type_uuid}", response_model=ActivityTypeResponse)
def update_activity_type_api(
    type_uuid: str,
    data: ActivityTypeUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    updated = update_activity_type(
        db=db,
        type_uuid=type_uuid,
        data=data,
        updater_uuid=admin.user_uuid,
    )

    if not updated:
        raise HTTPException(404, "Activity Type not found")

    return updated


# -----------------------------------------------------------
# DELETE Activity Type（soft delete, 僅 system_admin）
# -----------------------------------------------------------
@router.delete("/{type_uuid}")
def delete_activity_type_api(
    type_uuid: str,
    db: Session = Depends(get_db),
    admin = Depends(get_current_system_admin)
):
    deleted = soft_delete_activity_type(
        db=db,
        type_uuid=type_uuid,
        deleter_uuid=admin.user_uuid
    )

    if not deleted:
        raise HTTPException(404, "Activity Type not found")

    return {"deleted": True}
