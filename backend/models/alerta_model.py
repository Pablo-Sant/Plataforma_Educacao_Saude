from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
    
class AlertaModel(DBBaseModel):
    __tablename__='alertas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    texto = Column(Text, nullable=False)
    atendimentoID = Column(Integer, ForeignKey('atendimentos.id'))
    
    atendimentos = relationship('AtendimentoModel', back_populates='alerta')