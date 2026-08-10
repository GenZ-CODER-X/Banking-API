from fastapi import HTTPException, status

from app.repositries.user_repositries import UserRepositry
from app.services.hashing import verify
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from app.repositries.redis_repositries import RedisRepository
from app.repositries.login_repositry import LoginRepositry
def login_user(db, login_details,user_agent,ip_address):
    user = UserRepositry.get_by_email(db, login_details.email)

    if user is None:
        raise HTTPException(...)

    if not verify(login_details.password, user.password):
        raise HTTPException(...)
    
    
    refresh_token,expire_time_refresh_token=create_refresh_token(user.id)
    refresh_token_entry_data={
        "user_id":user.id,
        "refresh_token_hash":refresh_token,
        "device_name":user_agent,
        "expires_at":expire_time_refresh_token
    }
    LoginRepositry.refresh_token_to_db(db,refresh_token_entry_data)

    access_token = create_access_token(user.id)

    db.commit()

    return {
        "refresh_token":refresh_token,
        "access_token": access_token,
        "token_type": "bearer"
    }

#Flow of my logout API
#1.verify the refresh token 
# 2.Then blacklist the refresh token no need of access_token due to its short time and 
# 3.delete the refrsh token from db

def logout_user(db,refresh_token):
    redis_repo=RedisRepository()
    try:
        user_id=verify_refresh_token(refresh_token)
        is_valid = redis_repo.refresh_token_check(refresh_token)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Already logged out"
            )
        RedisRepository.blacklist_refresh_token(refresh_token,user_id)
        refresh_session = LoginRepositry.search_refresh_token(db, refresh_token)
        if refresh_session is None:
            raise HTTPException(
                status_code=401,
                detail="Session not found"
            )
        LoginRepositry.delete_refresh_token(db,refresh_token)
        db.commit()
        return {"message":"Logout Successful"}
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Logout Failed")

#Flow of my refresh
#1.Verify the JWT they sent 
#2.Check the redis if the token is blacklisted
#3.query the db
#5. Create a new refresh token and replace the old one in the DB
#6.blacklist the token 

def refresh_token(db,refresh_token):
    redis_repo=RedisRepository()
    try:
        user_id=verify_refresh_token(refresh_token)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"login attempt failed")
        status=redis_repo.refresh_token_check(refresh_token)
        if status==False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"loged out of device")
        refresh_session=LoginRepositry.search_refresh_token(db,refresh_token)
        if refresh_session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Authentication Failed")
        new_access_token = create_access_token(refresh_session.user_id)
        new_refresh_token,new_expire_time=create_refresh_token(refresh_session.user_id)
        redis_repo.blacklist_refresh_token(refresh_token,refresh_session.user_id)
        LoginRepositry.update_refresh_token(db,refresh_session,new_refresh_token,new_expire_time)
        db.commit()
        return {
    "access_token": new_access_token,
    "refresh_token": new_refresh_token,
    "token_type": "bearer"
}
    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Refresh token failed"
        )
    




    
    