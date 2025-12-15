# app/api/events/activity/template_fields.py

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import (
    require_organizer_admin,
    require_super_admin,
)

from app.crud.activity.crud_activity_template_field import activity_template_field_crud

from app.schemas.activity_template.activity_template_field_create import ActivityTemplateFieldCreate
from app.schemas.activity_template.activity_template_field_update import ActivityTemplateFieldUpdate
from app.schemas.activity_template.activity_template_field_response import ActivityTemplateFieldResponse

router = APIRouter(
    prefix="/events/activity/template-fields",
    tags=["Event Activity Template Fields"],
)

# ------------------------------------------------------------
# List fields by template (Organizer 可讀)
# ------------------------------------------------------------
@router.get(
    "/templates/{template_uuid}",
    response_model=List[ActivityTemplateFieldResponse],
)
def list_fields(
    template_uuid: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    return activity_template_field_crud.get_multi(
        db,
        filters={"template_uuid": template_uuid},
        order_by="sort_order",
    )


# ------------------------------------------------------------
# Get single field (Organizer 可讀)
# ------------------------------------------------------------
@router.get(
    "/{field_uuid}",
    response_model=ActivityTemplateFieldResponse,
)
def get_field(
    field_uuid: UUID,
    db: Session = Depends(get_db),
    _=Depends(require_organizer_admin),
):
    obj = activity_template_field_crud.get_by_uuid(db, uuid=field_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Template field not found")

    return ActivityTemplateFieldResponse.model_validate(obj)


# ------------------------------------------------------------
# Create field (Super admin only)
# ------------------------------------------------------------
@router.post(
    "",
    response_model=ActivityTemplateFieldResponse,
)
def create_field(
    data: ActivityTemplateFieldCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_field_crud.create(
        db=db,
        data=data,
        creator_uuid=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        created_by_role=getattr(admin, "role", "super_admin"),
    )

    return ActivityTemplateFieldResponse.model_validate(obj)


# ------------------------------------------------------------
# Update field (Super admin only)
# ------------------------------------------------------------
@router.put(
    "/{field_uuid}",
    response_model=ActivityTemplateFieldResponse,
)
def update_field(
    field_uuid: UUID,
    data: ActivityTemplateFieldUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_field_crud.get_by_uuid(db, uuid=field_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Template field not found")

    updated = activity_template_field_crud.update(
        db=db,
        db_obj=obj,
        data=data,
        updated_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        updated_by_role=getattr(admin, "role", "super_admin"),
    )

    return ActivityTemplateFieldResponse.model_validate(updated)


# ------------------------------------------------------------
# Delete field (soft delete, Super admin only)
# ------------------------------------------------------------
@router.delete("/{field_uuid}")
def delete_field(
    field_uuid: UUID,
    db: Session = Depends(get_db),
    admin=Depends(require_super_admin),
):
    obj = activity_template_field_crud.get_by_uuid(db, uuid=field_uuid)
    if not obj:
        raise HTTPException(status_code=404, detail="Template field not found")

    activity_template_field_crud.soft_delete(
        db=db,
        db_obj=obj,
        deleted_by=getattr(admin, "user_uuid", None) or getattr(admin, "uuid", None),
        deleted_by_role=getattr(admin, "role", "super_admin"),
    )

    return {"deleted": True}
