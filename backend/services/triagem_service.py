from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.resposta_model import RespostaModel
from backend.models.opcao_resposta_model import OpcaoRespostaModel

from backend.schemas.fluxo_schema import (
    TriagemResultado,
    ClassificacaoUrgencia
)

from backend.services.atendimento_service import AtendimentoService


async def calcular_pontuacao_total(db: AsyncSession, atendimento_id: int):

    result = await db.execute(
        select(OpcaoRespostaModel)
        .join(
            RespostaModel,
            RespostaModel.opcao_resposta_id == OpcaoRespostaModel.id
        )
        .where(RespostaModel.atendimento_id == atendimento_id)
    )

    respostas = result.scalars().all()

    return sum(resposta.pontuacao_risco for resposta in respostas)


async def buscar_classificacao_especifica(db: AsyncSession, atendimento_id: int):

    result = await db.execute(
        select(OpcaoRespostaModel.classificacao)
        .join(
            RespostaModel,
            RespostaModel.opcao_resposta_id == OpcaoRespostaModel.id
        )
        .where(
            RespostaModel.atendimento_id == atendimento_id,
            OpcaoRespostaModel.classificacao.is_not(None)
        )
        .order_by(RespostaModel.id.desc())
    )

    return result.scalars().first()


async def classificar_por_pontuacao(pontuacao_total: int):

    if pontuacao_total >= 10:
        return ClassificacaoUrgencia.RISCO_ALTO_POR_PONTUACAO

    elif pontuacao_total >= 5:
        return ClassificacaoUrgencia.RISCO_MODERADO_POR_PONTUACAO

    return ClassificacaoUrgencia.BAIXO_RISCO


async def finalizar_triagem(db: AsyncSession, atendimento_id: int):

    pontuacao_total = await calcular_pontuacao_total(db, atendimento_id)

    classificacao_especifica = await buscar_classificacao_especifica(
        db, atendimento_id
    )

    if classificacao_especifica:
        classificacao = classificacao_especifica
    else:
        classificacao = await classificar_por_pontuacao(pontuacao_total)

    resultado = TriagemResultado(
        classificacao_triagem=classificacao,
        pontuacao_total=pontuacao_total
    )


    await AtendimentoService.atualizar_com_triagem(
        db, atendimento_id, resultado
    )

    return resultado