from fastapi import FastAPI,HTTPException,status,Depends,Header
from db.database import get_db
from schemas.transactions_schemas import Transaction,Transaction_Response
from sqlalchemy.orm import Session
from core.security import get_curent_user
from services.Transaction_services import transaction

app=FastAPI()
@app.post('/transactions',response_model=Transaction_Response)
def transaction(transaction_details:Transaction,db:Session=Depends(get_db),Current_user=Depends(get_curent_user),idempotency_key: str = Header(...)):
    return transaction(db,Current_user,transaction_details)