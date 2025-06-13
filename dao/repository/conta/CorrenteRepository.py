from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository
from models.Conta.Corrente import Corrente

class ContaRepository(BaseRepository[Corrente]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Corrente]:
        result = await self.db.execute(select(Corrente))
        return result.scalars().all()

    async def create(self, conta_corrente_data: dict) -> Corrente:
        try:
            novo_conta = Corrente(**conta_corrente_data)
            self.db.add(novo_conta)
            await self.db.commit()
            await self.db.refresh(novo_conta)
            return novo_conta
        except Exception as e:
            print(e)

    async def update(self) -> Optional[Corrente]:
        pass

    async def delete(self) -> bool:
        pass