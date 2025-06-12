from fastapi import HTTPException


async def validate_current_user(current_user):
    
    # validar se o current_user realmente existe no banco de dados

    if not current_user:
        raise HTTPException(status_code=403, detail="Error to get token")

    if current_user["tipo_usuario"] not in ['admin', 'gerente']:
        raise HTTPException(status_code=403, detail="Apenas admin ou gerente podem cadastrar funcionários.")
