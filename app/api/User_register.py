from fastapi import status,HTTPException,FastAPI,Response,Depends
from fastapi.params import Body
from pydantic import BaseModel
from repositries import user_repositries
from schemas import User_schemas
from sqlalchemy.orm import Session
from db import database
from services import auth_services,email_service
app=FastAPI()

@app.post('/register',status_code=status.HTTP_201_CREATED,response_model=User_schemas.Userout)
def user_register(user_details:User_schemas.UserCreate,db:Session=Depends(database.get_db)):
    return auth_services.register_user(db,user_details)
    
@app.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(database.get_db)
):
    return email_service.verify_email(db, token)

@app.post("/reset-password")
def reset_password(
    request:User_schemas.ResetPassword,
    db:Session=Depends(database.get_db)
):
    return auth_services.reset_password(request,db)