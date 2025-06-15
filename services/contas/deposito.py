from datetime import datetime
from fastapi import HTTPException

from dao.repository.conta.TransacaoRepository import TransacaoRepository

from util.find_account_by_cpf import find_account_by_cpf
from util.save_auditoria import save_auditoria

from decimal import Decimal

async def depositar(valor, session, current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Error to find corrent user")

    conta = await find_account_by_cpf(session, current_user["cpf"])

    if not conta:
        raise HTTPException(status_code=400, detail="Fail to find the account")

    valor_num = valor["valor"]

    transacao_data = {
        "id_conta_origem": conta.id_conta,
        "tipo_transacao": "DEPOSITO",
        "valor": Decimal(valor_num),
        "data_hora": datetime.now(),
        "descricao": "Depósito em conta"
    }
    await TransacaoRepository(session).create(transacao_data)
    
    await save_auditoria(
        session, {
        "id_usuario": current_user["id_usuario"],
        "acao": "DEPOSITO",
        "data_hora": datetime.now(),
        "detalhes": f"Depósito de R$ {valor_num} na conta {conta.id_conta}"
    })

    return {"message": "Valor depositado com sucesso."}