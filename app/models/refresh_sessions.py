from db.database import Base
from sqlalchemy import Column,String,Integer,TIMESTAMP,text

class Refresh_session(Base):
    __tablename__="refresh_session"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,nullable=False)
    refresh_token_hash=Column(String,nullable=False,unique=True)
    device_name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'))
