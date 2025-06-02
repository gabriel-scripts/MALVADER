from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

class Agencia:
    __tablename__ = 'agencia'

    id_agencia = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codigo_agencia = Column(String(20), nullable=False, unique=True)
    endereco_id = Column(Integer, primary_key=True, nullable=False)

    def __init__(self, id_agencia, nome, codigo_agencia, endereco_id):
        self.id_agencia = id_agencia
        self.nome = nome
        self.codigo_agencia = codigo_agencia
        self.endereco_id = endereco_id