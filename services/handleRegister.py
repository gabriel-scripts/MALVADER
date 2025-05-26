from dao.ClienteRepository import ClienteRepository

from models.Cliente import Cliente
from models.Funcionario import Funcionario
from models.Usuario import Usuario

from util.isValidCpf import isValidCpf
from util.hashPassword import generate_hash
from util.parseDataToUser import parseDataToUser

def validate_data():
    try:
        cliente_cpf = ClienteRepository.get_by_cpf(Cliente.cpf)
        if(isValidCpf(Cliente) == False):
            raise ValueError("CPF cannot be null")
        if Cliente.cpf is None or Cliente.cpf == '':
            raise ValueError("CPF cannot be null")
        if Cliente.nome is None or Cliente.nome == '':
            raise ValueError("Name cannot be null.")
        if Cliente.data_nascimento is None:
            raise ValueError("Data cannot be null")
        if Cliente.telefone is None or Cliente.telefone == '':
            raise ValueError("Phone cannot be null.") 
        if cliente_cpf:
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

def handleRegister(form_data):
    try:
        if form_data["tipo_usuario"] == 'cliente':
            cliente_data = form_data
            cliente_data["senha_hash"] = generate_hash(cliente_data["senha"])

            user_data = parseDataToUser(form_data)

            registerUsuario(user_data)
            registerCliente(cliente_data)
        if(form_data["tipo_usuario"] == 'funcionario'):
            funcionario_data = form_data
            funcionario_data["senha_hash"] = generate_hash(cliente_data["senha"])
            registerUsuario()
            registerFuncionario(cliente_data)
        if(form_data["tipo_usuario"] == None):
            raise ValueError("Error: user type passe cannot be null.")
        else:
            raise ValueError("Error(handleRegister): user type not recognized.")
    except Exception as e:
        print(f"Erro on handleRegister: {e}")
        raise e