from sqlalchemy import Column, Integer, String, Date,  Boolean, VARCHAR
from sqlalchemy.orm import relationship

from dao.config.database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String(20))
    tipo_usuario = Column(String(20), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    otp_ativo = Column(String(6), default=False)
    otp_expiracao = Column(Date)
    email = Column(VARCHAR(255), unique=True, nullable=False)

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    funcionarios = relationship("Funcionario", back_populates="usuario")
    endereco = relationship("Endereco", back_populates="usuario", uselist=False)
    
    def __init__(self, nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash, email):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.tipo_usuario = tipo_usuario
        self.senha_hash = senha_hash
        self.email = email