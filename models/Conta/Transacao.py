from sqlalchemy import Column, Integer, DECIMAL, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Transacao(Base):
    __tablename__ = 'transacao'

    id_transacao = Column(Integer, primary_key=True, autoincrement=True)
    id_conta_origem = Column(Integer, ForeignKey("conta.id_conta"), nullable=False)
    id_conta_destino = Column(Integer, ForeignKey("conta.id_conta"))
    tipo_transacao = Column(Enum('deposito', 'saque', 'transferencia', 'pagamento', 'investimento'), nullable=False)
    valor = Column(DECIMAL(15,2), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    descricao = Column(String(255))

    conta_origem = relationship("Conta", foreign_keys=[id_conta_origem], back_populates="transacoes_origem")
    conta_destino = relationship("Conta", foreign_keys=[id_conta_destino], back_populates="transacoes_destino")