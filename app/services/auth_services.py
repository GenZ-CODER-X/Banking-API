from fastapi import HTTPException,status
from repositries.user_repositries import UserRepositry
from hashing import hash_password
import uuid
from repositries.redis_repositries import RedisRepository
from email_service import send_verification_email
redis=RedisRepository()
def register_user(db,user_details):

    exisisting_user_email=UserRepositry.get_by_email(db,user_details.email)
    exisisting_user_ph_no=UserRepositry.get_by_ph_no(db,user_details.ph_no)
    if exisisting_user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with given email exsists")
    if exisisting_user_ph_no:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User with given ph_no exsists")
    
    hashed_password=hash_password(user_details.password)
    user_details.password=hashed_password
    new_user=UserRepositry.create_user(db,user_details)
    db.commit()
    verification_token=uuid.uuid4().hex
    redis.store_verification_token(verification_token,new_user.id)
    verification_link = (
    f"http://localhost:8000/verify-email?token={verification_token}"
)
    send_verification_email(new_user.email,verification_link)
    return new_user

def verify_email(db, token):
    try:
        user_id=redis.email_token_verification(token)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Invalid Token or link expired")
        UserRepositry.mark_email_verified(db,user_id)
        redis.delete_verification_token(verification_token)
        db.commit()

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )
    return {
        "message":"Email verification successful"
    }
        

