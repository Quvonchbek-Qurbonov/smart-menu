from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryResponse
from app.cruds.category import CategoryCRUD
from app.utils.auth import get_current_user
from app.utils.database import get_db

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/restaurant/{restaurant_id}", response_model=list[CategoryResponse])
def get_restaurant_categories(
        rest_id: int,
        db: Session = Depends(get_db), payload = Depends(get_current_user)
):
    """Get all categories for a specific restaurant"""
    categories = CategoryCRUD.get_categories(db, restaurant_id=rest_id)
    return categories


@router.post("/new", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db), payload = Depends(get_current_user)
):
    """Create a new category"""
    # Check if category already exists for this restaurant
    existing = db.query(Category).filter(
        Category.name == category_data.name,
        Category.restaurant_id == category_data.restaurant_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category '{category_data.name}' already exists for this restaurant"
        )

    new_category = CategoryCRUD.create_category(db, category_data)
    return new_category