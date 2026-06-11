from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import DB_URL

# create engine
engine = create_engine(
      DB_URL,
      pool_size=10,          
      max_overflow=20,
      pool_pre_ping=True  
)

# create SessionLocal
SessionLocal = sessionmaker(
      autocommit=False,
      autoflush=False,
      bind=engine
)

# Base class for models
Base = declarative_base()


# get_db dependency for endpoints
def get_db() -> Generator[Session, None, None]:
      '''
      create session for each request
      '''
      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()