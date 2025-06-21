from fastapi import HTTPException
from util.is_cpf_valid import isValidCpf
import re
from datetime import date

async def validate_data(user_data: dict):

    cpf_length = len(user_data["cpf"])
    telefone_length = len(user_data.get("telefone"))
    estado_length = len(user_data["endereco"]["estado"])
    cep_length = len(user_data["endereco"]["cep"])
    local_length = len(user_data["endereco"]["local"])
    numero_casa_length = len(str(user_data["endereco"]["numero_casa"]))
    bairro_length = len(user_data["endereco"]["bairro"])
    cidade_lenth = len(user_data["endereco"]["cidade"])
    complemento_length = len(user_data["endereco"]["complemento"])

    if estado_length != 2:
        raise HTTPException(status_code=400, detail="Estado only have 2 caracteres")

    if cpf_length != 11:
        raise HTTPException(status_code=400, detail="CPF only have 11 caracteres")

    if telefone_length > 15:
        raise HTTPException(status_code=400, detail="Telefone only have 15 caracteres")

    if cep_length != 8:
        raise HTTPException(status_code=400, detail="Cep need to have 8 caracteres")

    if local_length > 100:
        raise HTTPException(status_code=400, detail="Local only have 100 caracteres")

    if numero_casa_length > 100:
        raise HTTPException(status_code=400, detail="Numero casa only have 10 caracteres")

    if bairro_length > 50:
        raise HTTPException(status_code=400, detail="Bairro only have 50 caracteres")

    if complemento_length > 50:
        raise HTTPException(status_code=400, detail="Complemento only have 100 caracteres")

    if cidade_lenth > 50:
        raise HTTPException(status_code=400, detail="Cidade only have 50 caracteres")

    if not user_data["email"]: 
        raise HTTPException(status_code=400, detail="'email' cannot be null")
    if not user_data["tipo_usuario"]:
        raise HTTPException(status_code=400, detail="'tipo_usuario' cannot be null")
    if not isValidCpf(user_data["cpf"]):
        raise HTTPException(status_code=400, detail="CPF invalid")
    if not user_data.get("cpf"):
        raise HTTPException(status_code=400, detail="'CPF' cannot be null")
    if not user_data.get("nome"):
        raise HTTPException(status_code=400, detail="Nome cannot be null")
    if not user_data.get("data_nascimento"):
        raise HTTPException(status_code=400, detail="'Data de nascimento' cannot be null")
    if not user_data.get("telefone"):
        raise HTTPException(status_code=400, detail="'Telefone' cannot be null") 
    
    if not user_data["endereco"]["cep"]:
        raise HTTPException(status_code=400, detail="Cep cannot be null")    
    if not user_data["endereco"]["local"]:
        raise HTTPException(status_code=400, detail="Local cannot be null")  
    if not user_data["endereco"]["numero_casa"]:
        raise HTTPException(status_code=400, detail="Numero_casa cannot be null")
    if not user_data["endereco"]["bairro"]:
        raise HTTPException(status_code=400, detail="Bairro cannot be null")    
    if not user_data["endereco"]["cidade"]:
        raise HTTPException(status_code=400, detail="Cidade cannot be null")  
    if not user_data["endereco"]["estado"]:
        raise HTTPException(status_code=400, detail="Estado cannot be null")
    
async def cpf_exists(user_data, user_repository):
    existing = await user_repository.find_by_cpf(user_data["cpf"])
    if existing:
        raise HTTPException(status_code=400, detail="Cpf already exists.")

async def email_exists(user_data, user_repository):
    existing = await user_repository.find_by_email(user_data["email"])
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists.")

async def is_password_strong(user_password: str):
    password_length = len(user_password)
    if password_length < 12:
        raise HTTPException(status_code=400, detail="password need 12 caracteres length")
    if not re.search(r"[A-Z]", user_password):
        raise HTTPException(status_code=400, detail="password need at least one UPPERCASE")
    if not re.search(r"[a-z]", user_password):
        raise HTTPException(status_code=400, detail="password need at least one DOWNCASE")
    if not re.search(r"[0-9]", user_password):
        raise HTTPException(status_code=400, detail="password need at least one number")
    if not re.search(r"[!@#$%^&*()_+=-]", user_password):
        raise HTTPException(status_code=400, detail="password need at least one special caracterer")