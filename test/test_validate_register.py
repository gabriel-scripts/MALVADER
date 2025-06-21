import pytest
from fastapi import HTTPException
from services.validadeData import validate_data

@pytest.mark.anyio
async def test_validate_data_success():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "70284527009",  
        "nome": "Teste",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabrisEmail@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    try:
        resultado = await validate_data(user_data)
        print(resultado)
    except HTTPException:
        pytest.fail("validate_data should not raise HTTPException for valid data")

@pytest.mark.asyncio
async def test_validate_data_missing_nome():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "70284527009",  
        "nome": "",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabrisEmail@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "Nome cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_missing_email():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "70284527009",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "'email' cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_missing_telefone():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "70284527009",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "",
        "email": "gabriel@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "'Telefone' cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_missing_data_nascimento():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "70284527009",  
        "nome": "gabriel",
        "data_nascimento": "",
        "telefone": "11999999999",
        "email": "gabriel@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "'Data de nascimento' cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_missing_tipo_usuario():
    user_data = {
        "tipo_usuario": "",
        "cpf": "70284527009",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabriel@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "'tipo_usuario' cannot be null" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_small_length_cpf():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "000000",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabrisEmail@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "CPF only have 11 caracteres" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_invalid_cpf():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "12345678911",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabrisEmail@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "CPF invalid" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_out_length_cpf():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "000000000000",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabrisEmail@gmail.com",
        "endereco": {
            "estado": "DF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "CPF only have 11 caracteres" in str(excinfo.value)

@pytest.mark.asyncio
async def test_validate_data_out_length_estado():
    user_data = {
        "tipo_usuario": "cliente",
        "cpf": "000000000",  
        "nome": "gabriel",
        "data_nascimento": "2000-01-01",
        "telefone": "11999999999",
        "email": "gabriel@gmail.com",
        "endereco": {
            "estado": "DFF",
            "cep": "12345678",
            "local": "algum",
            "numero_casa": "12345",
            "bairro": "algum bairro",
            "cidade": "alguma cidade",
            "complemento": "algum complemento"

        }
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_data(user_data)
    assert "Estado only have 2 caracteres" in str(excinfo.value)