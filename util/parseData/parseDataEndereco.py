def parseDataEndereco(user_data, id_usuario):
    endereco = {
        "id_usuario": id_usuario,
        "cep": user_data["endereco"]["cep"],
        "local": user_data["endereco"]["local"],
        "numero_casa": user_data["endereco"]["numero_casa"],
        "bairro": user_data["endereco"]["bairro"],
        "cidade": user_data["endereco"]["cidade"],
        "estado": user_data["endereco"]["estado"],
        "complemento": user_data["endereco"]["complemento"],
    }
    return endereco