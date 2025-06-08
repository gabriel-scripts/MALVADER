from dao.UserRepository import UserRepository
from dao.config.database import SessionLocal
from dao.config.createTables import create_tables

create_tables()

def test():
    db = SessionLocal()
    user = UserRepository(db)
    user_data = {
        "nome": "Teste",
        "cpf": "12345678901",
        "data_nascimento": "2000-01-01",
        "telefone": "11987654321",                    
        "tipo_usuario": "cliente",
        "senha_hash": "hash123"
    }

    user.create(user_data) 
    pass

test()