from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class RespostaIAModel(DBBaseModel):
    __tablename__='respostasIA'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    atendimentoID = Column(Integer, ForeignKey('atendimentos.id'))
    
    atendimento = relationship('AtendimentoModel', back_populates='respostaIA')