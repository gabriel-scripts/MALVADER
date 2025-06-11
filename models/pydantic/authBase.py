from typing import Optional
from pydantic import BaseModel

class AuthBase(BaseModel):
    cpf: str
    senha: str
    otp: str
    codigo_funcionario: Optional[str] = None