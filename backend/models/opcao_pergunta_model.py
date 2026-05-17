from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime

class OpcaoPerguntaModel(DBBaseModel):
    __tablename__='opcao_pergunta'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    perguntaID = Column(Integer, ForeignKey('perguntas.id'))
    
    pergunta = relationship('PerguntaModel', back_populates='opcao_pergunta')