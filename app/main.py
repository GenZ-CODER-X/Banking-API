from fastapi import FastAPI

app=FastAPI() 

@app.get("/hello")
def root():
    return  {"message":"Welcome to Banking API"}

@app.get("user/{user_id}")
def get_user():
    return {"user_id":10}