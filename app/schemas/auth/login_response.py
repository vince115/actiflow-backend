# app/schemas/auth/login_response.py

from pydantic import BaseModel
from app.schemas.user.user_response import UserResponse

class LoginResponse(BaseModel):
   
    user: UserResponse

    model_config = {"from_attributes": True}

