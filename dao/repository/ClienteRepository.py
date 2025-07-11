from typing import List, Optional
from sqlalchemy import select

from dao.repository.BaseRepository import BaseRepository
from models.Cliente import Cliente

from typing import List, Optional
from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from models.Cliente import Cliente

class ClienteRepository(BaseRepository[Cliente]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Cliente]:
        result = await self.db.execute(select(Cliente))
        return result.scalars().all()

    async def get_by_id(self, id_cliente: int) -> Optional[Cliente]:
        result = await self.db.execute(select(Cliente).where(Cliente.id_cliente == id_cliente))
        return result.scalars().first()
    
    async def find_by_user_id(self, id_usuario: str) -> Optional[Cliente]:
        try:
            result = await self.db.execute(select(Cliente).where(Cliente.id_usuario == id_usuario))
            return result.scalars().first()
        except Exception as e:
            print(e)

    async def create(self, cliente_data: dict) -> Cliente:
        try:
            novo_cliente = Cliente(**cliente_data)
            self.db.add(novo_cliente)
            await self.db.commit()
            await self.db.refresh(novo_cliente)
            return novo_cliente
        except Exception as e:
            print(e)

    async def update(self, id_cliente: int, cliente_data: dict) -> Optional[Cliente]:
        await self.db.execute(
            update(Cliente)
            .where(Cliente.id_cliente == id_cliente)
            .values(**cliente_data)
        )
        await self.db.commit()
        return await self.get_by_id(id_cliente)

    async def delete(self, id_cliente: int) -> bool:
        user = await self.get_by_id(id_cliente)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True