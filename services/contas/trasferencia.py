from datetime import datetime
from fastapi import HTTPException

from dao.repository.conta.ContaRepository import ContaRepository
from dao.repository.conta.TransacaoRepository import TransacaoRepository
from util import save_auditoria


async def transferir(id_conta_origem, id_conta_destino, valor, session, usuario_logado):
    conta = await ContaRepository(session).get_by_id(id_conta_origem)
    if conta.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    transacao_data = {
        "id_conta_origem": id_conta_origem,
        "id_conta_destino": id_conta_destino,
        "tipo_transacao": "TRANSFERENCIA",
        "valor": valor,
        "descricao": f"Transferência para conta {id_conta_destino}"
    }
    await TransacaoRepository(session).create(transacao_data)
    await save_auditoria(session, {
        "id_usuario": usuario_logado["id_usuario"],
        "acao": "TRANSFERENCIA",
        "data_hora": datetime.now(),
        "detalhes": f"Transferência de R${valor} da conta {id_conta_origem} para {id_conta_destino}"
    })