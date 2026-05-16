from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime



class PacienteProfile(DBBaseModel):
    __tablename__ = "pacientes"
    
    id = Column(Integer, ForeignKey('users.id'))
    cpf = Column(String(11), unique=True, nullable=False)
    idade = Column(Integer, CheckConstraint('idade >= 0'), nullable=False)
    
    atendimentos = relationship('AtendimentoModel', back_populates='paciente', cascade='all, delete-orphan')
    