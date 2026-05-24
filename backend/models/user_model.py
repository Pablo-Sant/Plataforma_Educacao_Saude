from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class RoleEnum(str, Enum):
    PACIENTE = 'paciente'
    MEDICO = 'medico'



class UserModel(DBBaseModel):
    __tablename__='users'
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=True)
    telefone = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.now)
    role = Column(SQLEnum(RoleEnum), nullable=False)
    
    medico = relationship('MedicoProfile', back_populates='user', uselist=False)
    paciente = relationship('PacienteProfile', back_populates='user', uselist=False)

