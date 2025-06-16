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