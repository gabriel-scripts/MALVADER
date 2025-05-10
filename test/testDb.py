from dao.UserRepository import UserRepository

def test():
    user = UserRepository()
    user_data = {
        "nome": "Teste",
        "cpf": "12345678901",
        "data_nascimento": "2000-01-01",
        "telefone": "11987654321",                    
        "tipo_usuario": "cliente",
        "senha_hash": "hash123"
    }

    user.addUser(user_data)
    pass

test()