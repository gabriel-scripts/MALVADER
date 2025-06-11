from jose import jwt
from datetime import datetime, timedelta


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import os

SECRET_KEY = os.getenv("JWT")
ALGORITHM = "HS256"

async def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("payload", payload)

        user_id = payload.get("id_usuario")
        tipo_usuario = payload.get("tipo_usuario")
        cargo = payload.get("cargo")
        codigo_funcionario = payload.get("codigo_funcionario")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = {
            "id_usuario": user_id, 
            "tipo_usuario": tipo_usuario, 
            "cargo": cargo, 
            "codigo_funcionario:": codigo_funcionario
            }

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Error to valid token")
    