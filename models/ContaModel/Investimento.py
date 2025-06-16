from sqlalchemy import Column, Integer, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Investimento(Base):
    __tablename__ = 'conta_investimento'

    id_conta_investimento = Column(Integer, primary_key=True, autoincrement=True)
    id_conta = Column(Integer, ForeignKey("conta.id_conta"), unique=True, nullable=False)
    perfil_risco = Column(Enum('conservador', 'moderado', 'arrojado'), nullable=False)
    valor_minimo = Column(DECIMAL(15,2), nullable=False)
    taxa_rendimento_base = Column(DECIMAL(5,4), nullable=False)
