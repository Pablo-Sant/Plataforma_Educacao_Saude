from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class RespostaModel(DBBaseModel):
    __tablename__='respostas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    resposta = Column(Text, nullable=False)
    atendimentoID = Column(Integer, ForeignKey('atendimentos.id'), nullable=False)
    perguntaID = Column(Integer, ForeignKey('perguntas.id'), nullable=False)
    opcao_perguntaID = Column(Integer, ForeignKey('opcao_pergunta.id'), nullable=False)
    
    atendimento = relationship('AtendimentoModel', back_populates='respostas')
    perguntas = relationship('PerguntaModel', back_populates='resposta')
    opcao_pergunta = relationship('OpcaoPerguntaModel', back_populates='resposta')