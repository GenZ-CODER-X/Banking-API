from pydantic import BaseModel

class Transaction(BaseModel):
    amount:float
    Receiver_acc_no:str
    description:str
class Transaction_Response(BaseModel):
    amount:float
    Transaction_Ref:str
    status:str
