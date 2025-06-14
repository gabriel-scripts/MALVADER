from datetime import datetime
from dao.repository.conta.TransacaoRepository import TransacaoRepository
from util import save_auditoria

async def depositar(id_conta, valor, session, usuario_logado):

    transacao_data = {
        "id_conta_origem": id_conta,
        "tipo_transacao": "DEPOSITO",
        "valor": valor,
        "descricao": "Depósito em conta"
    }
    await TransacaoRepository(session).create(transacao_data)
    
    await save_auditoria(
        session, {
        "id_usuario": usuario_logado["id_usuario"],
        "acao": "DEPOSITO",
        "data_hora": datetime.now(),
        "detalhes": f"Depósito de R${valor} na conta {id_conta}"
    })