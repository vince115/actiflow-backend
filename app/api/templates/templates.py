# app/api/templates/templates.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.schemas.activity_template import (
    ActivityTemplateCreate,
    ActivityTemplateUpdate,
    ActivityTemplateResponse,
)
from app.crud.activity_template import (
    create_template,
    get_template_by_id,
    get_templates,
    update_template,
    soft_delete_template,
)

router = APIRouter(
    prefix="/templates",
    tags=["Activity Templates"]
)


# ---------------------------------------
# GET all templates
# ---------------------------------------
@router.get("/", response_model=list[ActivityTemplateResponse])
def list_templates(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    取得所有活動模板（含 draft/published）
    """
    return get_templates(db)


# ---------------------------------------
# GET one template
# ---------------------------------------
@router.get("/{template_uuid}", response_model=ActivityTemplateResponse)
def get_one_template(
    template_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    template = get_template_by_id(db, template_uuid)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity template not found"
        )
    return template


# ---------------------------------------
# CREATE template
# ---------------------------------------
@router.post("/", response_model=ActivityTemplateResponse)
def create_template_api(
    data: ActivityTemplateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    建立活動模板（預設為 draft）
    """
    return create_template(db, data, created_by=current_user.user_uuid)


# ---------------------------------------
# UPDATE template
# ---------------------------------------
@router.put("/{template_uuid}", response_model=ActivityTemplateResponse)
def update_template_api(
    template_uuid: str,
    data: ActivityTemplateUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    template = get_template_by_id(db, template_uuid)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity template not found"
        )

    updated = update_template(db, template, data, updated_by=current_user.user_uuid)
    return updated


# ---------------------------------------
# DELETE (soft delete)
# ---------------------------------------
@router.delete("/{template_uuid}")
def delete_template_api(
    template_uuid: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    template = get_template_by_id(db, template_uuid)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity template not found"
        )

    soft_delete_template(db, template, deleted_by=current_user.user_uuid)
    return {"message": "Template deleted successfully"}
