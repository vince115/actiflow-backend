# app/schemas/auth/register_response.py

from pydantic import BaseModel
from app.schemas.user.user_response import UserResponse


class RegisterResponse(BaseModel):

    user: UserResponse

    model_config = {"from_attributes": True}