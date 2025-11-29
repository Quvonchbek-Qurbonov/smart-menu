from typing import Optional
from sqlalchemy.orm import Session

from app.models import Meal, Category
from app.schemas.meal import MealCreate




class MealCRUD:

    @staticmethod
    def get_meals_by_restaurant(db: Session, restaurant_id: int):
        """Get all meals for a restaurant through categories"""
        return db.query(Meal).join(Category).filter(
            Category.restaurant_id == restaurant_id
        ).all()

    @staticmethod
    def create_meal(db: Session, meal: MealCreate):
        db_meal = Meal(**meal.dict())
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal

    @staticmethod
    def update_meal(db: Session, meal_id: int, meal: MealCreate):
        db_meal = MealCRUD.get_meal(db, meal_id)
        if not db_meal:
            return None

        update_data = meal.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_meal, key, value)

        db.commit()
        db.refresh(db_meal)
        return db_meal

    @staticmethod
    def delete_meal(db: Session, meal_id: int):
        db_meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if db_meal:
            db.delete(db_meal)
            db.commit()
            return True
        return False




