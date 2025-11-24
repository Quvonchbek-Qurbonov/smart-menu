from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Otp


class OtpCrud:
    @staticmethod
    def create(db: Session, otp: Otp):
        db.add(otp)
        db.commit()


    @staticmethod
    def verify(db: Session, data: Otp):
        otp = db.query(Otp).filter(Otp.otp == data.otp, Otp.user_id == data.user_id).first()
        if otp:
            db.delete(otp)
            db.commit()
            return True
        else:
            raise HTTPException(404, "OTP not found")
