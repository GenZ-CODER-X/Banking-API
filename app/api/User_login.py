from fastapi import FastAPI,status,Depends
from schemas.login_token_schema import Login,Token
from sqlalchemy.orm import Session
from db import database
from repositries.user_repositries import UserRepositry

app=FastAPI()
@app.post('/login',status_code=status.HTTP_202_ACCEPTED,response_model=Token)
def login(user_credentials:Login,db:Session=Depends(database.get_db)):
    return login(db, user_credentials)
    