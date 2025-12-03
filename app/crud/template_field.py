# app/crud/template_field.py

import uuid
from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.template_field import TemplateField
from app.schemas.template_field import (
    TemplateFieldCreate,
    TemplateFieldUpdate,
)


# ---------------------------------------------------------
# 取得某 Template 下的所有欄位（依 sort_order 排序）
# ---------------------------------------------------------
def get_fields_by_template(db: Session, template_uuid: str):
    return (
        db.query(TemplateField)
        .filter(
            TemplateField.template_uuid == template_uuid,
            TemplateField.is_deleted == False
        )
        .order_by(asc(TemplateField.sort_order))
        .all()
    )


# ---------------------------------------------------------
# 取得單一欄位（以 field_uuid 查）
# ---------------------------------------------------------
def get_field_by_id(db: Session, field_uuid: str):
    return (
        db.query(TemplateField)
        .filter(TemplateField.field_uuid == field_uuid, TemplateField.is_deleted == False)
        .first()
    )


# ---------------------------------------------------------
# 建立 Template Field
# ---------------------------------------------------------
def create_field(
    db: Session,
    template_uuid: str,
    data: TemplateFieldCreate,
    created_by: str | None = None,
):
    field = TemplateField(
        field_uuid=str(uuid.uuid4()),
        template_uuid=template_uuid,
        field_key=data.field_key,
        label=data.label,
        field_type=data.field_type,
        required=data.required,
        options=data.options,
        sort_order=data.sort_order,
        created_by=created_by,
    )

    db.add(field)
    db.commit()
    db.refresh(field)
    return field


# ---------------------------------------------------------
# 更新欄位
# ---------------------------------------------------------
def update_field(
    db: Session,
    field: TemplateField,
    data: TemplateFieldUpdate,
    updated_by: str | None = None,
):
    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(field, key, value)

    field.updated_by = updated_by

    db.commit()
    db.refresh(field)
    return field


# ---------------------------------------------------------
# Soft Delete（假刪除）
# ---------------------------------------------------------
from datetime import datetime

def soft_delete_field(
    db: Session,
    field: TemplateField,
    deleted_by: str | None = None,
):
    field.is_deleted = True
    field.deleted_by = deleted_by
    field.deleted_at = datetime.utcnow()

    db.commit()
    return True
