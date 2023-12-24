from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import db connection from env
import os


SQLALCHEMY_DATABASE_URL = os.getenv("DBCONN") or "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()