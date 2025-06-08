def parseDataToFuncionario(user_data):
    funcinario = {
        "score_credito": user_data["score_credito"],
        "id_usuario": user_data["id_usuario"]
    }
    return funcinario