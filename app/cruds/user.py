from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User


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
