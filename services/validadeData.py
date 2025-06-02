from util.isValidCpf import isValidCpf

import re

async def validate_data(user_data: dict):
    if user_data["tipo_usuario"] is None:
        raise ValueError("Error: tipo_usuario cannot be null")
    if not isValidCpf(user_data["cpf"]):
        raise ValueError("CPF invalid")
    if not user_data.get("cpf"):
        raise ValueError("CPF cannot be null")
    if not user_data.get("nome"):
        raise ValueError("Nome cannot be null")
    if not user_data.get("data_nascimento"):
        raise ValueError("Data de nascimento cannot be null")
    if not user_data.get("telefone"):
        raise ValueError("Telefone cannot be null") 
    
async def cpf_exists(user_data, user_repo):
    existing = await user_repo.find_by_cpf(user_data["cpf"])
    if existing:
        raise ValueError("Usuário já existe no banco de dados")
    
async def is_password_strong(user_password: str):
    password_length = len(user_password)
    if password_length < 12:
        raise ValueError("password need 12 caracteres length")

    if not re.search(r"[A-Z]", user_password):
        raise ValueError("password need at least one UPPERCASE")

    if not re.search(r"[a-z]", user_password):
        raise ValueError("password need at least one DOWNCASE")

    if not re.search(r"[0-9]", user_password):
        raise ValueError("password need at least one number")

    if not re.search(r"[!@#$%^&*()_+=-]", user_password):
        raise ValueError("password need at least one special caracterer")