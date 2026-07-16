from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete

from backend.models.pergunta_model import PerguntaModel
from backend.models.opcao_resposta_model import OpcaoRespostaModel
from backend.models.resposta_model import RespostaModel


async def buscar_pergunta(
    db: AsyncSession,
    pergunta_id: int
):
    return await db.get(
        PerguntaModel,
        pergunta_id
    )


async def buscar_opcoes(
    db: AsyncSession,
    pergunta_id: int
):
    result = await db.execute(
        select(OpcaoRespostaModel)
        .where(
            OpcaoRespostaModel.pergunta_id == pergunta_id
        )
    )

    return result.scalars().all()


async def buscar_opcao(
    db: AsyncSession,
    opcao_id: int
):
    return await db.get(
        OpcaoRespostaModel,
        opcao_id
    )


async def salvar_resposta(
    db: AsyncSession,
    atendimento_id: int,
    pergunta_id: int,
    opcao_resposta_id: int,
    resposta_texto: str
):
    resposta = RespostaModel(
        atendimento_id=atendimento_id,
        pergunta_id=pergunta_id,
        opcao_resposta_id=opcao_resposta_id,
        resposta=resposta_texto
    )

    db.add(resposta)

    await db.commit()
    await db.refresh(resposta)

    return resposta


async def obter_proxima_pergunta(
    db: AsyncSession,
    opcao_id: int
):
    opcao = await buscar_opcao(
        db,
        opcao_id
    )

    if not opcao:
        return None

    if opcao.encerra_fluxo:
        return None

    if not opcao.proxima_pergunta_id:
        return None

    return await buscar_pergunta(
        db,
        opcao.proxima_pergunta_id
    )
    

async def limpar_respostas_atendimento(
    db: AsyncSession,
    atendimento_id: int
):

    await db.execute(
        delete(RespostaModel)
        .where(
            RespostaModel.atendimento_id ==
            atendimento_id
        )
    )

    await db.commit()