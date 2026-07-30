from pydantic import BaseModel,EmailStr,Timestamp
from datetime import datetime

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str
    ph_no:str
    
#Schema For user_out of registartion
class Userout(BaseModel):
    name:str
    created_at:datetime




