# app/api/events/admin/types.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_super_admin

from app.crud.activity.crud_activity_type import activity_type_crud

from app.schemas.activity_type.activity_type_create import ActivityTypeCreate
from app.schemas.activity_type.activity_type_update import ActivityTypeUpdate
from app.schemas.activity_type.activity_type_response import ActivityTypeResponse

router = APIRouter(
    prefix="/admin/activity-types",
    tags=["Admin - Activity Types"],
)


# -------------------------------------------------------------------
# List activity types
# -------------------------------------------------------------------
@router.get("", response_model=list[ActivityTypeResponse])
def list_activity_types(
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    objs = activity_type_crud.get_multi(db)
    return [ActivityTypeResponse.model_validate(o) for o in objs]


# -------------------------------------------------------------------
# Create activity type
# -------------------------------------------------------------------
@router.post("", response_model=ActivityTypeResponse)
def create_activity_type(
    data: ActivityTypeCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    obj = activity_type_crud.create(db, data=data)
    return ActivityTypeResponse.model_validate(obj)


# -------------------------------------------------------------------
# Update activity type
# -------------------------------------------------------------------
@router.patch("/{type_uuid}", response_model=ActivityTypeResponse)
def update_activity_type(
    type_uuid: UUID,
    data: ActivityTypeUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    obj = activity_type_crud.get(db, type_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="ActivityType not found")

    obj = activity_type_crud.update(db, obj, data=data)
    return ActivityTypeResponse.model_validate(obj)
