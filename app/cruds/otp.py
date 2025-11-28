from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Otp, User
from app.utils.email import send_otp


class OtpCrud:
    @staticmethod
    def create(db: Session, otp: Otp):
        user = db.query(User).filter(User.id == otp.user_id).first()
        try:
            send_otp(email=user.email, otp=otp.otp)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Email is not sent")
        db.add(otp)
        db.commit()


    @staticmethod
    def verify(db: Session, data: Otp):
        otp = db.query(Otp).filter(Otp.otp == data.otp, Otp.user_id == data.user_id).first()
        if otp:
            db.delete(otp)
            db.commit()
        else:
            raise HTTPException(404, "OTP not found")