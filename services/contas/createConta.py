from datetime import datetime
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

async def create_conta(input_data, session, current_user):
    print("create_conta:", current_user)
    
    user_db_current = UserRepository(session)
    endereco_db_current = EnderecoRepository(session)
    cliente_db = ClienteRepository(session)

    conta_db = ContaRepository(session)
    conta_corrente_db = CorrenteRepository(session)
    conta_investimento_db = InvestimentoRepository(session)
    conta_poupanca_db = PoupancaRepository(session)
    agencia_db = AgenciaRepository(session)

    user_current = await user_db_current.find_by_cpf(current_user["cpf"])
    endereco = await endereco_db_current.find_by_user_id(user_current.id_usuario)
    cliente = await cliente_db.find_by_user_id(user_current.id_usuario)
    conta = await conta_db.find_by_cliente_id(cliente.id_cliente)

    if conta != None:
        raise HTTPException(status_code=400, detail="Conta alredy exists")

    input_data_dict = input_data.dict()

    input_data_dict["numero_conta"] = await gerar_numero_conta(session)
    input_data_dict["data_abertura"] = datetime.now()
    input_data_dict["status"] = "ativa"
    input_data_dict["saldo"] = Decimal('0.00')

    input_data_dict["agencia"]["endereco_id"] = endereco.id_endereco
    agencia = {
        "nome": input_data_dict["agencia"]["nome"],
        "codigo_agencia": input_data_dict["agencia"]["codigo_agencia"],
        "endereco_id": input_data_dict["agencia"]["endereco_id"],
    }

    agencia_nova = await agencia_db.create(agencia)

    if not agencia_nova:
        raise HTTPException(status_code=400, detail="Fail to register agencia")
    
    conta = {
        "numero_conta": input_data_dict["numero_conta"],
        "id_agencia": agencia_nova.id_agencia,
        "data_abertura": input_data_dict["data_abertura"],
        "status": input_data_dict["status"],
        "saldo": input_data_dict["saldo"],
        "id_cliente": cliente.id_cliente
    }

    conta_criada = await conta_db.create(input_data_dict)

    if not conta_criada:
        raise HTTPException(status_code=400, detail="Fail to create account")
    
    if input_data_dict["tipo_conta"] not in ['poupanca', 'corrente', 'investimento']:
         raise HTTPException(status_code=400, detail="Conta must be 'poupanca' 'corrente' 'investimento'")

    if input_data_dict["tipo_conta"] == 'poupanca':
        poupanca = {
            "id_conta": conta_criada.id_conta,
            "taxa_redimento": Decimal,
            "ultimo_rendimento": datetime
        }
        conta_poupanca_db.create(poupanca)

    
    if input_data_dict["tipo_conta"] == 'corrente':
        corrente = {
            "id_conta": conta_criada.id_conta,
            "limite": Decimal(10000.0000), 
            "data_vencimento": datetime, # FRONT
            "taxa_manutencao": gerar_taxa()
        }
        conta_corrente_db.create(corrente)

    if input_data_dict["tipo_conta"] == 'investimento':
        investimento = {
            "id_conta": conta_criada.id_conta,
            "perfil_risco": "conservador", # FRONT
            "valor_minimo": Decimal, 
            "taxa_redimento_base": Decimal
        }
        conta_investimento_db.create(investimento)