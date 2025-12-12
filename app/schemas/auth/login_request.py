# app/schemas/auth/login_request.py

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    
    email: EmailStr
    
    password: str