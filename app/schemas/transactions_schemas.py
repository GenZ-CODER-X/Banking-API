from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Transaction(BaseModel):
    amount:Decimal
    Receiver_acc_no:str
    description:str
class Transaction_Response(BaseModel):
    amount:Decimal
    Transaction_Ref:str
    status:str

class TransactionHistoryResponse(BaseModel):
    Transaction_Ref:str
    amount:Decimal
    sender_account_no:str
    receiver_account_no:str
    status:str
    description:str | None = None
    created_at:datetime

