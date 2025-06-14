from datetime import datetime
from fastapi import HTTPException

from dao.repository.conta.ContaRepository import ContaRepository
from dao.repository.conta.TransacaoRepository import TransacaoRepository
from util import save_auditoria


async def sacar(id_conta, valor, session, usuario_logado):
    conta = await ContaRepository(session).get_by_id(id_conta)
    if conta.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    transacao_data = {
        "id_conta_origem": id_conta,
        "tipo_transacao": "SAQUE",
        "valor": valor,
        "descricao": "Saque em conta"
    }
    await TransacaoRepository(session).create(transacao_data)
    await save_auditoria(session, {
        "id_usuario": usuario_logado["id_usuario"],
        "acao": "SAQUE",
        "data_hora": datetime.now(),
        "detalhes": f"Saque de R${valor} na conta {id_conta}"
    })