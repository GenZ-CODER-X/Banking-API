from fastapi import HTTPException,status
from repositries.user_repositries import UserRepositry
from hashing import hash_password
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
    return new_user
def new_user_confirmation_email():
    pass

