# app/api/templates/template_fields.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user

from app.schemas.template_field import (
    TemplateFieldCreate,
    TemplateFieldUpdate,
    TemplateFieldResponse,
)
from app.crud.template_field import (
    get_fields_by_template,
    get_field_by_id,
    create_field,
    update_field,
    soft_delete_field,
)

router = APIRouter(
    prefix="/template-fields",
    tags=["Activity Template Fields"],
)
