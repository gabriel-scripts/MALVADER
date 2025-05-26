from models.Usuario import Usuario

def parseDataToUser(data):
    dataParsed = {
        "nome": data[0],
        "cpf": data[1],
        "data_nascimento": data[2],
        "telefone": data[3],
        "tipo_usuario": data[4],
        "senha_hash": data[5]
    }
    usuario = Usuario(dataParsed["nome"], dataParsed["cpf"], dataParsed["data_nascimento"], dataParsed["telefone"], dataParsed["tipo_usuario"], dataParsed["senha_hash"])
    return usuario