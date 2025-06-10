from sqlalchemy import text

async def generate_otp(session, id_usuario):
    result = await session.execute(
        text("CALL gerar_otp(:id_usuario)"),
        {"id_usuario": id_usuario}
    )
    row = result.fetchone()
    if row:
        return row[0]