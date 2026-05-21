from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime


class MedicoProfile(DBBaseModel):
    __tablename__='medicos'
    
    id_medico = Column(Integer, ForeignKey('users.id'), primary_key=True)
    CRM = Column(String, unique=True, nullable=False)
    
    user = relationship('UserModel', back_populates='medico')
    atendimentos = relationship('AtendimentosModel', back_populates='medico')   