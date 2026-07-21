from sqlalchemy import case, select
from backend.models.atendimentos_model import AtendimentoModel, StatusEnum, ClassificacaoRiscoEnum

from sqlalchemy.ext.asyncio import AsyncSession


async def listar_fila(db: AsyncSession):

    prioridade = case(
        (AtendimentoModel.classificacao_risco == ClassificacaoRiscoEnum.ALTO, 0),
        (AtendimentoModel.classificacao_risco == ClassificacaoRiscoEnum.MEDIO, 1),
        (AtendimentoModel.classificacao_risco == ClassificacaoRiscoEnum.BAIXO, 2),
        else_=3
    )

    result = await db.execute(
        select(AtendimentoModel)
        .where(AtendimentoModel.status == StatusEnum.AGUARDANDO_ATENDIMENTO)
        .order_by(prioridade, AtendimentoModel.data_atendimento.asc())
    )

    return result.scalars().all()