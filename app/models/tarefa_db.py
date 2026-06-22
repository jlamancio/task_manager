from sqlalchemy import Column, Integer, String, DateTime, Date
from database.db import Base 

class TarefaDB(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    status = Column(String, default="pendente", nullable=False)
    prioridade = Column(String, default="media", nullable=False)
    data_criacao = Column(DateTime, nullable=False)
    data_vencimento = Column(Date, nullable=False)