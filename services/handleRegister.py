from dao.ClienteRepository import ClienteRepository
from dao.FuncionarioRepository import FuncionarioRepository

from dao.UserRepository import UserRepository

from services.validadeData import validate_data, cpf_exists, is_password_strong

from util.hashPassword import generate_hash
from util.parseData.ParseToCliente import parseDataToCliente
from util.parseData.parseDataFuncionario import parseDataToFuncionario
from util.parseData.parseDataToUser import parseDataToUser

async def registerUsuario(Usuario: dict, session):
    user_repo = UserRepository(session)
    usuario = await user_repo.create(Usuario)
    return usuario

async def registerCliente(Cliente: dict, session):
    cliente_repository = ClienteRepository(session)
    cliente = await cliente_repository.create(Cliente)
    return cliente

async def registerFuncionario(Funcionario: dict, session):
    funcionario_repository = FuncionarioRepository(session)
    funcionario = await funcionario_repository.create(Funcionario)
    return funcionario

async def handleRegister(user_data, session):
    try:
        user_data_dict = user_data.dict()

        user_repository = UserRepository(session)

        await validate_data(user_data_dict)
        await cpf_exists(user_data_dict, user_repository)
        await is_password_strong(user_data_dict["senha_hash"])

        user_data_dict["senha_hash"] = generate_hash(user_data_dict["senha_hash"])

        user_parsed_data = parseDataToUser(user_data_dict)

        if user_data_dict["tipo_usuario"] == 'cliente':
            await registerUsuario(user_parsed_data, session)
            cliente_parsed_data = parseDataToCliente(user_data_dict, user_parsed_data)
            await registerCliente(cliente_parsed_data, session)
            return {"200": "Cliente registed with success"}

        if user_data_dict["tipo_usuario"] == 'funcionario':
            registerUsuario(user_parsed_data, session)
            funcionario_parsed_data = parseDataToFuncionario(user_data_dict)
            await registerFuncionario(funcionario_parsed_data, session)
            return {"200": "Funcionario registed with success"}
        
    except Exception as e:
        print(f"Erro on handleRegister: {e}")
        raise e