from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from datetime import date

class AgenciaBase(BaseModel):
    nome: str
    codigo_agencia: str
    endereco_id: Optional[str] = None

class ContaBase(BaseModel):
    numero_conta: Optional[str] = None
    id_agencia: Optional[str] = None
    saldo: Optional[Decimal] = Decimal('0.00')
    tipo_conta: str
    id_cliente: Optional[str] = None
    data_abertura: Optional[date] = None
    status: Optional[str] = 'ativa'
    agencia: AgenciaBase
    perfil_risco: Optional[str] = None