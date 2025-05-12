
from sqlalchemy.orm import Session
from models.Usuario import Usuario

from dao.BaseRepository import BaseRepository

from typing import Optional, List

class UserRepository(BaseRepository[Usuario]):
    def get_all(self) -> List[Usuario]:
        return self.db.query(Usuario).all()

    def create(self, user_data: dict) -> Usuario:
        try:
            novo_user = Usuario(**user_data)
            self.db.add(novo_user)
            self.db.commit()
            self.db.refresh(novo_user)
            return novo_user
        except TypeError as E:
            print(f'Error to save user {E}')

    def get_by_id(self, id_usuario: int) -> Optional[Usuario]:
        try:
            return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        except TypeError as E:
            print(f'Error to get user {E}')
    
    def update(self, id_usuario: int, usuario_user: dict) -> Optional[Usuario]:
        try:
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).update(usuario_user)
            self.db.commit() 
            self.db.refresh(usuario_user)
        except TypeError as E:
            print(f'Error to update user {E}')

    def delete(self, id_usuario: int) -> bool:
        user = self.get_by_id(id_usuario)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True