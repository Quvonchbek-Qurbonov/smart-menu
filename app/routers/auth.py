from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import (Activate, ActivateResponse, Register, RegisterResponse, Verify,
                              Login, LoginResponse)
from app.utils.database import get_db
from app.cruds import UserCrud, OtpCrud
from app.models import User, Otp
from app.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    generate_otp
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


@router.post("/register/activate", response_model=ActivateResponse, status_code=status.HTTP_201_CREATED)
def activate(data: Activate, db: Session = Depends(get_db)):
    code = generate_otp()
    otp = Otp(otp=code, user_id=data.user_id)
    OtpCrud.create(db=db, otp=otp)
    return {"code_sent": True}


@router.post("/register/verify", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def verify(data: Verify, db: Session = Depends(get_db)):
    otp = Otp(otp=data.otp, user_id=data.user_id)
    OtpCrud.verify(db=db, data=otp)
    UserCrud.verify(db=db, user_id=data.user_id)
    user = db.query(User).filter(User.id == data.user_id).first()
    return user


@router.post("/register/login", status_code=status.HTTP_201_CREATED)
def login(data: Login, db: Session = Depends(get_db)):
    user = UserCrud.login(db=db, email=data.email, password=data.password)
    data = {"sub": str(user.id)}
    token = create_access_token(data=data)
    return {"data": {
        "id": user.id,
        "full_name": user.full_name,
        "gender": user.gender,
        "age": user.age,
        "email": user.email,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }, "access_token": token}
