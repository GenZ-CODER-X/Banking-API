from db.database import Base
from sqlalchemy import Column,String,Integer,PrimaryKey,text,ForeignKey,TIMESTAMP,Numeric

class Account(Base):
    __tablename__="accounts"
    id=Column(Integer,primary_key=True)
    account_number=Column(String,unique=True,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete='CASCADE'))
    account_type=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    status=Column(String,server_default=text('Active'))
    balance=Column(Numeric(12,2),nullable=False,server_default=0)