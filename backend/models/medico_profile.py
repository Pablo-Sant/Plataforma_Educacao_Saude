from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime


class MedicoProfile(DBBaseModel):
    __tablename__='medicos'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    crm = Column(String, unique=True, nullable=False)
    clinica_id = Column(Integer, ForeignKey('clinicas.id'), nullable=False)
    
    user = relationship('UserModel', back_populates='medico')
    atendimentos = relationship('AtendimentoModel', back_populates='medico')  
    clinica = relationship('ClinicaModel', back_populates='medicos') 