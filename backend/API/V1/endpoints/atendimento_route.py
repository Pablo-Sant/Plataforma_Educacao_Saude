from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.deps import get_session

from backend.schemas.atendimento_schema import (
    AtendimentoInput,
    AtendimentoResponse
)

from backend.services.atendimento_service import (
    AtendimentoService
)

router = APIRouter()


@router.post(
    "/",
    response_model=AtendimentoResponse,
    status_code=201
)
async def criar_atendimento(
    payload: AtendimentoInput,
    db: AsyncSession = Depends(get_session)
):

    return await AtendimentoService.criar(
        payload,
        db
    )


@router.get(
    "/{atendimento_id}",
    response_model=AtendimentoResponse
)
async def buscar_atendimento(
    atendimento_id: int,
    db: AsyncSession = Depends(get_session)
):

    atendimento = await AtendimentoService.buscar_por_id(
        atendimento_id,
        db
    )

    if not atendimento:
        raise HTTPException(
            status_code=404,
            detail="Atendimento não encontrado"
        )

    return atendimento