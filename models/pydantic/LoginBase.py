from pydantic import BaseModel

class LoginBase(BaseModel):
    cpf: str
    senha: str