from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.deps import get_session

from backend.schemas.fila_schema import FilaResponse

from backend.services.fila_service import (
    listar_fila,
    buscar_por_codigo,
    chamar_proximo,
    remover_da_fila
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[FilaResponse]
)
async def listar(
    db: AsyncSession = Depends(get_session)
):

    return await listar_fila(db)


@router.get(
    "/proximo",
    response_model=FilaResponse
)
async def proximo(
    db: AsyncSession = Depends(get_session)
):

    paciente = await chamar_proximo(db)

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Fila vazia."
        )

    return paciente


@router.get(
    "/{codigo}",
    response_model=FilaResponse
)
async def buscar(
    codigo: str,
    db: AsyncSession = Depends(get_session)
):

    paciente = await buscar_por_codigo(
        db,
        codigo
    )

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado."
        )

    return paciente


@router.delete(
    "/{codigo}",
    response_model=FilaResponse
)
async def remover(
    codigo: str,
    db: AsyncSession = Depends(get_session)
):

    paciente = await remover_da_fila(
        db,
        codigo
    )

    if not paciente:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado."
        )

    return paciente