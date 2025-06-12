from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

import os

try:
    async def get_async_session():
        async with SessionLocal() as session:
            yield session

    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+asyncmy://root:verysecret@localhost:33789/MALVADER")

    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600
    )

    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    Base = declarative_base()
    
except Exception as e:
    print(f"Error loading database configuration: {e}")
    raise