import pytest
from fastapi import HTTPException
from services.validadeData import validate_data

import asyncio

@pytest.mark.asyncio
async def test_validate_data_success():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "702.845.270-09",  
        "nome": "Teste",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999"
    }
    try:
        await validate_data(user_data)
    except HTTPException:
        pytest.fail("validate_data should not raise HTTPException for valid data")

@pytest.mark.asyncio
async def test_validate_data_missing_nome():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "12345678909",
        "nome": "",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999"
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "Nome cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_invalid_cpf():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "00000000000",  
        "nome": "Teste",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999"
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "CPF invalid" in str(excinfo.value)