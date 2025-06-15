from datetime import datetime
from fastapi import HTTPException

from dao.repository.conta.TransacaoRepository import TransacaoRepository
from util.save_auditoria import save_auditoria

from util.find_account_by_cpf import find_account_by_cpf

async def transferir(transferencia, session, usuario_logado):
    if not usuario_logado:
        raise HTTPException(status_code=400, detail="erro ao validar token")

    tranferencia_dict = transferencia.dict()

    print("TRANSFERENCIAA:", tranferencia_dict)

    valor = tranferencia_dict["valor"]
    conta_destino = await find_account_by_cpf(session, tranferencia_dict["cpf_destino"])
    print("CONTAA DESTINOO", conta_destino)
    if not conta_destino:
        raise HTTPException(status_code=400, detail="Conta destino associada a esse cpf não existe")

    conta = await find_account_by_cpf(session, usuario_logado["cpf"])
    print("CONTAAA", conta)
    if conta.saldo < tranferencia_dict["valor"]:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    transacao_data = {
        "id_conta_origem": conta.id_conta,
        "id_conta_destino": conta_destino.id_conta,
        "tipo_transacao": "TRANSFERENCIA",
        "valor": tranferencia_dict["valor"],
         "data_hora": datetime.now(), 
        "descricao": f"Transferência para conta {conta_destino.id_conta}"
    }
    await TransacaoRepository(session).create(transacao_data)
    await save_auditoria(session, {
        "id_usuario": usuario_logado["id_usuario"],
        "acao": "TRANSFERENCIA",
        "data_hora": datetime.now(),
        "detalhes": f"Transferência de R${valor} da conta {conta.id_conta} para {conta_destino.id_conta}"
    })

    return {"[200]", "Tranferência realizada com sucesso"}