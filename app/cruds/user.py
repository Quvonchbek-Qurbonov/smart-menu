from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User, Otp
from app.utils import get_password_hash, verify_password


class UserCrud:
    @staticmethod
    def check_email(db: Session, email: str):
        result = db.query(User).filter(User.email == email).first()
        if result:
            raise HTTPException(400, "Email already registered")
        return True

    @staticmethod
    def add(db: Session, user: User):
        db.add(user)
        db.commit()

    @staticmethod
    def verify(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        user.is_verified = True
        db.commit()

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(400, "Email not registered")
        if not user.is_verified:
            raise HTTPException(400, "Email not verified")
        if not verify_password(password, str(user.hashed_password)):
            raise HTTPException(400, "Incorrect password")
        return user

    @staticmethod
    def update(db: Session, user_id: int, fullname: str, age: int):
        user = db.query(User).filter(User.id == user_id).first()
        user.full_name = fullname
        user.age = age
        db.commit()
        return user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()




