from decimal import Decimal
from fastapi import HTTPException
from util.find_account_by_cpf import find_account_by_cpf

from services.contas.deposito_diario import calcular_deposito_diario


async def getSaldo(session, current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Erro to find user")

    conta = await find_account_by_cpf(session, current_user["cpf"])
    if not conta:
        raise HTTPException(status_code=400, detail="Erro to find account")

    valor_saldo = Decimal(conta.saldo)

    deposito_diario = await calcular_deposito_diario(session, conta)

    return {
        "id_conta": f"{conta.id_conta}", 
        "valor": f"{valor_saldo}", 
        "depositado_hoje": str(deposito_diario)
    }