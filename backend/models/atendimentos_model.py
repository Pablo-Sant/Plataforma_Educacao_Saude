from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Text
from core.configs import DBBaseModel
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class ClassificacaoRiscoEnum(str, Enum):
    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    
    
class StatusEnum(str, Enum):
    AGUARDANDO = 'aguardando'
    EM_ATENDIMENTO = 'em_atendimento'
    FINALIZADO = 'finalizado'
    

class AtendimentoModel(DBBaseModel):
    __tablename__='atendimentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    classificacao_risco = Column(SQLEnum(ClassificacaoRiscoEnum), nullable=False)
    status = Column(SQLEnum(StatusEnum), nullable=False)
    descricao = Column(Text(500), nullable=False)
    data_atendimento = Column(DateTime, default=datetime.now, nullable=False)
    pacienteID = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medicoID = Column(Integer, ForeignKey('medicos.id'), nullable=False)
    
    paciente = relationship('PacienteModel', back_populates='atendimentos')
    medico = relationship('MedicoModel', back_populates='atendimentos')
    perguntas = relationship('PerguntaModel', back_populates='atendimentos', cascade='all, delete-orphan')
    alerta = relationship('AtendimentoModel', back_populates='atendimentos', cascade='all, delete-orphan')
    respostaIA = relationship('RespostaIAModel', back_populates='atendimento', cascade='all, delete-orphan')
    respostas = relationship('RespostaModel', back_populates='atendimento', cascade='all, delete-orphan')