from sqlalchemy.future import select
from dao.repository.BaseRepository import BaseRepository
from typing import List, Optional

from models.Funcionario import Funcionario

class FuncionarioRepository(BaseRepository[Funcionario]):
    async def get_by_id(self, id: int) -> Optional[Funcionario]:
        try:
            result = await self.db.execute(select(Funcionario).where(Funcionario.id_funcionario == id))
            return result.scalars().first()
        except Exception as e:
            print(f"error to get funcionario by id: {e}")

    async def get_all(self) -> List[Funcionario]:
        result = await self.db.execute(select(Funcionario))
        return result.scalars().all()

    async def find_by_codigo(self, codigo_funcionario: str) -> Optional[Funcionario]:
        result = await self.db.execute(
            select(Funcionario).where(Funcionario.codigo_funcionario == codigo_funcionario)
        )
        return result.scalars().first()

    async def create(self, funcionario_data: dict) -> Funcionario:
        funcionario = Funcionario(**funcionario_data)
        self.db.add(funcionario)
        await self.db.commit()
        await self.db.refresh(funcionario)
        return funcionario

    async def update(self, id: int, funcionario_data: dict) -> Optional[Funcionario]:
        funcionario = await self.get_by_id(id)
        if not funcionario:
            return None
        for key, value in funcionario_data.items():
            setattr(funcionario, key, value)
        await self.db.commit()
        await self.db.refresh(funcionario)
        return funcionario

    async def delete(self, id: int) -> bool:
        funcionario = await self.get_by_id(id)
        if not funcionario:
            return False
        await self.db.delete(funcionario)
        await self.db.commit()
        return True