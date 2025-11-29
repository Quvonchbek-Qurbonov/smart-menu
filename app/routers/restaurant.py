from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import Restaurant
from app.schemas.restaurant import RestaurantResponse, RestaurantCreate
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.cruds.restaurant import RestaurantCrud


router = APIRouter(prefix="/restaurants", tags=["Restaurants cruds"])


@router.post("", response_model=RestaurantResponse)
def create(body: RestaurantCreate, db: Session = Depends(get_db), payload = Depends(get_current_user)):
    try:
        role = payload["role"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    if role.lower() in ["operator", "admin"]:
        restaurant = Restaurant(name=body.name,
                                owner_id=body.owner_id,
                                description=body.description,
                                avatar=body.avatar,
                                location=body.location)
        result = RestaurantCrud.create(db=db, restaurant=restaurant)
        return result
    raise HTTPException(status_code=401, detail="You do not have permission to perform this action")


@router.get("/all", response_model=List[RestaurantResponse])
def get_all(db: Session = Depends(get_db)):
    return RestaurantCrud.get_all(db=db)


@router.get("/{id}", response_model=RestaurantResponse)
def get(id: int, db: Session = Depends(get_db)):
    return RestaurantCrud.get_by_id(id=id, db=db)