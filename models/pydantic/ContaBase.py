from decimal import Decimal
from typing import Literal, Optional
from pydantic import BaseModel
from datetime import date

class AgenciaBase(BaseModel):
    nome: str
    codigo_agencia: int
    endereco_id: Optional[str] = None

class ContaBase(BaseModel):
    # numero_conta: Optional[int] = None
    id_agencia: Optional[int] = None
    cpf_cliente: str
    saldo: Optional[Decimal] = Decimal('0.00')
    tipo_conta:  Literal['poupanca', 'corrente', 'investimento']
    id_cliente: Optional[int] = None
    data_abertura: Optional[date] = None
    status: Optional[Literal['ativa', 'inativa', 'bloqueada']] = 'ativa'
    agencia: AgenciaBase
    perfil_risco: Literal['baixo', 'medio', 'alto']