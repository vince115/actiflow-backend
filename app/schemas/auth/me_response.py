# app/schemas/auth/me_response.py

from pydantic import BaseModel
from app.schemas.user.user_response import UserResponse


class MeResponse(BaseModel):

    user: UserResponse
    
    model_config = {"from_attributes": True}
