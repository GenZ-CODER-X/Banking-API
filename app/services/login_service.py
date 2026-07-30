from fastapi import HTTPException,status
from repositries.user_repositries import UserRepositry
from hashing import verify
from core.security import create_access_token

def login_user(db, login_details):
    user = UserRepositry.get_by_email(db, login_details.email)

    if user is None:
        raise HTTPException(...)

    if not verify(login_details.password, user.password):
        raise HTTPException(...)

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }