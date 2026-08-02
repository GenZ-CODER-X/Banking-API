from fastapi import HTTPException,status
from repositries.user_repositries import UserRepositry
from hashing import verify
from core.security import create_access_token,create_refresh_token,verify_refresh_token
from repositries.redis_repositries import RedisRepository
from repositries.login_repositry import LoginRepositry


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

def logout_user(db,Current_User,refresh_token):
    user_id=verify_refresh_token(refresh_token)
    RedisRepository.blacklist_refresh_token(refresh_token,user_id)
    LoginRepositry.delete_refresh_token(refresh_token)
    db.commit()
    return 

#Flow of my refresh
#1.Verify the JWT they sent 
#2.Check the redis if the token is blacklisted
#3.query the db
#5. Create a new refresh token and replace the old one in the DB
#6.blacklist the token 

def refresh_token(db,refresh_token):
    user_id=verify_refresh_token(refresh_token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"login attempt failed")
    status=RedisRepository.refresh_token_check(refresh_token)
    if status==False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"loged out of device")
    Current_User=LoginRepositry.search_refresh_token(db,refresh_token)
    if Current_User is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Authentication Failed")
    new_access_token = create_access_token(Current_User.user_id)
    new_refresh_token=create_refresh_token(Current_User.user_id)
    RedisRepository.blacklist_refresh_token(refresh_token,Current_User.user_id)
    LoginRepositry.update_refresh_token(db,Current_User,new_refresh_token)
    db.commit()
    return {
    "access_token": new_access_token,
    "refresh_token": new_refresh_token,
    "token_type": "bearer"
}

    




    
    