from services.validadeData import validate_data
from util.hashPassword import verificar_senha

async def handleLogin(senha):
    try: 
        validate_data(senha)
        verificar_senha(senha)

    except Exception as e:
        pass