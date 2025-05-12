from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

class Transacao:
    __tablename__ = 'transacao'

    id_conta = Column(Integer, primary_key=True, autoincrement=True)