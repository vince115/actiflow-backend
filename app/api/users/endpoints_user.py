# app/api/users/endpoints_user.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.db import get_db
from app.core.security import verify_password, hash_password
from app.core.jwt import create_access_token
from app.core.dependencies import get_current_user

from app.schemas.user.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    UserLoginResponse
)
from crud.user.user import (
    create_user,
    list_users,
    get_user_by_email,
    get_user_by_uuid,
    update_user,
    soft_delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])

# ============================================================
# 一般使用者區（無需 system_admin）
# ============================================================

# ------------------------------------------------------------
# 1. 註冊 User Register
# ------------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):

    # Email unique
    exist = get_user_by_email(db, data.email)
    if exist:
        raise HTTPException(400, "Email already registered")

    user = create_user(db, data)
    return UserResponse.model_validate(user)


# ------------------------------------------------------------
# 2. 登入 User Login
# ------------------------------------------------------------
@router.post("/login", response_model=UserLoginResponse)
def login_user(data: UserLogin, db: Session = Depends(get_db)):

    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(400, "Email not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "Incorrect password")

    token = create_access_token({
        "sub": str(user.uuid),
        "role": "user"
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user),
    }


# ------------------------------------------------------------
# 3.取得自己資料 Get my profile
# ------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


# ------------------------------------------------------------
# 4.更新自己資料 Update my profile
# ------------------------------------------------------------
@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_user = update_user(db, current_user.uuid, data)
    return UserResponse.model_validate(updated_user)


# ------------------------------------------------------------
# 5. 變更密碼 Change password
# ------------------------------------------------------------
@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(400, "Old password incorrect")

    current_user.password_hash = hash_password(new_password)
    db.commit()

    return {"message": "Password updated successfully"}

# ============================================================
# 系統管理員區（system_admin 才能操作）
# ============================================================

def assert_system_admin(user):
    if user.role != "system_admin":
        raise HTTPException(403, "Only system_admin can perform this action")
    
# ------------------------------------------------------------
# 6. 建立使用者（後台專用）
# ------------------------------------------------------------
@router.post("/", response_model=UserResponse)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_system_admin(user)

    return create_user(db, data)


# ------------------------------------------------------------
# 7. 管理員查看全部使用者（含搜尋）
# ------------------------------------------------------------
@router.get("/", response_model=List[UserResponse])
def list_all_users(
    q: Optional[str] = Query(None, description="搜尋 email / name / phone"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_system_admin(user)

    users = list_users(db, skip=skip, limit=limit)

    if q:
        q_lower = q.lower()
        users = [
            u for u in users
            if (
                (u.email and q_lower in u.email.lower()) or
                (u.name and q_lower in u.name.lower()) or
                (u.phone and q_lower in str(u.phone))
            )
        ]

    return users

# ------------------------------------------------------------
# 8. 管理員讀取使用者
# ------------------------------------------------------------
@router.get("/{user_uuid}", response_model=UserResponse)
def get_single_user(
    user_uuid: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_system_admin(user)

    target = get_user_by_uuid(db, user_uuid)
    if not target or target.is_deleted:
        raise HTTPException(404, "User not found")
    return UserResponse.model_validate(target)


# ------------------------------------------------------------
# 9. 管理員更新使用者 Update user (system_admin)
# ------------------------------------------------------------
@router.put("/{user_uuid}", response_model=UserResponse)
def update_user_detail(
    user_uuid: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_system_admin(user)

    user = update_user(db, user_uuid, data)
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse.model_validate(user)

# ------------------------------------------------------------
# 10. 管理員軟刪除使用者 Soft delete user (system_admin)
# ------------------------------------------------------------
@router.delete("/{user_uuid}")
def delete_user(
    user_uuid: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    assert_system_admin(user)

    deleted = soft_delete_user(db, user_uuid)
    if not deleted:
        raise HTTPException(404, "User not found")
    return {"deleted": True}

