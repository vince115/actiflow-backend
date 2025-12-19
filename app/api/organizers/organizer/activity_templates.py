# app/api/organizers/organizer/activity_templates.py

# Organizer 後台 - Activity Template CRUD（owner / admin）
# Canonical Organizer API

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.core.dependencies import (
    require_current_organizer_admin,
)

from app.schemas.activity_template.activity_template_create import (
    ActivityTemplateCreate,
)
from app.schemas.activity_template.activity_template_update import (
    ActivityTemplateUpdate,
)
from app.schemas.activity_template.activity_template_response import (
    ActivityTemplateResponse,
)
from app.schemas.common.pagination import PaginatedResponse

from app.crud.activity.crud_activity_template import (
    activity_template_crud,
)

from app.models.activity.activity_template import ActivityTemplate


router = APIRouter(
    prefix="/activity-templates",
    tags=["Organizer - Activity Templates"],
)


# -------------------------------------------------------------------
# List templates
# -------------------------------------------------------------------
@router.get("", response_model=PaginatedResponse[ActivityTemplateResponse])
def list_activity_templates(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    query = (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.organizer_uuid == membership.organizer_uuid,
            ActivityTemplate.is_deleted == False,
        )
    )

    total = query.count()
    templates = (
        query
        .order_by(ActivityTemplate.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedResponse(
        items=[
            ActivityTemplateResponse.model_validate(t)
            for t in templates
        ],
        total=total,
        page=page,
        page_size=page_size,
    )


# -------------------------------------------------------------------
# Create template
# -------------------------------------------------------------------
@router.post("", response_model=ActivityTemplateResponse)
def create_template(
    data: ActivityTemplateCreate,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    template = ActivityTemplate(
        **data.model_dump(),
        organizer_uuid=membership.organizer_uuid,
        created_by=membership.user_uuid,
        created_by_role=membership.role,
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return ActivityTemplateResponse.model_validate(template)



# -------------------------------------------------------------------
# Get single template
# -------------------------------------------------------------------
@router.get("/{template_uuid}", response_model=ActivityTemplateResponse)
def get_template(
    template_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    template = activity_template_crud.get(db, template_uuid)

    if (
        not template
        or template.is_deleted
        or template.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Template not found")

    return ActivityTemplateResponse.model_validate(template)


# -------------------------------------------------------------------
# Update template
# -------------------------------------------------------------------
@router.put("/{template_uuid}", response_model=ActivityTemplateResponse)
def update_template(
    template_uuid: UUID,
    data: ActivityTemplateUpdate,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    template = activity_template_crud.get(db, template_uuid)

    if (
        not template
        or template.is_deleted
        or template.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Template not found")

    updated = activity_template_crud.update(
        db=db,
        db_obj=template,
        data=data,
    )

    return ActivityTemplateResponse.model_validate(updated)


# -------------------------------------------------------------------
# Soft delete template
# -------------------------------------------------------------------
@router.delete("/{template_uuid}")
def delete_template(
    template_uuid: UUID,
    db: Session = Depends(get_db),
    membership=Depends(require_current_organizer_admin),
):
    template = activity_template_crud.get(db, template_uuid)

    if (
        not template
        or template.is_deleted
        or template.organizer_uuid != membership.organizer_uuid
    ):
        raise HTTPException(status_code=404, detail="Template not found")

    template.is_deleted = True
    template.deleted_by = membership.user_uuid
    template.deleted_by_role = membership.role

    db.add(template)
    db.commit()

    return {
        "deleted": True,
        "template_uuid": template_uuid,
    }



