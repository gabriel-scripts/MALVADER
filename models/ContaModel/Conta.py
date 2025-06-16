from sqlalchemy import Column, Integer, String, Date, ForeignKey, DECIMAL, Enum
from sqlalchemy.orm import relationship
from dao.config.database import Base
from models.Agencia import Agencia

class Conta(Base):
    __tablename__ = 'conta'

    id_conta = Column(Integer, primary_key=True, autoincrement=True)
    numero_conta = Column(String(20), unique=True, nullable=False)
    id_agencia = Column(Integer, ForeignKey("agencia.id_agencia"), nullable=False)
    saldo = Column(DECIMAL(15,2), default=0.00)
    tipo_conta = Column(Enum('poupanca', 'corrente', 'investimento'), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    data_abertura = Column(Date, nullable=False)
    status = Column(Enum('ativa', 'inativa', 'bloqueada'), default='ativa')
