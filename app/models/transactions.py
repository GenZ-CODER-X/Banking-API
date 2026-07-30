from db.database import Base
from sqlalchemy import Column,String,Integer,ForeignKey,TIMESTAMP,text,Numeric

class Transaction(Base):
    __tablename__='Transactions'
    id=Column(Integer,primary_key=True)
    amount=Column(Numeric(12,2),nullable=False)
    Transaction_Ref=Column(String,nullable=False,unique=True)
    Sender_ACC_id=Column(Integer,ForeignKey("accounts.id"),nullable=False)
    Receiver_ACC_id=Column(Integer,ForeignKey("accounts.id"),nullable=False)
    status=Column(String,server_default=text("'SUCCESSFUL'"))
    description=Column(String,server_default=text("None"))
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'))

