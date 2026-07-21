from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.deps import get_session
from backend.services.fila_service import listar_fila


router = APIRouter()

@router.get("/fila")
async def ver_fila(db: AsyncSession = Depends(get_session)):
    return await listar_fila(db)