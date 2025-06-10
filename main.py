import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.config.database import get_async_session 

from services.handleRegister import handleRegister
from services.handleLogin import handleLogin

from models.pydantic.Usuario import UsuarioBase
from models.pydantic.LoginBase import LoginBase

from util.send_otp import send_otp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"[200]": "Running - welcome to Malvader bank"}

@app.post("/api/register")
async def register_endpoint(form_data: UsuarioBase, session: AsyncSession = Depends(get_async_session)):
    await handleRegister(form_data, session)
    return {"[200]", "User saved with success"}

@app.post('/api/login')
async def login_endpoint(data: LoginBase, session: AsyncSession = Depends( get_async_session )):
    await handleLogin(data, session)
    return {"[200]", "OTP enviado para email com sucesso"}


# ROTAS DE TEST PARA ADMIN

@app.get("/api/getall")
def getbyall():
    pass 

@app.post('/api/test-otp')
async def verify_otp(email: str, otp: str):
    send_otp(email, otp)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)