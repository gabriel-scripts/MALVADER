from datetime import datetime
from decimal import Decimal
from models.ContaModel.Transacao import Transacao
from sqlalchemy import select, func, and_

async def calcular_deposito_diario(session, conta):
    hoje = datetime.now().date()
    stmt = select(func.coalesce(func.sum(Transacao.valor), 0)).where(
        and_(
            Transacao.id_conta_origem == conta.id_conta,
            Transacao.tipo_transacao == "DEPOSITO",
            func.date(Transacao.data_hora) == hoje
        )
    )
    result = await session.execute(stmt)
    depositado_hoje = result.scalar() or Decimal("0.00")
    return depositado_hoje