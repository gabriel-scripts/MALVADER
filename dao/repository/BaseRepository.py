from abc import abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def create(self, entity_data: dict) -> T:
        pass

    @abstractmethod
    async def update(self, id: int, entity_data: dict) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        pass