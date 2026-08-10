from fastapi import FastAPI
from app.api.User_login import router as login_router

app = FastAPI()

@app.get("/hello")
def root():
    return {"message": "Welcome to Banking API"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

app.include_router(login_router)