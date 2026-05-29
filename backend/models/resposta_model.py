from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class RespostaModel(DBBaseModel):
    __tablename__='respostas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resposta = Column(Text, nullable=False)
    atendimento_id = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    pergunta_id = Column(Integer, ForeignKey('perguntas.id'), nullable=False)
    opcao_resposta_id = Column(Integer, ForeignKey('opcao_resposta.id'), nullable=False)
    
    atendimento = relationship('AtendimentoModel', back_populates='respostas')
    