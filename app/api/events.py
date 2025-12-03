# app/api/events.py
from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/")
def get_events():
    return {"message": "GET all events"}

@router.get("/{event_uuid}")
def get_event(event_uuid: str):
    return {"message": "GET event", "id": event_uuid}

@router.post("/")
def create_event(data: dict):
    return {"message": "Created event", "data": data}

@router.put("/{event_uuid}")
def update_event(event_uuid: str, data: dict):
    return {"message": "Updated event", "id": event_uuid, "data": data}

@router.delete("/{event_uuid}")
def delete_event(event_uuid: str):
    return {"message": "Deleted event", "id": event_uuid}
