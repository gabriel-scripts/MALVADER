import hashlib

from fastapi import HTTPException
from datetime import datetime, timedelta

attempts = {}

async def verify_password(user_hashed_password, input_password, user_id):
    print(user_hashed_password)
    print("input:", input_password)
    tentativas = attempts.get(user_id, {"count": 0, "bloqueado_ate": None})

    if tentativas["bloqueado_ate"] and tentativas["bloqueado_ate"] > datetime.now():
        raise HTTPException(status_code=403, detail="User blocked for 10 minutos.")

    input_password_hashed = hashlib.md5(input_password.encode()).hexdigest()
    
    if not input_password_hashed: 
        raise HTTPException(status_code=400, detail="Error")


    print("Input hashed: ", input_password_hashed)

    if user_hashed_password != input_password_hashed:
        tentativas["count"] += 1
        if tentativas["count"] >= 3:
            tentativas["bloqueado_ate"] = datetime.now() + timedelta(minutes=10)
            tentativas["count"] = 0
            raise HTTPException(status_code=400, detail="Wrong password, user been blocked for 10 minutos")
        attempts[user_id] = tentativas
        raise HTTPException(status_code=400, detail="Invalid password")
   
    attempts[user_id] = {"count": 0, "bloqueado_ate": None}