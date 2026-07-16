from typing import Optional
from enum import Enum

from pydantic import BaseModel


class ClassificacaoUrgencia(str, Enum):
    BAIXO_RISCO = "BAIXO_RISCO"
    ACOMPANHAMENTO_CLINICO = "ACOMPANHAMENTO_CLINICO"
    ALTERACAO_CARDIOVASCULAR = "ALTERACAO_CARDIOVASCULAR"
    AVALIACAO_ABDOMINAL = "AVALIACAO_ABDOMINAL"
    AVALIACAO_URINARIA = "AVALIACAO_URINARIA"
    RISCO_DESIDRATACAO = "RISCO_DESIDRATACAO"
    SINDROME_VIRAL = "SINDROME_VIRAL"
    SINDROME_RESPIRATORIA = "SINDROME_RESPIRATORIA"
    LIMITACAO_MOTORA_GRAVE = "LIMITACAO_MOTORA_GRAVE"
    INCONSCIENCIA = "INCONSCIENCIA"
    SUSPEITA_AVC = "SUSPEITA_AVC"
    HEMORRAGIA_POSSIVEL = "HEMORRAGIA_POSSIVEL"
    EMERGENCIA_CARDIACA = "EMERGENCIA_CARDIACA"
    EMERGENCIA_RESPIRATORIA = "EMERGENCIA_RESPIRATORIA"


class OpcaoRespostaOut(BaseModel):
    id: int
    texto: str


class PerguntaFluxoOut(BaseModel):
    id: int
    texto: str
    tipo: str
    opcoes: list[OpcaoRespostaOut] = []


class FluxoRespostaInput(BaseModel):
    pergunta_id: int
    opcao_resposta_id: int


class TriagemResultado(BaseModel):
    classificacao: ClassificacaoUrgencia
    pontuacao_total: int


class FluxoRespostaOut(BaseModel):
    concluido: bool

    proxima_pergunta: Optional[
        PerguntaFluxoOut
    ] = None

    resultado: Optional[
        TriagemResultado
    ] = None