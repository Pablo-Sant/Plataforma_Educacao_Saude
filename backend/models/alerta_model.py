from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class ClassificacaoEnum(str, Enum):
    ALTO = 'alto'
    MEDIO = 'medio'
    BAIXO = 'baixo'
    

class AlertaModel(DBBaseModel):
    __tablename__='alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    classificacao_risco = Column(SQLEnum(ClassificacaoEnum), nullable=False)
    atendimentoID = Column(Integer, ForeignKey('atendimentos.id'))
    
    atendimentos = relationship('AtendimentoModel', back_populates='alerta')