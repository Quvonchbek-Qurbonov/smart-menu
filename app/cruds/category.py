from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category import CategoryCreate, CategoryResponse


class CategoryCRUD:


    @staticmethod
    def get_categories(db: Session, restaurant_id: int, skip: int = 0, limit: int = 100):
        query = db.query(Category)
        if restaurant_id:
            query = query.filter(Category.restaurant_id == restaurant_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        db_category = Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryResponse):
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None

        update_data = category.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False