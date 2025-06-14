import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.config.database import get_async_session 

from services.handleRegister import handleRegister,register_funcionario
from services.handleLogin import handleLogin
from services.auth import auth

from services.contas.createConta import create_conta

from models.pydantic.ContaBase import ContaBase
from models.pydantic.LoginFuncionario import LoginFuncionario
from models.pydantic.Usuario import UsuarioBase
from models.pydantic.LoginBase import LoginBase
from models.pydantic.authBase import AuthBase

from util.send_otp import send_otp
from util.jwt.JWT import get_current_user

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

@app.post('/api/register_funcionario')
async def register_funcionario_endpoint(form_data: UsuarioBase, session: AsyncSession = Depends(get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    await register_funcionario(form_data, session, usuario_ativo_sistema)
    return {"[200]", "Funcionario registed with succes"}

@app.post('/api/login_funcionario')
async def login_endpoint(data: LoginFuncionario, session: AsyncSession = Depends( get_async_session )):
    await handleLogin(data, session)
    return {"[200]", "OTP sended to email"}

@app.post('/api/login_cliente')
async def login_endpoint(data: LoginBase, session: AsyncSession = Depends( get_async_session )):
    await handleLogin(data, session)
    return {"[200]", "OTP sended to email"}

@app.post('/api/authenticate_user')
async def authenticate_user(user: AuthBase, session: AsyncSession = Depends( get_async_session)):
    response = await auth(user, session)
    return response

@app.post('/api/abrir_conta')
async def abrir_conta(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    if not usuario_ativo_sistema:
        raise HTTPException(status_code=400, detail="Usário não está ativo no sistema.")
    await create_conta(user, session, usuario_ativo_sistema)

@app.post('/api/deposito')
async def abrir_conta(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    pass

@app.post('/api/transeferencia')
async def abrir_conta(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    pass

@app.post('/api/saque')
async def abrir_conta(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
   pass

@app.get('/api/saldo')
async def abrir_conta(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    pass

# ROTAS DE TEST PARA ADMIN

@app.post('/api/test-otp')
async def verify_otp(email: str, otp: str, usuario_ativo_sistema = Depends(get_current_user)):
    if usuario_ativo_sistema.tipo_usuario != 'admin':
        raise HTTPException(status_code=400, detail="Error, only for admins.")
    send_otp(email, otp)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)