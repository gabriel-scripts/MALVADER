from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository
from models.ContaModel.Investimento import Investimento

class InvestimentoRepository(BaseRepository[Investimento]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Investimento]:
        result = await self.db.execute(select(Investimento))
        return result.scalars().all()

    async def create(self, conta_corrente_data: dict) -> Investimento:
        try:
            novo_conta = Investimento(**conta_corrente_data)
            self.db.add(novo_conta)
            await self.db.commit()
            await self.db.refresh(novo_conta)
            return novo_conta
        except Exception as e:
            print(e)

    async def update(self) -> Optional[Investimento]:
        pass

    async def delete(self) -> bool:
        pass