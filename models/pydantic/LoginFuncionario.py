from pydantic import BaseModel
        
class LoginFuncionario(BaseModel):
    cpf: str
    senha: str
    codigo_funcionario: str