from pydantic import BaseModel,EmailStr

class Login(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    sub:int

class UserEmail(BaseModel):
    email:EmailStr