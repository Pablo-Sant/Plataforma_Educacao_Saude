from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime



class PacienteProfile(DBBaseModel):
    __tablename__ = "pacientes"
    
    id_paciente = Column(Integer, ForeignKey('users.id'), primary_key=True)
    idade = Column(Integer, CheckConstraint('idade >= 0'), nullable=False)
    
    atendimentos = relationship('AtendimentoModel', back_populates='paciente', cascade='all, delete-orphan')
    
    user = relationship('UserModel', back_populates='paciente')