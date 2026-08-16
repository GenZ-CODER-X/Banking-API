from db.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text

class Audit(Base):
    __tablename__ = "Audit_log"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    transaction_id = Column(
        Integer,
        ForeignKey("Transactions.id", ondelete="CASCADE"),
        nullable=True
    )
    action = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )