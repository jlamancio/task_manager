from sqlalchemy import Column, Integer, String
from database.db import Base

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)