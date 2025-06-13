from dao.repository.conta.ContaRepository import ContaRepository

def validate():
    pass

async def create_conta(input_data, current_user):
    input_data_dict = input_data.dict()

