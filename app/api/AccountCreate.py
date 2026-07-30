from fastapi import FastAPI,Depends,status
from schemas import Account_schema
from db import database
from sqlalchemy.orm import Session
from sqlalchemy import text
from services import AccountCreation
from core.security import get_curent_user

app=FastAPI()
@app.post('/create_account',status_code=status.HTTP_201_CREATED,response_model=Account_schema.Account)
def account_create(account_credentials:Account_schema.AccountCreate,db:Session=Depends(database.get_db),current_user=Depends(get_curent_user)):
    return AccountCreation.account_creation(account_credentials,db,current_user)


