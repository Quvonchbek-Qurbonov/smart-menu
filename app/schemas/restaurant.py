from datetime import datetime

from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    owner_id: int
    description: str
    avatar: str
    location: str


class RestaurantResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    description: str
    avatar: str
    location: str
    views: int
    scans: int
    created_at: datetime