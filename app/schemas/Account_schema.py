from pydantic import BaseModel
from datetime import datetime

class AccountCreate(BaseModel):
    account_type:str

class Account(BaseModel):
   account_id:int
   account_number:str
   user_id:int
   account_type:str
   created_at:datetime
   status:str
   balance:float
   class config:
       orm_mode=True