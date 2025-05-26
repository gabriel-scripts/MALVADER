from dao.ClienteRepository import ClienteRepository
from dao.

from models.Cliente import Cliente
from models.Funcionario import Funcionario
from models.Usuario import Usuario

import json

from util.isValidCpf import isValidCpf
from util.hashPassword import generate_hash
from util.parseDataToUser import parseDataToUser

async def validate_data(user_data):
    try:
        if isValidCpf(user_data[""] == False):
            raise ValueError("CPF invalid")
        if user_data[""] is None or user_data[""] == '':
            raise ValueError("CPF cannot be null")
        if user_data[""] is None or user_data[""] == '':
            raise ValueError("Name cannot be null.")
        if user_data[""] is None:
            raise ValueError("Data cannot be null")
        if user_data[""]or user_data[""] == '':
            raise ValueError("Phone cannot be null.") 
        
        if user_data[""] == 'funcionario':
            cpf = await
        if user_data[""] == 'funcget_by_cpfionario':
            cpf = await ClienteRepository.get_by_cpf(user_data[""])

        if cpf:
            raise ValueError("Cliente alredy exists on data base")
    except Exception as e:
        print(f"error on validateCliete  {e}")
        raise e

def registerCliente(Cliente: Cliente):
    try:
        ClienteRepository.save(Cliente)
    except Exception as e:
        print(f"Erro ao registrar cliente: {e}")

def registerFuncionario(Funcionario: Funcionario):
    pass

def registerUsuario():
    pass

async def handleRegister(form_data):
    try:
        data_dict = json.loads(form_data)
        validate_data(form_data)

        if form_data["tipo_usuario"] == 'cliente':
            cliente_data = data_dict
            
            user_data = parseDataToUser(data_dict)
            registerUsuario(user_data)
            cliente_data["senha_hash"] = await generate_hash(cliente_data["senha"])

            registerUsuario(user_data)
            registerCliente(cliente_data)

        if(form_data["tipo_usuario"] == 'funcionario'): 
            user_data = parseDataToUser(form_data)
            validate_data(user_data)

            funcionario_data = form_data
            funcionario_data["senha_hash"] = await generate_hash(cliente_data["senha"])
            registerUsuario()
            registerFuncionario(cliente_data)

        if(form_data["tipo_usuario"] == None):
            raise ValueError("Error: user type passe cannot be null.")
        else:
            raise ValueError("Error(handleRegister): user type not recognized.")
    except Exception as e:
        print(f"Erro on handleRegister: {e}")
        raise e