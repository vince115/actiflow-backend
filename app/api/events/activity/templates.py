# app/api/events/activity/templates.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import (
    require_organizer_admin,
    require_super_admin,
)

from app.crud.activity.crud_activity_template import activity_template_crud

from app.schemas.activity_template.activity_template_create import ActivityTemplateCreate
from app.schemas.activity_template.activity_template_update import ActivityTemplateUpdate
from app.schemas.activity_template.activity_template_response import ActivityTemplateResponse


router = APIRouter(
    prefix="/events/activity/templates",
    tags=["Event Activity Templates"],
)

# ------------------------------------------------------------
# List templates (Organizer admin 可讀)
# ------------------------------------------------------------
@router.get(
    "",
    response_model=List[ActivityTemplateResponse],
)
def list_templates(
    active_only: bool = Query(False, description="是否只列出 is_active=True"),
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    filters: dict[str, bool] = {}
    if active_only:
        filters["is_active"] = True

    objs = activity_template_crud.get_multi(db, filters=filters)
    return [ActivityTemplateResponse.model_validate(o) for o in objs]


# ------------------------------------------------------------
# Get template (Organizer admin 可讀)
# ------------------------------------------------------------
@router.get(
    "/{template_uuid}",
    response_model=ActivityTemplateResponse,
)
def get_template(
    template_uuid: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    obj = activity_template_crud.get_by_uuid(db, uuid=template_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Template not found")

    return ActivityTemplateResponse.model_validate(obj)


# ------------------------------------------------------------
# Create template (Super admin only)
# ------------------------------------------------------------
@router.post(
    "",
    response_model=ActivityTemplateResponse,
)
def create_template(
    data: ActivityTemplateCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_crud.create(
        db=db,
        data=data,
        creator_uuid=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        created_by_role=getattr(admin, "role", "super_admin"),
    )
    return ActivityTemplateResponse.model_validate(obj)


# ------------------------------------------------------------
# Update template (Super admin only)
# ------------------------------------------------------------
@router.put(
    "/{template_uuid}",
    response_model=ActivityTemplateResponse,
)
def update_template(
    template_uuid: UUID,
    data: ActivityTemplateUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_crud.get_by_uuid(db, uuid=template_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Template not found")

    updated = activity_template_crud.update(
        db=db,
        db_obj=obj,
        data=data,
        updated_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        updated_by_role=getattr(admin, "role", "super_admin"),
    )

    return ActivityTemplateResponse.model_validate(updated)


# ------------------------------------------------------------
# Delete template (soft delete, Super admin only)
# ------------------------------------------------------------
@router.delete("/{template_uuid}")
def delete_template(
    template_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_crud.get_by_uuid(db, uuid=template_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Activity Template not found")

    activity_template_crud.soft_delete(
        db=db,
        db_obj=obj,
        deleted_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        deleted_by_role=getattr(admin, "role", "super_admin"),
    )

    return {"deleted": True}