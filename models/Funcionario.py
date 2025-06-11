from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Funcionario(Base):
    __tablename__ = 'funcionario'
    id_funcionario= Column(Integer, primary_key=True, autoincrement=True)
    
    codigo_funcionario = Column(String(11), unique=True, nullable=False)
    cargo = Column(String(20), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)
    id_supervisor = Column(String(20), nullable=False)

    usuario = relationship("Usuario", back_populates="funcionarios", uselist=False) 