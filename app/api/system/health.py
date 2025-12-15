# app/api/system/health.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/system/health",
    tags=["System - Health"],
)


@router.get("/")
def health_check():
    """
    系統健康檢查（Cloud Run / Load Balancer 用）
    """
    return {
        "status": "ok",
        "service": "actiflow-backend",
    }
