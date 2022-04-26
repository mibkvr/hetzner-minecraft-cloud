import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
connect_args = {"check_same_thread": False}

# Default to local SQL-Lite File if POSTGRES is none
if POSTGRES_HOST is not None:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB_NAME}"
    connect_args = {}
else:
    logging.exception("No POSTGRES_HOST found, using SQL-Lite")
# pool_pre_ping to check if connection is still alive
# recycle to keep the connection open


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=3600, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
