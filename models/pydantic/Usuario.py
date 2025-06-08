from pydantic import BaseModel
from typing import Optional
from datetime import date

class UsuarioBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date 
    telefone: str
    tipo_usuario: str
    senha_hash: str
    email: str
    score_credito:  Optional[str] = None
    cargo:  Optional[str] = None
    id_supervisor:  Optional[str] = None