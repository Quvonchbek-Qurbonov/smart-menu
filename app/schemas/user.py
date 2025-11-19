from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Register(BaseModel):
    full_name: str
    gender: str
    age: int
    email: str = EmailStr()
    password: str = Field(..., min_length=6)


class RegisterResponse(BaseModel):
    id: int
    full_name: str
    gender: str
    age: int
    email: str
    created_at: datetime
    updated_at: datetime