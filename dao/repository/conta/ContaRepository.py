from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository
from models.ContaModel.Conta import Conta

class ContaRepository(BaseRepository[Conta]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Conta]:
        result = await self.db.execute(select(Conta))
        return result.scalars().all()

    async def create(self, conta_data: dict) -> Conta:
        try:
            novo_conta = Conta(**conta_data)
            self.db.add(novo_conta)
            await self.db.commit()
            await self.db.refresh(novo_conta)
            return novo_conta
        except Exception as e:
            print(e)

    async def find_by_cliente_id(self, id_cliente: str) -> Optional[Conta]:
        result = await self.db.execute(select(Conta).where(Conta.id_cliente == id_cliente))
        return result.scalars().first()

    async def update(self) -> Optional[Conta]:
        pass

    async def delete(self) -> bool:
        pass