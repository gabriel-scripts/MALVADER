from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from dao.config.database import Base
from sqlalchemy.ext.declarative import declarative_base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    data_nascimento = Column(Date)
    telefone = Column(String(20))
    tipo_usuario = Column(String(20), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    otp_ativo = Column(Boolean, default=False)
    otp_expiracao = Column(Date)

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    
    def __init__(self, nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.tipo_usuario = tipo_usuario
        self.senha_hash = senha_hash
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usuario}, nome='{self.nome}', tipo={self.tipo_usuario})>"

    @property
    def nome_completo(self):
        return self._nome
    
    @nome_completo.setter    
    def nome_completo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome deve ser uma string não vazia")
        self._nome = valor.strip()