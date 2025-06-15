from datetime import datetime
from fastapi import HTTPException

from dao.repository.conta.TransacaoRepository import TransacaoRepository
from util.find_account_by_cpf import find_account_by_cpf
from util.save_auditoria import save_auditoria

from decimal import Decimal

from sqlalchemy.exc import IntegrityError, DBAPIError
from services.contas.deposito_diario import calcular_deposito_diario

async def depositar(valor, session, current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Error to find corrent user")

    conta = await find_account_by_cpf(session, current_user["cpf"])

    if not conta:
        raise HTTPException(status_code=400, detail="Fail to find the account")

    valor_num = valor["valor"]

    try:
        valor_decimal = Decimal(valor_num)
        valor_decimal = valor_decimal.quantize(Decimal("0.01"))
    except Exception:
        raise HTTPException(status_code=400, detail="Valor inválido para depósito.")

    depositado_hoje = await calcular_deposito_diario(session, conta)
    
    transacao_data = {
        "id_conta_origem": conta.id_conta,
        "tipo_transacao": "DEPOSITO",
        "valor": valor_decimal,
        "data_hora": datetime.now(),
        "descricao": "Depósito em conta"
    }
    try:
        await TransacaoRepository(session).create(transacao_data)
    except (IntegrityError, DBAPIError) as e:
        if "Limite diário de depósito excedido" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Limite diário de depósito excedido. Você só pode depositar até R$ 10.000,00 por dia."
            )
        raise HTTPException(status_code=400, detail="Erro ao processar depósito.")

    await save_auditoria(
        session, {
        "id_usuario": current_user["id_usuario"],
        "acao": "DEPOSITO",
        "data_hora": datetime.now(),
        "detalhes": f"Depósito de R$ {valor_num} na conta {conta.id_conta}"
    })

    return {
        "deposito": f"{valor_num}",
        "conta": f"{conta.id_conta}",
        "depositado_hoje": str(depositado_hoje)
    }