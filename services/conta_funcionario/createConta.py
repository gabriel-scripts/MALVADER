from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import text

from dao.repository.EnderecoRepository import EnderecoRepository
from dao.repository.UserRepository import UserRepository
from dao.repository.ClienteRepository import ClienteRepository

from dao.repository.conta.AgenciaRepository import AgenciaRepository
from dao.repository.conta.ContaRepository import ContaRepository
from dao.repository.conta.CorrenteRepository import CorrenteRepository
from dao.repository.conta.investimentoRepository import InvestimentoRepository
from dao.repository.conta.PoupancaRepository import PoupancaRepository


async def gerar_numero_conta(session):
    result = await session.execute(
        text("CALL gerar_numero_conta()")
    )
    await session.commit() 
    row = result.fetchone()
    if row:
        return row[0]
    
async def gerar_taxa(session):
    result = await session.execute(
        text("CALL gerar_taxa_manutencao()")
    )
    await session.commit() 
    row = result.fetchone()
    if row:
        return row[0]

def parse_data_to_agencia(input_data_dict, id_endereco):
    agencia = {
        "nome": input_data_dict["agencia"]["nome"],
        "codigo_agencia": input_data_dict["agencia"]["codigo_agencia"],
        "endereco_id": id_endereco,
    }
    return agencia

async def parse_data_to_account(session, input_data_dict, id_da_agencia, id_cliente):
    conta = {
        "numero_conta": await gerar_numero_conta(session),
        "id_agencia": id_da_agencia,
        "tipo_conta": input_data_dict["tipo_conta"],
        "data_abertura": datetime.now(),
        "id_cliente": id_cliente,
        "saldo": Decimal('0.00'),
        "status": "ativa"
    }
    return conta

async def conta_type(input_data_dict, session, conta_criada):
    if input_data_dict["tipo_conta"] not in ['poupanca', 'corrente', 'investimento']:
         raise HTTPException(status_code=400, detail="Conta must be 'poupanca', 'corrente', 'investimento'")

    conta_corrente_db = CorrenteRepository(session)
    conta_investimento_db = InvestimentoRepository(session)
    conta_poupanca_db = PoupancaRepository(session)

    if input_data_dict["tipo_conta"] == 'poupanca':
        poupanca = {
            "id_conta": conta_criada.id_conta,
            "taxa_rendimento": Decimal('0.005'),
            "ultimo_rendimento": datetime.now().date() 
        }
        conta_poupanca = await conta_poupanca_db.create(poupanca)
        if not conta_poupanca:
            raise HTTPException(status_code=400, detail="Fail to create conta poupanca")
    
    if input_data_dict["tipo_conta"] == 'corrente':
        corrente = {
            "id_conta": conta_criada.id_conta,
            "limite": Decimal(10000.0000), 
            "data_vencimento": datetime.now() + timedelta(weeks=120),  
            "taxa_manutencao": await gerar_taxa(session) 
        }
        conta_corrente = await conta_corrente_db.create(corrente)

        if not conta_corrente:
            raise HTTPException(status_code=400, detail="Fail to create conta corrente")

    if input_data_dict["tipo_conta"] == 'investimento':
        if not input_data_dict["perfil_risco"]:
             raise HTTPException(status_code=400, detail="Account need a risk perfil")

        investimento = {
            "id_conta": conta_criada.id_conta,
            "perfil_risco": input_data_dict["perfil_risco"], 
            "valor_minimo": Decimal('1000.00'),
            "taxa_rendimento_base": Decimal('0.01') 
        }
        conta_investimeto = await conta_investimento_db.create(investimento)

        if not conta_investimeto:
            raise HTTPException(status_code=400, detail="Fail to create conta investimento")

async def create_agencia(session, input_data_dict, id_endereco):
    agencia_db = AgenciaRepository(session)
    agencia = parse_data_to_agencia(input_data_dict, id_endereco)
    return await agencia_db.create(agencia)

async def buscar_agencia(session, codigo_agencia):
    agencia_db = AgenciaRepository(session)
    agencia = await agencia_db.find_by_codigo_agencia(codigo_agencia)
    return agencia
    
async def validate_current_user(current_user):
    if not current_user:
        raise HTTPException(status_code=400, detail="Usuário não está autenticado.")

    if current_user["tipo_usuario"] != 'funcionario':
        raise HTTPException(status_code=400, detail="Somente funcionários podem criar contas")
    
async def user_exists(input_data_dict, user_db_current):
    user_account = await user_db_current.find_by_cpf(input_data_dict["cpf_cliente"])
    if not user_account:
        raise HTTPException(status_code=400, detail="Usuário não foi encontrado")
    return user_account

async def create_conta(input_data, session, current_user):
    input_data_dict = input_data.dict()
    
    await validate_current_user(current_user)

    user_db_current = UserRepository(session)
    endereco_db_current = EnderecoRepository(session)
    cliente_db = ClienteRepository(session)
    conta_db = ContaRepository(session)
    
    user_account = await user_exists(input_data_dict, user_db_current)
    
    endereco = await endereco_db_current.find_by_user_id(user_account.id_usuario)
    cliente = await cliente_db.find_by_user_id(user_account.id_usuario)
    conta = await conta_db.find_by_cliente_id(cliente.id_cliente)

    if conta != None:
        raise HTTPException(status_code=400, detail="Conta alredy exists")
        
    agencia = await buscar_agencia(session, input_data_dict["agencia"]["codigo_agencia"])

    if not agencia:
        agencia = await create_agencia(session, input_data_dict, endereco.id_endereco)
        if not agencia:
            raise HTTPException(status_code=400, detail="Fail to register agencia")

    id_agencia = agencia.id_agencia

    conta = await parse_data_to_account(session, input_data_dict, id_agencia, cliente.id_cliente)
    conta_criada = await conta_db.create(conta)

    if not conta_criada:
        raise HTTPException(status_code=400, detail="Fail to create bank create account")

    await conta_type(input_data_dict, session, conta_criada)