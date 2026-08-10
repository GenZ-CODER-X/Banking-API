from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core import config

db_url=config.settings.database_url
engine=create_engine(db_url)
Base=declarative_base()
sessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

def get_db():
    print("Waiting for the connection")
    db=sessionLocal()
    try:
        print("Connecting to DB")
        yield db
        print("Connected to DB")
        
    finally:
        db.close()
