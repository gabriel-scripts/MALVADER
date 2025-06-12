from models.Usuario import Usuario

def parseDataToUser(data):
    usuario = {
        "nome": data["nome"],
        "cpf": data["cpf"],
        "data_nascimento":data["data_nascimento"],
        "telefone": data["telefone"],
        "tipo_usuario": data["tipo_usuario"],
        "senha_hash": data["senha_hash"],
        "email":data["email"]
    }
    return usuario