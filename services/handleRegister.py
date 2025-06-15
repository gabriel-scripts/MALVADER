from datetime import datetime

from fastapi import HTTPException

from dao.repository.ClienteRepository import ClienteRepository
from dao.repository.FuncionarioRepository import FuncionarioRepository
from dao.repository.EnderecoRepository import EnderecoRepository

from dao.repository.UserRepository import UserRepository

from services.validateCurrentUser import validate_current_user
from services.validadeData import validate_data, cpf_exists, email_exists, is_password_strong

from util.generate.generate_hash import generate_hash
from util.generate.generate_codigo_funcionario import generate_codigo_funcionario

from util.parseData.ParseToCliente import parseDataToCliente
from util.parseData.parseDataFuncionario import parseDataToFuncionario
from util.parseData.parseDataToUser import parseDataToUser
from util.parseData.parseDataEndereco import parseDataEndereco
from util.save_auditoria import save_auditoria
from util.parseData.parseInput import parseInput

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

    await validate_data(user_data.dict())

    user_data_dict = parseInput(user_data.dict())
    print(user_data_dict)
    print("clear data:", user_data_dict)

    user_repository = UserRepository(session)

    await validate_data(user_data_dict)
    await cpf_exists(user_data_dict, user_repository)
    await email_exists(user_data_dict, user_repository)
    await is_password_strong(user_data_dict["senha_hash"])

    user_data_dict["senha_hash"] = generate_hash(user_data_dict["senha_hash"])
    user_parsed_data = parseDataToUser(user_data_dict)
    
    if user_data_dict["tipo_usuario"] == 'admin':
        raise HTTPException(status_code=403, detail="Invalid user type")

    if user_data_dict["tipo_usuario"] == 'cliente':
        usuario_salvo = await registerUsuario(user_parsed_data, session)                
        endereco_parsed_data = parseDataEndereco(user_data_dict, usuario_salvo.id_usuario)
        cliente_parsed_data = parseDataToCliente(user_data_dict, usuario_salvo)
        await registerCliente(cliente_parsed_data, session)
        await registerEndereco(endereco_parsed_data, session)

        auditoria_data = {
            "id_usuario": usuario_salvo.id_usuario,
            "acao": "register_funcionario",
            "data_hora": datetime.now(),
            "detalhes": f"Usuário {usuario_salvo.email} registrado como cliente."
        }

        await save_auditoria(session, auditoria_data)

        return {"200": "Cliente registed with success"}


async def register_funcionario(user_data, session, current_user):
    
        print("register_funcionario CURRENT_USER:", current_user)

        await validate_data(user_data.dict())
        user_data_dict = parseInput(user_data.dict())

        print("register_funcionario user_data_dict:", user_data_dict)

        user_repository = UserRepository(session)
        
        current_funcionario_repository = FuncionarioRepository(session)
        supervisor = await current_funcionario_repository.find_by_codigo(current_user["codigo_funcionario"])
        
        if not supervisor: 
            raise HTTPException(status_code=403, detail="Supervisor not found on database")
        
        await validate_data(user_data_dict)
        await validate_current_user(current_user)
        await cpf_exists(user_data_dict, user_repository)
        await email_exists(user_data_dict, user_repository)
        
        user_data_dict["senha_hash"] = generate_hash(user_data_dict["senha_hash"])
        user_data_dict["codigo_funcionario"] = await generate_codigo_funcionario(session)
        user_parsed_data = parseDataToUser(user_data_dict)

        if user_data_dict["tipo_usuario"] == 'funcionario':
            usuario_salvo = await registerUsuario(user_parsed_data, session)
            endereco_parsed_data = parseDataEndereco(user_data_dict, usuario_salvo.id_usuario)
            funcionario_parsed_data = parseDataToFuncionario(user_data_dict, usuario_salvo.id_usuario, supervisor.id_funcionario)
            
            try:
                await registerFuncionario(funcionario_parsed_data, session)
                await registerEndereco(endereco_parsed_data, session)
            except Exception as e:
                print("error to save funcionario:", e)

            auditoria_data = {
                "id_usuario": usuario_salvo.id_usuario,
                "acao": "register_funcionario",
                "data_hora": datetime.now(),
                "detalhes": f"Usuário {usuario_salvo.email} registrado como funcionário."
            }
            
            await save_auditoria(session, auditoria_data)

            codigo_funcionario = user_data_dict["codigo_funcionario"] 

            return {"200": f"Funcionario registed with success, codigo: {codigo_funcionario}"}