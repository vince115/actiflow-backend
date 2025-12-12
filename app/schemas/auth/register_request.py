# app/schemas/auth/register_request.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    
    email: EmailStr
    password: str = Field(min_length=6)
    name: Optional[str] = None