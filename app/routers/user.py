from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserUpdate, UserResponse
from app.utils.database import get_db
from app.utils.auth import get_current_user
from app.cruds.user import UserCrud

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/users", tags=["User cruds"])
security = HTTPBearer()


@router.put("/update", response_model=UserResponse)
def update(user: UserUpdate, db: Session = Depends(get_db), payload = Depends(get_current_user)):
    result = UserCrud.update(db, payload["sub"], user.full_name, user.age)
    return result


@router.get("/all", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), payload = Depends(get_current_user)):
    users = UserCrud.get_all_users(db)
    return users