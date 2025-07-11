from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.Usuario import Usuario

from dao.repository.BaseRepository import BaseRepository

from typing import Optional, List


class UserRepository(BaseRepository[Usuario]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_all(self) -> List[Usuario]:
        result = await self.db.execute(select(Usuario))
        return result.scalars().all()

    async def get_by_id(self, id_usuario: int) -> Optional[Usuario]:
        try:
            result = await self.db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
            return result.scalars().first()
        except Exception as e:
            print(f'Error to get user {e}')

    async def find_by_cpf(self, cpf):
        try:
            result = await self.db.execute(select(Usuario).where(Usuario.cpf == cpf))
            user = result.scalars().first()
            return user
        except Exception as e:
            print(f"Error to get cpf: {e}")
            return None

    async def find_by_email(self, email):
        try:
            result = await self.db.execute(select(Usuario).where(Usuario.email == email))
            email_usuario = result.scalars().first()
            return email_usuario
        except Exception as e:
            print(f"Error to get email: {e}")
            return None

    async def create(self, user_data: dict) -> Usuario:
        try:
            novo_user = Usuario(**user_data)
            self.db.add(novo_user)
            await self.db.commit()
            await self.db.refresh(novo_user)
            return novo_user
        except Exception as e:
            await self.db.rollback()
            if "Duplicate entry" in str(e):
                raise HTTPException(status_code=400, detail="Email already exists.") 
            print(f"Error to save user {e}")
            return None

    async def update(self, id_usuario: int, usuario_user: dict) -> Optional[Usuario]:
        try:
            await self.db.execute(
                update(Usuario)
                .where(Usuario.id_usuario == id_usuario)
                .values(**usuario_user)
            )
            await self.db.commit()
            return await self.get_by_id(id_usuario)
        except Exception as e:
            print(f'Error to update user {e}')

    async def delete(self, id_usuario: int) -> bool:
        user = await self.get_by_id(id_usuario)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True