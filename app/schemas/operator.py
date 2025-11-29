from datetime import datetime

from pydantic import BaseModel

class OperatorCreate(BaseModel):
    full_name: str
    gender: str
    age: int
    email: str
    password: str

class OperatorResponse(BaseModel):
    id: int
    full_name: str
    gender: str
    age: int
    email: str
    created_at: datetime
    updated_at: datetime