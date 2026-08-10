from app.db.database import Base
from sqlalchemy import Column,String,Integer,TIMESTAMP,text

class RefreshSession(Base):
    __tablename__="refresh_sessions"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,nullable=False)
    refresh_token_hash=Column(String,nullable=False,unique=True)
    device_name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=text('now()'))
    expires_at = Column(TIMESTAMP, nullable=False)
