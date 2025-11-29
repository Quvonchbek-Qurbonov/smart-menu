from pydantic import BaseModel
from typing import Optional

class MealCreate(BaseModel):

    name: str
    price: float
    category_id: int
    image_url: str
    description: Optional[str] = None

class MealResponse(BaseModel):
    name: str
    price: float
    category_id: int
    image_url: str
    description: str




