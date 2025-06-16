from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date

class Endereco(BaseModel):
    cep: str
    local: str
    numero_casa: int
    bairro: str
    cidade: str 
    estado: str
    complemento: Optional[str] = None

class UsuarioBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date 
    telefone: str
    tipo_usuario: Literal['funcionario', 'cliente', 'admin']
    senha_hash: str
    email: str
    score_credito:  Optional[str] = None
    cargo:  Optional[str] = None
    id_supervisor:  Optional[str] = None
    codigo_funcionario:  Optional[str] = None
    endereco: Endereco