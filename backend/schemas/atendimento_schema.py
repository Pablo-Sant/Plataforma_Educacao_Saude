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
    status: Optional[Status] = None
    descricao: Optional[str] = Field(None, max_length=500)
    resumo_ia: Optional[str] = None
    classificacao_risco: Optional[ClassificacaoRiscoEnum] = None    
    
       
class AtendimentoInput(BaseModel):
    clinica_id: int
    paciente_id: int
    


class AtendimentoResponse(AtendimentoBase):
    id: int
    data_atendimento: datetime
    paciente_id: int
    medico_id: Optional[int] = None

    
    model_config = {
    "from_attributes": True
}
    