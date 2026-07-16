from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLEnum
)

from sqlalchemy.orm import relationship

from datetime import datetime
from enum import Enum

from backend.core.configs import DBBaseModel


class ClassificacaoFilaEnum(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"


class FilaModel(DBBaseModel):

    __tablename__ = "fila"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    atendimento_id = Column(
        Integer,
        ForeignKey("atendimentos.id"),
        nullable=False,
        unique=True
    )

    codigo = Column(
        String(4),
        nullable=False,
        unique=True
    )

    classificacao = Column(
        SQLEnum(ClassificacaoFilaEnum),
        nullable=False
    )

    pontuacao = Column(
        Integer,
        nullable=False
    )

    criado_em = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )


    atendimento = relationship(
        "AtendimentoModel",
        back_populates="fila"
    )