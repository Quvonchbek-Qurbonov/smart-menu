from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Restaurant, Operator


class RestaurantCrud:
    @staticmethod
    def create(db: Session, restaurant: Restaurant):
        existence = db.query(Restaurant).filter(Restaurant.name == restaurant.name).first()
        if existence:
            raise HTTPException(status_code=400, detail="Restaurant with same name exists")
        operator = db.query(Operator).filter(Operator.id == restaurant.owner_id).first()
        if not operator:
            raise HTTPException(status_code=400, detail="Operator not found by given id")

        db.add(restaurant)
        db.commit()
        return restaurant

    @staticmethod
    def get_all(db: Session):
        result = db.query(Restaurant).all()
        if not result:
            raise HTTPException(status_code=404, detail="Restaurants not found")
        return result

    @staticmethod
    def get_by_id(db: Session, id: int):
        result = db.query(Restaurant).filter(Restaurant.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return result