from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    def __init__(self, db: Session):
        self.db = db
    
    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, id: int, entity_data: dict) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
    
    def _commit_refresh(self, entity: T) -> T:
        self.db.commit()
        self.db.refresh(entity)
        return entity