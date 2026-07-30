from db.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,text,Numeric,TIMESTAMP

class Ledger(Base):
    __tablename__="ledger"
    account_id=Column(Integer,ForeignKey("accounts.id"))
    transaction_id=Column(Integer,ForeignKey("transactions.id"))
    amount=Column(Numeric(12,2),nullable=False)
    transaction_type=Column(String,nullable=False)
    noted_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'))
