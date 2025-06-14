from sqlalchemy import Column, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Corrente(Base):
    __tablename__ = 'conta_corrente'

    id_conta_corrente = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey("conta.id_conta"), unique=True, nullable=False)
    limite = Column(DECIMAL(15,2), default=0.00)
    data_vencimento = Column(Date)
    taxa_manutencao = Column(DECIMAL(5,2))
