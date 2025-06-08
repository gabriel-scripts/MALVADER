from fastapi import HTTPException
from util.isValidCpf import isValidCpf
import re

async def validate_data(user_data: dict):
    if user_data["tipo_usuario"] is None:
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
    
async def cpf_exists(user_data, user_repository):
    try:
        existing = await user_repository.find_by_cpf(user_data["cpf"])
        if existing:
            raise HTTPException(status_code=400, detail="Usuário already exists.")
    except Exception as e:
        raise Exception(f"[error]: ValidateData.py on cpf_exists() as: {e}")
    
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