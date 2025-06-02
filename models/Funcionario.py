from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Funcionario(Base):
    __tablename__ = 'funcionario'
      
    id_funcionario= Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    codigo_funcionario = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date)

    cargo = Column(String(20), nullable=False)
    id_usuario = Column(String(20), nullable=False)
    id_supervisor = Column(String(20), nullable=False)
    senha_hash = Column(String(255), nullable=False, unique=True)

    usuario = relationship("Usuario", back_populates="usuario", uselist=False)

    def __init__(self, id_funcionario, nome, codigo_funcionario, data_nascimento, cargo, id_usuario, id_supervisor):
        self.id_funcionario = id_funcionario
        self.nome = nome
        self.codigo_funcionario = codigo_funcionario
        self.data_nascimento = data_nascimento
        self.cargo = cargo
        self.id_usuario = id_usuario
        self.id_supervisor = id_supervisor