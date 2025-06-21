from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from fastapi import HTTPException

from services.conta_funcionario.createConta import create_conta, validate_current_user
from models.pydantic.ContaBase import ContaBase, AgenciaBase


@pytest.fixture
def mock_repos():
    user = MagicMock(id_usuario=1)
    endereco = MagicMock(id_endereco=1)
    cliente = MagicMock(id_cliente=1)
    agencia = MagicMock(id_agencia=1234)
    conta_db = MagicMock()
    conta_db.create = AsyncMock(return_value=MagicMock(id_conta=1))
    conta_db.find_by_cliente_id = AsyncMock(return_value=None)

    patches = [
        patch("services.conta_funcionario.createConta.UserRepository"),
        patch("services.conta_funcionario.createConta.EnderecoRepository"),
        patch("services.conta_funcionario.createConta.ClienteRepository"),
        patch("services.conta_funcionario.createConta.AgenciaRepository"),
        patch("services.conta_funcionario.createConta.ContaRepository"),
        patch("services.conta_funcionario.createConta.CorrenteRepository", return_value=AsyncMock()),
        patch("services.conta_funcionario.createConta.PoupancaRepository", return_value=AsyncMock()),
        patch("services.conta_funcionario.createConta.InvestimentoRepository", return_value=AsyncMock()),
        patch("services.conta_funcionario.createConta.gerar_numero_conta", AsyncMock(return_value=123456)),
        patch("services.conta_funcionario.createConta.gerar_taxa", AsyncMock(return_value=10.0)),
    ]
    actives = [p.start() for p in patches]

    actives[0].return_value.find_by_cpf = AsyncMock(return_value=user)
    actives[1].return_value.find_by_user_id = AsyncMock(return_value=endereco)
    actives[2].return_value.find_by_user_id = AsyncMock(return_value=cliente)
    actives[3].return_value.find_by_codigo_agencia = AsyncMock(return_value=agencia)
    actives[4].return_value = conta_db

    yield {
        "user": user,
        "endereco": endereco,
        "cliente": cliente,
        "agencia": agencia,
        "conta_db": conta_db,
        "patches": actives
    }
    for p in patches:
        p.stop()

@pytest.mark.anyio
async def test_validate_create_success(mock_repos):
    conta = ContaBase(
        id_agencia=1234,
        cpf_cliente="08350090170",
        saldo=0,
        tipo_conta="corrente",
        id_cliente=1,
        data_abertura="2024-06-21",
        status="ativa",
        agencia=AgenciaBase(
            nome="Nome da agencia",
            codigo_agencia=1,
            endereco_id=None
        ),
        perfil_risco="baixo"
    )
    current_user = {"tipo_usuario": "funcionario"}
    session = AsyncMock()
    await create_conta(conta, session, current_user)

@pytest.mark.anyio
async def test_create_conta_usuario_not_exists(mock_repos):
    mock_repos["patches"][0].return_value.find_by_cpf = AsyncMock(return_value=None)
    conta = ContaBase(
        id_agencia=1234,
        cpf_cliente="08350090170",
        saldo=0,
        tipo_conta="corrente",
        id_cliente=1,
        data_abertura="2024-06-21",
        status="ativa",
        agencia=AgenciaBase(
            nome="Nome da agencia",
            codigo_agencia=1,
            endereco_id=None
        ),
        perfil_risco="baixo"
    )

    current_user = {"tipo_usuario": "funcionario"}
    session = AsyncMock()
    with pytest.raises(HTTPException) as excinfo:
        await create_conta(conta, session, current_user)
    assert excinfo.value.status_code == 400
    assert "Usuário não foi encontrado" in str(excinfo.value)

@pytest.mark.anyio
async def test_validate_funcionario():
    current_user = {
        "tipo_usuario": "cliente"
    }
    with pytest.raises(HTTPException) as excinfo:
        await validate_current_user(current_user)
    assert "Somente funcionários podem criar contas" in str(excinfo.value)