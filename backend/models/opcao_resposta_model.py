from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from backend.core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime

class OpcaoRespostaModel(DBBaseModel):
    __tablename__='opcao_pergunta'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    perguntaID = Column(Integer, ForeignKey('perguntas.id'))
    proxima_pergunta_id = Column(Integer, ForeignKey('perguntas.id'), nullable=False)
    
    pergunta = relationship('PerguntaModel', back_populates='opcao_pergunta')