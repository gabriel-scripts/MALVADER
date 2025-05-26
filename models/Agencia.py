from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean


class Agencia:
    __tablename__ = 'agencia'

    id_agencia = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    codigo_agencia = Column(String(20), nullable=False, unique=True)
    endereco_id = Column(Integer, primary_key=True, nullable=False)
    