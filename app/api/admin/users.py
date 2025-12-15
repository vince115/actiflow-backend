# app/api/admin/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_super_admin

from app.crud.user.crud_user import user_crud

from app.schemas.user.user_update import UserUpdate
from app.schemas.user.user_public import UserPublic

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin - Users"]
)

# ------------------------------------------------------------
# 1. 列出所有使用者（僅 super_admin）
# ------------------------------------------------------------
@router.get("/", response_model=list[UserPublic])
def admin_list_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    users = user_crud.get_multi(db)
    return users


# ------------------------------------------------------------
# 2. 查看單一使用者（僅 super_admin）
# ------------------------------------------------------------
@router.get("/{uuid}", response_model=UserPublic)
def admin_get_user(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    user = user_crud.get(db, uuid)
    if not user:
        raise HTTPException(404, "User not found")
    return user


# ------------------------------------------------------------
# 3. 更新使用者資料（僅 super_admin）
# ------------------------------------------------------------
@router.put("/{uuid}", response_model=UserPublic)
def admin_update_user(
    uuid: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    db_obj = user_crud.get(db, uuid)
    if not db_obj:
        raise HTTPException(404, "User not found")
    updated = user_crud.update(db, db_obj=db_obj, data=data)

    if not updated:
        raise HTTPException(404, "User not found")

    return updated


# ------------------------------------------------------------
# 4. 假刪除使用者（僅 super_admin）
# ------------------------------------------------------------
@router.delete("/{uuid}")
def admin_soft_delete_user(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    deleted = user_crud.delete(db, uuid)
    if not deleted:
        raise HTTPException(404, "User not found")

    return {"message": "User soft-deleted", "uuid": uuid}


# ------------------------------------------------------------
# 5. 強制重設密碼（僅 super_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/force-reset-password")
def admin_force_reset_password(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    new_pass = user_crud.force_reset_password(db, uuid)
    if not new_pass:
        raise HTTPException(404, "User not found")

    return {
        "message": "Password force reset",
        "uuid": uuid,
        "new_password": new_pass  # ⚠ 可選：要不要回傳明碼按需求決定
    }


# ------------------------------------------------------------
# 6. 停用帳號（僅 super_admin）
# ------------------------------------------------------------
@router.post("/{uuid}/disable")
def admin_disable_user(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_super_admin)
):
    ok = user_crud.delete(db, uuid)
    if not ok:
        raise HTTPException(404, "User not found")

    return {
        "message": "User disabled", 
        "uuid": uuid
    }



@router.post("/{uuid}/enable")
def admin_enable_user(
    uuid: str,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_super_admin),
):
    ok = user_crud.set_active(db, uuid, True)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "User enabled",
        "uuid": uuid,
    }