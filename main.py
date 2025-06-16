from decimal import Decimal
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dao.config.database import get_async_session 

from services.handleRegister import handleRegister,register_funcionario
from services.handleLogin import handleLogin
from services.auth import auth

from services.contas.getSaldo import getSaldo
from services.contas.deposito import depositar
from services.contas.trasferencia import transferir

from services.get_all_functions.get_all import *
from util.find_account_by_cpf import *
from services.conta_funcionario.createConta import create_conta

from models.pydantic.TranferirBase import TranferirBase
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
    data_dict = data.dict()
    
    if not data_dict["codigo_funcionario"]:
        raise HTTPException(status_code=400, detail="é necessário o código do funcionario.")

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

@app.post('/api/depositar')
async def abrir_conta(valor: dict, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    response = await depositar(valor, session, usuario_ativo_sistema)
    return response

@app.post('/api/depositar')
async def abrir_conta(valor: dict, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    response = await depositar(valor, session, usuario_ativo_sistema)
    return response


@app.post('/api/transferir')
async def tranferir(tranferencia: TranferirBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    response = await transferir(tranferencia, session, usuario_ativo_sistema)
    return response

@app.post('/api/saque')
async def sacar(user: ContaBase, session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
   pass

@app.get('/api/saldo')
async def saldo(session: AsyncSession = Depends( get_async_session), usuario_ativo_sistema = Depends(get_current_user)):
    resultado = await getSaldo(session, usuario_ativo_sistema)
    return resultado

@app.post('/api/get_user')
async def user_by_cpf(cpf: dict, session: AsyncSession = Depends( get_async_session)):
    return await get_user_by_cpf(session, cpf)

@app.post('/api/get_conta')
async def conta_by_codigo(conta_codigo: dict, session: AsyncSession = Depends( get_async_session)):
    return await get_by_numero_conta(session, conta_codigo)

@app.post('/api/get_funcionario')
async def funcionario_by_codigo(conta_codigo: dict, session: AsyncSession = Depends( get_async_session)):
    return await get_by_codigo(session, conta_codigo)


# ROTAS DE TEST PARA ADMIN

@app.post('/api/test-otp')
async def verify_otp(test: dict, usuario_ativo_sistema = Depends(get_current_user)):
    if usuario_ativo_sistema.tipo_usuario != 'admin':
        raise HTTPException(status_code=400, detail="Error, only for admins.")
    send_otp(test["email"], test["otp"])

@app.get('/api/get_all_agencias')
async def listar_agencias(session: AsyncSession = Depends( get_async_session)):
    return await get_all_agencia(session)

@app.get('/api/get_all_contas')
async def listar_contas(session: AsyncSession = Depends( get_async_session)):
    return await get_all_contas(session)

@app.get('/api/get_all_funcionarios')
async def listar_contas(session: AsyncSession = Depends( get_async_session)):
    return await get_all_funcionarios(session)

@app.post("/api/buscar_conta_cpf")
async def buscar_contar(cpf: str, session: AsyncSession = Depends( get_async_session)):
    conta = await find_account_by_cpf(session, cpf)
    return conta

@app.post("/api/buscar_usuario_cpf")
async def buscar_contar(cpf: dict, session: AsyncSession = Depends( get_async_session)):
    conta = await find_user_by_cpf(session, cpf)
    return conta

@app.get('/api/get_all_usuarios')
async def listar_usuarios(session: AsyncSession = Depends( get_async_session)):
    return await get_all_usuarios(session)

@app.get('/api/get_all_clientes')
async def listar_clientes(session: AsyncSession = Depends( get_async_session)):
    return await get_all_clientes(session)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)