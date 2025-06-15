from fastapi import HTTPException
from util.find_account_by_cpf import find_account_by_cpf

async def getSaldo(session, current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Erro to find user")
    try:
        conta = await find_account_by_cpf(session, current_user["cpf"])
        if not conta:
            raise HTTPException(status_code=400, detail="Erro to find account")

        return conta.saldo
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"error: {e}")