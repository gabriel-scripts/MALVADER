from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values
config = dotenv_values(".env")
import os

banco = os.getenv('DB_NAME')
senha = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}/{banco}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()