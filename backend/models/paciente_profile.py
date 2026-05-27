from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime



class PacienteProfile(DBBaseModel):
    __tablename__ = "pacientes"
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    idade = Column(Integer, CheckConstraint('idade >= 0'), nullable=False)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'), nullable=False)
    
    
    atendimentos = relationship('AtendimentoModel', back_populates='paciente')
    user = relationship('UserModel', back_populates='paciente')
    clinica = relationship('ClinicaModel', back_populates='user')