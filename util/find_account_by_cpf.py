from dao.repository.ClienteRepository import ClienteRepository
from dao.repository.UserRepository import UserRepository
from dao.repository.conta.ContaRepository import ContaRepository


async def find_account_by_cpf(session, cpf):
    user_db_current = UserRepository(session)
    cliente_db = ClienteRepository(session)
    conta_db = ContaRepository(session)

    user = await user_db_current.find_by_cpf(cpf)
    cliente = await cliente_db.find_by_user_id(user.id_usuario)
    conta = await conta_db.find_by_cliente_id(cliente.id_cliente)

    return conta