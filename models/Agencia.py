from sqlalchemy import Column, Integer, String, ForeignKey
from dao.config.database import Base

class Agencia(Base):
    __tablename__ = 'agencia'
    id_agencia = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    codigo_agencia = Column(String(10), unique=True, nullable=False)
    endereco_id = Column(Integer, ForeignKey("endereco.id_endereco"))