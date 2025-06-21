from fastapi import HTTPException
from dao.repository.conta.AgenciaRepository import AgenciaRepository
from dao.repository.conta.ContaRepository import ContaRepository
from dao.repository.UserRepository import UserRepository
from dao.repository.FuncionarioRepository import FuncionarioRepository
from dao.repository.ClienteRepository import ClienteRepository

async def get_all_agencia(session):
    agencia_db = AgenciaRepository(session)
    return await agencia_db.get_all()

async def get_all_contas(session):
    agencia_db = ContaRepository(session)
    return await agencia_db.get_all()

async def get_all_clientes(session):
    agencia_db = ClienteRepository(session)
    return await agencia_db.get_all()

async def get_all_usuarios(session):
    agencia_db = UserRepository(session)
    return await agencia_db.get_all()

async def get_all_funcionarios(session):
    agencia_db = FuncionarioRepository(session)
    return await agencia_db.get_all()

async def get_by_numero_conta(session, numero_conta):
    conta_db = ContaRepository(session)
    conta = await conta_db.find_by_numero_conta(numero_conta["conta"])
    if not conta: 
        raise HTTPException(status_code=400, detail="Conta not exists")
    
    return {"conta": conta.numero_conta, "saldo": conta.saldo, "abertura": conta.data_abertura}

async def get_user_by_cpf(session, cpf):
    user_db = UserRepository(session)
    conta = await user_db.find_by_cpf(cpf["cpf"])
    if not conta: 
        raise HTTPException(status_code=400, detail="Conta not exists")
    
    return {"data_nascimento": conta.data_nascimento, "telefone": conta.telefone, "email": conta.email}

async def get_by_codigo(session, codigo):
    funcionario_db = FuncionarioRepository(session)
    conta = await funcionario_db.find_by_codigo(codigo["codigo"])
    if not conta: 
        raise HTTPException(status_code=400, detail="Conta not exists")
    
    return {"cargo": conta.cargo, "id_supervisor":  conta.id_supervisor}