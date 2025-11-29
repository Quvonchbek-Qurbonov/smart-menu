
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.cruds.meal import MealCRUD
from app.schemas.meal import MealCreate, MealResponse
from app.schemas.user import UserResponse
from app.utils.auth import get_current_user
from app.utils.database import get_db

router = APIRouter(prefix="/meals", tags=["Meals"])


@router.get("/category/{category_id}", response_model=MealResponse, status_code=status.HTTP_200_OK)
def get_meals( category_id: int, db: Session = Depends(get_db), payload=Depends(get_current_user)):
    """Get all meals for a specific restaurant and category"""
    meals = MealCRUD.get_meals_by_restaurant(db, category_id)
    return meals


@router.post("/new",  status_code=status.HTTP_201_CREATED)
def create_meal(meal_data: MealCreate, db: Session = Depends(get_db), payload=Depends(get_current_user)):
    """Create a new meal"""
    new_meal = MealCRUD.create_meal(db, meal_data)
    return new_meal
