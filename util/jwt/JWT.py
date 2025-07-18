from jose import jwt
from datetime import datetime, timedelta


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

SECRET_KEY = os.getenv("JWT")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"

REFRESH_EXPIRE_MINUTES = 60 * 24 * 7  

async def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=120)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def create_refresh_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=REFRESH_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id_usuario")
        tipo_usuario = payload.get("tipo_usuario")
        cargo = payload.get("cargo")
        codigo_funcionario = payload.get("codigo_funcionario")
        cpf = payload.get("cpf")
        email = payload.get("email")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        if tipo_usuario == 'cliente':
            user = {
                "id_usuario": user_id,
                "tipo_usuario": tipo_usuario,
                "cpf": cpf,
                "email": email
            }
            return user
        
        if tipo_usuario == 'funcionario' or 'admin':
            user = {
                "id_usuario": user_id,
                "tipo_usuario": tipo_usuario,
                "cargo": cargo,
                "codigo_funcionario": codigo_funcionario,
                "cpf": cpf
            }
            print("USER ON PAYLOAD", user)
            return user
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Error to valid token")

# token = create_access_token(
#      data={
#          "id_usuario": 1,
#          "tipo_usuario": 'admin',
#          "cargo": 'gerente',
#          "codigo_funcionario": '10101',
#          "cpf": "00000000000"
#      }
# )

# print(token)