from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from passlib.context import CryptContext
from .config import settings
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from app.repositries.user_repositries import UserRepositry
from app.schemas.login_token_schema import TokenData
from app.db.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 
def hash_password(password:str):
    return pwd_context.hash(password)

def verify(plainpassword,storedpassword):
    return pwd_context.verify(plainpassword,storedpassword)

def create_access_token(user_id:int) -> str:
    expire_time=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
    "sub": str(user_id),
    "token_type":"access_token",
    "exp": expire_time
}
    token=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return token,expire_time

def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesnt exsist")
        if payload.get("token_type") != "access_token":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldnt verify the user")
    
    return int(user_id)

def get_curent_user(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    token_data=verify_access_token(token)
    Current_User=UserRepositry.get_user_by_user_id(db,token_data)
    if  Current_User is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesnt exsist")
    return  Current_User

def create_refresh_token(user_id:int)->str:
    expire_time=datetime.now(timezone.utc)+timedelta(minutes=settings.refresh_token_expire_minutes)
    payload={
        "sub":str(user_id),
        "token_type":"refresh_token",
        "exp":expire_time
    }
    refresh_token=jwt.encode(payload,settings.secret_key,algorithm=settings.algorithm)
    return refresh_token,expire_time


def verify_refresh_token(token:str):
    try:
        payload=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User doesnt exsist")
        if payload.get("token_type") != "refresh_token":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldnt verify the user")
    