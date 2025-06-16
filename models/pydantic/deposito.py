from decimal import Decimal
from pydantic import BaseModel

class deposito(BaseModel):
    valor: Decimal