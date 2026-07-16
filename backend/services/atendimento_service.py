from backend.models.atendimentos_model import (
    AtendimentoModel,
    ClassificacaoRiscoEnum,
    StatusEnum
)

from backend.schemas.fluxo_schema import (
    TriagemResultado,
    ClassificacaoUrgencia
)

from sqlalchemy.ext.asyncio import AsyncSession


class AtendimentoService:

    @staticmethod
    async def atualizar_com_triagem(
        db: AsyncSession,
        atendimento_id: int,
        resultado: TriagemResultado
    ):

        atendimento = await db.get(
            AtendimentoModel,
            atendimento_id
        )

        if not atendimento:
            return None

        
        if resultado.classificacao in [
            "EMERGENCIA_RESPIRATORIA",
            "EMERGENCIA_CARDIACA",
            "SUSPEITA_AVC",
            ClassificacaoUrgencia.ALTA
        ]:
            atendimento.classificacao_risco = (
                ClassificacaoRiscoEnum.ALTO
            )

        elif resultado.classificacao == ClassificacaoUrgencia.MEDIA:
            atendimento.classificacao_risco = (
                ClassificacaoRiscoEnum.MEDIO
            )

        else:
            atendimento.classificacao_risco = (
                ClassificacaoRiscoEnum.BAIXO
            )

        atendimento.status = (
            StatusEnum.AGUARDANDO
        )

        atendimento.resumo_ia = (
            f"Paciente classificado como "
            f"{atendimento.classificacao_risco.value} "
            f"durante a triagem."
        )

        await db.commit()
        await db.refresh(atendimento)

        return atendimento