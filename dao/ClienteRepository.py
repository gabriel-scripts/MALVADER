from models.Usuario import Cliente
from dao.BaseRepository import BaseRepository
from typing import Optional, List

class ClienteRepository(BaseRepository[Cliente]):
    def get_all(self) -> List[Cliente]:
        with self.db.session() as session:
            return session.query(Cliente).all()

    def get_by_id(self, id):
        try:
            with self.db.session() as session:
                cliente = session.query(Cliente).filter(Cliente.id == id).first()
                if not cliente:
                    raise ValueError(f"Cliente with id {id} not found")
                return cliente
        except ValueError as e:
            print(f"Error to get cliente: {e}")
            return None
        
    def create(self, cliente):
        try: 
            with self.db.session() as session:
                session.add(cliente)
                session.commit()
                return cliente
        except Exception as e:
            session.rollback()
            print(f"Error creating cliente: {e}")
            return None

    def update(self, cliente):
        try:
            with self.db.session() as session:
                existing_cliente = session.query(Cliente).filter(Cliente.id == cliente.id).first()
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

    def delete(self, id):
        try:
            with self.db.session() as session:
                cliente = session.query(Cliente).filter(Cliente.id == id).first()
                if not cliente:
                    raise ValueError(f"Cliente with id {id} not found")
                session.delete(cliente)
                session.commit()
                return True
        except ValueError as e:
            print(f"Error deleting cliente: {e}")
            return False
        
    def get_all(self):
        try:
            with self.db.session() as session:
                return session.query(Cliente).all()
        except Exception as e:
            print(f"Error getting all clientes: {e}")