from sqlalchemy import Column, Integer, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Poupanca(Base):
    __tablename__ = 'conta_poupanca'

    id_conta_poupanca = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey("conta.id_conta"), unique=True, nullable=False)
    taxa_rendimento = Column(DECIMAL(5,4), nullable=False)
    ultimo_rendimento = Column(Date)

    conta = relationship("Conta", back_populates="poupanca")