from typing import Optional
from pydantic import BaseModel

class LoginBase(BaseModel):
    cpf: str
    senha: str
    codigo_funcionario: Optional[str] = None