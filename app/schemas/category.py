from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    icon: str
    restaurant_id: int


class CategoryResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str
    icon: str



