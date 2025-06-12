from dao.repository.UserRepository import UserRepository
from dao.config.database import get_async_session
from dao.config.createTables import create_tables
from dao.repository.EnderecoRepository import EnderecoRepository


from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

def test(session: AsyncSession = Depends(get_async_session)):

    user = UserRepository(session)
    endereco = EnderecoRepository(session)

    user_data = {
        "nome": "Teste",
        "cpf": "12345678901",
        "data_nascimento": "2000-01-01",
        "telefone": "11987654321",                    
        "tipo_usuario": "cliente",
        "senha_hash": "hash123"
    }

    endereco = {
        "id_usuario": 1,
        "cep": "TEST",
        "local": "TEST",
        "numero_casa": 123,
        "bairro": "TEST",
        "cidade": "TEST",
        "estado": "TEST",
        "complemento": "TEST"
    }
    endereco.create(endereco)
    

test()