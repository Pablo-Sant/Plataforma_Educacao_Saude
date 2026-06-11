from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime


class PerguntaModel(DBBaseModel):
    __tablename__='perguntas'
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    tipo = Column(Text) 
    created_at = Column(DateTime, default=datetime.now)
    opcao_resposta = relationship('OpcaoRespostaModel', foreign_keys='OpcaoRespostaModel.pergunta_id', back_populates='pergunta')