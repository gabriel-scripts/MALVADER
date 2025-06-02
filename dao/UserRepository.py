from sqlalchemy.future import select

from models.Usuario import Usuario

from dao.BaseRepository import BaseRepository

from typing import Optional, List

class UserRepository(BaseRepository[Usuario]):
    async def get_all(self) -> List[Usuario]:
        return self.db.query(Usuario).all()

    async def get_by_id(self, id_usuario: int) -> Optional[Usuario]:
        try:
            result = await self.db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
            return result.scalars().first()
        except TypeError as E:
            print(f'Error to get user {E}')

    async def create(self, user_data: dict) -> Usuario:
        try:
            novo_user = Usuario(**user_data)
            self.db.add(novo_user)
            await self.db.commit()
            await self.db.refresh(novo_user)
            return novo_user
        except TypeError as E:
            print(f'Error to save user {E}')

    async def update(self, id_usuario: int, usuario_user: dict) -> Optional[Usuario]:
        try:
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).update(usuario_user)
            self.db.commit() 
            self.db.refresh(usuario_user)
        except TypeError as E:
            print(f'Error to update user {E}')

    async def delete(self, id_usuario: int) -> bool:
        user = self.get_by_id(id_usuario)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True