from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.deps import get_session

from backend.models.atendimentos_model import AtendimentoModel

from backend.schemas.fluxo_schema import (
    FluxoRespostaInput,
    FluxoRespostaOut,
    PerguntaFluxoOut,
    OpcaoRespostaOut,
    TriagemResultado
)

from backend.services.fluxo_service import (
    buscar_pergunta,
    buscar_opcoes,
    buscar_opcao,
    salvar_resposta,
    obter_proxima_pergunta,
    limpar_respostas_atendimento
)

from backend.services.triagem_service import (
    finalizar_triagem
)


router = APIRouter()


@router.post(
    "/{atendimento_id}/iniciar",
    response_model=FluxoRespostaOut
)
async def iniciar_fluxo(
    atendimento_id: int,
    db: AsyncSession = Depends(get_session)
):

    atendimento = await db.get(
        AtendimentoModel,
        atendimento_id
    )

    if not atendimento:
        raise HTTPException(
            status_code=404,
            detail="Atendimento não encontrado"
        )

    pergunta = await buscar_pergunta(
        db,
        1
    )

    opcoes = await buscar_opcoes(
        db,
        pergunta.id
    )

    return FluxoRespostaOut(
        concluido=False,
        proxima_pergunta=PerguntaFluxoOut(
            id=pergunta.id,
            texto=pergunta.texto,
            tipo=pergunta.tipo,
            opcoes=[
                OpcaoRespostaOut(
                    id=opcao.id,
                    texto=opcao.texto
                )
                for opcao in opcoes
            ]
        )
    )
    
    
    
@router.post(
    "/{atendimento_id}/responder",
    response_model=FluxoRespostaOut
)
async def responder_pergunta(
    atendimento_id: int,
    body: FluxoRespostaInput,
    db: AsyncSession = Depends(get_session)
):

    opcao = await buscar_opcao(
        db,
        body.opcao_resposta_id
    )

    if not opcao:
        raise HTTPException(
            status_code=404,
            detail="Opção não encontrada"
        )

    await salvar_resposta(
        db,
        atendimento_id,
        body.pergunta_id,
        body.opcao_resposta_id,
        opcao.texto
    )

    if opcao.encerra_fluxo:

        resultado = await finalizar_triagem(
            db,
            atendimento_id
        )

        return FluxoRespostaOut(
            concluido=True,
            resultado=resultado
        )

    proxima_pergunta = await obter_proxima_pergunta(
        db,
        body.opcao_resposta_id
    )

    opcoes = await buscar_opcoes(
        db,
        proxima_pergunta.id
    )

    return FluxoRespostaOut(
        concluido=False,
        proxima_pergunta=PerguntaFluxoOut(
            id=proxima_pergunta.id,
            texto=proxima_pergunta.texto,
            tipo=proxima_pergunta.tipo,
            opcoes=[
                OpcaoRespostaOut(
                    id=opcao.id,
                    texto=opcao.texto
                )
                for opcao in opcoes
            ]
        )
    )
    
    
    
@router.get(
    "/{atendimento_id}/resultado",
    response_model=TriagemResultado
)
async def buscar_resultado_triagem(
    atendimento_id: int,
    db: AsyncSession = Depends(get_session)
):

    atendimento = await db.get(
        AtendimentoModel,
        atendimento_id
    )

    if not atendimento:
        raise HTTPException(
            status_code=404,
            detail="Atendimento não encontrado"
        )

    resultado = await finalizar_triagem(
        db,
        atendimento_id
    )

    return resultado


@router.delete(
    "/{atendimento_id}/reiniciar",
    response_model=FluxoRespostaOut
)
async def reiniciar_triagem(
    atendimento_id: int,
    db: AsyncSession = Depends(get_session)
):

    atendimento = await db.get(
        AtendimentoModel,
        atendimento_id
    )

    if not atendimento:
        raise HTTPException(
            status_code=404,
            detail="Atendimento não encontrado"
        )

    await limpar_respostas_atendimento(
        db,
        atendimento_id
    )

    pergunta = await buscar_pergunta(
        db,
        1
    )

    opcoes = await buscar_opcoes(
        db,
        pergunta.id
    )

    return FluxoRespostaOut(
        concluido=False,
        proxima_pergunta=PerguntaFluxoOut(
            id=pergunta.id,
            texto=pergunta.texto,
            tipo=pergunta.tipo,
            opcoes=[
                OpcaoRespostaOut(
                    id=opcao.id,
                    texto=opcao.texto
                )
                for opcao in opcoes
            ]
        )
    )