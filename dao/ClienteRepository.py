from models.Usuario import Cliente
from dao.BaseRepository import BaseRepository
from typing import Optional, List

from sqlalchemy.orm import AsyncSession

class ClienteRepository(BaseRepository[Cliente]):

    async def __init__(self, session: AsyncSession):
        super().__init__(session, Cliente)

    async def get_all(self) -> List[Cliente]:
        with await self.db.session() as session:
            return session.query(Cliente).all()

    async def find_by_cpf(self, cpf):
        try:
            with self.db.session() as session:
                cpf_cliente = await session.query(Cliente).filter(Cliente.cpf == cpf).first()
                if not cpf:
                    raise ValueError(f"Cliente with cpf {cpf} not found")
                return cpf_cliente
    
        except Exception as e:
            print(f"Error to get cpf: {e}")
            return None

    async def get_by_id(self, id):
        try:
            with self.db.session() as session:
                cliente = await session.query(Cliente).filter(Cliente.id == id).first()
                if not cliente:
                    raise ValueError(f"Cliente with id {id} not found")
                return cliente
        except ValueError as e:
            print(f"Error to get cliente: {e}")
            return None
        
    async def create(self, cliente):
        try: 
            with self.db.session() as session:
                await session.add(cliente)
                await session.commit()
                return cliente
        except Exception as e:
            session.rollback()
            print(f"Error creating cliente: {e}")
            return None

    async def update(self, cliente):
        try:
            with self.db.session() as session:
                existing_cliente = await session.query(Cliente).filter(Cliente.id == cliente.id).first()
                if existing_cliente:
                    for key, value in cliente.__dict__.items():
                        setattr(existing_cliente, key, value)
                    session.commit()
                    return existing_cliente
                return None
        except Exception as e:
            session.rollback()
            print(f"Error updating cliente: {e}")
            return None

    async def delete(self, id):
        try:
            with self.db.session() as session:
                cliente = await session.query(Cliente).filter(Cliente.id == id).first()
                if not cliente:
                    raise ValueError(f"Cliente with id {id} not found")
                await session.delete(cliente)
                await session.commit()
                return True
        except ValueError as e:
            print(f"Error deleting cliente: {e}")
            return False
        
    async def get_all(self):
        try:
            with self.db.session() as session:
                return await session.query(Cliente).all()
        except Exception as e:
            print(f"Error getting all clientes: {e}")