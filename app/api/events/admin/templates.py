# app/api/events/admin/templates.py 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import require_super_admin

from app.crud.activity.crud_activity_template import activity_template_crud

from app.schemas.activity_template.activity_template_create import ActivityTemplateCreate
from app.schemas.activity_template.activity_template_update import ActivityTemplateUpdate
from app.schemas.activity_template.activity_template_response import ActivityTemplateResponse

router = APIRouter(
    prefix="/admin/activity-templates",
    tags=["Admin - Activity Templates"],
)


# -------------------------------------------------------------------
# List activity templates
# -------------------------------------------------------------------
@router.get("", response_model=list[ActivityTemplateResponse])
def list_activity_templates(
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    objs = activity_template_crud.get_multi(db)
    return [ActivityTemplateResponse.model_validate(o) for o in objs]


# -------------------------------------------------------------------
# Create activity template
# -------------------------------------------------------------------
@router.post("", response_model=ActivityTemplateResponse)
def create_activity_template(
    data: ActivityTemplateCreate,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    obj = activity_template_crud.create(db, data=data)
    return ActivityTemplateResponse.model_validate(obj)


# -------------------------------------------------------------------
# Update activity template
# -------------------------------------------------------------------
@router.patch("/{template_uuid}", response_model=ActivityTemplateResponse)
def update_activity_template(
    template_uuid: UUID,
    data: ActivityTemplateUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(require_super_admin),
):
    obj = activity_template_crud.get_by_uuid(db, template_uuid)

    if not obj:
        raise HTTPException(status_code=404, detail="ActivityTemplate not found")

    obj = activity_template_crud.update(db, obj, data=data)
    return ActivityTemplateResponse.model_validate(obj)