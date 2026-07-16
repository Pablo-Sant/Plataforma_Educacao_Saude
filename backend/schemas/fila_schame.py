from datetime import datetime

from pydantic import BaseModel

from backend.models.fila_model import ClassificacaoFilaEnum


class FilaResponse(BaseModel):

    id: int
    atendimento_id: int
    codigo: str
    classificacao: ClassificacaoFilaEnum
    pontuacao: int
    criado_em: datetime


    class Config:
        from_attributes = True