from dao.repository.AuditoriaRepository import AuditoriaRepository

async def save_auditoria(session, Auditoria: dict):
    auditoria_repository = AuditoriaRepository(session)
    audioria = await auditoria_repository.create(Auditoria)
    return audioria