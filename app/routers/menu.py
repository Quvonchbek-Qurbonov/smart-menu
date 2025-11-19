from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.models.menu import Category, MenuItem
from app.models.user import User
from app.schemas.menu import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    MenuItemCreate, MenuItemUpdate, MenuItemResponse
)
from app.utils.dependencies import get_admin_user

router = APIRouter(prefix="/menu", tags=["Menu"])


# ========== CATEGORIES ==========

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        is_active: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all categories (public endpoint)"""
    query = db.query(Category)

    if is_active is not None:
        query = query.filter(Category.is_active == is_active)

    categories = query.offset(skip).limit(limit).all()
    return categories


@router.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Create a new category (Admin only)"""
    # Check if category with same name exists
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )

    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Update a category (Admin only)"""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Update fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Delete a category (Admin only)"""
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check if category has menu items
    if category.menu_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with existing menu items"
        )

    db.delete(category)
    db.commit()

    return None


# ========== MENU ITEMS ==========

@router.get("/items", response_model=List[MenuItemResponse])
def get_menu_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        category_id: Optional[int] = None,
        is_available: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """Get all menu items (public endpoint)"""
    query = db.query(MenuItem)

    if category_id:
        query = query.filter(MenuItem.category_id == category_id)

    if is_available is not None:
        query = query.filter(MenuItem.is_available == is_available)

    items = query.offset(skip).limit(limit).all()
    return items


@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item by ID"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    return item


@router.post("/items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(
        item_data: MenuItemCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Create a new menu item (Admin only)"""
    # Verify category exists
    category = db.query(Category).filter(Category.id == item_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    item = MenuItem(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
        item_id: int,
        item_data: MenuItemUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Update a menu item (Admin only)"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    # If category_id is being updated, verify it exists
    if item_data.category_id:
        category = db.query(Category).filter(Category.id == item_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

    # Update fields
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
        item_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_admin_user)
):
    """Delete a menu item (Admin only)"""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )

    db.delete(item)
    db.commit()

    return None