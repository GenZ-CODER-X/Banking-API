from fastapi import FastAPI,status,Depends,Header
from schemas.login_token_schema import Login,Token
from sqlalchemy.orm import Session
from db import database
from services import login_service
from repositries.user_repositries import UserRepositry

app=FastAPI()
@app.post('/login',status_code=status.HTTP_202_ACCEPTED,response_model=Token)
def login(user_credentials:Login,db:Session=Depends(database.get_db)):
    return login_service.login_user(db, user_credentials)


@app.post('/refresh',status_code=status.HTTP_100_CONTINUE,response_model=Token)
def refresh(db:Session=Depends(database.get_db),refresh_token:str=Header(...),):
    

