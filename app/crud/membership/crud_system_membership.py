# app/crud/membership/crud_system_membership.py

from sqlalchemy.orm import Session

from app.crud.base.crud_base import CRUDBase
from app.models.membership.system_membership import SystemMembership
from app.schemas.membership.system.system_membership_create import SystemMembershipCreate
from app.schemas.membership.system.system_membership_update import SystemMembershipUpdate


class CRUDSystemMembership(CRUDBase[SystemMembership]):
    """
    SystemMembership CRUD
    -------------------------------------------------
    用途：
    - 系統層級的使用者身份 / 角色 / 狀態
    - RBAC 核心資料
    """

    def create(
        self, 
        db: Session, 
        data: SystemMembershipCreate
    ) -> SystemMembership:
        return super().create(
            db, 
            obj_in=data.model_dump()
        )

    def update(
        self, 
        db: Session, 
        db_obj: SystemMembership, 
        data: SystemMembershipUpdate
    ) -> SystemMembership:
        return super().update(
            db, 
            db_obj=db_obj, 
            obj_in=data.model_dump(exclude_unset=True)
        )

    # ------------------------------------------------------------
    #  取得某 user 的 SystemMembership（instance method）
    # ------------------------------------------------------------
    def get_by_user_uuid(self, db: Session, user_uuid: str) -> SystemMembership:
        return (
            db.query(SystemMembership)
            .filter(
                SystemMembership.user_uuid == user_uuid,
                SystemMembership.is_deleted == False
            )
            .first()
        )

# 實例化 CRUD
system_membership_crud = CRUDSystemMembership(SystemMembership)

# ------------------------------------------------------------
# ⭐ module-level wrapper（供 API 直接 import）
# ------------------------------------------------------------
def get_system_membership(db: Session, user_uuid: str) -> SystemMembership:
    return system_membership_crud.get_by_user_uuid(db, user_uuid)

