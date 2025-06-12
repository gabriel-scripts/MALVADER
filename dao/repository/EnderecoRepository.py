from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository
from models.Cliente import Cliente

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from dao.repository.BaseRepository import BaseRepository
from models.Endereco import Endereco

class EnderecoRepository(BaseRepository[Endereco]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Endereco]:
        result = await self.db.execute(select(Endereco))
        return result.scalars().all()

    async def create(self, endereco_data: dict) -> Endereco:
        try:
            novo_endereco = Endereco(**endereco_data)
            self.db.add(novo_endereco)
            await self.db.commit()
            await self.db.refresh(novo_endereco)
            return novo_endereco
        except Exception as e:
            print(e)

    async def update(self) -> Optional[Endereco]:
        pass

    async def delete(self) -> bool:
        pass