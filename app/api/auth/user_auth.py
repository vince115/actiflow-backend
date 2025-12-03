# app/api/auth/user_auth.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt import create_access_token
from app.core.security import verify_password, hash_password
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from app.crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_uuid,
)
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth/users", tags=["User Auth"])

# ------------------------------------------------------------
# 註冊（一般 Email 註冊）
# ------------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):

    # email 重複判斷
    if data.email:
        exist = get_user_by_email(db, data.email)
        if exist:
            raise HTTPException(400, "Email already registered")

    # 建立使用者
    user = create_user(db, data)

    return UserResponse.from_orm(user)

# ------------------------------------------------------------
# Login（Email + Password）
# ------------------------------------------------------------
@router.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(400, "Email not found")

    if not user.password_hash:
        raise HTTPException(400, "This account must login via provider login")

    if not verify_password(password, user.password_hash):
        raise HTTPException(400, "Incorrect password")

    # JWT payload（sub = user.uuid）
    token = create_access_token({"sub": str(user.uuid)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user),
    }

# ------------------------------------------------------------
# 取得自己的資料
# ------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return UserResponse.from_orm(current_user)


# ------------------------------------------------------------
# 更新自己的資料
# ------------------------------------------------------------
@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # 更新資料
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return UserResponse.from_orm(current_user)


# ------------------------------------------------------------
# 修改密碼
# ------------------------------------------------------------
@router.post("/change-password")
def change_password(
    old_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # ← 明確告訴它是 User
):

    if not current_user.password_hash:
        raise HTTPException(400, "This account does not support password login")

    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(400, "Old password incorrect")

    current_user.password_hash = hash_password(new_password)
    db.commit()

    return {"message": "Password updated successfully"}


# ------------------------------------------------------------
# 忘記密碼（可選）
# ------------------------------------------------------------
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    """
    你之後可以實作：
    1. 產生 token
    2. 寄出 email
    3. 讓 user reset password
    """
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(400, "Email not found")

    return {"message": "Password reset flow not implemented yet"}

# ------------------------------------------------------------

@router.get("/oauth2/google")
def google_login():
    """
    未來這裡放 Google OAuth2 redirect
    """
    return {"message": "Google login pending implementation"}


@router.get("/oauth2/facebook")
def fb_login():
    """
    未來這裡放 Facebook OAuth2 redirect
    """
    return {"message": "Facebook login pending implementation"}
