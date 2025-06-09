from dao.repository.ClienteRepository import ClienteRepository
from dao.repository.FuncionarioRepository import FuncionarioRepository
from dao.repository.EnderecoRepository import EnderecoRepository
from fastapi import HTTPException

from dao.repository.UserRepository import UserRepository

from services.validadeData import validate_data, cpf_exists, email_exists, is_password_strong

from util.hashPassword import generate_hash
from util.parseData.ParseToCliente import parseDataToCliente
from util.parseData.parseDataFuncionario import parseDataToFuncionario
from util.parseData.parseDataToUser import parseDataToUser
from util.parseData.parseDataEndereco import parseDataEndereco

async def registerUsuario(usuario: dict, session):
    user_repo = UserRepository(session)
    usuario = await user_repo.create(usuario)
    return usuario

async def registerCliente(cliente: dict, session):
    cliente_repository = ClienteRepository(session)
    cliente = await cliente_repository.create(cliente)
    return cliente

async def registerFuncionario(funcionario: dict, session):
    funcionario_repository = FuncionarioRepository(session)
    funcionario = await funcionario_repository.create(funcionario)
    return funcionario

async def registerEndereco(endereco: dict, session):
    endereco_repository = EnderecoRepository(session)
    endereco = await endereco_repository.create(endereco)
    return endereco

async def handleRegister(user_data, session):
    
    user_data_dict = user_data.dict()

    user_repository = UserRepository(session)

    await validate_data(user_data_dict)
    await cpf_exists(user_data_dict, user_repository)
    await email_exists(user_data_dict, user_repository)
    await is_password_strong(user_data_dict["senha_hash"])

    user_data_dict["senha_hash"] = generate_hash(user_data_dict["senha_hash"])

    user_parsed_data = parseDataToUser(user_data_dict)
    
    if user_data_dict["tipo_usuario"] == 'cliente':
        usuario_salvo = await registerUsuario(user_parsed_data, session)                
        endereco_parsed_data = parseDataEndereco(user_data_dict, usuario_salvo.id_usuario)
        cliente_parsed_data = parseDataToCliente(user_data_dict, usuario_salvo)
        await registerCliente(cliente_parsed_data, session)
        await registerEndereco(endereco_parsed_data, session)
        return {"200": "Cliente registed with success"}

    if user_data_dict["tipo_usuario"] == 'funcionario':
        #falta validar a hierarquia
        usuario_salvo = await registerUsuario(user_parsed_data, session)
        funcionario_parsed_data = parseDataToFuncionario(user_data_dict,  usuario_salvo)
        await registerFuncionario(funcionario_parsed_data, session)
        await registerEndereco(endereco_parsed_data, session)
        return {"200": "Funcionario registed with success"}
