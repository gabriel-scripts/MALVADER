from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
        
class TranferirBase(BaseModel):
    agencia:  Optional[str] = None
    cpf_destino: str
    valor: Decimal
