from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

class Poupanca:
    __tablename__ = 'conta_poupanca'

    id_conta_poupanca = Column(Integer, primary_key=True, autoincrement=True)