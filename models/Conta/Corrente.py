from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

class Corrente:
    __tablename__ = 'conta'

    id_conta = Column(Integer, primary_key=True, autoincrement=True)