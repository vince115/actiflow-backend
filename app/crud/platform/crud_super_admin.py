# app/crud/platform/crud_super_admin.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.platform.super_admin import SuperAdmin
from app.schemas.platform.super_admin_create import SuperAdminCreate
from app.schemas.platform.super_admin_update import SuperAdminUpdate


class CRUDSuperAdmin(CRUDBase[SuperAdmin]):
    """
    SuperAdmin CRUD
    -------------------------------------------------
    用途：
    - 平台最高權限管理者
    - 管理整個 ActiFlow 平台
    """

    def create(
        self,
        db: Session,
        data: SuperAdminCreate
    ) -> SuperAdmin:
        return super().create(
            db,
            obj_in=data.model_dump(),
        )

    def update(
        self,
        db: Session,
        db_obj: SuperAdmin,
        data: SuperAdminUpdate
    ) -> SuperAdmin:
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=data.model_dump(exclude_unset=True),
        )


super_admin_crud = CRUDSuperAdmin(SuperAdmin)
