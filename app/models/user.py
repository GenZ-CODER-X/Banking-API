from db.database import Base
from sqlalchemy.sql.expression import null
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,Boolean

class User(Base):
     __tablename__ = "users"
     id=Column(Integer,primary_key=True)
     name=Column(String(100),nullable=False)
     email=Column(String(25),nullable=False,unique=True)
     password_hash=Column(String,nullable=False)
     phone_number=Column(String(15),unique=True,nullable=False)
     role=Column(String,nullable=False)
     is_verified=Column(Boolean,nullable=False,server_default=text('false'))
     created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
     updated_at=Column(TIMESTAMP,nullable=False,server_default=text('now()'))
     