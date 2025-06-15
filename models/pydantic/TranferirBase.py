from decimal import Decimal
from pydantic import BaseModel
        
class TranferirBase(BaseModel):
    cpf_destino: str
    valor: Decimal
