from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Boolean
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime


class ClinicaModel(DBBaseModel):
    __tablename__= 'clinicas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    telefone = Column(String(20), nullable=False)
    endereco = Column(String(255), nullable=True)
    ativa = Column(Boolean, default=True)

    medicos = relationship('MedicoProfile', back_populates='clinica', cascade='all, delete-orphan')
    atendimentos= relationship('AtendimentoModel', back_populates='clinica', cascade='all, delete-orphan')
    pacientes = relationship('PacienteProfile', back_populates='clinica', cascade='all, delete-orphan')