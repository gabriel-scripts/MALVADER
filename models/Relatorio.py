from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Relatorio(Base):
    __tablename__ = "relatorio"

    id_relatorio = Column(Integer, primary_key=True, autoincrement=True)
    id_funcionario = Column(Integer, ForeignKey("funcionario.id_funcionario"), nullable=False)
    tipo_relatorio = Column(String(50), nullable=False)
    data_geracao = Column(DateTime, nullable=False)
    conteudo = Column(Text)