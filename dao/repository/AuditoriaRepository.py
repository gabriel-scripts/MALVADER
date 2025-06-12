from typing import List, Optional
from models.Auditoria import Auditoria
from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository

class AuditoriaRepository(BaseRepository[Auditoria]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Auditoria]:
        pass

    async def create(self, auditoria_data: dict) -> Auditoria:
        try:
            novo_endereco = Auditoria(**auditoria_data)
            self.db.add(novo_endereco)
            await self.db.commit()
            await self.db.refresh(novo_endereco)
            return novo_endereco
        except Exception as e:
            print(e)

    async def update(self) -> Optional[Auditoria]:
        pass

    async def delete(self) -> bool:
        pass