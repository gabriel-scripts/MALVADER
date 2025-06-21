import hashlib

from fastapi import HTTPException
from datetime import datetime, timedelta

from util.save_auditoria import save_auditoria

attempts = {}

async def verify_password(user_hashed_password, input_password, user_id, session):
    tentativas = attempts.get(user_id, {"count": 0, "bloqueado_ate": None})

    if tentativas["bloqueado_ate"] and tentativas["bloqueado_ate"] > datetime.now():
        raise HTTPException(status_code=403, detail="User blocked for 10 minutos.")

    input_password_hashed = hashlib.md5(input_password.encode()).hexdigest()
    
    if not input_password_hashed: 
        raise HTTPException(status_code=400, detail="Error")

    if user_hashed_password != input_password_hashed:
        tentativas["count"] += 1
        if tentativas["count"] >= 3:
            
            auditoria_data = {
                "id_usuario": user_id,
                "acao": "logar_funcionario",
                "data_hora": datetime.now(),
                "detalhes": f"Usuário {user_id} falhou ao logar, bloqueado por 10 minutos."
            }

            await save_auditoria(session, auditoria_data)

            tentativas["bloqueado_ate"] = datetime.now() + timedelta(minutes=10)
            tentativas["count"] = 0
            raise HTTPException(status_code=400, detail="Wrong password, user been blocked for 10 minutos")
        attempts[user_id] = tentativas
        raise HTTPException(status_code=400, detail="Invalid password")
   
    attempts[user_id] = {"count": 0, "bloqueado_ate": None}