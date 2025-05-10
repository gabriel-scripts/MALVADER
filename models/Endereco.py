from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Endereco(Base):
    __tablename__ = 'enderecos'
    
    id_endereco = Column(Integer, primary_key=True, autoincrement=True)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(255))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)
    
    usuario_id = Column(Integer, ForeignKey('usuarios.id_usuario'))
    
    usuario = relationship("Usuario", back_populates="enderecos")
    
    def __init__(self, logradouro, numero, complemento, bairro, cidade, estado, cep):
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
