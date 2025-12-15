# app/api/auth/logout.py

from fastapi import APIRouter, Response

router = APIRouter()


@router.post("/logout")
def logout(response: Response):
    """
    登出：清除 access_token、refresh_token Cookie
    """

    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return {"message": "Logged out successfully"}
