# app/crud/activity_template.py

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.activity_template import ActivityTemplate
from app.models.template_field import TemplateField

from app.schemas.activity_template import ActivityTemplateCreate, ActivityTemplateUpdate
from app.schemas.template_field import TemplateFieldCreate

# -----------------------------------------------------------
# 1. 建立 Template
# -----------------------------------------------------------
def create_template(
    db: Session,
    data: ActivityTemplateCreate,
    created_by: str | None = None
):
    template = ActivityTemplate(
        template_uuid=str(uuid.uuid4()),          # 對外 key
        activity_type_uuid=data.activity_type_uuid,
        name=data.name,
        description=data.description,
        sort_order=data.sort_order or 100,
        config=data.config or {},
        created_by=created_by,
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return template


# -----------------------------------------------------------
# 2.取得單一 Template (by template_uuid)
# -----------------------------------------------------------
def get_template_by_id(db: Session, template_uuid: str):
    return (
        db.query(ActivityTemplate)
        .filter(
            ActivityTemplate.template_uuid == template_uuid,
            ActivityTemplate.is_deleted == False,
        )
        .first()
    )



# -----------------------------------------------------------
# 3.列出所有 Template（依排序）
# -----------------------------------------------------------
def get_templates(db: Session):
    return (
        db.query(ActivityTemplate)
        .filter(ActivityTemplate.is_deleted == False)
        .order_by(asc(ActivityTemplate.sort_order))
        .all()
    )

# -----------------------------------------------------------
# 4.更新 Template
# -----------------------------------------------------------
def update_template(
    db: Session,
    template: ActivityTemplate,
    data: ActivityTemplateUpdate,
    updated_by: str | None = None,
):
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        
        if key == "config" and value is None:
            value = {}
        
        setattr(template, key, value)

    template.updated_by = updated_by
    template.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(template)
    return template


# -----------------------------------------------------------
# 5.假刪除 Template
# -----------------------------------------------------------
def soft_delete_template(
    db: Session,
    template: ActivityTemplate,
    deleted_by: str | None = None,
):
    template.is_deleted = True
    template.deleted_at = datetime.now(timezone.utc)
    template.deleted_by = deleted_by

    db.commit()
    return True


# -----------------------------------------------------------
# 6.模板內的欄位：取得所有欄位
# -----------------------------------------------------------
def get_template_fields(db: Session, template_uuid: str):
    return (
        db.query(TemplateField)
        .filter(
            TemplateField.template_uuid == template_uuid,
            TemplateField.is_deleted == False,
        )
        .order_by(asc(TemplateField.sort_order))
        .all()
    )

# -----------------------------------------------------------
# 7. 查詢單一欄位
# -----------------------------------------------------------
def get_template_field(db: Session, field_uuid: str):
    return (
        db.query(TemplateField)
        .filter(
            TemplateField.field_uuid == field_uuid,
            TemplateField.is_deleted == False,
        )
        .first()
    )

# -----------------------------------------------------------
# 8. 新增欄位（配合 TemplateField）
# -----------------------------------------------------------
def add_template_field(
    db: Session,
    template_uuid: str,
    field_data: TemplateFieldCreate,
    created_by: str | None = None,
):
    field = TemplateField(
        field_uuid=str(uuid.uuid4()),
        template_uuid=template_uuid,
        field_key=field_data.field_key,
        label=field_data.label,
        field_type=field_data.field_type,
        required=field_data.required,
        options=field_data.options,
        sort_order=field_data.sort_order or 0,

        created_by=created_by,
    )

    db.add(field)
    db.commit()
    db.refresh(field)
    return field

# -----------------------------------------------------------
# 9. 刪除欄位（假刪除）
# -----------------------------------------------------------
def delete_template_field(
    db: Session,
    field_uuid: str,
    deleted_by: str | None = None,
):
    field = (
        db.query(TemplateField)
        .filter(
            TemplateField.field_uuid == field_uuid,
            TemplateField.is_deleted == False,
        )
        .first()
    )

    if not field:
        return None

    field.is_deleted = True
    field.deleted_at = datetime.now(timezone.utc)
    field.deleted_by = deleted_by

    db.commit()
    return field
