
from sqlalchemy.orm import Session
from models import Item
from models.Usuario import Usuario

from BaseRepository import BaseRepository

from typing import Optional, List

class UserRepository(BaseRepository[Usuario]):
    def addUser(self, user_data: dict) -> Usuario:
        try:
            novo_user = Usuario(**user_data)
            self.db.add(novo_user)
            self.db.commit
            self.db.refresh(novo_user)
            return novo_user
        except TypeError as E:
            print(f'Error to save user {E}')

    def getUserById(self, id_usuario: int) -> Optional[Usuario]:
        try:
            return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        except TypeError as E:
            print(f'Error to get user {E}')
    
    def updateUser(self, id_usuario: int, usuario_user: dict):
        return