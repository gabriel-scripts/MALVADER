from http.client import HTTPException
from dao.repository.conta import ContaRepository

async def getSaldo(session, current_user):
    conta_db = ContaRepository(session)

    conta = conta_db.find_by_cliente_id(current_user["id_usuario"])

    if not conta:
        raise HTTPException(status_code=400, detail="Erro to find account")

    return conta.saldo