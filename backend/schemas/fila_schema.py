from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from backend.schemas.atendimento_schema import ClassificacaoRiscoEnum


class FilaItemOut(BaseModel):
    id: int
    paciente_id: int
    paciente_nome: str
    classificacao_risco: Optional[ClassificacaoRiscoEnum] = None
    classificacao_triagem: Optional[str] = None
    data_atendimento: datetime

    model_config = {"from_attributes": True}