from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class ClassificacaoRiscoEnum(str, Enum):
    BAIXO = 'baixo'
    MEDIO = 'medio'
    ALTO =  'alto'
    


class Status(str, Enum):
    AGUARDANDO = 'aguardando'
    EM_ATENDIMENTO = 'em_atendimento'
    FINALIZADO = 'finalizado'
    
    
    
class AtendimentoBase(BaseModel):
    classificacao_risco: ClassificacaoRiscoEnum
    status: Status
    descricao: str = Field(..., max_length=500)
    resumo_ia: str
    
    
       
class AtendimentoInput(AtendimentoBase):
    pass


class AtendimentoResponse(AtendimentoBase):
    id: int
    data_atendimento: datetime
    paciente_id: int
    medico_id: int
    