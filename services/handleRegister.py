from dao.ClienteRepository import ClienteRepository
from dao.FuncionarioRepository import FuncionarioRepository

from dao.UserRepository import UserRepository

from models.Cliente import Cliente
from models.Funcionario import Funcionario
from models.Usuario import Usuario

from validadeData import validate_data, cpf_exists, is_password_strong
import json

from util.hashPassword import generate_hash
from util.parseDataToUser import parseDataToUser

async def registerUsuario(Usuario: Usuario, session):
    user_repo = UserRepository(session)
    usuario = await user_repo.create(Usuario)
    return usuario

async def registerCliente(Cliente: Cliente, session):
    cliente_repo = ClienteRepository(session)
    cliente = await cliente_repo.create(Cliente)
    return cliente

async def registerFuncionario(Funcionario: Funcionario, session):
    funcionario_repo = FuncionarioRepository(session)
    funcionario = await funcionario_repo.create(Funcionario)
    return funcionario

async def handleRegister(form_data, session):
    try:
        user_repository = UserRepository(session)
       
        if isinstance(form_data, str):
            data_dict = json.loads(form_data)

        await validate_data(data_dict)
        await cpf_exists(data_dict["cpf"], user_repository)
        await is_password_strong(data_dict["senha"])

        data_dict["senha_hash"] = await generate_hash(data_dict["senha"])
        tipo_usuario = data_dict.get("tipo_usuario")

        cpf_exists(data_dict["senha_hash"])

        if tipo_usuario == 'cliente':
            user_data = parseDataToUser(data_dict)
            usuario = await registerUsuario(user_data, session)
            cliente_data = {**data_dict, "id_usuario": usuario.id_usuario}
            await registerCliente(cliente_data, session)
            return {"200": "Cliente registed with success"}

        if tipo_usuario == 'funcionario':
            user_data = parseDataToUser(data_dict)
            usuario = await registerUsuario(user_data, session)
            funcionario_data = {**data_dict, "id_usuario": usuario.id_usuario}
            await registerFuncionario(funcionario_data, session)
            return {"200": "Funcionario registed with success"}
        
    except Exception as e:
        print(f"Erro on handleRegister: {e}")
        raise e