# app/api/activity_templates.py

from fastapi import APIRouter

router = APIRouter(prefix="/activity-templates", tags=["Activity Templates"])

@router.get("/")
def list_activity_templates():
    return {"message": "OK"}
