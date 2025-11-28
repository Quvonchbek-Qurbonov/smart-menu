from datetime import datetime
from pydantic import BaseModel


class UserUpdate(BaseModel):
    full_name: str
    age: int


class UserResponse(BaseModel):
    id: int
    full_name: str
    gender: str
    age: int
    email: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
