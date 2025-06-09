from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dao.config.database import Base

class Endereco(Base):
    __tablename__ = 'endereco'
    
    id_endereco = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"), nullable=False)

    cep = Column(String(10), nullable=False)
    local = Column(String(100), nullable=False)
    numero_casa = Column(Integer, nullable=False)
    complemento = Column(String(255))
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(2), nullable=False)
    
    usuario = relationship("Usuario", back_populates="endereco")
    
    def __init__(self, id_usuario, cep, local, numero_casa, complemento, bairro, cidade, estado):
        self.id_usuario = id_usuario,
        self.cep = cep
        self.local = local
        self.numero_casa = numero_casa
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado