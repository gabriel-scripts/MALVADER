from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository
from models.Agencia import Agencia

class AgenciaRepository(BaseRepository[Agencia]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Agencia]:
        result = await self.db.execute(select(Agencia))
        return result.scalars().all()

    async def create(self, agencia_data: dict) -> Agencia:
        try:
            novo_agencia = Agencia(**agencia_data)
            self.db.add(novo_agencia)
            await self.db.commit()
            await self.db.refresh(novo_agencia)
            return novo_agencia
        except Exception as e:
            print(e)

    async def update(self) -> Optional[Agencia]:
        pass

    async def delete(self) -> bool:
        pass