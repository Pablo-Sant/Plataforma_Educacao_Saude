from backend.models.atendimentos_model import (
    AtendimentoModel,
    ClassificacaoRiscoEnum,
    StatusEnum
)

from backend.schemas.atendimento_schema import AtendimentoInput
from backend.schemas.fluxo_schema import TriagemResultado, ClassificacaoUrgencia

from sqlalchemy.ext.asyncio import AsyncSession



MAPA_CLASSIFICACAO_URGENCIA_PARA_RISCO = {
    ClassificacaoUrgencia.EMERGENCIA_RESPIRATORIA: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.EMERGENCIA_CARDIACA: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.SUSPEITA_AVC: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.INCONSCIENCIA: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.HEMORRAGIA_POSSIVEL: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.LIMITACAO_MOTORA_GRAVE: ClassificacaoRiscoEnum.ALTO,
    ClassificacaoUrgencia.RISCO_ALTO_POR_PONTUACAO: ClassificacaoRiscoEnum.ALTO,

    ClassificacaoUrgencia.ALTERACAO_CARDIOVASCULAR: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.AVALIACAO_ABDOMINAL: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.AVALIACAO_URINARIA: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.RISCO_DESIDRATACAO: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.SINDROME_RESPIRATORIA: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.SINDROME_VIRAL: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.ACOMPANHAMENTO_CLINICO: ClassificacaoRiscoEnum.MEDIO,
    ClassificacaoUrgencia.RISCO_MODERADO_POR_PONTUACAO: ClassificacaoRiscoEnum.MEDIO,

    ClassificacaoUrgencia.BAIXO_RISCO: ClassificacaoRiscoEnum.BAIXO,
}


class AtendimentoService:

    @staticmethod
    async def buscar_por_id(atendimento_id: int, db: AsyncSession):
        return await db.get(AtendimentoModel, atendimento_id)

    @staticmethod
    async def atualizar_com_triagem(
        db: AsyncSession,
        atendimento_id: int,
        resultado: TriagemResultado
    ):
        atendimento = await db.get(AtendimentoModel, atendimento_id)

        if not atendimento:
            return None

        risco = MAPA_CLASSIFICACAO_URGENCIA_PARA_RISCO.get(
            resultado.classificacao_triagem
        )

        if risco is None:
            raise ValueError(
                f"Classificação '{resultado.classificacao_triagem}' "
                f"sem mapeamento de risco definido."
            )

        atendimento.classificacao_risco = risco
        atendimento.classificacao_triagem = resultado.classificacao_triagem.value

        atendimento.status = StatusEnum.AGUARDANDO_ATENDIMENTO

        atendimento.resumo_ia = (
            f"Paciente classificado como risco {risco.value} "
            f"(triagem: {resultado.classificacao_triagem.value}, "
            f"pontuação: {resultado.pontuacao_total}) "
            f"durante a triagem."
        )

        await db.commit()
        await db.refresh(atendimento)

        return atendimento

    @staticmethod
    async def criar(payload: AtendimentoInput, db: AsyncSession):

        atendimento = AtendimentoModel(
            paciente_id=payload.paciente_id,
            clinica_id=payload.clinica_id,

           
            status=StatusEnum.AGUARDANDO_TRIAGEM,
            classificacao_risco=None,
            classificacao_triagem=None,
            descricao=None,
            resumo_ia=None,
            medico_id=None
        )

        db.add(atendimento)

        await db.commit()
        await db.refresh(atendimento)

        return atendimento