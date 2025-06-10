
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from dao.config.database import Base

class Auditoria(Base):
    __tablename__ = 'auditoria'
    id_auditoria = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    acao = Column(String(50), nullable=False)
    data_hora = Column(Date, nullable=False)
    detalhes = Column(Text)