from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import Operator


class OperatorCrud:
    @staticmethod
    def create(db: Session, operator: Operator):
        result = db.query(Operator).filter(Operator.email == operator.email).first()
        if result:
            raise HTTPException(status_code=400, detail="Email already registered")
        db.add(operator)
        db.commit()
        return operator

