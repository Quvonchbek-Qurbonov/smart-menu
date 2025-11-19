from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.cruds.user import UserCrud
from app.models import User
from app.schemas import Register, RegisterResponse
from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register/user", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: Register, db: Session = Depends(get_db)):
    UserCrud.check_email(db, user_data.email)
    password_hash = get_password_hash(user_data.password)
    user = User(full_name=user_data.full_name,
                gender=user_data.gender,
                age=user_data.age,
                email=user_data.email,
                hashed_password=password_hash,
                is_verified=False)
    UserCrud.add(db=db, user=user)
    return {
        "id": user.id,
        "full_name": user.full_name,
        "gender": user.gender,
        "age": user.age,
        "email": user.email,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }