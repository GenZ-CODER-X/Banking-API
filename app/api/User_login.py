from fastapi import FastAPI,status,Depends,Header,Request
from schemas.login_token_schema import Login,Token,UserEmail
from sqlalchemy.orm import Session
from db import database
from services import login_service,auth_services
from core.security import get_curent_user

app=FastAPI()

@app.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Token
)
def login(
    request: Request,
    user_credentials: Login,
    db: Session = Depends(database.get_db)
):
    user_agent = request.headers.get("User-Agent")
    ip_address = request.client.host

    return login_service.login_user(
    db,
    user_credentials,
    user_agent,
    ip_address,
)
@app.post('/refresh',status_code=status.HTTP_200_OK,response_model=Token)
def refresh(db:Session=Depends(database.get_db),refresh_token:str=Header(...)):
    return login_service.refresh_token(db,refresh_token)

@app.post("/logout",status_code=status.HTTP_200_OK)
def logout(db:Session=Depends(database.get_db),Current_user=Depends(get_curent_user),refresh_token:str=Header(...)):
    return login_service.logout_user(db,Current_user,refresh_token)

@app.post("/forgot_password",status_code=status.HTTP_200_OK)
def forgot_password(current_user_email:UserEmail,db:Session=Depends(database.get_db)):
    return auth_services.forgot_password(db,current_user_email)


