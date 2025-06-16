from util.clear_data import remove_special_characters, remove_space, only_numbers

def parseInput(data):
    input_clear = {
        "nome": data["nome"],
        "cpf": only_numbers(data["cpf"]),
        "data_nascimento": data["data_nascimento"],
        "telefone": only_numbers(data["telefone"]),
        "tipo_usuario": remove_space(data["tipo_usuario"]),
        "senha_hash": data["senha_hash"],
        "email":data["email"],
        "score_credito": data["score_credito"],
        "cargo": data["cargo"], 
        "id_supervisor": data["id_supervisor"], 
        "endereco":{
            "cep": only_numbers(data["endereco"]["cep"]),
            "local": data["endereco"]["local"],
            "numero_casa": only_numbers(str(data["endereco"]["numero_casa"])),
            "bairro": data["endereco"]["bairro"],
            "cidade": data["endereco"]["cidade"],
            "estado": remove_space(data["endereco"]["estado"]),
            "complemento": remove_special_characters(data["endereco"]["complemento"])
        }
    }
    return input_clear