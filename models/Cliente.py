from dao.config.database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Cliente(Base):
    __tablename__ = 'clientes'
    
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    score_credito = Column(Integer)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), unique=True)
    
    usuario = relationship("Usuario", back_populates="cliente")
    
    def __init__(self, score_credito, usuario):
        self.score_credito = score_credito
        self.usuario = usuario
    
    def __repr__(self):
        return f"<Cliente(id={self.id_cliente}, score={self.score_credito})>"