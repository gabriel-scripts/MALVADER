def parseDataToFuncionario(user_data,  id_usuario, id_supervisor):
    funcinario = {
        "id_usuario": id_usuario,
        "codigo_funcionario": user_data["codigo_funcionario"],
        "cargo": user_data["cargo"],
        "id_supervisor": id_supervisor
    }
    return funcinario