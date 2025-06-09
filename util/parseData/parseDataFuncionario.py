def parseDataToFuncionario(user_data,  usuario_objeto):
    funcinario = {
        "nome": user_data["nome"],
        "codigo_funcionario": user_data["codigo_funcionario"],
        "data_nascimento": user_data["data_nascimento"],
        "cargo": user_data["cargo"],
        "id_usuario": user_data["id_usuario"],
        "senha_hash": user_data["senha_hash"],
        "usuario": usuario_objeto,
    }
    return funcinario