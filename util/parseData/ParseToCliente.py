from models.Cliente import Cliente

def parseDataToCliente(user_data, user_object):
    cliente = Cliente(
        usuario= user_object,
        score_credito= user_data["score_credito"],
    )
    return cliente