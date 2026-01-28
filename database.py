from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection():
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL, echo=True)
    return engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_connection())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()