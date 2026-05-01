from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime



class PacienteModel(DBBaseModel):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    telefone = Column(String(20), nullable=False)
    idade = Column(Integer, CheckConstraint('idade >= 0'), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)
    
    atendimentos = relationship('AtendimentoModel', back_populates='paciente', cascade='all, delete-orphan')
    