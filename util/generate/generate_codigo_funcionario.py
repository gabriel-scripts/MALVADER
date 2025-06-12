from sqlalchemy import text


async def generate_codigo_funcionario(session):
    result = await session.execute(
        text("CALL gerar_codigo()"),
    )
    codigo = result.fetchone()[0]
    return codigo