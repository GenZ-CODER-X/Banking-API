from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Transaction(BaseModel):
    amount:float
    Receiver_acc_no:str
    description:str
class Transaction_Response(BaseModel):
    amount:float
    Transaction_Ref:str
    status:str

class TransactionHistoryResponse(BaseModel):
    Transaction_Ref:str
    amount:Decimal
    sender_account:str
    receiver_account:str
    status:str
    description:str | None = None
    created_at:datetime