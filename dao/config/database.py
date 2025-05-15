from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import dotenv_values

try:
    config = dotenv_values(".env")

    DATA_BASE_URL = os.getenv("DATABASE_URL", config.get("DATABASE_URL"))

    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:verysecret@localhost:33789/MALVADER'

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
    
except Exception as e:
    print(f"Error loading database configuration: {e}")
    raise