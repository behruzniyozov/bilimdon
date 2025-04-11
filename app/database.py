from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session, DeclarativeBase
from typing import Annotated
from fastapi import Depends

from dotenv import load_dotenv
import os

# Get values from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

# Fix for the db_port issue
if not db_port or db_port.lower() == "none":
    db_port = "5432"  # Default PostgreSQL port

# Build the SQLAlchemy connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Base class - use this if you're using SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# Or use this if you're using an older SQLAlchemy version
# Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency
DB_DEPENDENCY = Annotated[Session, Depends(get_db)]