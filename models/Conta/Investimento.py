from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean

class Investimento:
    __tablename__ = 'conta_investimento'

    id_conta = Column(Integer, primary_key=True, autoincrement=True)