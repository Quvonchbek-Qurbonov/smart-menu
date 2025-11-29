from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Operator
from app.schemas.operator import OperatorCreate, OperatorResponse
from app.utils.database import get_db
from app.utils.auth import get_current_user, get_password_hash
from app.cruds.operator import OperatorCrud


router = APIRouter(prefix="/operators", tags=["Operator cruds"])


@router.post("/operator", response_model=OperatorResponse)
def create(body: OperatorCreate, db: Session = Depends(get_db), payload = Depends(get_current_user)):
    try:
        role = payload["role"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    if role.lower() != "admin":
        raise HTTPException(status_code=400, detail="You do not have permission to perform this action")
    operator = Operator(
        full_name = body.full_name,
        gender = body.gender,
        age = body.age,
        email = body.email,
        hashed_password = get_password_hash(body.password),
    )

    return OperatorCrud.create(db, operator)

